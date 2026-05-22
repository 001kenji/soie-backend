from django.urls import path
from .views import (
    ProductListView, ProductDetailView, FeaturedProductsView,
    TrendingProductsView, CategoryListView, ReviewCreateView,
    HeroImagesView   
)

urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('featured/', FeaturedProductsView.as_view(), name='featured-products'),
    path('trending/', TrendingProductsView.as_view(), name='trending-products'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('hero-images/', HeroImagesView.as_view(), name='hero-images'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('<slug:slug>/reviews/', ReviewCreateView.as_view(), name='review-create'),
]