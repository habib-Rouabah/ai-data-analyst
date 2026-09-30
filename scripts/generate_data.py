import csv
import os
import random
from datetime import date, timedelta

random.seed(42)

OUTPUT_DIR = "data"

CATEGORY_NAMES = [
    "Electronics",
    "Books",
    "Clothing",
    "Home",
    "Sports",
    "Toys",
    "Beauty",
    "Grocery",
]

COUNTRIES = [
    "France",
    "Germany",
    "Spain",
    "Italy",
    "United Kingdom",
    "Belgium",
    "Netherlands",
]

STATUSES = ["completed", "completed", "completed", "completed", "cancelled", "returned"]

PRODUCT_WORDS = {
    "Electronics": ["Headphones", "Smartphone", "Laptop", "Charger", "Speaker"],
    "Books": ["Novel", "Cookbook", "Biography", "Comic", "Textbook"],
    "Clothing": ["T-Shirt", "Jeans", "Jacket", "Sneakers", "Cap"],
    "Home": ["Lamp", "Cushion", "Mug", "Blanket", "Vase"],
    "Sports": ["Football", "Yoga Mat", "Dumbbell", "Bottle", "Racket"],
    "Toys": ["Puzzle", "Robot", "Doll", "Blocks", "Board Game"],
    "Beauty": ["Perfume", "Cream", "Shampoo", "Lipstick", "Serum"],
    "Grocery": ["Coffee", "Tea", "Chocolate", "Olive Oil", "Honey"],
}


def _random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))


def _month_weight(day):
    if day.year == 2025 and day.month == 3:
        return 0.3
    if day.month in (11, 12):
        return 1.6
    return 1.0


def generate_products():
    products = []
    product_id = 1
    for category_id, name in enumerate(CATEGORY_NAMES, start=1):
        for word in PRODUCT_WORDS[name]:
            price = round(random.uniform(5, 500), 2)
            products.append((product_id, word, category_id, price))
            product_id += 1
    return products


def generate_customers(count, start, end):
    customers = []
    for customer_id in range(1, count + 1):
        country = random.choice(COUNTRIES)
        signup = _random_date(start, end).isoformat()
        customers.append((customer_id, f"Customer {customer_id}", country, signup))
    return customers


def generate_orders(customers_count, start, end):
    orders = []
    order_id = 1
    day = start
    while day <= end:
        base = random.randint(3, 9)
        count = max(0, round(base * _month_weight(day)))
        for _ in range(count):
            customer_id = random.randint(1, customers_count)
            status = random.choice(STATUSES)
            orders.append((order_id, customer_id, day.isoformat(), status))
            order_id += 1
        day += timedelta(days=1)
    return orders


def generate_order_items(orders, products):
    price_by_product = {product[0]: product[3] for product in products}
    product_ids = list(price_by_product.keys())
    items = []
    item_id = 1
    for order in orders:
        for _ in range(random.randint(1, 5)):
            product_id = random.choice(product_ids)
            quantity = random.randint(1, 4)
            items.append((item_id, order[0], product_id, quantity, price_by_product[product_id]))
            item_id += 1
    return items


def _write(filename, header, rows):
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        writer.writerows(rows)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    start = date(2024, 1, 1)
    end = date(2025, 12, 31)

    categories = list(enumerate(CATEGORY_NAMES, start=1))
    products = generate_products()
    customers = generate_customers(300, start, end)
    orders = generate_orders(len(customers), start, end)
    order_items = generate_order_items(orders, products)

    _write("categories.csv", ["category_id", "name"], categories)
    _write("products.csv", ["product_id", "name", "category_id", "price"], products)
    _write("customers.csv", ["customer_id", "name", "country", "signup_date"], customers)
    _write("orders.csv", ["order_id", "customer_id", "order_date", "status"], orders)
    _write(
        "order_items.csv",
        ["order_item_id", "order_id", "product_id", "quantity", "unit_price"],
        order_items,
    )

    print(
        f"Generated {len(products)} products, {len(customers)} customers, "
        f"{len(orders)} orders, {len(order_items)} order items"
    )


if __name__ == "__main__":
    main()
