from django.contrib import admin
from .models import Order, OrderItem, ShippingAddress, Cart


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'inches', 'unit_price', 'quantity', 'subtotal')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'status', 'total', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_number', 'user__email')
    readonly_fields = ('order_number', 'created_at', 'updated_at')
    inlines = [OrderItemInline]
    actions = ['mark_shipped']

    def mark_shipped(self, request, queryset):
        for order in queryset:
            order.status = 'shipped'
            order.save()
            from apps.accounts.tasks import send_shipping_update_email
            send_shipping_update_email.delay(str(order.id))
        self.message_user(request, f'{queryset.count()} orders marked as shipped.')
    mark_shipped.short_description = 'Mark selected orders as Shipped'


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'city', 'country', 'phone')
    search_fields = ('full_name', 'email', 'city')