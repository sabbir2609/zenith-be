# user/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter


app_name = "user"

router = DefaultRouter()

urlpatterns = router.urls
