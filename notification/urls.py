from django.urls import path

from .views import NotificationPage

app_name = "notification"


urlpatterns = [
    path("", NotificationPage.as_view(), name="notification"),
]
