from django.urls import path
from rest_framework_nested import routers
from user.views import ProfileViewSet, OwnerProfileUpdateViewSet, ClientProfileUpdateViewSet
from store.views import CartViewSet, CatagoryViewSet, CarViewSet, OwnerCarViewSet, CartItemViewSet, OrderViewSet


router = routers.DefaultRouter()
router.register('profile', ProfileViewSet, basename='profile')
router.register('ownerprofile', OwnerProfileUpdateViewSet,
                basename='ownerprofile')
router.register('clientprofile', ClientProfileUpdateViewSet,
                basename='clientprofile')
#######################
router.register('catagory', CatagoryViewSet)
router.register('car', CarViewSet)
router.register('ownercar', OwnerCarViewSet, basename='ownercar')
router.register('cart', CartViewSet, basename='cart')
router.register('order', OrderViewSet, basename='order')

cart_router = routers.NestedDefaultRouter(router, 'cart', lookup='cart')
cart_router.register('items', CartItemViewSet, basename='cartitems')

urlpatterns = router.urls+cart_router.urls
