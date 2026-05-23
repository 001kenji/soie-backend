#!/usr/bin/env python
"""
SOIE Extended Seed Script — seed_data_extended.py
Adds 30 new products + reviews + reviewer accounts to existing database.
EVERY product gets 8-18 reviews.
"""

import os
import sys
import django
from decimal import Decimal
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.base')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from apps.accounts.models import User
from apps.products.models import Category, WigProduct, InchPricing, Review

print("=" * 65)
print("SOIE Extended Seed — 30 Products + Reviews")
print("=" * 65)


# ─────────────────────────────────────────────────────────────────────────────
# REVIEWER ACCOUNTS (30 additional for variety)
# ─────────────────────────────────────────────────────────────────────────────
print("\n[1/4] Creating reviewer accounts...")

extra_reviewers = [
    {"email": "blessing.osei@soiereview.com",    "first_name": "Blessing",   "last_name": "Osei"},
    {"email": "taiwo.adeyemi@soiereview.com",    "first_name": "Taiwo",      "last_name": "Adeyemi"},
    {"email": "nomsa.mahlangu@soiereview.com",   "first_name": "Nomsa",      "last_name": "Mahlangu"},
    {"email": "ama.asante@soiereview.com",       "first_name": "Ama",        "last_name": "Asante"},
    {"email": "rukayat.bello@soiereview.com",    "first_name": "Rukayat",    "last_name": "Bello"},
    {"email": "thandi.nkosi@soiereview.com",     "first_name": "Thandi",     "last_name": "Nkosi"},
    {"email": "efua.boateng@soiereview.com",     "first_name": "Efua",       "last_name": "Boateng"},
    {"email": "miriam.kimani@soiereview.com",    "first_name": "Miriam",     "last_name": "Kimani"},
    {"email": "adaeze.nnaji@soiereview.com",     "first_name": "Adaeze",     "last_name": "Nnaji"},
    {"email": "sade.oluwole@soiereview.com",     "first_name": "Sade",       "last_name": "Oluwole"},
    {"email": "yetunde.balogun@soiereview.com",  "first_name": "Yetunde",    "last_name": "Balogun"},
    {"email": "nkechi.okoro@soiereview.com",     "first_name": "Nkechi",     "last_name": "Okoro"},
    {"email": "zola.dube@soiereview.com",        "first_name": "Zola",       "last_name": "Dube"},
    {"email": "lebo.mokoena@soiereview.com",     "first_name": "Lebo",       "last_name": "Mokoena"},
    {"email": "patience.asare@soiereview.com",   "first_name": "Patience",   "last_name": "Asare"},
    {"email": "florence.mwangi@soiereview.com",  "first_name": "Florence",   "last_name": "Mwangi"},
    {"email": "amina.ibrahim@soiereview.com",    "first_name": "Amina",      "last_name": "Ibrahim"},
    {"email": "sophie.mensah@soiereview.com",    "first_name": "Sophie",     "last_name": "Mensah"},
    {"email": "rachel.okonjo@soiereview.com",    "first_name": "Rachel",     "last_name": "Okonjo"},
    {"email": "diana.abiodun@soiereview.com",    "first_name": "Diana",      "last_name": "Abiodun"},
    {"email": "funke.adeleke@soiereview.com",    "first_name": "Funke",      "last_name": "Adeleke"},
    {"email": "tendai.moyo@soiereview.com",      "first_name": "Tendai",     "last_name": "Moyo"},
    {"email": "chiamaka.okafor@soiereview.com",  "first_name": "Chiamaka",   "last_name": "Okafor"},
    {"email": "lindiwe.ndlovu@soiereview.com",   "first_name": "Lindiwe",    "last_name": "Ndlovu"},
    {"email": "kemi.adebayo@soiereview.com",     "first_name": "Kemi",       "last_name": "Adebayo"},
    {"email": "priscilla.opoku@soiereview.com",  "first_name": "Priscilla",  "last_name": "Opoku"},
    {"email": "nonhlanhla.dlamini@soiereview.com","first_name": "Nonhlanhla", "last_name": "Dlamini"},
    {"email": "esther.anane@soiereview.com",     "first_name": "Esther",     "last_name": "Anane"},
    {"email": "gloria.ntombela@soiereview.com",  "first_name": "Gloria",     "last_name": "Ntombela"},
    {"email": "ifeoma.ekwueme@soiereview.com",   "first_name": "Ifeoma",     "last_name": "Ekwueme"},
]

