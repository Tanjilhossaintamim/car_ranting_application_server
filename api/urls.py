from django.urls import path
from rest_framework_nested import routers
from user.views import ProfileViewSet
from store.views import CatagoryViewSet, CarViewSet, OwnerCarViewSet


router = routers.DefaultRouter()
router.register('profile', ProfileViewSet, basename='profile')
router.register('catagory', CatagoryViewSet)
router.register('car', CarViewSet)
router.register('ownercar', OwnerCarViewSet, basename='ownercar')

urlpatterns = router.urls
