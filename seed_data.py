#!/usr/bin/env python
"""
SOIE Database Seed Script
Run from the backend directory:
    python manage.py shell < seed_data.py
    -- or --
    cd backend && python seed_data.py
"""

import os
import sys
import django
from decimal import Decimal

# ─── Django setup (only needed if running as standalone script) ───────────────
if not os.environ.get('DJANGO_SETTINGS_MODULE'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.base')
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    django.setup()

# ─── Imports (after Django setup) ─────────────────────────────────────────────
from apps.accounts.models import User
from apps.products.models import Category, WigProduct, InchPricing, Review,HeroImage
from apps.shipping.models import ShippingConfig


print("=" * 60)
print("SOIE Seed Script")
print("=" * 60)


# ──────────────────────────────────────────────────────────────────────────────
# 1. SHIPPING CONFIGURATION
# ──────────────────────────────────────────────────────────────────────────────
print("\n[1/5] Creating shipping configuration...")

ShippingConfig.objects.all().delete()
ShippingConfig.objects.create(
    name               = "Standard Express Shipping",
    fee_usd            = Decimal("12.00"),
    estimated_days_min = 8,
    estimated_days_max = 15,
    description        = "Shipped from Asia via express international courier. Typical delivery 8–15 business days after payment confirmation.",
    is_active          = True,
)
print("      Shipping config created: $12.00 | 8–15 days")


# ──────────────────────────────────────────────────────────────────────────────
# 2. CATEGORIES
# ──────────────────────────────────────────────────────────────────────────────
print("\n[2/5] Creating categories...")

categories_data = [
    {"name": "Lace Front Wigs",  "slug": "lace-front-wigs",  "description": "Premium 13x4 and 13x6 lace frontal wigs for a natural hairline."},
    {"name": "Closure Wigs",     "slug": "closure-wigs",     "description": "4x4 and 5x5 lace closure wigs for versatile styling."},
    {"name": "Full Lace Wigs",   "slug": "full-lace-wigs",   "description": "Full lace wigs for maximum styling flexibility."},
]

cats = {}
for cd in categories_data:
    cat, created = Category.objects.get_or_create(slug=cd["slug"], defaults=cd)
    cats[cd["slug"]] = cat
    print(f"      {'Created' if created else 'Exists '}: {cat.name}")


# ──────────────────────────────────────────────────────────────────────────────
# 3. WIG PRODUCTS & PRICING
# ──────────────────────────────────────────────────────────────────────────────
print("\n[3/5] Creating wig products and inch pricing...")

products_data = [
    {
        "name":              "13x4 Transparent Lace Front Vietnamese Virgin Hair Straight Wig",
        "slug":              "vietnamese-virgin-straight-13x4",
        "category_slug":     "lace-front-wigs",
        "short_description": "Flawless straight look with 100% Vietnamese virgin hair and a wide 13x4 transparent lace front.",
        "description": (
            "Get a flawless, natural look with this 13x4 transparent lace frontal wig made from 100% Vietnamese virgin hair. "
            "Features silky straight strands, a pre-plucked hairline with baby hairs, and a wide lace for versatile middle, "
            "side, or free parting. Soft, strong, and tangle-free for a long-lasting, natural finish.\n\n"
            "Hair is collected with intact cuticles to ensure minimal shedding and maximum shine. "
            "Can be dyed, bleached, cut, and heat-styled up to 180°C without compromising quality."
        ),
        "hair_type":         "straight",
        "lace_type":         "13x4",
        "density":           "150",
        "care_instructions": (
            "Wash with sulfate-free, cold water. Gently detangle from tips to roots using a wide-tooth comb. "
            "Air dry on a wig stand. Apply a light serum for shine. Avoid sleeping in the wig without a satin cap. "
            "Store on a wig stand when not in use."
        ),
        "is_featured":       True,
        "is_trending":       False,
        "pricing": [
            (12, Decimal("60.00"), 15),
            (14, Decimal("70.00"), 15),
            (16, Decimal("80.00"), 12),
            (18, Decimal("90.00"), 12),
            (20, Decimal("100.00"), 10),
            (22, Decimal("110.00"), 10),
            (24, Decimal("120.00"), 8),
            (26, Decimal("130.00"), 8),
            (28, Decimal("140.00"), 6),
            (30, Decimal("150.00"), 5),
        ],
    },
    {
        "name":              "Indian Virgin Hair 13x4 Transparent Lace Front Deep Wave Wig",
        "slug":              "indian-virgin-deep-wave-13x4",
        "category_slug":     "lace-front-wigs",
        "short_description": "Defined, bouncy deep wave curls with 100% Indian virgin hair and a seamless transparent lace front.",
        "description": (
            "100% Indian Virgin Hair with intact cuticles for natural shine and minimal shedding. "
            "The 13x4 transparent lace provides a natural hairline that blends seamlessly with most skin tones. "
            "Deep Wave texture features defined, bouncy S-curls with high volume and lasting hold. "
            "Pre-plucked hairline with baby hairs for a realistic, ready-to-wear finish.\n\n"
            "180% density for maximum fullness and volume. Can be dyed, bleached, straightened, and "
            "heat styled without losing the wave pattern. Suitable for all occasions."
        ),
        "hair_type":         "deep_wave",
        "lace_type":         "13x4",
        "density":           "180",
        "care_instructions": (
            "To maintain the deep wave pattern, wash with a curl-enhancing shampoo and conditioner. "
            "Do not rub — squeeze gently and air dry. Scrunch with a wave-defining cream while damp. "
            "Avoid brushing when dry to prevent frizz. Use a diffuser on low heat if needed."
        ),
        "is_featured":       True,
        "is_trending":       True,
        "pricing": [
            (12, Decimal("48.00"), 15),
            (14, Decimal("58.00"), 15),
            (16, Decimal("68.00"), 12),
            (18, Decimal("78.00"), 12),
            (20, Decimal("88.00"), 10),
            (22, Decimal("98.00"), 10),
            (24, Decimal("108.00"), 8),
            (26, Decimal("118.00"), 8),
            (28, Decimal("128.00"), 6),
            (30, Decimal("138.00"), 5),
        ],
    },
    {
        "name":              "Japanese Virgin Hair 13x4 Transparent Lace Front Loose Wave Wig",
        "slug":              "japanese-virgin-loose-wave-13x4",
        "category_slug":     "lace-front-wigs",
        "short_description": "Soft, flowing loose waves with silky Japanese virgin hair and an undetectable transparent lace front.",
        "description": (
            "100% Japanese Virgin Hair with intact cuticles for a silky, lightweight feel and minimal shedding. "
            "The 13x4 transparent lace creates an undetectable hairline that blends smoothly with most skin tones. "
            "Loose Wave texture features soft, flowing waves with natural volume and bounce for an effortless look. "
            "Pre-plucked hairline with baby hairs for a realistic, ready-to-wear finish.\n\n"
            "180% density. Can be dyed, bleached, straightened, and heat styled while maintaining the wave pattern. "
            "Japanese hair is known for its exceptional silkiness and long-lasting texture retention."
        ),
        "hair_type":         "loose_wave",
        "lace_type":         "13x4",
        "density":           "180",
        "care_instructions": (
            "Wash gently with lukewarm water and a moisturising shampoo. Apply a hydrating conditioner and leave for 5 minutes. "
            "Rinse and gently squeeze out excess water — do not wring. Air dry naturally or use a low-heat diffuser. "
            "Finger-style the waves while damp for best results. Avoid excessive heat styling."
        ),
        "is_featured":       True,
        "is_trending":       True,
        "pricing": [
            (12, Decimal("48.00"), 15),
            (14, Decimal("58.00"), 15),
            (16, Decimal("68.00"), 12),
            (18, Decimal("78.00"), 12),
            (20, Decimal("88.00"), 10),
            (22, Decimal("98.00"), 10),
            (24, Decimal("108.00"), 8),
            (26, Decimal("118.00"), 8),
            (28, Decimal("128.00"), 6),
            (30, Decimal("138.00"), 5),
        ],
    },
    {
        "name":              "13x4 Transparent Lace Front Vietnamese Virgin Hair Deep Curl Wig",
        "slug":              "vietnamese-virgin-deep-curl-13x4",
        "category_slug":     "lace-front-wigs",
        "short_description": "Gorgeous, tight deep curls with 100% Vietnamese virgin hair. Full volume, natural hairline.",
        "description": (
            "Experience the beauty of rich, voluminous deep curls with this 13x4 transparent lace front wig, "
            "crafted from 100% Vietnamese virgin hair. The deep curl pattern creates stunning, coily ringlets "
            "with incredible bounce and definition — perfect for a bold, natural look.\n\n"
            "Features a pre-plucked hairline with baby hairs for a seamless blend. The transparent 13x4 lace "
            "allows for versatile parting options. 150% density gives a full, lush appearance without feeling heavy. "
            "Hair is completely free of chemical processing — no dyes, no perms, no silicone coating."
        ),
        "hair_type":         "curly",
        "lace_type":         "13x4",
        "density":           "150",
        "care_instructions": (
            "Deep curls require extra moisture to stay defined. Co-wash weekly with a hydrating conditioner. "
            "Apply a curl cream or gel while hair is soaking wet and scrunch upward. "
            "Air dry completely before wearing. Refresh with a water and leave-in conditioner spray. "
            "Avoid combing or brushing — use your fingers to detangle only."
        ),
        "is_featured":       False,
        "is_trending":       True,
        "pricing": [
            (10, Decimal("55.00"), 12),
            (12, Decimal("65.00"), 12),
            (14, Decimal("75.00"), 10),
            (16, Decimal("85.00"), 10),
            (18, Decimal("95.00"), 8),
            (20, Decimal("105.00"), 8),
            (22, Decimal("115.00"), 6),
            (24, Decimal("125.00"), 6),
            (26, Decimal("135.00"), 4),
            (28, Decimal("145.00"), 4),
        ],
    },
]

# ─── Hero Image slots (create empty slots for admin to fill via image upload) ──

print("\n[+] Creating hero image slots...")
for slot, label in HeroImage.SLOT_CHOICES:
    HeroImage.objects.get_or_create(slot=slot, defaults={'alt_text': label, 'is_active': False})
    print(f"      Slot ready: {slot}")
print("      Go to Admin → Hero Images to upload images for each slot.")

created_products = {}
for pd in products_data:
    pricing_data  = pd.pop("pricing")
    category_slug = pd.pop("category_slug")

    product, created = WigProduct.objects.get_or_create(
        slug=pd["slug"],
        defaults={
            **pd,
            "category":  cats.get(category_slug),
            "is_active": True,
        }
    )
    created_products[product.slug] = product
    status = "Created" if created else "Exists "
    print(f"      {status}: {product.name[:55]}...")

    # Create inch pricing
    for inches, price, stock in pricing_data:
        InchPricing.objects.get_or_create(
            product=product,
            inches=inches,
            defaults={"price": price, "stock_quantity": stock, "is_available": True},
        )
    print(f"              {len(pricing_data)} inch price tiers added")


# ──────────────────────────────────────────────────────────────────────────────
# 4. REVIEWER ACCOUNTS & REVIEWS
# ──────────────────────────────────────────────────────────────────────────────
print("\n[4/5] Creating reviewer accounts and reviews...")

reviewer_accounts = [
    {"email": "amara.ndiaye@soie-review.com",    "first_name": "Amara",    "last_name": "Ndiaye",    "password": "soie-review-2024!"},
    {"email": "fatima.okonkwo@soie-review.com",  "first_name": "Fatima",   "last_name": "Okonkwo",   "password": "soie-review-2024!"},
    {"email": "zanele.dlamini@soie-review.com",  "first_name": "Zanele",   "last_name": "Dlamini",   "password": "soie-review-2024!"},
    {"email": "aisha.kamara@soie-review.com",    "first_name": "Aisha",    "last_name": "Kamara",    "password": "soie-review-2024!"},
    {"email": "chioma.eze@soie-review.com",      "first_name": "Chioma",   "last_name": "Eze",       "password": "soie-review-2024!"},
    {"email": "naledi.sithole@soie-review.com",  "first_name": "Naledi",   "last_name": "Sithole",   "password": "soie-review-2024!"},
    {"email": "grace.mensah@soie-review.com",    "first_name": "Grace",    "last_name": "Mensah",    "password": "soie-review-2024!"},
    {"email": "sarah.london@soie-review.com",    "first_name": "Sarah",    "last_name": "Collins",   "password": "soie-review-2024!"},
    {"email": "priya.sharma@soie-review.com",    "first_name": "Priya",    "last_name": "Sharma",    "password": "soie-review-2024!"},
    {"email": "kefilwe.mokoena@soie-review.com", "first_name": "Kefilwe",  "last_name": "Mokoena",   "password": "soie-review-2024!"},
]

reviewer_users = {}
for ra in reviewer_accounts:
    user, created = User.objects.get_or_create(
        email=ra["email"],
        defaults={
            "first_name": ra["first_name"],
            "last_name":  ra["last_name"],
            "is_active":  True,
        },
    )
    if created:
        user.set_password(ra["password"])
        user.save()
    reviewer_users[ra["first_name"]] = user

print(f"      {len(reviewer_users)} reviewer accounts ready")

# ─── Reviews data ─────────────────────────────────────────────────────────────
reviews_data = [
    # ── Vietnamese Straight ──────────────────────────────────────────────────
    {
        "product_slug":  "vietnamese-virgin-straight-13x4",
        "reviewer_name": "Amara Ndiaye",
        "user_first":    "Amara",
        "rating":        5,
        "message": (
            "The deep wave was so good and looked very natural! Amazing quality for the price. "
            "I got many compliments from my colleagues. The lace blended perfectly with my skin. "
            "Shipping was fast — arrived in 11 days. Will definitely reorder."
        ),
        "is_approved": True,
    },
    {
        "product_slug":  "vietnamese-virgin-straight-13x4",
        "reviewer_name": "Sarah Collins",
        "user_first":    "Sarah",
        "rating":        5,
        "message": (
            "Really impressed with the softness and volume. I was hesitant to order from an online shop "
            "but SOIE exceeded all my expectations. The straight wig is absolutely silky — no tangling, "
            "no shedding. The lace is incredibly thin and natural-looking. 10 out of 10."
        ),
        "is_approved": True,
    },
    {
        "product_slug":  "vietnamese-virgin-straight-13x4",
        "reviewer_name": "Kefilwe Mokoena",
        "user_first":    "Kefilwe",
        "rating":        5,
        "message": (
            "I ordered the 20 inch and it is everything I wanted. Silky, full, and so natural-looking. "
            "The pre-plucked hairline saved me so much time. Arrived well-packaged in exactly 13 days. "
            "The price for this quality is honestly unbeatable."
        ),
        "is_approved": True,
    },
    # ── Indian Deep Wave ─────────────────────────────────────────────────────
    {
        "product_slug":  "indian-virgin-deep-wave-13x4",
        "reviewer_name": "Fatima Okonkwo",
        "user_first":    "Fatima",
        "rating":        5,
        "message": (
            "Amazing quality for the price. I got many compliments at my sister's wedding. "
            "The deep wave curls are so defined and bouncy — they did not drop all day even in humidity. "
            "I was worried the lace would be visible but it blended seamlessly. Highly recommend."
        ),
        "is_approved": True,
    },
    {
        "product_slug":  "indian-virgin-deep-wave-13x4",
        "reviewer_name": "Chioma Eze",
        "user_first":    "Chioma",
        "rating":        5,
        "message": (
            "The deep wave was so good and looked very natural. The 180% density is FULL — "
            "I was not expecting so much volume. It has been 3 months now and the wave pattern "
            "is still holding beautifully after multiple washes. This is my new favourite wig."
        ),
        "is_approved": True,
    },
    {
        "product_slug":  "indian-virgin-deep-wave-13x4",
        "reviewer_name": "Grace Mensah",
        "user_first":    "Grace",
        "rating":        5,
        "message": (
            "Really impressed with the softness and volume. The deep wave Indian hair feels so light on my head "
            "compared to other wigs I have worn. Received in 10 days — faster than expected. "
            "Customer service was also very responsive. Already recommended to 5 of my friends."
        ),
        "is_approved": True,
    },
    # ── Japanese Loose Wave ──────────────────────────────────────────────────
    {
        "product_slug":  "japanese-virgin-loose-wave-13x4",
        "reviewer_name": "Zanele Dlamini",
        "user_first":    "Zanele",
        "rating":        5,
        "message": (
            "SOIE has the most affordable luxury wigs I have ever found. I ordered the 24 inch loose wave "
            "Japanese wig and I am completely obsessed. The waves are so soft and flow beautifully. "
            "The lace is so thin it is practically invisible. I have received so many compliments."
        ),
        "is_approved": True,
    },
    {
        "product_slug":  "japanese-virgin-loose-wave-13x4",
        "reviewer_name": "Priya Sharma",
        "user_first":    "Priya",
        "rating":        5,
        "message": (
            "Amazing quality for the price. The Japanese hair has a unique silkiness that I have not "
            "experienced with other wigs. The loose waves are effortless and look completely natural. "
            "I wore it to a formal event and people genuinely thought it was my real hair. Stunning."
        ),
        "is_approved": True,
    },
    {
        "product_slug":  "japanese-virgin-loose-wave-13x4",
        "reviewer_name": "Naledi Sithole",
        "user_first":    "Naledi",
        "rating":        4,
        "message": (
            "Really impressed with the softness and volume. The only reason I am giving 4 stars instead of 5 "
            "is that my package took 16 days which was slightly over the estimated time. But the quality "
            "of the wig itself is exceptional — absolutely no complaints there. Would buy again."
        ),
        "is_approved": True,
    },
    # ── Vietnamese Deep Curl ─────────────────────────────────────────────────
    {
        "product_slug":  "vietnamese-virgin-deep-curl-13x4",
        "reviewer_name": "Aisha Kamara",
        "user_first":    "Aisha",
        "rating":        5,
        "message": (
            "The deep curl is everything! So bouncy and defined — exactly what I was looking for. "
            "The curls are tight and springy and have stayed gorgeous even after washing. "
            "The hairline blends so naturally with my skin. I got so many compliments at church."
        ),
        "is_approved": True,
    },
    {
        "product_slug":  "vietnamese-virgin-deep-curl-13x4",
        "reviewer_name": "Chioma Eze",
        "user_first":    "Chioma",
        "rating":        5,
        "message": (
            "Amazing quality for the price. I ordered the 22 inch and the volume is incredible. "
            "The curls are so defined and lively — they honestly look better than my natural hair. "
            "Delivery was smooth and arrived in 12 days. SOIE has gained a customer for life."
        ),
        "is_approved": True,
    },
]

review_count = 0
for rd in reviews_data:
    product_slug  = rd.pop("product_slug")
    user_first    = rd.pop("user_first")
    product = created_products.get(product_slug)
    user    = reviewer_users.get(user_first)

    if not product:
        print(f"      WARNING: product '{product_slug}' not found, skipping review")
        continue

    _, created = Review.objects.get_or_create(
        product       = product,
        reviewer_name = rd["reviewer_name"],
        defaults={
            **rd,
            "user": user,
        }
    )
    if created:
        review_count += 1

print(f"      {review_count} reviews created and approved")


# ──────────────────────────────────────────────────────────────────────────────
# 5. SUMMARY
# ──────────────────────────────────────────────────────────────────────────────
print("\n[5/5] Summary")
print("-" * 40)
print(f"  Categories:    {Category.objects.count()}")
print(f"  Products:      {WigProduct.objects.count()}")
print(f"  Inch Tiers:    {InchPricing.objects.count()}")
print(f"  Reviews:       {Review.objects.count()}")
print(f"  Users:         {User.objects.count()}")
print(f"  Shipping:      {ShippingConfig.objects.count()} config(s)")
print("-" * 40)
print("\nSeed complete. Visit /admin to upload product images.")
print("Admin bulk upload: Products → Select product → 'Bulk Upload Images' button")
print("=" * 60)