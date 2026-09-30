import os
import uuid

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

from src.config import settings


def build_chart(df):
    if df.empty or df.shape[1] < 2:
        return None

    label_col = df.columns[0]
    value_col = _first_numeric(df, exclude=label_col)
    if value_col is None:
        return None

    os.makedirs(settings.charts_dir, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 4.5))

    if _looks_temporal(label_col):
        ax.plot(df[label_col].astype(str), df[value_col], marker="o")
    else:
        top = df.sort_values(value_col, ascending=False).head(15)
        ax.bar(top[label_col].astype(str), top[value_col])

    ax.set_xlabel(label_col)
    ax.set_ylabel(value_col)
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()

    path = os.path.join(settings.charts_dir, f"{uuid.uuid4().hex}.png")
    fig.savefig(path, dpi=120)
    plt.close(fig)
    return path


def _first_numeric(df, exclude):
    for col in df.columns:
        if col != exclude and pd.api.types.is_numeric_dtype(df[col]):
            return col
    return None


def _looks_temporal(name):
    lowered = str(name).lower()
    return any(key in lowered for key in ("date", "month", "year", "day", "period"))
