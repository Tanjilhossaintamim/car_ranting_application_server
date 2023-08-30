from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
from .serializers import ClientSerializer, OwnerSerializer, OwnerProfileUpdateSerializer, ClientProfileUpdateSerializer
from .models import User, Client, Owner

# Create your views here.


class ProfileViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        user = self.request.user
        if Client.objects.filter(user=user.id).exists():
            return ClientSerializer
        return OwnerSerializer

    def get_queryset(self):
        user = self.request.user
        if Client.objects.filter(user=user.id).exists():
            return Client.objects.filter(user=user.id)
        return Owner.objects.filter(user=user.id)

    @action(detail=False, methods=['GET', 'PATCH'])
    def me(self, request):
        user = request.user
        if Client.objects.filter(user=user.id).exists():
            client = Client.objects.get(user=user.id)
            if request.method == 'GET':
                serializer = ClientSerializer(client)
                return Response(serializer.data)
            elif request.method == 'PATCH':
                serializer = ClientSerializer(client, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)

        elif Owner.objects.filter(user=user.id).exists():
            owner = Owner.objects.get(user=user.id)
            if request.method == 'GET':
                serializer = OwnerSerializer(owner)
                return Response(serializer.data)
            elif request.method == 'PATCH':
                serializer = OwnerSerializer(owner, request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)


class OwnerProfileUpdateViewSet(ModelViewSet):
    http_method_names = ['post']
    queryset = Owner.objects.all()
    serializer_class = OwnerProfileUpdateSerializer


class ClientProfileUpdateViewSet(ModelViewSet):
    http_method_names = ['post']

    queryset = Client.objects.all()
    serializer_class = ClientProfileUpdateSerializer
