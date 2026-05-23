from rest_framework import serializers
from django.conf import settings as django_settings
from .models import WigProduct, WigImage, InchPricing, Review, Category, HeroImage


def _absolute_image_url(image_field, context: dict):
    """
    Return the absolute URL for an ImageField value.

    Priority order:
    1. request.build_absolute_uri()  — uses the live HTTP request (best)
    2. settings.BACKEND_URL          — fallback for shell / Celery / emails
    3. relative URL                  — last resort, same as before the fix
    """
    if not image_field:
        return None
    relative = image_field.url
    request = context.get('request')
    if request is not None:
        return request.build_absolute_uri(relative)
    backend_url = getattr(django_settings, 'BACKEND_URL', '').rstrip('/')
    if backend_url:
        return f"{backend_url}{relative}"
    return relative


# ─────────────────────────────────────────────────────────────────────────────

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Category
        fields = ('id', 'name', 'slug', 'description')


class WigImageSerializer(serializers.ModelSerializer):
    """
    The image field is a SerializerMethodField so we can inject
    the absolute URL using the request from context.
    """
    image = serializers.SerializerMethodField()

    class Meta:
        model  = WigImage
        fields = ('id', 'image', 'alt_text', 'is_primary', 'order')

    def get_image(self, obj):
        return _absolute_image_url(obj.image, self.context)


class InchPricingSerializer(serializers.ModelSerializer):
    class Meta:
        model  = InchPricing
        fields = ('id', 'inches', 'price', 'stock_quantity', 'is_available')


class ReviewSerializer(serializers.ModelSerializer):
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
        value = value.strip()
        if len(value) < 10:
            raise serializers.ValidationError(
                "Review must be at least 10 characters."
            )
        if len(value) > 500:
            raise serializers.ValidationError(
                "Review must be under 500 characters."
            )
        return value

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
            is_approved=False,
            **validated_data,
        )


class WigProductListSerializer(serializers.ModelSerializer):
    """
    primary_image is a SerializerMethodField so we can pass the
    request context down into WigImageSerializer.
    """
    primary_image  = serializers.SerializerMethodField()
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

    def get_primary_image(self, obj):
        img = obj.primary_image   # model property returning WigImage or None
        if not img:
            return None
        # Pass context (which contains the request) into the nested serializer
        return WigImageSerializer(img, context=self.context).data


class WigProductDetailSerializer(serializers.ModelSerializer):
    """
    images, primary_image, and reviews are SerializerMethodFields
    so the request context flows through to nested serializers.
    """
    images         = serializers.SerializerMethodField()
    primary_image  = serializers.SerializerMethodField()
    inch_pricing   = InchPricingSerializer(many=True, read_only=True)
    reviews        = serializers.SerializerMethodField()
    average_rating = serializers.ReadOnlyField()
    review_count   = serializers.ReadOnlyField()
    category       = CategorySerializer(read_only=True)

    class Meta:
        model  = WigProduct
        fields = (
            'id', 'name', 'slug', 'description', 'short_description',
            'hair_type', 'lace_type', 'density', 'category',
            'is_featured', 'is_trending', 'care_instructions',
            'images', 'primary_image', 'inch_pricing', 'reviews',
            'average_rating', 'review_count', 'created_at',
        )

    def get_images(self, obj):
        return WigImageSerializer(
            obj.images.all(),
            many=True,
            context=self.context   # request context passed through
        ).data

    def get_primary_image(self, obj):
        img = obj.primary_image
        if not img:
            return None
        return WigImageSerializer(img, context=self.context).data

    def get_reviews(self, obj):
        request      = self.context.get('request')
        current_user = (
            request.user
            if (request and request.user and request.user.is_authenticated)
            else None
        )
        approved = list(obj.reviews.filter(is_approved=True).order_by('-created_at'))
        if current_user:
            own_pending = obj.reviews.filter(
                is_approved=False,
                user=current_user,
            ).first()
            if own_pending:
                approved = [own_pending] + approved
        return ReviewSerializer(
            approved, many=True, context=self.context
        ).data


class HeroImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model  = HeroImage
        fields = ('slot', 'image', 'alt_text')

    def get_image(self, obj):
        return _absolute_image_url(obj.image, self.context)