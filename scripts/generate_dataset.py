import json
import random
from faker import Faker

fake = Faker()
random.seed(42)

categories = {
    "toys": [
        "Shape Sorter",
        "Learning Walker",
        "Building Blocks",
        "Musical Toy",
        "Activity Cube",
        "Puzzle Board",
        "Stacking Rings",
        "Soft Plush Toy",
        "Alphabet Toy",
        "Educational Laptop",
    ],
    "feeding": [
        "Feeding Bottle",
        "Sipper Cup",
        "Baby Bowl Set",
        "High Chair",
        "Silicone Spoon",
        "Snack Container",
        "Bottle Warmer",
        "Bib Set",
        "Food Storage Container",
        "Breast Pump",
    ],
    "stroller": [
        "Compact Stroller",
        "Travel Stroller",
        "Jogging Stroller",
        "Twin Stroller",
        "Umbrella Stroller",
    ],
    "care": [
        "Baby Lotion",
        "Baby Shampoo",
        "Diaper Bag",
        "Baby Wipes",
        "Thermometer",
        "Nail Care Kit",
        "Baby Monitor",
        "Bath Tub",
        "Changing Mat",
        "Skin Cream",
    ],
    "travel": [
        "Car Seat",
        "Travel Crib",
        "Baby Carrier",
        "Travel Bag",
        "Portable Booster Seat",
        "Travel Organizer",
        "Neck Pillow",
        "Diaper Backpack",
    ]
}

age_ranges = [
    "0-1",
    "0-2",
    "0-3",
    "1-2",
    "1-3",
    "2-4",
    "3-5",
]

brands = [
    "Fisher-Price",
    "Chicco",
    "Mee Mee",
    "LuvLap",
    "Philips Avent",
    "Munchkin",
    "Babyhug",
    "TinySteps",
    "Pampers",
    "Johnson's",
    "Himalaya Baby",
    "R for Rabbit",
]

safety_tags = [
    "BPA-free",
    "Non-toxic material",
    "Smooth edges",
    "Dermatologically tested",
    "5-point safety harness",
    "Food-grade silicone",
    "Certified child-safe",
    "No sharp edges",
]

review_phrases = [
    "Highly rated by parents",
    "Excellent durability",
    "Very safe and reliable",
    "Great for daily use",
    "Loved by toddlers",
    "Premium quality product",
    "Very comfortable and lightweight",
    "Recommended for early learning",
]

products = []
product_id = 1

for _ in range(200):
    category = random.choice(list(categories.keys()))

    product_type = random.choice(categories[category])
    brand = random.choice(brands)

    name = f"{brand} {product_type}"

    price_ranges = {
        "toys": (500, 3000),
        "feeding": (300, 4000),
        "stroller": (3000, 15000),
        "care": (200, 5000),
        "travel": (1000, 12000),
    }

    min_price, max_price = price_ranges[category]

    description = fake.sentence(nb_words=10)

    product = {
        "id": f"p{product_id}",
        "name": name,
        "category": category,
        "age_range": random.choice(age_ranges),
        "price": random.randint(min_price, max_price),
        "description": description,
        "reviews": random.choice(review_phrases),
        "safety_info": random.choice(safety_tags),
    }

    products.append(product)
    product_id += 1


with open("data/products.json", "w", encoding="utf-8") as f:
    json.dump(products, f, indent=2)


print(f"Generated {len(products)} products successfully.")
print("Saved to data/products.json")
