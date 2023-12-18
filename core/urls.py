from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.db import router
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("user.urls"), name="user"),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include("main.urls"), name="main"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