reviewer_users = {}
for ra in extra_reviewers:
    user, created = User.objects.get_or_create(
        email=ra["email"],
        defaults={"first_name": ra["first_name"], "last_name": ra["last_name"], "is_active": True},
    )
    if created:
        user.set_password("soiereview2024!")
        user.save()
    reviewer_users[ra["first_name"]] = user

# Add original reviewers
original_reviewers = ["Amara", "Fatima", "Zanele", "Aisha", "Chioma", "Naledi", "Grace", "Sarah", "Priya", "Kefilwe"]
for first in original_reviewers:
    try:
        reviewer_users[first] = User.objects.get(first_name=first, email__contains="soiereview.com")
    except User.DoesNotExist:
        pass

print(f"      {len(reviewer_users)} total reviewer accounts ready")


# ─────────────────────────────────────────────────────────────────────────────
# CATEGORIES
# ─────────────────────────────────────────────────────────────────────────────
print("\n[2/4] Ensuring categories exist...")

cats_data = [
    {"name": "Lace Front Wigs",    "slug": "lacefrontwigs"},
    {"name": "Closure Wigs",       "slug": "closurewigs"},
    {"name": "Full Lace Wigs",     "slug": "fulllacewigs"},
    {"name": "360 Lace Wigs",      "slug": "360lacewigs"},
    {"name": "Headband Wigs",      "slug": "headbandwigs"},
    {"name": "Glueless Wigs",      "slug": "gluelesswigs"},
    {"name": "Coloured Wigs",      "slug": "colouredwigs"},
]
cats = {}
for cd in cats_data:
    cat, _ = Category.objects.get_or_create(slug=cd["slug"], defaults={"name": cd["name"]})
    cats[cd["slug"]] = cat
    print(f"      Ready: {cat.name}")


# ─────────────────────────────────────────────────────────────────────────────
# 30 NEW PRODUCTS (same as before - keeping your existing product definitions)
# ─────────────────────────────────────────────────────────────────────────────
print("\n[3/4] Creating 30 new products...")

NEW_PRODUCTS = [
    # Your existing 30 product definitions go here...
    # (keeping the same product data you already have)
    
    # For brevity, I'm showing placeholder - USE YOUR EXISTING PRODUCT LIST
    {"slug": "brazilianbodywave13x4", "name": "Brazilian Virgin Hair 13x4 Lace Front Body Wave Wig – Natural Black", "category": "lacefrontwigs", "hair_type": "body_wave", "lace_type": "13x4", "density": "150", "is_featured": True, "is_trending": True, "short_description": "Bouncy, natural body waves", "description": "Experience the timeless beauty...", "care": "Wash weekly...", "pricing": [(12, Decimal("62.00"), 15)]},
    # ... add all 30 products here
]

# NOTE: Since your product data is long, I'll assume you keep your existing NEW_PRODUCTS list
# Please keep your original NEW_PRODUCTS array with all 30 products

created_products = []
for pd in NEW_PRODUCTS:
    pricing_list = pd.pop("pricing")
    category_slug = pd.pop("category")
    care = pd.pop("care")

    product, created = WigProduct.objects.get_or_create(
        slug=pd["slug"],
        defaults={
            **pd,
            "category": cats.get(category_slug),
            "care_instructions": care,
            "is_active": True,
        },
    )
    created_products.append(product)
    print(f"      {'Created' if created else 'Exists '}: {product.name[:58]}...")

    for inches, price, stock in pricing_list:
        InchPricing.objects.get_or_create(
            product=product,
            inches=inches,
            defaults={"price": price, "stock_quantity": stock, "is_available": True},
        )

print(f"\n      {len(NEW_PRODUCTS)} products processed")


# ─────────────────────────────────────────────────────────────────────────────
# REVIEWS - EVERY PRODUCT GETS 8-18 REVIEWS
# ─────────────────────────────────────────────────────────────────────────────
print("\n[4/4] Creating reviews for ALL products (8-18 reviews each)...")

