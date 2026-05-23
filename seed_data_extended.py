#!/usr/bin/env python
"""
SOIE Extended Seed Script — seed_data_extended.py
Adds 30 new products + reviews + reviewer accounts to existing database.

Run AFTER seed_data.py (original seed):
    python manage.py shell < seed_data_extended.py
"""

import os
import sys
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.base')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from apps.accounts.models import User
from apps.products.models import Category, WigProduct, InchPricing, Review

print("=" * 65)
print("SOIE Extended Seed — 30 Products + Reviews")
print("=" * 65)


# ─────────────────────────────────────────────────────────────────────────────
# REVIEWER ACCOUNTS (20 additional)
# ─────────────────────────────────────────────────────────────────────────────
print("\n[1/4] Creating additional reviewer accounts...")

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

# Also pull in original reviewers
for first in ["Amara", "Fatima", "Zanele", "Aisha", "Chioma", "Naledi", "Grace", "Sarah", "Priya", "Kefilwe"]:
    try:
        reviewer_users[first] = User.objects.get(first_name=first, email__contains="soiereview.com")
    except User.DoesNotExist:
        pass

print(f"      {len(reviewer_users)} total reviewer accounts ready")


# ─────────────────────────────────────────────────────────────────────────────
# CATEGORIES (ensure all exist)
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
# 30 NEW PRODUCTS
# Each entry: name, slug, category, hair_type, lace_type, density,
#             short_desc, description, care, is_featured, is_trending,
#             pricing [(inches, price, stock), ...]
# ─────────────────────────────────────────────────────────────────────────────
print("\n[3/4] Creating 30 new products...")

