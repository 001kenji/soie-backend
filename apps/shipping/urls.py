from django.urls import path
from .views import ShippingConfigView

urlpatterns = [
    path("", ShippingConfigView.as_view(), name="shipping-config"),
]