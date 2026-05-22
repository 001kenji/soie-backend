from rest_framework import serializers
from django.conf import settings  # Add this import
from .models import WigProduct, WigImage, InchPricing, Review, Category,HeroImage   


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'description')


class WigImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()  # Change to SerializerMethodField
    
    class Meta:
        model = WigImage
        fields = ('id', 'image', 'alt_text', 'is_primary', 'order')
    
    def get_image(self, obj):  # This will work with SerializerMethodField
        if obj.image:
            backend_url = getattr(settings, 'BACKEND_URL', '')
            image_url = obj.image.url
            if backend_url and image_url:
                # Remove leading slash to avoid double slashes
                image_url = image_url.lstrip('/')
                return f"{backend_url}/{image_url}"
        return None


class InchPricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = InchPricing
        fields = ('id', 'inches', 'price', 'stock_quantity', 'is_available')


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'reviewer_name', 'message', 'rating', 'created_at')
        read_only_fields = ('id', 'created_at')


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('reviewer_name', 'message', 'rating')

    def create(self, validated_data):
        product = self.context['product']
        user = self.context['request'].user if self.context['request'].user.is_authenticated else None
        return Review.objects.create(product=product, user=user, **validated_data)


class WigProductListSerializer(serializers.ModelSerializer):
    primary_image = WigImageSerializer(read_only=True)  # This will now use the modified WigImageSerializer
    min_price = serializers.ReadOnlyField()
    average_rating = serializers.ReadOnlyField()
    review_count = serializers.ReadOnlyField()
    category = CategorySerializer(read_only=True)

    class Meta:
        model = WigProduct
        fields = (
            'id', 'name', 'slug', 'short_description', 'hair_type',
            'lace_type', 'density', 'is_featured', 'is_trending',
            'primary_image', 'min_price', 'average_rating', 'review_count', 'category'
        )

class HeroImageSerializer(serializers.ModelSerializer):
    class Meta:
        model  = HeroImage
        fields = ('slot', 'image', 'alt_text')

class WigProductDetailSerializer(serializers.ModelSerializer):
    images = WigImageSerializer(many=True, read_only=True)  # This will also use the modified WigImageSerializer
    inch_pricing = InchPricingSerializer(many=True, read_only=True)
    reviews = serializers.SerializerMethodField()
    average_rating = serializers.ReadOnlyField()
    review_count = serializers.ReadOnlyField()
    category = CategorySerializer(read_only=True)

    class Meta:
        model = WigProduct
        fields = (
            'id', 'name', 'slug', 'description', 'short_description',
            'hair_type', 'lace_type', 'density', 'category',
            'is_featured', 'is_trending', 'care_instructions',
            'images', 'inch_pricing', 'reviews',
            'average_rating', 'review_count', 'created_at'
        )

    def get_reviews(self, obj):
        approved = obj.reviews.filter(is_approved=True)
        return ReviewSerializer(approved, many=True).data