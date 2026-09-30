import pandas as pd

from src.db import engine


def run_query(sql):
    with engine.connect() as connection:
        return pd.read_sql(sql, connection)
