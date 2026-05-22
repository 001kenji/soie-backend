from django.urls import path
from .views import OrderListView, OrderDetailView, CartView, CartItemUpdateView, WishlistView

urlpatterns = [
    path('', OrderListView.as_view(), name='order-list'),
    path('<uuid:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/items/<uuid:item_id>/', CartItemUpdateView.as_view(), name='cart-item-update'),
    path('wishlist/', WishlistView.as_view(), name='wishlist'),
]