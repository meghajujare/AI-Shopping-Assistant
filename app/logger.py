import logging
import os
from app.config import settings

os.makedirs(os.path.dirname(settings.LOG_PATH), exist_ok=True)

logger = logging.getLogger("ai-shopping")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(settings.LOG_PATH)
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)