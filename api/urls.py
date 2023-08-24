from django.urls import path
from rest_framework_nested import routers
from user.views import ProfileViewSet


router = routers.DefaultRouter()
router.register('profile', ProfileViewSet, basename='profile')


urlpatterns = router.urls
