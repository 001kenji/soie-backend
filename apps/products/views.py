from rest_framework import generics, filters, status
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import WigProduct, Category, Review, HeroImage
from .serializers import (
    WigProductListSerializer,
    WigProductDetailSerializer,
    CategorySerializer,
    ReviewCreateSerializer,
    HeroImageSerializer,
)


class ProductListView(generics.ListAPIView):
    serializer_class   = WigProductListSerializer
    permission_classes = [AllowAny]
    filter_backends    = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields   = ['category__slug', 'hair_type', 'lace_type', 'is_featured', 'is_trending']
    search_fields      = ['name', 'description', 'short_description', 'hair_type']
    ordering_fields    = ['created_at', 'name']
    ordering           = ['-created_at']

    def get_queryset(self):
        return (
            WigProduct.objects
            .filter(is_active=True)
            .select_related('category')
            .prefetch_related('images', 'reviews')
        )


class FeaturedProductsView(generics.ListAPIView):
    serializer_class   = WigProductListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return (
            WigProduct.objects
            .filter(is_active=True, is_featured=True)
            .select_related('category')
            .prefetch_related('images', 'reviews')
            [:6]
        )


class TrendingProductsView(generics.ListAPIView):
    serializer_class   = WigProductListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return (
            WigProduct.objects
            .filter(is_active=True, is_trending=True)
            .select_related('category')
            .prefetch_related('images', 'reviews')
            [:6]
        )


class ProductDetailView(generics.RetrieveAPIView):
    serializer_class   = WigProductDetailSerializer
    permission_classes = [AllowAny]
    lookup_field       = 'slug'

    def get_queryset(self):
        return (
            WigProduct.objects
            .filter(is_active=True)
            .select_related('category')
            .prefetch_related('images', 'inch_pricing', 'reviews')
        )

    def get_serializer_context(self):
        # Pass request so the serializer can inspect request.user for review visibility
        ctx = super().get_serializer_context()
        ctx['request'] = self.request
        return ctx


class CategoryListView(generics.ListAPIView):
    serializer_class   = CategorySerializer
    permission_classes = [AllowAny]
    queryset           = Category.objects.all().order_by('name')


class ReviewCreateView(generics.CreateAPIView):
    serializer_class   = ReviewCreateSerializer
    permission_classes = [AllowAny]   # allow guests to review; user linked if authenticated

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['product'] = WigProduct.objects.get(slug=self.kwargs['slug'])
        ctx['request'] = self.request
        return ctx

    def create(self, request, *args, **kwargs):
        # Prevent duplicate reviews from authenticated users
        if request.user.is_authenticated:
            product = WigProduct.objects.get(slug=kwargs['slug'])
            existing = Review.objects.filter(product=product, user=request.user).exists()
            if existing:
                return Response(
                    {'status': 400, 'message': 'You have already submitted a review for this product.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'status': 201, 'message': 'Review submitted. It will appear after moderation.'},
            status=status.HTTP_201_CREATED,
        )


class HeroImagesView(generics.ListAPIView):
    """Returns all active hero slot images keyed by slot name."""
    serializer_class   = HeroImageSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return HeroImage.objects.filter(is_active=True)