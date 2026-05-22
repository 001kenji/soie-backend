from django.contrib import admin
from .models import ShippingConfig


@admin.register(ShippingConfig)
class ShippingConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'fee_usd', 'estimated_days_min', 'estimated_days_max', 'is_active')
    list_editable = ('fee_usd', 'is_active')