# ==============================================================================
# EVENT GENERATOR CONFIGURATION AND CATALOGS
# ==============================================================================

# Realistic funnel weight distribution: page_view > product_view > add_to_cart > checkout > purchase > payment
# remove_from_cart represents micro-interactions
EVENT_TYPES = ['page_view', 'product_view', 'add_to_cart', 'remove_from_cart', 'checkout', 'purchase', 'payment']
EVENT_WEIGHTS = [30, 25, 20, 5, 10, 7, 3]

# Core categories
CATEGORIES = [
    'Electronics', 'Clothing', 'Home & Kitchen', 'Books', 'Sports',
    'Beauty', 'Toys', 'Grocery', 'Automotive', 'Health'
]

# Product Catalog containing 50+ diverse products with realistic pricing
PRODUCTS = {
    "prod_elec_001": {"name": "iPhone 15 Pro Max", "category": "Electronics", "base_price": 1199.99},
    "prod_elec_002": {"name": "Samsung Galaxy S24 Ultra", "category": "Electronics", "base_price": 1299.99},
    "prod_elec_003": {"name": "MacBook Pro 16 M3", "category": "Electronics", "base_price": 2499.00},
    "prod_elec_004": {"name": "Sony WH-1000XM5 Headphones", "category": "Electronics", "base_price": 398.00},
    "prod_elec_005": {"name": "iPad Air M1", "category": "Electronics", "base_price": 599.00},
    "prod_elec_006": {"name": "Dell XPS 13 Laptop", "category": "Electronics", "base_price": 999.00},
    "prod_elec_007": {"name": "Nintendo Switch OLED", "category": "Electronics", "base_price": 349.99},
    "prod_elec_008": {"name": "LG 55-Inch C3 OLED TV", "category": "Electronics", "base_price": 1296.99},
    "prod_elec_009": {"name": "Apple Watch Series 9", "category": "Electronics", "base_price": 399.00},
    "prod_elec_010": {"name": "Bose SoundLink Revolve+", "category": "Electronics", "base_price": 229.00},

    "prod_clot_001": {"name": "Nike Air Max Sneakers", "category": "Clothing", "base_price": 150.00},
    "prod_clot_002": {"name": "Levi's 501 Original Fit Jeans", "category": "Clothing", "base_price": 79.50},
    "prod_clot_003": {"name": "Adidas Originals Trefoil Hoodie", "category": "Clothing", "base_price": 65.00},
    "prod_clot_004": {"name": "Patagonia Torrentshell Jacket", "category": "Clothing", "base_price": 149.00},
    "prod_clot_005": {"name": "Ray-Ban Classic Wayfarer", "category": "Clothing", "base_price": 163.00},
    "prod_clot_006": {"name": "Under Armour Tech Polo", "category": "Clothing", "base_price": 39.99},

    "prod_home_001": {"name": "Instant Pot Duo Plus 9-in-1", "category": "Home & Kitchen", "base_price": 129.95},
    "prod_home_002": {"name": "KitchenAid Artisan Stand Mixer", "category": "Home & Kitchen", "base_price": 449.99},
    "prod_home_003": {"name": "Dyson V15 Detect Vacuum", "category": "Home & Kitchen", "base_price": 749.99},
    "prod_home_004": {"name": "Keurig K-Elite Coffee Maker", "category": "Home & Kitchen", "base_price": 189.99},
    "prod_home_005": {"name": "Cuisinart 11-Piece Cookware Set", "category": "Home & Kitchen", "base_price": 199.00},
    "prod_home_006": {"name": "Ring Video Doorbell Plus", "category": "Home & Kitchen", "base_price": 149.99},

    "prod_book_001": {"name": "Atomic Habits by James Clear", "category": "Books", "base_price": 16.20},
    "prod_book_002": {"name": "Lessons in Chemistry", "category": "Books", "base_price": 14.99},
    "prod_book_003": {"name": "The Creative Act by Rick Rubin", "category": "Books", "base_price": 21.00},
    "prod_book_004": {"name": "Designing Data-Intensive Applications", "category": "Books", "base_price": 44.99},
    "prod_book_005": {"name": "Clean Code by Robert C. Martin", "category": "Books", "base_price": 38.50},

    "prod_spor_001": {"name": "Lululemon 5mm Yoga Mat", "category": "Sports", "base_price": 98.00},
    "prod_spor_002": {"name": "Bowflex SelectTech Dumbbells", "category": "Sports", "base_price": 429.00},
    "prod_spor_003": {"name": "Hydro Flask 32 oz Wide Mouth", "category": "Sports", "base_price": 44.95},
    "prod_spor_004": {"name": "Fitbit Charge 6 Fitness Tracker", "category": "Sports", "base_price": 159.95},
    "prod_spor_005": {"name": "Coleman Sundome 4-Person Tent", "category": "Sports", "base_price": 89.99},

    "prod_beau_001": {"name": "Estee Lauder Advanced Night Repair", "category": "Beauty", "base_price": 125.00},
    "prod_beau_002": {"name": "Ol恆lex No.3 Hair Perfector", "category": "Beauty", "base_price": 30.00},
    "prod_beau_003": {"name": "Dior Sauvage Eau de Parfum", "category": "Beauty", "base_price": 145.00},
    "prod_beau_004": {"name": "Laneige Lip Sleeping Mask", "category": "Beauty", "base_price": 24.00},
    "prod_beau_005": {"name": "CeraVe Hydrating Facial Cleanser", "category": "Beauty", "base_price": 17.99},

    "prod_toys_001": {"name": "LEGO Icons Pac-Man Arcade", "category": "Toys", "base_price": 269.99},
    "prod_toys_002": {"name": "Catan Board Game (Base Game)", "category": "Toys", "base_price": 48.00},
    "prod_toys_003": {"name": "Barbie Dreamhouse Playset", "category": "Toys", "base_price": 199.99},
    "prod_toys_004": {"name": "Hasbro Monopoly Deal Card Game", "category": "Toys", "base_price": 8.49},
    "prod_toys_005": {"name": "NERF Elite 2.0 Commander Blaster", "category": "Toys", "base_price": 14.99},

    "prod_groc_001": {"name": "Lavazza Super Crema Espresso", "category": "Grocery", "base_price": 22.99},
    "prod_groc_002": {"name": "Quest Protein Bar 12-Pack", "category": "Grocery", "base_price": 28.50},
    "prod_groc_003": {"name": "Bragg Organic Apple Cider Vinegar", "category": "Grocery", "base_price": 8.99},
    "prod_groc_004": {"name": "Matcha Kari Ceremony Matcha", "category": "Grocery", "base_price": 39.00},
    "prod_groc_005": {"name": "Kind Bars Caramel & Sea Salt", "category": "Grocery", "base_price": 15.99},

    "prod_auto_001": {"name": "Vantrue N4 3-Channel Dash Cam", "category": "Automotive", "base_price": 259.99},
    "prod_auto_002": {"name": "NOCO Genius5 Battery Charger", "category": "Automotive", "base_price": 69.95},
    "prod_auto_003": {"name": "Anker Car Phone Mount Charger", "category": "Automotive", "base_price": 49.99},
    "prod_auto_004": {"name": "Chemical Guys Car Wash Bucket Kit", "category": "Automotive", "base_price": 59.99},
    "prod_auto_005": {"name": "Armor All Multi-Purpose Cleaner", "category": "Automotive", "base_price": 9.99},

    "prod_heal_001": {"name": "Optimum Nutrition Whey Gold Standard", "category": "Health", "base_price": 79.99},
    "prod_heal_002": {"name": "Nature Made Vitamin D3 250ct", "category": "Health", "base_price": 15.49},
    "prod_heal_003": {"name": "Liquid I.V. Hydration Multiplier", "category": "Health", "base_price": 24.99},
    "prod_heal_004": {"name": "SmartyPants Kids Daily Gummy Multivitamin", "category": "Health", "base_price": 19.99},
    "prod_heal_005": {"name": "First Aid Only 299 Piece Kit", "category": "Health", "base_price": 22.50}
}

NUM_USERS = 1000
EVENTS_PER_SECOND = 5
SESSION_DURATION_MINUTES = 25
