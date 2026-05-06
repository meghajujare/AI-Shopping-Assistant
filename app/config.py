import os

from dotenv import load_dotenv
from pydantic import BaseModel


# Load environment variables
load_dotenv()


class Settings(BaseModel):

    # =========================
    # GROQ CONFIG
    # =========================
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")

    MODEL_NAME: str = os.getenv(
        "MODEL_NAME",
        "llama-3.1-8b-instant"
    )

    # =========================
    # RETRIEVAL CONFIG
    # =========================
    TOP_K: int = int(
        os.getenv("TOP_K", 5)
    )

    EMBEDDING_MODEL: str = os.getenv(
        "EMBEDDING_MODEL",
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    # =========================
    # DATA PATHS
    # =========================
    DATA_PATH: str = os.getenv(
        "DATA_PATH",
        "data/products.json"
    )

    LOG_PATH: str = os.getenv(
        "LOG_PATH",
        "logs/app.log"
    )

    # =========================
    # APP CONFIG
    # =========================
    LOG_LEVEL: str = os.getenv(
        "LOG_LEVEL",
        "INFO"
    )


# Singleton settings object
settings = Settings()