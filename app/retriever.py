import json
import numpy as np

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from app.config import settings
from app.models import Product


class Retriever:

    def __init__(self):

        print("\nLoading embedding model...")

        self.model = SentenceTransformer(
            settings.EMBEDDING_MODEL
        )

        print("Loading embeddings...")

        self.embeddings = np.load(
            "embeddings/embeddings.npy"
        )

        with open(
            "embeddings/products.json",
            "r",
            encoding="utf-8"
        ) as f:

            self.products = json.load(f)

        print(
            f"Loaded {len(self.products)} products"
        )

    # =====================================
    # RETRIEVAL
    # =====================================
    def retrieve(
        self,
        query: str,
        products: list,
        top_k: int = 5
    ):

        print("\nUSER QUERY:", query)

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True
        )

        similarities = cosine_similarity(
            query_embedding,
            self.embeddings
        )[0]

        ranked_indices = np.argsort(
            similarities
        )[::-1]

        allowed_ids = {
            p.id for p in products
        }

        retrieved = []

        print("\nTOP MATCHES:\n")

        for idx in ranked_indices:

            product = self.products[idx]

            if product["id"] not in allowed_ids:
                continue

            print(
                product["name"],
                "| score:",
                similarities[idx]
            )

            retrieved.append(
                Product(**product)
            )

            if len(retrieved) >= top_k:
                break

        return retrieved