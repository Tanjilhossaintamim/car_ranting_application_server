from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from .permissions import IsAdminOrReadOnly
from .pagination import DefaultPagination
from .filters import CarFilter
from .models import Catagory, Cart, Car, CartItem, OrderItem
from .serializers import CatagorySerializer, CarSerializer, CartSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer
# Create your views here.


class CatagoryViewSet(ModelViewSet):
    queryset = Catagory.objects.all()
    serializer_class = CatagorySerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title']

    def destroy(self, request, *args, **kwargs):
        if Car.objects.filter(catagory_id=self.kwargs['pk']).count() > 0:
            return Response({'error': 'Catagory Has Some Products'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class CarViewSet(ModelViewSet):
    queryset = Car.objects.select_related('catagory').all()
    serializer_class = CarSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title']
    filterset_class = CarFilter

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(car_id=self.kwargs['pk']).count() > 0:
            return Response({'error': 'Car Delete Not Possible This Car Has Order!'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}


class OwnerCarViewSet(ModelViewSet):
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title']
    filterset_class = CarFilter

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(car_id=self.kwargs['pk']).count() > 0:
            return Response({'error': 'Car Delete Not Possible This Car Has Order!'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        owner_id = self.request.user.id
        return Car.objects.filter(user=owner_id)

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}


class CartViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(pk=self.kwargs['pk'])


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        if self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}
