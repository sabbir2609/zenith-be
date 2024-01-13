from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.db import router
from django.urls import path, include


# Admin Site Config
admin.site.site_header = "Zenith System"
admin.site.site_title = "Zenith System"
admin.site.index_title = "Welcome to Zenith System Administrations"


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("auth/", include("user.urls"), name="user"),
    path("api/", include("main.urls"), name="main"),
    path("api/tasks/", include("management.urls"), name="management"),
    path("", include("notification.urls"), name="notification"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
