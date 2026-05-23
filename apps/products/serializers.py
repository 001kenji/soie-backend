from rest_framework import serializers
from .models import WigProduct, WigImage, InchPricing, Review, Category, HeroImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Category
        fields = ('id', 'name', 'slug', 'description')


class WigImageSerializer(serializers.ModelSerializer):
    class Meta:
        model  = WigImage
        fields = ('id', 'image', 'alt_text', 'is_primary', 'order')


class InchPricingSerializer(serializers.ModelSerializer):
    class Meta:
        model  = InchPricing
        fields = ('id', 'inches', 'price', 'stock_quantity', 'is_available')


class ReviewSerializer(serializers.ModelSerializer):
    """
    Includes `is_pending` so the frontend can show a moderation notice
    on the review owner's own unnapproved review.
    """
    is_pending = serializers.SerializerMethodField()

    class Meta:
        model  = Review
        fields = ('id', 'reviewer_name', 'message', 'rating', 'created_at', 'is_pending')
        read_only_fields = ('id', 'created_at')

    def get_is_pending(self, obj):
        return not obj.is_approved


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Review
        fields = ('reviewer_name', 'message', 'rating')

    def validate_message(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Review must be at least 10 characters.")
        if len(value) > 500:
            raise serializers.ValidationError("Review must be under 500 characters.")
        return value.strip()

    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def create(self, validated_data):
        product = self.context['product']
        request = self.context.get('request')
        user    = request.user if (request and request.user.is_authenticated) else None
        return Review.objects.create(
            product=product,
            user=user,
            is_approved=False,   # all reviews go through moderation
            **validated_data,
        )


class WigProductListSerializer(serializers.ModelSerializer):
    primary_image  = WigImageSerializer(read_only=True)
    min_price      = serializers.ReadOnlyField()
    average_rating = serializers.ReadOnlyField()
    review_count   = serializers.ReadOnlyField()
    category       = CategorySerializer(read_only=True)

    class Meta:
        model  = WigProduct
        fields = (
            'id', 'name', 'slug', 'short_description',
            'hair_type', 'lace_type', 'density',
            'is_featured', 'is_trending',
            'primary_image', 'min_price',
            'average_rating', 'review_count', 'category',
        )


class WigProductDetailSerializer(serializers.ModelSerializer):
    images         = WigImageSerializer(many=True, read_only=True)
    inch_pricing   = InchPricingSerializer(many=True, read_only=True)
    reviews        = serializers.SerializerMethodField()
    average_rating = serializers.ReadOnlyField()
    review_count   = serializers.ReadOnlyField()
    category       = CategorySerializer(read_only=True)
    primary_image  = WigImageSerializer(read_only=True)

    class Meta:
        model  = WigProduct
        fields = (
            'id', 'name', 'slug', 'description', 'short_description',
            'hair_type', 'lace_type', 'density', 'category',
            'is_featured', 'is_trending', 'care_instructions',
            'images', 'primary_image', 'inch_pricing', 'reviews',
            'average_rating', 'review_count', 'created_at',
        )

    def get_reviews(self, obj):
        request      = self.context.get('request')
        current_user = (
            request.user
            if (request and request.user and request.user.is_authenticated)
            else None
        )

        # All publicly approved reviews
        approved = list(obj.reviews.filter(is_approved=True).order_by('-created_at'))

        # Prepend the current user's own pending review (visible only to them)
        if current_user:
            own_pending = obj.reviews.filter(
                is_approved=False,
                user=current_user,
            ).first()
            if own_pending:
                approved = [own_pending] + approved

        return ReviewSerializer(approved, many=True, context=self.context).data


class HeroImageSerializer(serializers.ModelSerializer):
    class Meta:
        model  = HeroImage
        fields = ('slot', 'image', 'alt_text')