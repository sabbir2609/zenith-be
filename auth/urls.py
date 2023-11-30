from django.urls import path
from .views import ProfileView


appname = "auth"

urlpatterns = [
    path("profile/", ProfileView.as_view(), name="profile"),
]
