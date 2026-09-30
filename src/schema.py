from sqlalchemy import (
    Column,
    Date,
    Float,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
)

metadata = MetaData()

categories = Table(
    "categories",
    metadata,
    Column("category_id", Integer, primary_key=True),
    Column("name", String, nullable=False),
)

products = Table(
    "products",
    metadata,
    Column("product_id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("category_id", Integer, ForeignKey("categories.category_id")),
    Column("price", Float, nullable=False),
)

customers = Table(
    "customers",
    metadata,
    Column("customer_id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("country", String, nullable=False),
    Column("signup_date", Date, nullable=False),
)

orders = Table(
    "orders",
    metadata,
    Column("order_id", Integer, primary_key=True),
    Column("customer_id", Integer, ForeignKey("customers.customer_id")),
    Column("order_date", Date, nullable=False),
    Column("status", String, nullable=False),
)

order_items = Table(
    "order_items",
    metadata,
    Column("order_item_id", Integer, primary_key=True),
    Column("order_id", Integer, ForeignKey("orders.order_id")),
    Column("product_id", Integer, ForeignKey("products.product_id")),
    Column("quantity", Integer, nullable=False),
    Column("unit_price", Float, nullable=False),
)

SCHEMA_DESCRIPTION = """Base de données e-commerce (tables et colonnes) :

categories(category_id, name)
products(product_id, name, category_id -> categories.category_id, price)
customers(customer_id, name, country, signup_date)
orders(order_id, customer_id -> customers.customer_id, order_date, status)
order_items(order_item_id, order_id -> orders.order_id, product_id -> products.product_id, quantity, unit_price)

Règles métier :
- Le chiffre d'affaires d'une ligne de commande = order_items.quantity * order_items.unit_price.
- order_date et signup_date sont au format DATE (YYYY-MM-DD).
- status vaut 'completed', 'cancelled' ou 'returned'.
- Un chiffre d'affaires réalisé ne prend en compte que les commandes dont le status = 'completed'.
"""
