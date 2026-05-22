import uuid
from django.db import models

class ShippingConfig(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name                = models.CharField(max_length=100, default="Standard Shipping")
    fee_usd             = models.DecimalField(max_digits=8, decimal_places=2, default=12.00)
    estimated_days_min  = models.PositiveIntegerField(default=8)
    estimated_days_max  = models.PositiveIntegerField(default=15)
    description         = models.CharField(
        max_length=300,
        default="Shipped from China via express courier",
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name        = "Shipping Configuration"
        verbose_name_plural = "Shipping Configurations"

    def __str__(self):
        return f"{self.name} — ${self.fee_usd} ({self.estimated_days_min}–{self.estimated_days_max} days)"