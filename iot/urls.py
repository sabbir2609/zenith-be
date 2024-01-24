from django.urls import path
from .views import IoTPage

app_name = "iot"


urlpatterns = [
    path("", IoTPage.as_view(), name="iot"),
]