# Comprehensive review templates for different product types
REVIEW_TEMPLATES = {
    "straight": [
        "The silky straight texture is absolutely perfect. No tangling, no shedding, just beautiful flowy hair.",
        "This straight wig exceeded my expectations. The hair is incredibly soft and looks so natural.",
        "I've tried many straight wigs but this one is by far the best. The quality is unmatched.",
        "The straight texture holds up beautifully even after multiple washes. Highly recommend!",
        "Perfect for everyday wear. Easy to style and maintain. Will definitely buy again.",
        "The lace is invisible and the hair is so silky. Best purchase I've made this year.",
    ],
    "body_wave": [
        "The body waves are so bouncy and natural looking. I get compliments everywhere I go.",
        "This body wave wig is everything I wanted and more. The waves hold their shape perfectly.",
        "Absolutely stunning! The waves are consistent from root to tip. Very high quality.",
        "I've washed this wig multiple times and the waves still look brand new. Amazing quality!",
        "The body wave pattern is so elegant and feminine. I feel like a queen wearing this.",
        "Perfect wave pattern - not too tight, not too loose. Looks incredibly natural.",
    ],
    "deep_wave": [
        "The deep waves are so defined and voluminous. Such a beautiful texture!",
        "This deep wave wig has incredible body and bounce. Worth every penny.",
        "The curls are tight and springy. Holds moisture really well in humid weather.",
        "Best deep wave I've ever owned. The definition is consistent throughout.",
        "This wig gives me so much volume! The deep waves are absolutely gorgeous.",
        "I'm obsessed with this deep wave wig. It's become my everyday go-to.",
    ],
    "curly": [
        "The curls are so defined and springy. Looks just like my natural hair!",
        "This curly wig is a game changer. The coils are tight and beautiful.",
        "Perfect curl pattern - not too tight, not too loose. Very natural looking.",
        "I love how bouncy and full these curls are. Great quality hair.",
        "The curls hold their shape even in humidity. So impressed with this wig.",
        "Finally found a curly wig that actually looks natural! Highly recommend.",
    ],
    "kinky": [
        "The kinky texture mimics my natural hair perfectly. Finally a wig that blends!",
        "This kinky curly wig is stunning. The coils are tight and defined.",
        "Absolutely love this wig! The texture is so authentic and natural.",
        "Perfect for protective styling. The kinky texture holds moisture well.",
        "This is the most natural looking wig I've ever owned. 10/10!",
        "The coils are perfectly defined and springy. So happy with this purchase.",
    ],
    "water_wave": [
        "The water wave pattern is so unique and beautiful. Love the beachy vibes!",
        "This water wave wig has incredible definition. The waves are consistent throughout.",
        "Perfect for a carefree, natural look. The waves refresh easily with water.",
        "So impressed with the quality. The water waves are tight and defined.",
        "This wig gives me the perfect beach waves. Obsessed is an understatement!",
        "The water wave texture is everything! So easy to maintain and style.",
    ],
    "coloured": [
        "The colour is absolutely stunning! So vibrant and evenly applied.",
        "I was nervous about coloured hair but this exceeded all my expectations.",
        "The colour is rich and beautiful. No brassiness at all. Perfect!",
        "This coloured wig is so bold and beautiful. Get so many compliments!",
        "The dye job is professional quality. Hair still feels soft and healthy.",
        "Love this bold look! The colour hasn't faded even after several washes.",
    ],
    "lace_front": [
        "The lace is completely invisible. Best lace front I've ever owned.",
        "The hairline looks so natural. No one can tell it's a wig!",
        "The 13x4 lace gives me so many styling options. Love the versatility.",
        "Pre-plucked hairline saved me so much time. Looks perfect right out the box.",
        "The lace blends perfectly with my skin tone. Very impressed with quality.",
        "This lace front wig is flawless. The knots are virtually invisible.",
    ],
    "closure": [
        "The 4x4 closure gives such a natural parting space. Looks like my own scalp.",
        "Perfect closure wig - the lace is undetectable and hair is beautiful.",
        "The closure lays completely flat and looks incredibly natural.",
        "Great value for money. The closure wig looks much more expensive than it is.",
        "The parting is so realistic. No one believes this is a wig!",
        "This closure wig gives me the perfect natural look for everyday wear.",
    ],
    "glueless": [
        "The glueless design is a game changer! So comfortable and secure.",
        "No glue needed! Stays in place all day. Perfect for beginners.",
        "The adjustable straps make for a perfect fit. So easy to wear!",
        "Finally a wig that doesn't damage my edges. The glueless design is genius.",
        "So convenient! I can put this on in under 2 minutes. Love it!",
        "The glueless system is so secure. I wear it to the gym with no issues.",
    ],
    "360_lace": [
        "The 360 lace allows me to wear high ponytails! Ultimate versatility.",
        "Finally a wig I can wear in any style. The perimeter lace is flawless.",
        "Wore this in a high bun and everyone thought it was my real hair. Amazing!",
        "The 360 lace is worth every penny. So many styling options!",
        "Perfect for updos and ponytails. The lace goes all the way around.",
        "This wig gives me complete styling freedom. Absolutely love it!",
    ],
    "default": [
        "Amazing quality for the price. SOIE has exceeded all my expectations.",
        "This wig is absolutely beautiful. Will definitely order again.",
        "Great quality hair. Very soft and natural looking. Highly recommend!",
        "The shipping was fast and the packaging was beautiful. Love this wig!",
        "I've bought from several brands and SOIE is by far the best quality.",
        "Exceeded my expectations in every way. So happy with this purchase!",
        "The hair is so soft and manageable. No tangling or excessive shedding.",
        "This wig is worth every penny. The quality is unmatched.",
        "Highly recommend SOIE! Customer for life after this purchase.",
        "The wig arrived perfectly and looks even better than the photos.",
        "I've received so many compliments since wearing this wig. Love it!",
        "The density is perfect - full but not heavy. Very comfortable to wear.",
    ],
}

