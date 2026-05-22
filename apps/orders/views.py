from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Order, Cart, CartItem, Wishlist
from .serializers import OrderSerializer, CartSerializer
from apps.products.models import WigProduct, InchPricing


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items', 'shipping_address')


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return Response(CartSerializer(cart).data)

    def post(self, request):
        """Add item to cart."""
        cart, _ = Cart.objects.get_or_create(user=request.user)
        inch_pricing_id = request.data.get('inch_pricing_id')
        quantity = request.data.get('quantity', 1)

        try:
            pricing = InchPricing.objects.select_related('product').get(id=inch_pricing_id, is_available=True)
        except InchPricing.DoesNotExist:
            return Response({'error': 'Item not available'}, status=400)

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=pricing.product,
            inch_pricing=pricing,
            defaults={'quantity': quantity}
        )
        if not created:
            item.quantity += quantity
            item.save()

        return Response(CartSerializer(cart).data)

    def delete(self, request):
        """Clear cart."""
        Cart.objects.filter(user=request.user).delete()
        return Response(status=204)


class CartItemUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, item_id):
        try:
            item = CartItem.objects.get(id=item_id, cart__user=request.user)
            qty = request.data.get('quantity', 1)
            if qty < 1:
                item.delete()
            else:
                item.quantity = qty
                item.save()
            cart = Cart.objects.get(user=request.user)
            return Response(CartSerializer(cart).data)
        except CartItem.DoesNotExist:
            return Response({'error': 'Item not found'}, status=404)

    def delete(self, request, item_id):
        try:
            CartItem.objects.filter(id=item_id, cart__user=request.user).delete()
            cart = Cart.objects.get(user=request.user)
            return Response(CartSerializer(cart).data)
        except Exception:
            return Response(status=204)


class WishlistView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
        from apps.products.serializers import WigProductListSerializer
        return Response(WigProductListSerializer(wishlist.products.all(), many=True).data)

    def post(self, request):
        product_id = request.data.get('product_id')
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
        try:
            product = WigProduct.objects.get(id=product_id)
            if wishlist.products.filter(id=product_id).exists():
                wishlist.products.remove(product)
                return Response({'added': False})
            else:
                wishlist.products.add(product)
                return Response({'added': True})
        except WigProduct.DoesNotExist:
            return Response({'error': 'Product not found'}, status=404)