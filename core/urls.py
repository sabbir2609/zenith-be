from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.db import router
from django.urls import path, include

from .views import Homepage


# Admin Site Config
admin.site.site_header = "Zenith System"
admin.site.site_title = "Zenith System"
admin.site.index_title = "Welcome to Zenith System Administrations"


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("auth/", include("user.urls"), name="user"),
    path("api/main/", include("main.urls"), name="main"),
    path("api/management/", include("management.urls"), name="management"),
    path("api/iot/", include("iot.urls"), name="iot"),
    path("api/payment/", include("payment.urls"), name="payment"),
    # blog
    path("blog/", include("blog.urls"), name="blog"),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    # test pages
    path("", Homepage.as_view(), name="homepage"),
    path("notifications/", include("notification.urls"), name="notification"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
