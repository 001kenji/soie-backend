import uuid
from django.db import models
from django.utils.text import slugify
from apps.accounts.models import User


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class WigProduct(models.Model):
    HAIR_TYPE_CHOICES = [
        ('straight', 'Straight'),
        ('wavy', 'Wavy'),
        ('curly', 'Curly'),
        ('kinky', 'Kinky Curly'),
        ('body_wave', 'Body Wave'),
        ('deep_wave', 'Deep Wave'),
        ('loose_wave', 'Loose Wave'),
        ('water_wave', 'Water Wave'),
    ]

    LACE_TYPE_CHOICES = [
        ('4x4', '4x4 Lace Closure'),
        ('5x5', '5x5 Lace Closure'),
        ('13x4', '13x4 Lace Frontal'),
        ('13x6', '13x6 Lace Frontal'),
        ('full_lace', 'Full Lace'),
        ('no_lace', 'No Lace (Machine Made)'),
    ]

    DENSITY_CHOICES = [
        ('130', '130% Density'),
        ('150', '150% Density'),
        ('180', '180% Density'),
        ('200', '200% Density'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    hair_type = models.CharField(max_length=20, choices=HAIR_TYPE_CHOICES)
    lace_type = models.CharField(max_length=20, choices=LACE_TYPE_CHOICES, default='13x4')
    density = models.CharField(max_length=10, choices=DENSITY_CHOICES, default='150')
    is_featured = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    care_instructions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def primary_image(self):
        img = self.images.filter(is_primary=True).first()
        return img or self.images.first()

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return sum(r.rating for r in reviews) / len(reviews)
        return 0

    @property
    def review_count(self):
        return self.reviews.count()

    @property
    def min_price(self):
        pricing = self.inch_pricing.order_by('inches').first()
        return pricing.price if pricing else None


class WigImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(WigProduct, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.product.name} - Image {self.order}"

    def save(self, *args, **kwargs):
        if self.is_primary:
            WigImage.objects.filter(product=self.product, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)


class InchPricing(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(WigProduct, on_delete=models.CASCADE, related_name='inch_pricing')
    inches = models.PositiveIntegerField(help_text='Length in inches (e.g. 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30)')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=10)
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ('product', 'inches')
        ordering = ['inches']

    def __str__(self):
        return f"{self.product.name} — {self.inches}\" — ${self.price}"


class Review(models.Model):
    RATING_CHOICES = [(i, i) for i in range(1, 6)]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(WigProduct, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews')
    reviewer_name = models.CharField(max_length=100)
    message = models.TextField()
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, default=5)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.reviewer_name} — {self.product.name} ({self.rating}★)"

class HeroImage(models.Model):
    """
    Images shown in the website hero section and auth layout decorative rings.
    Admin can upload and manage these independently of product images.
    """
    SLOT_CHOICES = [
        ('hero_card',   'Hero Section — Main Card'),
        ('auth_ring_1', 'Auth Layout — Ring 1 (large)'),
        ('auth_ring_2', 'Auth Layout — Ring 2 (small)'),
    ]

    id         = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slot       = models.CharField(max_length=20, choices=SLOT_CHOICES, unique=True,
                                  help_text="Each slot holds one active image.")
    image      = models.ImageField(upload_to='hero/')
    alt_text   = models.CharField(max_length=200, blank=True)
    is_active  = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = 'Hero Image'
        verbose_name_plural = 'Hero Images'

    def __str__(self):
        return f"{self.get_slot_display()} — {'active' if self.is_active else 'inactive'}"

