import re

import sqlparse

FORBIDDEN = {
    "insert",
    "update",
    "delete",
    "drop",
    "alter",
    "create",
    "truncate",
    "replace",
    "grant",
    "revoke",
    "attach",
    "pragma",
    "exec",
    "execute",
    "merge",
    "call",
    "commit",
    "rollback",
}


class UnsafeQueryError(Exception):
    pass


def ensure_safe_select(sql, max_rows=1000):
    statements = [s for s in sqlparse.parse(sql) if str(s).strip()]
    if len(statements) != 1:
        raise UnsafeQueryError("Only a single statement is allowed.")

    if statements[0].get_type() != "SELECT":
        raise UnsafeQueryError("Only SELECT statements are allowed.")

    tokens = set(re.findall(r"[a-z_]+", sql.lower()))
    forbidden = tokens & FORBIDDEN
    if forbidden:
        raise UnsafeQueryError(f"Forbidden keyword detected: {', '.join(sorted(forbidden))}")

    return _apply_limit(sql, max_rows)


def _apply_limit(sql, max_rows):
    cleaned = sql.strip().rstrip(";")
    if re.search(r"\blimit\b", cleaned, re.IGNORECASE):
        return cleaned
    return f"{cleaned} LIMIT {max_rows}"
