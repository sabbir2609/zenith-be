from django.urls import path
from rest_framework_nested import routers

from .views import StripeCheckoutView

app_name = "payment"


urlpatterns = [
    path(
        "create-checkout-session/", StripeCheckoutView.as_view(), name="stripe-checkout"
    ),
]