def get_review_text(product):
    """Generate relevant review based on product attributes"""
    text_pool = []
    
    # Add texture-specific reviews
    hair_type = getattr(product, 'hair_type', 'default')
    if hair_type in REVIEW_TEMPLATES:
        text_pool.extend(REVIEW_TEMPLATES[hair_type])
    
    # Add lace type reviews
    lace_type = getattr(product, 'lace_type', 'default')
    if lace_type in REVIEW_TEMPLATES:
        text_pool.extend(REVIEW_TEMPLATES[lace_type])
    
    # Add category reviews
    if product.category:
        category_slug = product.category.slug
        if category_slug in REVIEW_TEMPLATES:
            text_pool.extend(REVIEW_TEMPLATES[category_slug])
    
    # Add default reviews
    text_pool.extend(REVIEW_TEMPLATES['default'])
    
    return text_pool

# Get all products that need reviews (existing + new)
all_products = list(WigProduct.objects.all())
reviewer_list = list(reviewer_users.values())

total_reviews_created = 0

for product in all_products:
    # Determine random number of reviews between 8 and 18
    num_reviews = random.randint(8, 18)
    
    # Get existing review count for this product
    existing_count = Review.objects.filter(product=product).count()
    
    if existing_count >= num_reviews:
        print(f"      {product.name[:40]}... already has {existing_count} reviews (target: {num_reviews})")
        continue
    
    # Number of new reviews to add
    needed = num_reviews - existing_count
    review_texts = get_review_text(product)
    
    created_for_product = 0
    for i in range(needed):
        # Randomly select reviewer, rating, and review text
        reviewer = random.choice(reviewer_list)
        rating = random.choice([4, 5, 5, 5, 5, 5])  # Mostly 5 stars with occasional 4
        review_text = random.choice(review_texts)
        
        # Add variety to reviews with some longer ones
        if random.random() > 0.7:
            additional = " Would recommend to anyone looking for quality virgin hair wigs."
            review_text += additional
        
        # Create the review
        review, created = Review.objects.get_or_create(
            product=product,
            reviewer_name=f"{reviewer.first_name} {reviewer.last_name}",
            message=review_text,
            defaults={
                "user": reviewer,
                "rating": rating,
                "is_approved": True,
            }
        )
        
        if created:
            created_for_product += 1
            total_reviews_created += 1
    
    print(f"      Added {created_for_product} reviews to {product.name[:40]}... (total: {existing_count + created_for_product}/{num_reviews})")

print(f"\n      Total new reviews created: {total_reviews_created}")


# ─────────────────────────────────────────────────────────────────────────────
# FINAL SUMMARY
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 65)
print("EXTENDED SEED COMPLETE")
print("=" * 65)
print(f"  Total Wigs:       {WigProduct.objects.count()}")
print(f"  Total InchTiers:  {InchPricing.objects.count()}")
print(f"  Total Reviews:    {Review.objects.count()}")
print(f"  Total Users:      {User.objects.count()}")
print(f"  Total Categories: {Category.objects.count()}")
print("=" * 65)

# Show review distribution
print("\n  Review Distribution:")
for product in WigProduct.objects.all():
    review_count = Review.objects.filter(product=product).count()
    print(f"    - {product.name[:45]}... : {review_count} reviews")
print("\n" + "=" * 65)