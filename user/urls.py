# user/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

app_name = "user"

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")

urlpatterns = router.urls
