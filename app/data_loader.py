import json
from typing import List
from app.models import Product
from app.config import settings
from app.logger import logger


class DataLoader:
    def __init__(self):
        self.products: List[Product] = []

    def load(self) -> List[Product]:
        try:
            logger.info(f"Loading products from {settings.DATA_PATH}")

            with open(settings.DATA_PATH, "r", encoding="utf-8") as f:
                raw_data = json.load(f)

            if not isinstance(raw_data, list):
                raise ValueError("Dataset must be a list of products")

            self.products = [Product(**item) for item in raw_data]

            logger.info(f"Loaded {len(self.products)} valid products")

            return self.products

        except FileNotFoundError:
            logger.error("Dataset file not found")
            raise

        except Exception as e:
            logger.error(f"Failed to load dataset: {str(e)}")
            raise

    def get_all(self) -> List[Product]:
        if not self.products:
            logger.warning("Products not loaded, calling load()")
            return self.load()
        return self.products