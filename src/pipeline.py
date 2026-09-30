from src.analyzer import summarize
from src.charts import build_chart
from src.config import settings
from src.executor import run_query
from src.sql_generator import generate_sql
from src.sql_guard import ensure_safe_select


def _dialect():
    return "postgresql" if settings.database_url.startswith("postgresql") else "sqlite"


def answer_question(question):
    sql = generate_sql(question, dialect=_dialect())
    safe_sql = ensure_safe_select(sql, max_rows=settings.max_rows)
    df = run_query(safe_sql)
    chart_path = build_chart(df)
    answer = summarize(question, df)
    return {
        "question": question,
        "sql": safe_sql,
        "answer": answer,
        "row_count": len(df),
        "rows": df.head(100).to_dict(orient="records"),
        "chart_path": chart_path,
    }
