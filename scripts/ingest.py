import os
import json
import numpy as np

from sentence_transformers import SentenceTransformer

from app.config import settings


EMBEDDINGS_DIR = "embeddings"

os.makedirs(
    EMBEDDINGS_DIR,
    exist_ok=True
)

PRODUCTS_OUTPUT = os.path.join(
    EMBEDDINGS_DIR,
    "products.json"
)

EMBEDDINGS_OUTPUT = os.path.join(
    EMBEDDINGS_DIR,
    "embeddings.npy"
)


# =========================================
# LOAD DATASET
# =========================================
with open(
    settings.DATA_PATH,
    "r",
    encoding="utf-8"
) as f:

    products = json.load(f)

print(f"\nLoaded {len(products)} products")


# =========================================
# LOAD MODEL
# =========================================
print("\nLoading embedding model...")

model = SentenceTransformer(
    settings.EMBEDDING_MODEL
)

print("Embedding model loaded")


# =========================================
# BUILD DOCUMENTS
# =========================================
documents = []

for p in products:

    text = f"""
    Product Name: {p['name']}
    Category: {p['category']}
    Description: {p['description']}
    Reviews: {p['reviews']}
    Safety: {p['safety_info']}
    Age Range: {p['age_range']}
    """

    documents.append(text)

print(f"\nPrepared {len(documents)} documents")


# =========================================
# GENERATE EMBEDDINGS
# =========================================
print("\nGenerating embeddings...")

embeddings = model.encode(
    documents,
    convert_to_numpy=True,
    show_progress_bar=True
)

print("\nEmbeddings generated")

print("Shape:", embeddings.shape)


# =========================================
# SAVE FILES
# =========================================
np.save(
    EMBEDDINGS_OUTPUT,
    embeddings
)

with open(
    PRODUCTS_OUTPUT,
    "w",
    encoding="utf-8"
) as f:

    json.dump(products, f, indent=2)

print("\nSaved embeddings successfully")