import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///data/ecommerce.db")
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    llm_model: str = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")
    temperature: float = float(os.getenv("TEMPERATURE", "0.0"))
    max_rows: int = int(os.getenv("MAX_ROWS", "1000"))
    charts_dir: str = os.getenv("CHARTS_DIR", "static/charts")


settings = Settings()