NEW_PRODUCTS = [

    # ── 1 ──
    {
        "name":        "Brazilian Virgin Hair 13x4 Lace Front Body Wave Wig – Natural Black",
        "slug":        "brazilianbodywave13x4",
        "category":    "lacefrontwigs",
        "hair_type":   "body_wave",
        "lace_type":   "13x4",
        "density":     "150",
        "is_featured": True,
        "is_trending": True,
        "short_description": "Bouncy, natural body waves with 100% Brazilian virgin hair and a seamless 13x4 transparent lace front.",
        "description": (
            "Experience the timeless beauty of body wave hair with this premium 13x4 lace front wig crafted from "
            "100% Brazilian virgin hair. Brazilian hair is renowned for its natural lustre, durability, and ability "
            "to blend seamlessly with a wide range of textures. The body wave pattern delivers soft, flowing Sshaped "
            "waves that frame the face beautifully and hold their shape even in humidity.\n\n"
            "Preplucked hairline with baby hairs creates a completely natural look straight out of the box. "
            "The transparent 13x4 lace provides a realistic scalp appearance and allows for flexible parting "
            "in the middle, side, or free style. 150% density ensures a full, natural volume that doesn't feel heavy."
        ),
        "care": "Wash weekly with moisturising shampoo. Air dry on a wig stand. Use a widetooth comb from tips to roots.",
        "pricing": [
            (12, Decimal("62.00"), 15), (14, Decimal("72.00"), 15),
            (16, Decimal("82.00"), 12), (18, Decimal("92.00"), 12),
            (20, Decimal("105.00"), 10), (22, Decimal("118.00"), 10),
            (24, Decimal("132.00"), 8), (26, Decimal("148.00"), 6),
            (28, Decimal("162.00"), 5), (30, Decimal("178.00"), 4),
        ],
    },

    # ── 2 ──
    {
        "name":        "Peruvian Virgin Hair 13x4 Lace Front Water Wave Wig – Natural Black",
        "slug":        "peruvianwaterwave13x4",
        "category":    "lacefrontwigs",
        "hair_type":   "wavy",
        "lace_type":   "13x4",
        "density":     "180",
        "is_featured": True,
        "is_trending": False,
        "short_description": "Gorgeous water wave texture with thick, fullbodied Peruvian virgin hair.",
        "description": (
            "Peruvian virgin hair is one of the most soughtafter hair types in the world, prized for its "
            "natural thickness, softness, and versatility. This 13x4 lace front water wave wig features "
            "tight, consistent wave patterns that create a stunning beachy look with incredible volume.\n\n"
            "The water wave pattern holds moisture beautifully, making it ideal for humid climates. "
            "180% density delivers an impressively full wig that still feels lightweight and comfortable. "
            "Can be blown out for a wavy look or allowed to dry naturally for defined waves."
        ),
        "care": "Refresh waves with a water and leavein conditioner spray. Scrunch while damp for definition. Avoid brushing dry.",
        "pricing": [
            (12, Decimal("58.00"), 15), (14, Decimal("68.00"), 15),
            (16, Decimal("78.00"), 12), (18, Decimal("88.00"), 12),
            (20, Decimal("98.00"), 10), (22, Decimal("112.00"), 10),
            (24, Decimal("126.00"), 8), (26, Decimal("140.00"), 6),
            (28, Decimal("155.00"), 5), (30, Decimal("170.00"), 4),
        ],
    },

    # ── 3 ──
    {
        "name":        "Malaysian Virgin Hair 4x4 Closure Straight Wig – Natural Black",
        "slug":        "malaysianstraight4x4closure",
        "category":    "closurewigs",
        "hair_type":   "straight",
        "lace_type":   "4x4",
        "density":     "180",
        "is_featured": False,
        "is_trending": True,
        "short_description": "Silky straight Malaysian virgin hair with a natural 4x4 lace closure for everyday elegance.",
        "description": (
            "Malaysian virgin hair is celebrated for its natural shine, softness, and medium density that makes it "
            "feel like your own hair. This 4x4 lace closure straight wig offers a simple, elegant look that works "
            "for any occasion — from boardroom to brunch.\n\n"
            "The 4x4 lace closure sits at the crown and provides a realistic parting space. At 180% density, "
            "this wig delivers impressive fullness while remaining comfortable for allday wear. "
            "Straightens perfectly and holds up beautifully to heat styling."
        ),
        "care": "Wash with cool water and gentle shampoo. Blow dry on low heat. Straighten at 150–180°C maximum.",
        "pricing": [
            (10, Decimal("52.00"), 18), (12, Decimal("62.00"), 18),
            (14, Decimal("72.00"), 15), (16, Decimal("82.00"), 12),
            (18, Decimal("94.00"), 10), (20, Decimal("108.00"), 10),
            (22, Decimal("122.00"), 8), (24, Decimal("138.00"), 6),
            (26, Decimal("155.00"), 5),
        ],
    },

    # ── 4 ──
    {
        "name":        "Brazilian Virgin Hair 13x6 Lace Front Kinky Curly Wig – Natural Black",
        "slug":        "braziliankinkycurly13x6",
        "category":    "lacefrontwigs",
        "hair_type":   "kinky",
        "lace_type":   "13x6",
        "density":     "150",
        "is_featured": True,
        "is_trending": True,
        "short_description": "Bold, defined kinky curls with 100% Brazilian hair and a wide 13x6 lace for maximum styling freedom.",
        "description": (
            "Celebrate your natural texture with this stunning kinky curly wig made from 100% Brazilian virgin hair. "
            "The kinky curl pattern mimics natural Type 4 coily hair, delivering coils that are tight, springy, "
            "and full of personality. The wide 13x6 lace frontal provides more scalp coverage and allows for "
            "deeper parting than the standard 13x4.\n\n"
            "At 150% density, the wig is full without being overwhelming. Kinky curly hair absorbs moisture well, "
            "so regular deep conditioning keeps it looking vibrant. Perfect for protective styling."
        ),
        "care": "Cowash weekly. Apply curl cream on soaking wet hair. Air dry or diffuse on low heat. Never brush dry.",
        "pricing": [
            (10, Decimal("65.00"), 12), (12, Decimal("78.00"), 12),
            (14, Decimal("92.00"), 10), (16, Decimal("108.00"), 10),
            (18, Decimal("125.00"), 8), (20, Decimal("142.00"), 8),
            (22, Decimal("162.00"), 6), (24, Decimal("182.00"), 5),
            (26, Decimal("205.00"), 4),
        ],
    },

    # ── 5 ──
    {
        "name":        "Vietnamese Virgin Hair 360 Lace Frontal Body Wave Wig – Natural Black",
        "slug":        "vietnamesebodywave360lace",
        "category":    "360lacewigs",
        "hair_type":   "body_wave",
        "lace_type":   "full_lace",
        "density":     "150",
        "is_featured": False,
        "is_trending": True,
        "short_description": "Fullperimeter 360 lace with silky Vietnamese body wave — ultimate styling freedom.",
        "description": (
            "The 360 lace frontal wig wraps lace completely around the perimeter of the wig cap, giving you "
            "the freedom to style your hair in any direction — up, down, or in a high ponytail — while maintaining "
            "a completely natural hairline. Made from premium Vietnamese virgin hair, this body wave wig delivers "
            "the signature glossy, flowing waves that Vietnamese hair is famous for.\n\n"
            "The full 360degree lace coverage means no tracks are visible from any angle. "
            "Ideal for updos, braids, and high ponytails. A premium choice for those who love styling versatility."
        ),
        "care": "Store in a silk bag when not wearing. Deep condition monthly. Secure wig with adjustable straps or wig tape.",
        "pricing": [
            (12, Decimal("88.00"), 10), (14, Decimal("102.00"), 10),
            (16, Decimal("118.00"), 8), (18, Decimal("135.00"), 8),
            (20, Decimal("155.00"), 6), (22, Decimal("175.00"), 5),
            (24, Decimal("198.00"), 4), (26, Decimal("222.00"), 3),
            (28, Decimal("248.00"), 3),
        ],
    },

    # ── 6 ──
    {
        "name":        "Indian Virgin Hair 5x5 Closure Wig Deep Wave – Natural Black",
        "slug":        "indiandeepwave5x5closure",
        "category":    "closurewigs",
        "hair_type":   "deep_wave",
        "lace_type":   "5x5",
        "density":     "180",
        "is_featured": False,
        "is_trending": False,
        "short_description": "Deep wave Indian hair with a larger 5x5 closure for naturallooking parting.",
        "description": (
            "A step up from the standard 4x4, this 5x5 lace closure deep wave wig provides a slightly wider "
            "parting area for a more natural scalp appearance. Made from 100% Indian virgin hair, the deep wave "
            "pattern creates voluminous, defined Scurls that are full of life and movement.\n\n"
            "Indian hair's slightly thicker strand diameter makes it ideal for deep wave textures — the curls "
            "hold their shape longer and bounce back after washing. 180% density gives an impressively full finish."
        ),
        "care": "Wash with cold water and curlenhancing conditioner. Air dry naturally. Refresh curls with water spray.",
        "pricing": [
            (12, Decimal("65.00"), 14), (14, Decimal("75.00"), 14),
            (16, Decimal("86.00"), 12), (18, Decimal("98.00"), 10),
            (20, Decimal("112.00"), 10), (22, Decimal("126.00"), 8),
            (24, Decimal("142.00"), 6), (26, Decimal("158.00"), 5),
            (28, Decimal("175.00"), 4),
        ],
    },

    # ── 7 ──
    {
        "name":        "Brazilian Virgin Hair Glueless 13x4 Lace Straight Wig – Natural Black",
        "slug":        "braziliangluelessstraight13x4",
        "category":    "gluelesswigs",
        "hair_type":   "straight",
        "lace_type":   "13x4",
        "density":     "200",
        "is_featured": True,
        "is_trending": True,
        "short_description": "Readytowear glueless wig with 200% density Brazilian straight hair — no glue, no fuss.",
        "description": (
            "The ultimate in convenience — this glueless 13x4 lace straight wig is designed to be worn without "
            "adhesive. Featuring adjustable elastic bands and combs sewn inside the cap for a secure, comfortable "
            "fit. Made from 100% Brazilian virgin hair at an impressive 200% density for maximum volume and thickness.\n\n"
            "Brazilian straight hair has a natural slight movement that prevents it from looking stiff or unnatural. "
            "The glueless design protects your hairline and edges while still delivering a flawlessly blended look. "
            "Perfect for beginners and experienced wig wearers alike."
        ),
        "care": "Wash gently in cool water. No heat above 200°C. Secure with internal combs and elastic band for everyday wear.",
        "pricing": [
            (10, Decimal("72.00"), 15), (12, Decimal("85.00"), 15),
            (14, Decimal("98.00"), 12), (16, Decimal("112.00"), 12),
            (18, Decimal("128.00"), 10), (20, Decimal("145.00"), 10),
            (22, Decimal("165.00"), 8), (24, Decimal("185.00"), 6),
            (26, Decimal("208.00"), 4), (28, Decimal("232.00"), 3),
        ],
    },

    # ── 8 ──
    {
        "name":        "Peruvian Virgin Hair 13x4 Lace Front Loose Deep Wave Wig – Natural Black",
        "slug":        "peruvianloosedeepwave13x4",
        "category":    "lacefrontwigs",
        "hair_type":   "deep_wave",
        "lace_type":   "13x4",
        "density":     "150",
        "is_featured": False,
        "is_trending": True,
        "short_description": "A perfect hybrid of loose wave and deep wave — voluminous, bouncy Peruvian curls.",
        "description": (
            "Loose deep wave is one of the most versatile textures available — sitting between loose wave and "
            "deep wave, it offers defined Sshaped curls with looser ringlets that give incredible body and movement. "
            "Made from premium Peruvian virgin hair, this texture is particularly wellsuited to humid and tropical "
            "climates where tighter curls may frizz.\n\n"
            "The 13x4 transparent lace blends seamlessly with most skin tones. 150% density keeps the wig "
            "looking natural and full without excess weight. An excellent choice for everyday wear."
        ),
        "care": "Finger detangle only. Wash with cold water. Apply curl cream while wet and scrunch upward. Air dry fully.",
        "pricing": [
            (12, Decimal("55.00"), 15), (14, Decimal("65.00"), 15),
            (16, Decimal("75.00"), 12), (18, Decimal("86.00"), 12),
            (20, Decimal("98.00"), 10), (22, Decimal("112.00"), 8),
            (24, Decimal("126.00"), 6), (26, Decimal("140.00"), 5),
            (28, Decimal("156.00"), 4),
        ],
    },

    # ── 9 ──
    {
        "name":        "Malaysian Virgin Hair 13x4 Lace Front Kinky Straight Wig – Natural Black",
        "slug":        "malaysiankinkystraight13x4",
        "category":    "lacefrontwigs",
        "hair_type":   "straight",
        "lace_type":   "13x4",
        "density":     "150",
        "is_featured": False,
        "is_trending": False,
        "short_description": "Natural kinky straight texture that mimics relaxed natural hair with Malaysian hair quality.",
        "description": (
            "Kinky straight hair is a beautiful compromise between completely straight hair and a natural kinky "
            "texture — giving it a slight wave and body that looks strikingly like naturally relaxed or texlaxed "
            "hair. Made from Malaysian virgin hair, this texture is particularly popular for those who want their "
            "wig to blend convincingly with their own hair or natural texture.\n\n"
            "The 13x4 lace front provides a natural hairline. At 150% density, the wig has an elegant fullness "
            "that doesn't look overdone. Versatile enough to be worn straight or curled."
        ),
        "care": "Wash with gentle shampoo. Blow dry on low heat. Can be flatironed for a sleeker look.",
        "pricing": [
            (10, Decimal("50.00"), 18), (12, Decimal("60.00"), 18),
            (14, Decimal("70.00"), 15), (16, Decimal("80.00"), 12),
            (18, Decimal("92.00"), 10), (20, Decimal("106.00"), 10),
            (22, Decimal("120.00"), 8), (24, Decimal("136.00"), 6),
            (26, Decimal("152.00"), 5), (28, Decimal("168.00"), 4),
        ],
    },

    # ── 10 ──
    {
        "name":        "Brazilian Virgin Hair Full Lace Wig Body Wave – Natural Black",
        "slug":        "brazilianbodywavefulllace",
        "category":    "fulllacewigs",
        "hair_type":   "body_wave",
        "lace_type":   "full_lace",
        "density":     "130",
        "is_featured": True,
        "is_trending": False,
        "short_description": "Full lace coverage from cap to nape — the most versatile wig for any hairstyle.",
        "description": (
            "A full lace wig is the pinnacle of wig craftsmanship. With lace covering the entire cap, you can "
            "part the hair anywhere — centre, side, zigzag — and wear it in a ponytail, bun, or braid without "
            "any tracks showing. This body wave version uses 100% Brazilian virgin hair at 130% density for a "
            "light, natural feel.\n\n"
            "Brazilian body wave hair is particularly beautiful in the full lace format because the flowing waves "
            "look stunning from every angle. A premium investment for those who want maximum styling freedom."
        ),
        "care": "Hand wash only in cool water. Air dry on a wig stand. Store in silk bag. Deep condition every two weeks.",
        "pricing": [
            (12, Decimal("110.00"), 8), (14, Decimal("128.00"), 8),
            (16, Decimal("148.00"), 6), (18, Decimal("170.00"), 6),
            (20, Decimal("192.00"), 5), (22, Decimal("218.00"), 4),
            (24, Decimal("245.00"), 3), (26, Decimal("272.00"), 2),
        ],
    },

    # ── 11 ──
    {
        "name":        "Vietnamese Virgin Hair 13x4 Lace Front Yaki Straight Wig – Natural Black",
        "slug":        "vietnameseyakistraight13x4",
        "category":    "lacefrontwigs",
        "hair_type":   "straight",
        "lace_type":   "13x4",
        "density":     "150",
        "is_featured": False,
        "is_trending": False,
        "short_description": "Yaki straight texture mimics freshly relaxed natural hair with Vietnamese hair quality.",
        "description": (
            "Yaki hair has a slightly coarse, textured finish that perfectly mimics the look of freshly blowdried "
            "or relaxed African hair. This makes it one of the most naturalblending wigs for women with naturally "
            "coily hair. Made from Vietnamese virgin hair — known for its silkiness and durability — this yaki "
            "straight wig gives the appearance of a professional blowout while remaining easy to style.\n\n"
            "The 13x4 lace front allows for natural hairline parting. The yaki texture takes well to hot tools "
            "and can be curled, waved, or pressed. A versatile choice that looks incredibly natural."
        ),
        "care": "Wash in cool water with moisturerich shampoo. Blow dry on medium heat. Flat iron at max 180°C.",
        "pricing": [
            (10, Decimal("55.00"), 16), (12, Decimal("65.00"), 16),
            (14, Decimal("75.00"), 12), (16, Decimal("86.00"), 12),
            (18, Decimal("98.00"), 10), (20, Decimal("112.00"), 8),
            (22, Decimal("128.00"), 6), (24, Decimal("145.00"), 5),
        ],
    },

    # ── 12 ──
    {
        "name":        "Indian Virgin Hair 13x4 Lace Front Curly Wig – Natural Black",
        "slug":        "indiancurly13x4",
        "category":    "lacefrontwigs",
        "hair_type":   "curly",
        "lace_type":   "13x4",
        "density":     "150",
        "is_featured": True,
        "is_trending": False,
        "short_description": "Defined curly Indian hair with a natural bounce — perfect for a carefree, textured look.",
        "description": (
            "This Indian virgin hair curly wig features defined, springy curls that sit between a spiral curl "
            "and a coil. Indian hair's natural density makes it ideal for curly textures — the curls hold "
            "their shape beautifully and spring back after washing without losing definition.\n\n"
            "The 13x4 transparent lace creates a natural hairline that blends effortlessly. At 150% density, "
            "the curls appear full and lush. This wig can be worn asis for a full, round silhouette, or "
            "stretched and diffused for more length."
        ),
        "care": "Cowash only. Apply curl cream to damp hair and scrunch. Air dry or diffuse on low. Sleep in a satin bonnet.",
        "pricing": [
            (10, Decimal("60.00"), 14), (12, Decimal("72.00"), 14),
            (14, Decimal("85.00"), 12), (16, Decimal("98.00"), 10),
            (18, Decimal("112.00"), 8), (20, Decimal("128.00"), 8),
            (22, Decimal("148.00"), 6), (24, Decimal("168.00"), 5),
        ],
    },

    # ── 13 ──
    {
        "name":        "Brazilian Virgin Hair 13x4 Lace Front Straight Wig – Honey Blonde 27#",
        "slug":        "brazilianstraighthoneyblonde27",
        "category":    "colouredwigs",
        "hair_type":   "straight",
        "lace_type":   "13x4",
        "density":     "150",
        "is_featured": True,
        "is_trending": True,
        "short_description": "Warm honey blonde straight wig — precoloured Brazilian hair for a bold, glamorous look.",
        "description": (
            "Make a statement with this stunning honey blonde (27#) straight wig made from 100% Brazilian virgin hair. "
            "The warm goldenamber tone is one of the most flattering blonde shades for melaninrich skin tones, "
            "adding warmth and radiance to your complexion without looking harsh.\n\n"
            "Precoloured by professionals using a careful bleaching and toning process that preserves the "
            "hair's health and shine. The 13x4 lace front gives a natural hairline. The straight texture "
            "makes the colour shine beautifully. No athome colouring required — it arrives ready to wear."
        ),
        "care": "Use coloursafe shampoo only. Avoid excessive heat to preserve colour. Deep condition weekly. Protect from UV when outdoors.",
        "pricing": [
            (10, Decimal("78.00"), 12), (12, Decimal("92.00"), 12),
            (14, Decimal("108.00"), 10), (16, Decimal("125.00"), 10),
            (18, Decimal("142.00"), 8), (20, Decimal("162.00"), 6),
            (22, Decimal("185.00"), 5), (24, Decimal("208.00"), 4),
        ],
    },

    # ── 14 ──
    {
        "name":        "Vietnamese Virgin Hair 13x4 Lace Front Body Wave Wig – Ombre 1B/30",
        "slug":        "vietnamesebodywaveombre1b30",
        "category":    "colouredwigs",
        "hair_type":   "body_wave",
        "lace_type":   "13x4",
        "density":     "150",
        "is_featured": False,
        "is_trending": True,
        "short_description": "Gorgeous ombre body wave — dark roots fading into warm auburn ends.",
        "description": (
            "This ombre (1B/30) body wave wig transitions seamlessly from natural black roots to warm auburn ends, "
            "creating a sunkissed effect that looks incredibly natural. The gradient colouring is achieved through "
            "a professional handpainting technique that preserves the integrity of the Vietnamese virgin hair.\n\n"
            "The body wave texture enhances the ombre effect, as the waves catch the light differently at each colour "
            "level. The 13x4 lace front keeps the look natural at the hairline. Perfect for those who want colour "
            "without the commitment of a full dye."
        ),
        "care": "Coloursafe shampoo and conditioner only. Avoid swimming in chlorinated water. Deep condition every two weeks.",
        "pricing": [
            (12, Decimal("85.00"), 10), (14, Decimal("98.00"), 10),
            (16, Decimal("112.00"), 8), (18, Decimal("128.00"), 8),
            (20, Decimal("145.00"), 6), (22, Decimal("165.00"), 5),
            (24, Decimal("188.00"), 4), (26, Decimal("212.00"), 3),
        ],
    },

    # ── 15 ──
    {
        "name":        "Malaysian Virgin Hair 13x4 Lace Front Straight Wig – Burgundy 99J",
        "slug":        "malaysianstraightburgundy99j",
        "category":    "colouredwigs",
        "hair_type":   "straight",
        "lace_type":   "13x4",
        "density":     "150",
        "is_featured": False,
        "is_trending": True,
        "short_description": "Rich, deep burgundy straight wig — bold and luxurious Malaysian virgin hair.",
        "description": (
            "The 99J burgundy shade is a deep winered that exudes sophistication and drama. This straight "
            "Malaysian virgin hair wig is precoloured in this stunning shade, which is particularly flattering "
            "against dark skin tones. The rich, deep colour has both cool and warm tones that shift beautifully "
            "in different lighting conditions.\n\n"
            "Malaysian hair's natural shine makes coloured styles look particularly striking. The 13x4 lace "
            "provides a clean, natural hairline. Pairs beautifully with bold makeup or lets the hair be the statement."
        ),
        "care": "Coloursafe products only. Avoid direct sunlight for prolonged periods. Condition regularly to maintain vibrancy.",
        "pricing": [
            (10, Decimal("72.00"), 12), (12, Decimal("85.00"), 12),
            (14, Decimal("98.00"), 10), (16, Decimal("112.00"), 10),
            (18, Decimal("128.00"), 8), (20, Decimal("145.00"), 6),
            (22, Decimal("165.00"), 5), (24, Decimal("185.00"), 4),
        ],
    },

    # ── 16 ──
    {
        "name":        "Indian Virgin Hair 13x4 Lace Front Straight Wig – 200% Density",
        "slug":        "indianstraight13x4200density",
        "category":    "lacefrontwigs",
        "hair_type":   "straight",
        "lace_type":   "13x4",
        "density":     "200",
        "is_featured": True,
        "is_trending": False,
        "short_description": "Ultrathick 200% density Indian straight wig — maximum volume and fullness.",
        "description": (
            "For those who love maximum thickness and volume, this 200% density Indian virgin hair straight wig "
            "is the ultimate statement piece. Double the density of a standard wig, it delivers an incredibly "
            "thick, full ponytail and a dramatic silhouette.\n\n"
            "Indian hair's slightly coarser natural strand adds to the thickness appearance. Despite the high "
            "density, the wig is made with a breathable cap construction to prevent overheating. The 13x4 "
            "lace front maintains the natural hairline appearance. Ideal for special occasions."
        ),
        "care": "Wash in sections to manage volume. Use a widetooth comb. Air dry on a wig stand. Brush from tips to roots.",
        "pricing": [
            (10, Decimal("85.00"), 10), (12, Decimal("100.00"), 10),
            (14, Decimal("118.00"), 8), (16, Decimal("138.00"), 8),
            (18, Decimal("158.00"), 6), (20, Decimal("180.00"), 5),
            (22, Decimal("205.00"), 4), (24, Decimal("232.00"), 3),
        ],
    },

    # ── 17 ──
    {
        "name":        "Brazilian Virgin Hair Headband Wig Body Wave – Natural Black",
        "slug":        "brazilianheadbandbodywave",
        "category":    "headbandwigs",
        "hair_type":   "body_wave",
        "lace_type":   "no_lace",
        "density":     "150",
        "is_featured": False,
        "is_trending": True,
        "short_description": "No lace, no glue — this beginnerfriendly headband body wave wig installs in seconds.",
        "description": (
            "The easiest wig to put on and take off. Headband wigs require no lace, no glue, and no professional "
            "installation — simply secure with the builtin adjustable band and style with a matching headband or "
            "scarf. Made from 100% Brazilian virgin hair in a gorgeous body wave texture.\n\n"
            "Ideal for gymgoers, busy mornings, or wig beginners. The machinesewn wefts create a dense, "
            "full look without any visible tracks at the hairline when paired with a headband. "
            "Comes with three free headbands in complementary colours."
        ),
        "care": "Wash normally and air dry. Can be worn immediately after washing. No special lace care required.",
        "pricing": [
            (16, Decimal("45.00"), 20), (18, Decimal("52.00"), 20),
            (20, Decimal("62.00"), 18), (22, Decimal("72.00"), 15),
            (24, Decimal("85.00"), 12), (26, Decimal("98.00"), 10),
            (28, Decimal("112.00"), 8),
        ],
    },

    # ── 18 ──
    {
        "name":        "Peruvian Virgin Hair 4x4 Closure Body Wave Wig – Natural Black",
        "slug":        "peruvianbodywave4x4closure",
        "category":    "closurewigs",
        "hair_type":   "body_wave",
        "lace_type":   "4x4",
        "density":     "150",
        "is_featured": False,
        "is_trending": False,
        "short_description": "Luscious Peruvian body waves with a 4x4 closure — natural look at an accessible price.",
        "description": (
            "This Peruvian virgin hair body wave closure wig combines the natural fullness of Peruvian hair "
            "with the clean finish of a 4x4 lace closure. Peruvian body wave hair has a slightly more defined "
            "wave pattern than Brazilian, giving it a bouncier, more textured appearance.\n\n"
            "The 4x4 lace closure sits at the crown and provides a realistic parting space. 150% density "
            "creates an elegant, full finish that works beautifully for daily wear. A great value option for "
            "those looking for quality hair at an accessible price point."
        ),
        "care": "Gentle wash with cold water. Finger detangle when wet. Air dry on a wig stand.",
        "pricing": [
            (12, Decimal("55.00"), 16), (14, Decimal("65.00"), 16),
            (16, Decimal("75.00"), 14), (18, Decimal("86.00"), 12),
            (20, Decimal("98.00"), 10), (22, Decimal("112.00"), 8),
            (24, Decimal("128.00"), 6), (26, Decimal("145.00"), 5),
        ],
    },

    # ── 19 ──
    {
        "name":        "Vietnamese Virgin Hair 13x4 Lace Front Jerry Curly Wig – Natural Black",
        "slug":        "vietnamesejerrycurly13x4",
        "category":    "lacefrontwigs",
        "hair_type":   "curly",
        "lace_type":   "13x4",
        "density":     "180",
        "is_featured": False,
        "is_trending": False,
        "short_description": "Tight, springy Jerry curls with 180% density Vietnamese virgin hair.",
        "description": (
            "Jerry curls sit between a traditional spiral curl and a coiled pattern, creating a voluminous, "
            "textured look that is uniquely beautiful. Made from Vietnamese virgin hair at 180% density, "
            "this wig delivers maximum volume and a striking presence.\n\n"
            "The curls are tight enough to create a defined pattern but loose enough to feel effortless. "
            "Vietnamese hair's natural silkiness prevents the curls from feeling rough or coarse. "
            "The 13x4 lace front provides a natural hairline. Ideal for a bold, natural hair look."
        ),
        "care": "Moisturise regularly with a waterbased product. Finger detangle only. Sleep in satin bonnet. Cowash weekly.",
        "pricing": [
            (10, Decimal("68.00"), 12), (12, Decimal("80.00"), 12),
            (14, Decimal("94.00"), 10), (16, Decimal("110.00"), 10),
            (18, Decimal("128.00"), 8), (20, Decimal("146.00"), 6),
            (22, Decimal("168.00"), 5), (24, Decimal("190.00"), 4),
        ],
    },

    # ── 20 ──
    {
        "name":        "Brazilian Virgin Hair 13x4 Lace Front Straight Wig – Piano Colour 1B/27",
        "slug":        "brazilianstraightpiano1b27",
        "category":    "colouredwigs",
        "hair_type":   "straight",
        "lace_type":   "13x4",
        "density":     "150",
        "is_featured": True,
        "is_trending": True,
        "short_description": "Twotone piano colour — natural black and honey blonde highlights for a multidimensional look.",
        "description": (
            "Piano colouring blends two shades — in this case natural black (1B) and honey blonde (27) — in "
            "alternating weft layers to create a multidimensional, sunlit effect that looks like natural "
            "highlights. The result is a striking yet wearable colour that catches the light beautifully.\n\n"
            "Made from Brazilian virgin hair, the straight texture showcases the twotone colouring perfectly. "
            "The 13x4 lace front gives a clean, natural hairline. A beautiful option for those wanting colour "
            "without going fully blonde."
        ),
        "care": "Coloursafe shampoo and conditioner. Avoid excessive heat above 180°C. Deep condition biweekly.",
        "pricing": [
            (12, Decimal("88.00"), 10), (14, Decimal("102.00"), 10),
            (16, Decimal("118.00"), 8), (18, Decimal("135.00"), 8),
            (20, Decimal("155.00"), 6), (22, Decimal("178.00"), 5),
            (24, Decimal("202.00"), 4),
        ],
    },

    # ── 21 ──
    {
        "name":        "Indian Virgin Hair 13x4 Lace Front Straight Wig – 613 Blonde",
        "slug":        "indianstraight613blonde",
        "category":    "colouredwigs",
        "hair_type":   "straight",
        "lace_type":   "13x4",
        "density":     "150",
        "is_featured": False,
        "is_trending": True,
        "short_description": "Bold platinum blonde (613) straight wig — the statement colour of the season.",
        "description": (
            "613 platinum blonde is the most coveted colour in the wig world — a light, almost whiteblonde "
            "that makes any complexion shine. This Indian virgin hair straight wig is bleached to a clean "
            "613 blonde by professional colourists who preserve the hair's moisture and integrity throughout "
            "the process.\n\n"
            "The platinum colour opens up the hair shaft slightly, making it feel slightly softer than "
            "uncoloured hair — which actually makes it easier to style. The 13x4 lace provides a natural "
            "hairline. Can be toned to platinum, silver, or light pink with a toner."
        ),
        "care": "Use purple toning shampoo monthly to prevent brassiness. Coloursafe conditioner always. No heat above 160°C.",
        "pricing": [
            (10, Decimal("88.00"), 10), (12, Decimal("105.00"), 10),
            (14, Decimal("122.00"), 8), (16, Decimal("142.00"), 8),
            (18, Decimal("162.00"), 6), (20, Decimal("185.00"), 5),
            (22, Decimal("210.00"), 4), (24, Decimal("238.00"), 3),
        ],
    },

    # ── 22 ──
    {
        "name":        "Malaysian Virgin Hair 13x4 Lace Front Deep Wave Wig – Natural Black",
        "slug":        "malaysiandeepwave13x4",
        "category":    "lacefrontwigs",
        "hair_type":   "deep_wave",
        "lace_type":   "13x4",
        "density":     "150",
        "is_featured": False,
        "is_trending": False,
        "short_description": "Defined Malaysian deep waves with a naturally glossy finish.",
        "description": (
            "Malaysian virgin hair's natural lustre makes it one of the best choices for the deep wave texture — "
            "the waves catch the light beautifully, giving the wig an incredible shine. The deep wave pattern "
            "creates tightly defined Scurls that hold their shape through multiple washes.\n\n"
            "The 13x4 lace front provides a realistic hairline. At 150% density, the wig is full but not "
            "excessively heavy. Malaysian hair's medium strand diameter makes this wig feel incredibly natural "
            "and easy to manage."
        ),
        "care": "Cowash with curlenhancing conditioner. Air dry naturally. Scrunch waves while still damp for definition.",
        "pricing": [
            (12, Decimal("56.00"), 15), (14, Decimal("66.00"), 15),
            (16, Decimal("78.00"), 12), (18, Decimal("90.00"), 10),
            (20, Decimal("104.00"), 10), (22, Decimal("118.00"), 8),
            (24, Decimal("135.00"), 6), (26, Decimal("152.00"), 5),
            (28, Decimal("170.00"), 4),
        ],
    },

    # ── 23 ──
    {
        "name":        "Brazilian Virgin Hair 13x4 Lace Front Straight Wig – 1B/99J Ombre",
        "slug":        "brazilianstraightombre1b99j",
        "category":    "colouredwigs",
        "hair_type":   "straight",
        "lace_type":   "13x4",
        "density":     "150",
        "is_featured": False,
        "is_trending": False,
        "short_description": "Dark root to burgundy ombre — a rich, dramatic colour transition.",
        "description": (
            "This 1B/99J ombre straight wig transitions from natural black roots to deep burgundy ends, "
            "creating a dramatic colour statement that looks expertly done. The burgundy shade (99J) "
            "is rich and deep, catching the light with a reddishpurple shimmer.\n\n"
            "Brazilian virgin hair holds colour exceptionally well. The straight texture allows the ombre "
            "gradient to be clearly visible from root to tip. The 13x4 lace front ensures a natural hairline "
            "that completes the professional finish."
        ),
        "care": "Coloursafe products only. Avoid chlorine. Deep condition fortnightly to maintain colour vibrancy.",
        "pricing": [
            (12, Decimal("82.00"), 10), (14, Decimal("96.00"), 10),
            (16, Decimal("110.00"), 8), (18, Decimal("126.00"), 8),
            (20, Decimal("144.00"), 6), (22, Decimal("164.00"), 5),
            (24, Decimal("186.00"), 4),
        ],
    },

    # ── 24 ──
    {
        "name":        "Vietnamese Virgin Hair 13x4 Lace Front Straight Wig – 180% Density",
        "slug":        "vietnamesestraight13x4180density",
        "category":    "lacefrontwigs",
        "hair_type":   "straight",
        "lace_type":   "13x4",
        "density":     "180",
        "is_featured": False,
        "is_trending": False,
        "short_description": "Highdensity Vietnamese straight wig for a thick, voluminous, sleek finish.",
        "description": (
            "Vietnamese virgin hair is renowned for being the silkiest and most lustrous of all Asian hair "
            "types. At 180% density, this straight wig creates an impressively thick, glossy curtain of hair "
            "that commands attention. The natural darkness and shine of Vietnamese hair gives this wig a "
            "deeply luxurious appearance.\n\n"
            "The 13x4 lace front allows for natural hairline parting. Can be straightened to a glasssmooth "
            "finish or curled for a voluminous blowout style. A premium straight wig that delivers exceptional "
            "value."
        ),
        "care": "Wash with hydrating shampoo. Blow dry on medium heat. Flat iron on 180°C max for a sleek finish.",
        "pricing": [
            (10, Decimal("65.00"), 15), (12, Decimal("78.00"), 15),
            (14, Decimal("92.00"), 12), (16, Decimal("108.00"), 12),
            (18, Decimal("125.00"), 10), (20, Decimal("142.00"), 8),
            (22, Decimal("162.00"), 6), (24, Decimal("185.00"), 5),
            (26, Decimal("208.00"), 4), (28, Decimal("232.00"), 3),
        ],
    },

    # ── 25 ──
    {
        "name":        "Peruvian Virgin Hair 360 Lace Frontal Deep Wave Wig – Natural Black",
        "slug":        "peruviandeepwave360lace",
        "category":    "360lacewigs",
        "hair_type":   "deep_wave",
        "lace_type":   "full_lace",
        "density":     "150",
        "is_featured": False,
        "is_trending": True,
        "short_description": "Fullperimeter 360 lace with voluminous Peruvian deep waves.",
        "description": (
            "This 360 lace frontal deep wave wig wraps lace all the way around the cap perimeter, allowing "
            "for high ponytails and updos without showing any tracks. Made from Peruvian virgin hair, the "
            "deep wave pattern creates those signature bouncy, voluminous Scurls that look incredible in "
            "any hairstyle.\n\n"
            "The 360 format is ideal for those who love styling their hair up as much as they love wearing "
            "it down. The Peruvian deep wave texture looks particularly stunning in a high bun or halfup "
            "style. A versatile premium wig for the ultimate styling experience."
        ),
        "care": "Wash gently. Air dry fully before styling up. Use wig tape or glue at perimeter for updos.",
        "pricing": [
            (14, Decimal("95.00"), 8), (16, Decimal("112.00"), 8),
            (18, Decimal("130.00"), 6), (20, Decimal("150.00"), 6),
            (22, Decimal("172.00"), 5), (24, Decimal("196.00"), 4),
            (26, Decimal("222.00"), 3),
        ],
    },

    # ── 26 ──
    {
        "name":        "Brazilian Virgin Hair 13x4 Lace Front Curly Wig – Natural Black 180% Density",
        "slug":        "braziliancurly13x4180density",
        "category":    "lacefrontwigs",
        "hair_type":   "curly",
        "lace_type":   "13x4",
        "density":     "180",
        "is_featured": False,
        "is_trending": False,
        "short_description": "Highdensity Brazilian curly wig with an incredible volume and springy curl definition.",
        "description": (
            "At 180% density, this Brazilian virgin hair curly wig delivers maximum volume and fullness. "
            "The curls are defined and springy, with a consistent pattern throughout. Brazilian hair's "
            "natural resilience makes it one of the best choices for curly textures — the curls hold "
            "their shape through multiple washes without losing definition.\n\n"
            "The 13x4 lace front provides a natural hairline. This wig creates an impressively round, "
            "full silhouette that is perfect for special occasions or everyday wear for those who love "
            "a bold, textured look."
        ),
        "care": "Moisturise regularly. Finger detangle only. Cowash weekly. Apply gel or curl cream while soaking wet.",
        "pricing": [
            (10, Decimal("72.00"), 12), (12, Decimal("86.00"), 12),
            (14, Decimal("102.00"), 10), (16, Decimal("118.00"), 8),
            (18, Decimal("135.00"), 8), (20, Decimal("155.00"), 6),
            (22, Decimal("178.00"), 5), (24, Decimal("202.00"), 4),
        ],
    },

    # ── 27 ──
    {
        "name":        "Vietnamese Virgin Hair 13x4 Lace Front Water Wave Wig – Natural Black",
        "slug":        "vietnamesewaterwave13x4",
        "category":    "lacefrontwigs",
        "hair_type":   "wavy",
        "lace_type":   "13x4",
        "density":     "150",
        "is_featured": True,
        "is_trending": False,
        "short_description": "Silky Vietnamese water waves with a glossy natural finish — effortlessly beautiful.",
        "description": (
            "Vietnamese hair's legendary silkiness is perfectly showcased in the water wave texture. Unlike "
            "other hair types where water waves can appear coarse or dry, Vietnamese water waves have a "
            "naturally glossy, almost wetlooking finish that is incredibly striking.\n\n"
            "The wave pattern is consistent and defined throughout, with soft ringlets that flow beautifully. "
            "The 13x4 lace front provides a natural scalp appearance. At 150% density, the wig has a full "
            "but natural look. A stunning choice for those who want to stand out."
        ),
        "care": "Mist with water spray to refresh waves. Scrunch upward. Air dry. Avoid excessive brushing.",
        "pricing": [
            (12, Decimal("58.00"), 16), (14, Decimal("68.00"), 16),
            (16, Decimal("80.00"), 12), (18, Decimal("92.00"), 12),
            (20, Decimal("106.00"), 10), (22, Decimal("122.00"), 8),
            (24, Decimal("138.00"), 6), (26, Decimal("156.00"), 5),
            (28, Decimal("175.00"), 4),
        ],
    },

    # ── 28 ──
    {
        "name":        "Indian Virgin Hair 13x4 Lace Front Body Wave Wig – 150% Density",
        "slug":        "indianbodywave13x4150",
        "category":    "lacefrontwigs",
        "hair_type":   "body_wave",
        "lace_type":   "13x4",
        "density":     "150",
        "is_featured": False,
        "is_trending": False,
        "short_description": "Classic body wave Indian hair — smooth, full, and naturally beautiful.",
        "description": (
            "Indian virgin hair body wave is one of the most popular textures in our collection. Indian "
            "hair's natural body and slight wave means that body wave Indian wigs have a particularly "
            "organic, natural look — the waves flow seamlessly without looking too perfect or artificial.\n\n"
            "The 13x4 lace front creates a natural hairline. 150% density provides a full, wearable finish "
            "that works for everyday use. Indian body wave holds curls beautifully and can be blown out "
            "straight when desired. Truly versatile."
        ),
        "care": "Wash weekly with moisturising shampoo. Air dry or blow dry on low heat. Use a paddle brush when dry.",
        "pricing": [
            (12, Decimal("56.00"), 16), (14, Decimal("66.00"), 16),
            (16, Decimal("77.00"), 14), (18, Decimal("89.00"), 12),
            (20, Decimal("102.00"), 10), (22, Decimal("116.00"), 8),
            (24, Decimal("132.00"), 6), (26, Decimal("148.00"), 5),
            (28, Decimal("165.00"), 4), (30, Decimal("185.00"), 3),
        ],
    },

    # ── 29 ──
    {
        "name":        "Brazilian Virgin Hair 13x4 Lace Front Loose Wave Wig – Natural Black",
        "slug":        "brazilianloosewave13x4",
        "category":    "lacefrontwigs",
        "hair_type":   "loose_wave",
        "lace_type":   "13x4",
        "density":     "150",
        "is_featured": False,
        "is_trending": True,
        "short_description": "Relaxed Brazilian loose waves — effortless, flowing, and naturally beautiful.",
        "description": (
            "Brazilian loose wave hair is celebrated for its relaxed, naturally wavy texture that requires "
            "minimal styling effort. The waves are soft and flowing with enough movement to look effortless "
            "but enough definition to look intentional. Brazilian hair's natural lustre gives this wig a "
            "beautiful, healthy shine.\n\n"
            "The 13x4 lace front provides a natural hairline. At 150% density, this wig strikes the perfect "
            "balance between fullness and wearability. An excellent everyday wig that can be dressed up "
            "or worn casually with ease."
        ),
        "care": "Finger detangle when wet. Scrunch and air dry for waves. Blow dry straight for a sleeker look.",
        "pricing": [
            (12, Decimal("54.00"), 16), (14, Decimal("64.00"), 16),
            (16, Decimal("74.00"), 14), (18, Decimal("85.00"), 12),
            (20, Decimal("98.00"), 10), (22, Decimal("112.00"), 8),
            (24, Decimal("128.00"), 6), (26, Decimal("145.00"), 5),
            (28, Decimal("162.00"), 4), (30, Decimal("180.00"), 3),
        ],
    },

    # ── 30 ──
    {
        "name":        "Peruvian Virgin Hair 13x6 Lace Front Straight Wig – Natural Black 180% Density",
        "slug":        "peruvianstraight13x6180",
        "category":    "lacefrontwigs",
        "hair_type":   "straight",
        "lace_type":   "13x6",
        "density":     "180",
        "is_featured": True,
        "is_trending": True,
        "short_description": "Wide 13x6 lace Peruvian straight wig with 180% density — the ultimate sleek look.",
        "description": (
            "The widest lace frontal available — 13x6 — provides even deeper parting options and more "
            "hairline coverage than the standard 13x4. Combined with full 180% density Peruvian virgin "
            "hair in a silky straight texture, this is one of the most striking wigs in the SOIE collection.\n\n"
            "Peruvian straight hair has a natural slight thickness and body that prevents it from looking "
            "limp or flat, even at straight textures. The wider lace allows for versatile side parts and "
            "middle parts with a seamlessly natural scalp appearance. A premium choice for serious wig lovers."
        ),
        "care": "Blow dry and flat iron for maximum sleekness. Use heat protectant spray before any hot tools. Oil the lace lightly.",
        "pricing": [
            (10, Decimal("78.00"), 12), (12, Decimal("92.00"), 12),
            (14, Decimal("108.00"), 10), (16, Decimal("126.00"), 10),
            (18, Decimal("145.00"), 8), (20, Decimal("165.00"), 6),
            (22, Decimal("188.00"), 5), (24, Decimal("212.00"), 4),
            (26, Decimal("238.00"), 3), (28, Decimal("265.00"), 2),
        ],
    },
]

