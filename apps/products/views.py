from rest_framework import generics, filters, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import WigProduct, Category, Review,HeroImage
from .serializers import (
    WigProductListSerializer, WigProductDetailSerializer,
    CategorySerializer, ReviewCreateSerializer,HeroImageSerializer
)
from rest_framework.permissions import AllowAny

class ProductListView(generics.ListAPIView):
    serializer_class = WigProductListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__slug', 'hair_type', 'lace_type', 'is_featured', 'is_trending']
    search_fields = ['name', 'description', 'hair_type']
    ordering_fields = ['created_at', 'name']
    ordering = ['-created_at']

    def get_queryset(self):
        return WigProduct.objects.filter(is_active=True).prefetch_related('images', 'reviews')

class HeroImagesView(generics.ListAPIView):
    """Returns all active hero slot images. Frontend maps by slot name."""
    serializer_class   = HeroImageSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return HeroImage.objects.filter(is_active=True)

class FeaturedProductsView(generics.ListAPIView):
    serializer_class = WigProductListSerializer

    def get_queryset(self):
        return WigProduct.objects.filter(is_active=True, is_featured=True).prefetch_related('images', 'reviews')[:6]


class TrendingProductsView(generics.ListAPIView):
    serializer_class = WigProductListSerializer

    def get_queryset(self):
        return WigProduct.objects.filter(is_active=True, is_trending=True).prefetch_related('images', 'reviews')[:6]


class ProductDetailView(generics.RetrieveAPIView):
    serializer_class = WigProductDetailSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return WigProduct.objects.filter(is_active=True).prefetch_related('images', 'inch_pricing', 'reviews')


class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewCreateSerializer

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['product'] = WigProduct.objects.get(slug=self.kwargs['slug'])
        return ctx

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review = serializer.save()
        return Response(
            {'detail': 'Review submitted. It will appear after moderation.'},
            status=status.HTTP_201_CREATED
        )