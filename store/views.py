from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from .permissions import IsAdminOrReadOnly
from .pagination import DefaultPagination
from .filters import CarFilter
from .models import Catagory, Cart, Car
from .serializers import CatagorySerializer, CarSerializer
# Create your views here.


class CatagoryViewSet(ModelViewSet):
    queryset = Catagory.objects.all()
    serializer_class = CatagorySerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title']


class CarViewSet(ModelViewSet):
    queryset = Car.objects.select_related('catagory').all()
    serializer_class = CarSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title']
    filterset_class = CarFilter

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}


class OwnerCarViewSet(ModelViewSet):
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title']
    filterset_class = CarFilter

    def get_queryset(self):
        owner_id = self.request.user.id
        return Car.objects.filter(user=owner_id)

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}
