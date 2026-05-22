from rest_framework import serializers
from .models import Order, OrderItem, Cart, CartItem, ShippingAddress, Wishlist
from apps.products.serializers import WigProductListSerializer, InchPricingSerializer


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = ('id', 'full_name', 'email', 'phone', 'address_line1',
                  'address_line2', 'city', 'state', 'country', 'postal_code')


class CartItemSerializer(serializers.ModelSerializer):
    product = WigProductListSerializer(read_only=True)  # This will automatically use the updated WigProductListSerializer
    inch_pricing = InchPricingSerializer(read_only=True)
    subtotal = serializers.ReadOnlyField()

    class Meta:
        model = CartItem
        fields = ('id', 'product', 'inch_pricing', 'quantity', 'subtotal')


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.ReadOnlyField()
    item_count = serializers.ReadOnlyField()

    class Meta:
        model = Cart
        fields = ('id', 'items', 'total', 'item_count')


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'product_name', 'inches', 'unit_price', 'quantity', 'subtotal')


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    shipping_address = ShippingAddressSerializer(read_only=True)
    payment_status = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'id', 'order_number', 'status', 'subtotal', 'shipping_fee', 'total',
            'estimated_delivery', 'items', 'shipping_address', 'payment_status', 'created_at'
        )

    def get_payment_status(self, obj):
        try:
            return obj.payment.status
        except Exception:
            return 'pending'