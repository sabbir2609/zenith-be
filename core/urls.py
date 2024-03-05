from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.db import router
from django.urls import path, include

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from .views import Homepage


# Admin Site Config
admin.site.site_header = "Zenith System"
admin.site.site_title = "Zenith System"
admin.site.index_title = "Welcome to Zenith System Administrations"


urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("user.urls"), name="user"),
    path("api/main/", include("main.urls"), name="main"),
    path("api/management/", include("management.urls"), name="management"),
    path("api/facility/", include("facility.urls"), name="facility"),
    path("api/iot/", include("iot.urls"), name="iot"),
    # blog
    path("blog/", include("blog.urls"), name="blog"),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    # test pages
    path("", Homepage.as_view(), name="homepage"),
    path("notifications/", include("notification.urls"), name="notification"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Spectacular URL Patterns
urlpatterns += [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
