import csv
import os
from datetime import date

from sqlalchemy import insert

from src.db import engine
from src.schema import (
    categories,
    customers,
    metadata,
    order_items,
    orders,
    products,
)

DATA_DIR = "data"


def _rows(filename):
    path = os.path.join(DATA_DIR, filename)
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _categories():
    return [
        {"category_id": int(r["category_id"]), "name": r["name"]}
        for r in _rows("categories.csv")
    ]


def _products():
    return [
        {
            "product_id": int(r["product_id"]),
            "name": r["name"],
            "category_id": int(r["category_id"]),
            "price": float(r["price"]),
        }
        for r in _rows("products.csv")
    ]


def _customers():
    return [
        {
            "customer_id": int(r["customer_id"]),
            "name": r["name"],
            "country": r["country"],
            "signup_date": date.fromisoformat(r["signup_date"]),
        }
        for r in _rows("customers.csv")
    ]


def _orders():
    return [
        {
            "order_id": int(r["order_id"]),
            "customer_id": int(r["customer_id"]),
            "order_date": date.fromisoformat(r["order_date"]),
            "status": r["status"],
        }
        for r in _rows("orders.csv")
    ]


def _order_items():
    return [
        {
            "order_item_id": int(r["order_item_id"]),
            "order_id": int(r["order_id"]),
            "product_id": int(r["product_id"]),
            "quantity": int(r["quantity"]),
            "unit_price": float(r["unit_price"]),
        }
        for r in _rows("order_items.csv")
    ]


def main():
    metadata.drop_all(engine)
    metadata.create_all(engine)
    with engine.begin() as connection:
        connection.execute(insert(categories), _categories())
        connection.execute(insert(products), _products())
        connection.execute(insert(customers), _customers())
        connection.execute(insert(orders), _orders())
        connection.execute(insert(order_items), _order_items())
    print("Database seeded.")


if __name__ == "__main__":
    main()
