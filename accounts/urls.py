# user/urls.py
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from .views import (
    CustomProviderAuthView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    CustomTokenVerifyView,
    LogoutView,
)


app_name = "accounts"

router = DefaultRouter()

urlpatterns = [
    re_path(
        r"^o/(P<provider>\S+)/$", CustomProviderAuthView.as_view(), name="provider-auth"
    ),
    path("jwt/create/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("jwt/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("jwt/verify/", CustomTokenVerifyView.as_view(), name="token_verify"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("", include("djoser.urls")),
    path("", include("djoser.urls.jwt")),
    path("", include("djoser.social.urls")),
] + router.urls
