import re

from src.llm import complete
from src.prompts import SQL_SYSTEM
from src.schema import SCHEMA_DESCRIPTION


def generate_sql(question, dialect="sqlite"):
    system = SQL_SYSTEM.format(schema=SCHEMA_DESCRIPTION, dialect=dialect)
    raw = complete(system, question)
    return _extract_sql(raw)


def _extract_sql(text):
    fence = re.search(r"```(?:sql)?\s*(.+?)```", text, re.DOTALL | re.IGNORECASE)
    sql = fence.group(1) if fence else text
    return sql.strip().rstrip(";").strip()
