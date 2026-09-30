import pytest

from src.sql_guard import UnsafeQueryError, ensure_safe_select


def test_select_gets_limit_applied():
    result = ensure_safe_select("SELECT name FROM products", max_rows=100)
    assert "LIMIT 100" in result


def test_existing_limit_preserved():
    result = ensure_safe_select("SELECT name FROM products LIMIT 5", max_rows=100)
    assert result.lower().count("limit") == 1


@pytest.mark.parametrize(
    "sql",
    [
        "DELETE FROM products",
        "DROP TABLE orders",
        "INSERT INTO products VALUES (1)",
        "UPDATE products SET price = 0",
    ],
)
def test_forbidden_statements_rejected(sql):
    with pytest.raises(UnsafeQueryError):
        ensure_safe_select(sql)


def test_multiple_statements_rejected():
    with pytest.raises(UnsafeQueryError):
        ensure_safe_select("SELECT 1; SELECT 2")
