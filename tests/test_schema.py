from src.schema import metadata


def test_expected_tables_present():
    tables = set(metadata.tables.keys())
    assert {"categories", "products", "customers", "orders", "order_items"} <= tables
