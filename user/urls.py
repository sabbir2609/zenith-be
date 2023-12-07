# user/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    CustomTokenVerifyView,
    LogoutView,
)


app_name = "user"

router = DefaultRouter()

urlpatterns = [
    path("jwt/create/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("jwt/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("jwt/verify/", CustomTokenVerifyView.as_view(), name="token_verify"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("", include("djoser.urls")),
    path("", include("djoser.urls.jwt")),
] + router.urls