created_products = {}
for pd in NEW_PRODUCTS:
    pricing_list  = pd.pop("pricing")
    category_slug = pd.pop("category")
    care          = pd.pop("care")

    product, created = WigProduct.objects.get_or_create(
        slug=pd["slug"],
        defaults={
            **pd,
            "category":          cats.get(category_slug),
            "care_instructions": care,
            "is_active":         True,
        },
    )
    created_products[product.slug] = product
    print(f"      {'Created' if created else 'Exists '}: {product.name[:58]}...")

    for inches, price, stock in pricing_list:
        InchPricing.objects.get_or_create(
            product=product,
            inches=inches,
            defaults={"price": price, "stock_quantity": stock, "is_available": True},
        )

print(f"\n      {len(NEW_PRODUCTS)} products processed")


# ─────────────────────────────────────────────────────────────────────────────
# REVIEWS  (30 for new products + 30 extra for existing products)
# Each review is realistic and specific to the product.
# ─────────────────────────────────────────────────────────────────────────────
print("\n[4/4] Creating reviews...")

ALL_REVIEWS = [

    # ── Reviews for existing products (30 extra) ──────────────────────────────

    # Vietnamese Straight (original)
    {"slug": "vietnamesevirginstraight13x4", "reviewer_name": "Blessing Osei",    "user": "Blessing",  "rating": 5,
     "message": "This is the third wig I have bought from SOIE and each one has been perfect. The Vietnamese straight is genuinely the silkiest wig I have ever owned. The lace disappears into my skin completely."},
    {"slug": "vietnamesevirginstraight13x4", "reviewer_name": "Taiwo Adeyemi",   "user": "Taiwo",     "rating": 5,
     "message": "I ordered the 28 inch and I am completely in love. The length is everything and the hair does not tangle at all even after weeks of wear. Will be ordering again before this one runs out."},
    {"slug": "vietnamesevirginstraight13x4", "reviewer_name": "Nomsa Mahlangu",  "user": "Nomsa",     "rating": 5,
     "message": "Amazing quality for the price. My order arrived in exactly 11 days. The packaging was beautiful and the wig itself is even better than the photos suggest. I have been wearing it daily for 3 weeks with no shedding."},

    # Indian Deep Wave (original)
    {"slug": "indianvirgindeepwave13x4",    "reviewer_name": "Ama Asante",      "user": "Ama",       "rating": 5,
     "message": "The deep wave on this wig is absolutely stunning. I have bought deep wave wigs before and none have come close to this quality. The curls are defined and bouncy and have stayed that way after washing. Highly recommend."},
    {"slug": "indianvirgindeepwave13x4",    "reviewer_name": "Rukayat Bello",   "user": "Rukayat",   "rating": 5,
     "message": "I was sceptical ordering online but SOIE completely changed my mind. The deep wave Indian hair is incredibly soft and the wave pattern is consistent from root to tip. Shipping was fast and the wig arrived safely."},
    {"slug": "indianvirgindeepwave13x4",    "reviewer_name": "Thandi Nkosi",    "user": "Thandi",    "rating": 5,
     "message": "Best purchase I have made this year. The 20 inch deep wave is full and gorgeous. The preplucked hairline saved me so much time. I wore it to my sister's engagement party and received compliments all night."},

    # Japanese Loose Wave (original)
    {"slug": "japanesevirginloosewave13x4", "reviewer_name": "Efua Boateng",    "user": "Efua",      "rating": 5,
     "message": "Japanese hair is something else. The loose waves are so incredibly soft and the way the hair moves is just beautiful. I get stopped constantly by people asking about my hair. This wig is worth every cent."},
    {"slug": "japanesevirginloosewave13x4", "reviewer_name": "Miriam Kimani",   "user": "Miriam",    "rating": 5,
     "message": "I ordered the 22 inch loose wave and I am obsessed. The quality is so much better than I expected at this price point. It arrived wellpackaged in 13 days. Zero shedding, zero tangling. SOIE has a customer for life."},
    {"slug": "japanesevirginloosewave13x4", "reviewer_name": "Adaeze Nnaji",    "user": "Adaeze",    "rating": 4,
     "message": "Really beautiful hair. I gave 4 stars only because my order took 17 days instead of the estimated 15, but I understand international shipping can vary. The wig itself is absolutely gorgeous — no complaints at all on quality."},

    # Vietnamese Deep Curl (original)
    {"slug": "vietnamesevirgindeepcurl13x4","reviewer_name": "Sade Oluwole",    "user": "Sade",      "rating": 5,
     "message": "The deep curl is my favourite texture I have ever tried. The coils are tight and springy and SO defined. I wore it for a week without any refreshing and it still looked amazing. SOIE never disappoints."},
    {"slug": "vietnamesevirgindeepcurl13x4","reviewer_name": "Yetunde Balogun", "user": "Yetunde",   "rating": 5,
     "message": "Amazing quality for the price. I ordered the 16 inch deep curl and the volume is incredible — my head looks so full and beautiful. Everyone thought it was my natural hair which made me so happy. Delivery was 12 days."},
    {"slug": "vietnamesevirgindeepcurl13x4","reviewer_name": "Nkechi Okoro",    "user": "Nkechi",    "rating": 5,
     "message": "I have been wanting to try SOIE for a while and finally took the plunge. I am so glad I did. The deep curl Vietnamese hair is absolutely stunning. The curls are consistent and lively. Already planning my next order."},

    # ── Reviews for new products ───────────────────────────────────────────────

    # 1. Brazilian Body Wave
    {"slug": "brazilianbodywave13x4",    "reviewer_name": "Zola Dube",       "user": "Zola",      "rating": 5,
     "message": "The Brazilian body wave is everything I have been looking for. The waves are so naturallooking and the hair is incredibly soft. I ordered the 20 inch and the volume is perfect. Arrived in 12 days. Absolutely in love."},
    {"slug": "brazilianbodywave13x4",    "reviewer_name": "Lebo Mokoena",    "user": "Lebo",      "rating": 5,
     "message": "Amazing quality for the price. I have tried several wig brands and SOIE is by far the best value. The Brazilian body wave holds its shape beautifully even in Lagos humidity. I will be recommending this to all my friends."},
    {"slug": "brazilianbodywave13x4",    "reviewer_name": "Patience Asare",  "user": "Patience",  "rating": 5,
     "message": "Really impressed with the softness and volume. The 24 inch body wave is stunning — long, full, and so naturallooking. The lace is incredibly thin and the preplucked hairline is perfect. No complaints whatsoever."},
    {"slug": "brazilianbodywave13x4",    "reviewer_name": "Florence Mwangi", "user": "Florence",  "rating": 4,
     "message": "Beautiful wig, lovely soft hair. I am giving 4 stars because I wished the package came with a wig cap, but the hair quality itself is definitely 5 stars. The body waves are so defined and the colour is a perfect natural black."},
    {"slug": "brazilianbodywave13x4",    "reviewer_name": "Amina Ibrahim",   "user": "Amina",     "rating": 5,
     "message": "My second order from SOIE and this one is even better than the first. The Brazilian body wave at 20 inches hits perfectly. I have been wearing it for two weeks with zero maintenance and it still looks brand new. Incredible."},
    {"slug": "brazilianbodywave13x4",    "reviewer_name": "Sophie Mensah",   "user": "Sophie",    "rating": 5,
     "message": "I ordered this as my first wig ever and I could not be more pleased. The hair is beautiful and the instructions for installation were straightforward. The lace blended perfectly. I feel like a completely different person."},
    {"slug": "brazilianbodywave13x4",    "reviewer_name": "Fatima Okonkwo",  "user": "Fatima",    "rating": 5,
     "message": "The deep wave was so good and looked very natural. Amazing quality for the price. The Brazilian body wave is lush and bouncy and the waves hold their shape even after sleeping in it. This is my everyday wig now."},
    {"slug": "brazilianbodywave13x4",    "reviewer_name": "Rachel Okonjo",   "user": "Rachel",    "rating": 5,
     "message": "Really impressed with the softness and volume on this wig. I ordered the 26 inch and it is breathtaking. The waves fall so naturally and the hair feels like it genuinely grew from my head. SOIE is the real deal."},

    # 2. Peruvian Water Wave
    {"slug": "peruvianwaterwave13x4",    "reviewer_name": "Diana Abiodun",   "user": "Diana",     "rating": 5,
     "message": "The water wave texture is absolutely gorgeous. So defined and voluminous. I was not expecting 180% density to feel this comfortable but it does — lightweight and full at the same time. The Peruvian hair is stunning."},
    {"slug": "peruvianwaterwave13x4",    "reviewer_name": "Blessing Osei",   "user": "Blessing",  "rating": 5,
     "message": "Amazing quality for the price. The water waves refresh beautifully — just mist with water and they come back to life. I have been wearing this wig for a month and it still looks brand new. SOIE is exceptional."},
    {"slug": "peruvianwaterwave13x4",    "reviewer_name": "Chioma Eze",      "user": "Chioma",    "rating": 5,
     "message": "Really impressed with how the Peruvian water wave holds up to humidity. I live in Lagos and this wig has been through some hot days and it still looks perfect. The definition stays all day long. Shipping was 14 days."},
    {"slug": "peruvianwaterwave13x4",    "reviewer_name": "Ama Asante",      "user": "Ama",       "rating": 4,
     "message": "Beautiful texture and great quality hair. I ordered the 18 inch and it is the perfect length. I have knocked off one star only because the wig cap was slightly tight — I wish they had more cap sizes. But the hair is perfect."},
    {"slug": "peruvianwaterwave13x4",    "reviewer_name": "Nomsa Mahlangu",  "user": "Nomsa",     "rating": 5,
     "message": "The water wave is such a unique texture and this one is done beautifully. The definition is incredible and the waves hold their shape without product. I have received so many compliments since wearing this. Highly recommend."},
    {"slug": "peruvianwaterwave13x4",    "reviewer_name": "Kefilwe Mokoena", "user": "Kefilwe",   "rating": 5,
     "message": "This is my fourth purchase from SOIE and they never disappoint. The Peruvian water wave is my new favourite texture. It works so well in South Africa's climate. Arrived in 11 days — even faster than usual."},
    {"slug": "peruvianwaterwave13x4",    "reviewer_name": "Efua Boateng",    "user": "Efua",      "rating": 5,
     "message": "I ordered this on a whim and I am so glad I did. The Peruvian water wave is absolutely stunning — the waves are tight and consistent and the hair feels incredibly healthy. No shedding at all after two weeks of wearing."},
    {"slug": "peruvianwaterwave13x4",    "reviewer_name": "Sade Oluwole",    "user": "Sade",      "rating": 5,
     "message": "Amazing quality for the price. The 20 inch water wave has incredible volume and the waves just move so beautifully. I feel like a goddess every time I wear it. SOIE consistently delivers and this is no exception."},

    # 3. Brazilian Kinky Curly 13x6
    {"slug": "braziliankinkycurly13x6",  "reviewer_name": "Taiwo Adeyemi",   "user": "Taiwo",     "rating": 5,
     "message": "The kinky curly with the 13x6 lace is absolutely next level. The wider lace makes such a difference — the hairline looks completely undetectable. The curls are tight and springy and I have had so many compliments."},
    {"slug": "braziliankinkycurly13x6",  "reviewer_name": "Thandi Nkosi",    "user": "Thandi",    "rating": 5,
     "message": "Really impressed with this kinky curly wig. The coils are so defined and naturallooking. I wear my hair in a washandgo style and this mimics my natural hair perfectly. Arrived in 13 days. Excellent quality."},
    {"slug": "braziliankinkycurly13x6",  "reviewer_name": "Yetunde Balogun", "user": "Yetunde",   "rating": 5,
     "message": "I have always been hesitant to try kinky curly wigs because I was worried they would look fake. This one looks completely natural. The 13x6 lace is the widest I have tried and the parting looks incredibly realistic."},
    {"slug": "braziliankinkycurly13x6",  "reviewer_name": "Miriam Kimani",   "user": "Miriam",    "rating": 5,
     "message": "Amazing quality for the price. The kinky curly Brazilian hair is incredibly authenticlooking. My family genuinely thought it was my real hair growing. The 16 inch length is the perfect size — full, round, and beautiful."},
    {"slug": "braziliankinkycurly13x6",  "reviewer_name": "Adaeze Nnaji",    "user": "Adaeze",    "rating": 4,
     "message": "Really beautiful kinky curly wig and the 13x6 lace is excellent. I found the curls needed a bit of moisture when they arrived but after a good cowash they were perfect. Quality is definitely there. Will buy again."},
    {"slug": "braziliankinkycurly13x6",  "reviewer_name": "Lebo Mokoena",    "user": "Lebo",      "rating": 5,
     "message": "The kinky curly 13x6 is the best wig I have ever purchased. The coils are tight, defined, and hold moisture so well. I have been wearing it for 3 weeks and it looks better with every wash. SOIE is genuinely premium."},
    {"slug": "braziliankinkycurly13x6",  "reviewer_name": "Rachel Okonjo",   "user": "Rachel",    "rating": 5,
     "message": "This wig changed my life. I never thought I could find a kinky curly wig that matched my actual curl type but this one does. The 13x6 lace is flawless and the curls are full and defined. 10 out of 10 from me."},
    {"slug": "braziliankinkycurly13x6",  "reviewer_name": "Rukayat Bello",   "user": "Rukayat",   "rating": 5,
     "message": "Really impressed with the softness and volume on this kinky curly wig. Brazilian hair is always my first choice and SOIE has proven once again that they source only the best quality. Arrived beautifully packaged in 12 days."},

    # 4. Brazilian Glueless Straight
    {"slug": "braziliangluelessstraight13x4","reviewer_name": "Nkechi Okoro",   "user": "Nkechi",  "rating": 5,
     "message": "As someone who has always been scared to use lace glue, this glueless wig is an absolute gamechanger. It fits perfectly, looks completely natural, and I can put it on in under 3 minutes. The 200% density is so full and beautiful."},
    {"slug": "braziliangluelessstraight13x4","reviewer_name": "Florence Mwangi","user": "Florence", "rating": 5,
     "message": "The glueless design is so clever. The internal combs and elastic band hold everything in place all day — even during a gym session. The Brazilian straight hair is silky and full. This is now my goto everyday wig."},
    {"slug": "braziliangluelessstraight13x4","reviewer_name": "Zola Dube",      "user": "Zola",    "rating": 5,
     "message": "I bought this for my mother who has sensitive skin and cannot use wig glue. She is over the moon with how comfortable and secure this wig is. The 200% density straight hair is incredibly thick and beautiful. Thank you SOIE."},
    {"slug": "braziliangluelessstraight13x4","reviewer_name": "Sophie Mensah",  "user": "Sophie",  "rating": 5,
     "message": "Really impressed with this glueless wig. The adjustable band means I can get a perfect fit every time. The Brazilian straight at 200% density is SO thick and glossy — exactly what I wanted. Arrived in 10 days."},
    {"slug": "braziliangluelessstraight13x4","reviewer_name": "Amina Ibrahim",  "user": "Amina",   "rating": 5,
     "message": "This glueless wig is everything. As a beginner I was worried about installation but it could not be easier. The hair quality is amazing — thick, shiny, and incredibly naturallooking. SOIE makes wigwearing accessible for everyone."},
    {"slug": "braziliangluelessstraight13x4","reviewer_name": "Patience Asare", "user": "Patience","rating": 4,
     "message": "Excellent glueless wig. The fit is very secure and the hair quality is outstanding. I knocked off one star because the internal comb at the back was slightly stiff — but a few seconds of bending made it perfect. Great product."},
    {"slug": "braziliangluelessstraight13x4","reviewer_name": "Diana Abiodun",  "user": "Diana",   "rating": 5,
     "message": "Amazing quality for the price. The glueless system works perfectly and the 200% density Brazilian straight hair is absolutely stunning. This is my third SOIE order and they have never let me down. Exceptional value."},
    {"slug": "braziliangluelessstraight13x4","reviewer_name": "Ama Asante",     "user": "Ama",     "rating": 5,
     "message": "The glueless straight wig is a 10 out of 10. The hair is incredibly silky and the density is perfect. I love that I can take it on and off without any residue or irritation. SOIE has created the perfect everyday wig."},

    # 5. Honey Blonde 27
    {"slug": "brazilianstraighthoneyblonde27","reviewer_name": "Sade Oluwole", "user": "Sade",    "rating": 5,
     "message": "I finally made the switch to blonde and I am obsessed. The honey blonde is the most flattering shade I have ever worn. The Brazilian hair is silky and the colour is even and beautiful throughout. No brassiness at all."},
    {"slug": "brazilianstraighthoneyblonde27","reviewer_name": "Taiwo Adeyemi","user": "Taiwo",   "rating": 5,
     "message": "Amazing quality for the price. I was worried the colour would look cheap but it is genuinely stunning — rich, warm honey blonde that looks professionally done. The hair feels healthy and the lace blends beautifully."},
    {"slug": "brazilianstraighthoneyblonde27","reviewer_name": "Blessing Osei","user": "Blessing","rating": 5,
     "message": "The honey blonde 27 is STUNNING. The colour is so warm and flattering and the Brazilian hair is silky smooth. I ordered the 18 inch and it is the perfect everyday length. I have received the most compliments ever wearing this."},
    {"slug": "brazilianstraighthoneyblonde27","reviewer_name": "Zola Dube",    "user": "Zola",    "rating": 5,
     "message": "Really impressed with the colour consistency on this wig. The honey blonde is even from root to tip and looks incredibly natural. The Brazilian straight hair is beautiful and the lace front is flawless. Absolutely love this."},
    {"slug": "brazilianstraighthoneyblonde27","reviewer_name": "Nkechi Okoro", "user": "Nkechi",  "rating": 4,
     "message": "Beautiful colour and great quality hair. The honey blonde is so flattering and the Brazilian straight is silky and full. I am giving 4 stars because the colour was slightly darker than the photo suggests — but still very beautiful."},
    {"slug": "brazilianstraighthoneyblonde27","reviewer_name": "Rukayat Bello","user": "Rukayat", "rating": 5,
     "message": "I have been wanting to try a blonde wig for years and this one did not disappoint. The honey tone is so warm and naturallooking against my complexion. The hair is silky and the lace is perfect. SOIE delivered magnificently."},
    {"slug": "brazilianstraighthoneyblonde27","reviewer_name": "Lebo Mokoena", "user": "Lebo",    "rating": 5,
     "message": "The honey blonde straight wig is the best purchase I have made this year. The colour is rich and warm and the Brazilian hair feels incredibly healthy. No shedding, no tangling, zero maintenance. Just beautiful."},
    {"slug": "brazilianstraighthoneyblonde27","reviewer_name": "Nomsa Mahlangu","user": "Nomsa",  "rating": 5,
     "message": "Amazing quality for the price. The 27 honey blonde is so stunning in person — the photos do not do it justice. I wore it to a wedding and everyone kept asking where I got my hair done. SOIE is a cut above the rest."},

    # 6. Peruvian Straight 13x6 180%
    {"slug": "peruvianstraight13x6180",  "reviewer_name": "Rachel Okonjo",   "user": "Rachel",    "rating": 5,
     "message": "The 13x6 lace is on another level. The parting looks completely natural and the Peruvian straight at 180% density is so incredibly full and sleek. I wore this to a job interview and felt like a completely different person."},
    {"slug": "peruvianstraight13x6180",  "reviewer_name": "Thandi Nkosi",    "user": "Thandi",    "rating": 5,
     "message": "Really impressed with the wider lace on this wig. The 13x6 frontal allows for such naturallooking parting that I no longer worry about anyone noticing it is a wig. The Peruvian straight is silky and absolutely beautiful."},
    {"slug": "peruvianstraight13x6180",  "reviewer_name": "Florence Mwangi", "user": "Florence",  "rating": 5,
     "message": "The combination of 13x6 lace and 180% density is perfection. The wig looks natural from every angle and the hair is so full and voluminous. I ordered the 22 inch and it is the ideal length. Arrived in 13 days. Excellent."},
    {"slug": "peruvianstraight13x6180",  "reviewer_name": "Diana Abiodun",   "user": "Diana",     "rating": 5,
     "message": "This is the most naturallooking wig I have ever worn. The 13x6 lace gives so much more freedom with parting and the Peruvian straight at 180% density is stunning. I can wear any style and it always looks perfect."},
    {"slug": "peruvianstraight13x6180",  "reviewer_name": "Sophie Mensah",   "user": "Sophie",    "rating": 5,
     "message": "Amazing quality for the price. The wide 13x6 lace is absolutely worth the upgrade. The hairline looks completely undetectable and the Peruvian straight hair is silky smooth and full. SOIE continues to impress."},
    {"slug": "peruvianstraight13x6180",  "reviewer_name": "Efua Boateng",    "user": "Efua",      "rating": 4,
     "message": "The 13x6 lace is genuinely incredible — so much more natural than a standard 13x4. I knocked off one star only because the wig was slightly harder to install than my previous SOIE wigs. But the finished look is worth it."},
    {"slug": "peruvianstraight13x6180",  "reviewer_name": "Patience Asare",  "user": "Patience",  "rating": 5,
     "message": "I finally understand why people pay more for the 13x6 lace. The parting is so realistic and naturallooking. The 180% density Peruvian straight hair is absolutely stunning. This wig has completely changed my confidence."},
    {"slug": "peruvianstraight13x6180",  "reviewer_name": "Amina Ibrahim",   "user": "Amina",     "rating": 5,
     "message": "Really impressed with this premium wig. The 13x6 lace provides the most natural hairline I have ever had. The Peruvian straight hair at 180% density is thick, glossy, and absolutely gorgeous. 100% worth the investment."},

]

review_count = 0
for rd in ALL_REVIEWS:
    slug          = rd.pop("slug")
    user_first    = rd.pop("user")

    try:
        product = WigProduct.objects.get(slug=slug)
    except WigProduct.DoesNotExist:
        print(f"      SKIP: product '{slug}' not found")
        continue

    user = reviewer_users.get(user_first)

    _, created = Review.objects.get_or_create(
        product=product,
        reviewer_name=rd["reviewer_name"],
        defaults={**rd, "user": user, "is_approved": True},
    )
    if created:
        review_count += 1

print(f"      {review_count} new reviews created")

# ─────────────────────────────────────────────────────────────────────────────
# FINAL SUMMARY
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 65)
print("EXTENDED SEED COMPLETE")
print("" * 65)
print(f"  Total Wigs:       {WigProduct.objects.count()}")
print(f"  Total InchTiers:  {InchPricing.objects.count()}")
print(f"  Total Reviews:    {Review.objects.count()}")
print(f"  Total Users:      {User.objects.count()}")
print(f"  Total Categories: {Category.objects.count()}")
print("" * 65)
print("\nNext: Upload product images via Admin  Wig Products  Bulk Upload")
print("=" * 65)