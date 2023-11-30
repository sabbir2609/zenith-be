from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("auth.urls"), name="auth"),
    # restframework auth url
    path("api-auth/", include("rest_framework.urls")),
]
