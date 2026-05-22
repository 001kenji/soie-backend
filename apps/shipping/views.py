from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import ShippingConfig


class ShippingConfigView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        config = ShippingConfig.objects.filter(is_active=True).first()
        if not config:
            return Response({"fee_usd": 12.00, "estimated_days_min": 8, "estimated_days_max": 15})
        return Response({
            "name":                config.name,
            "fee_usd":             str(config.fee_usd),
            "estimated_days_min":  config.estimated_days_min,
            "estimated_days_max":  config.estimated_days_max,
            "description":         config.description,
        })