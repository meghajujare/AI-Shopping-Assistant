# AI Shopping Assistant

AI Shopping Assistant is an AI-powered semantic recommendation system that helps parents discover relevant products based on user queries, child age, budget, and category preferences.

The system uses Sentence Transformers for semantic search, embedding-based retrieval for product matching, and Groq-hosted LLMs for intelligent recommendation reasoning.

---

## Live Demo

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ai-shopping-assistant-megha.streamlit.app/)

---

## Features

- Semantic product search
- AI-powered recommendations
- Budget-aware filtering
- Category-based retrieval
- Confidence scoring
- Streamlit web interface
- Groq LLM integration
- Embedding-based semantic similarity
- Supports 200+ parenting products

---

## Tech Stack

### Frontend
- Streamlit

### Backend
- Python

### AI / ML
- Sentence Transformers
- Semantic Search
- Embedding Retrieval
- Groq LLM API

### Libraries
- NumPy
- Scikit-learn
- OpenAI SDK
- Pandas

---

## Project Architecture

```text
User Query
    ↓
Embedding Generation
    ↓
Semantic Retrieval
    ↓
Filtering (Age / Budget / Category)
    ↓
Ranking
    ↓
LLM-based Recommendation
    ↓
Streamlit UI
```

---

## Folder Structure

```text
AI-Shopping-Assistant/
│
├── app/
│   ├── api.py
│   ├── config.py
│   ├── data_loader.py
│   ├── filter.py
│   ├── logger.py
│   ├── models.py
│   ├── parser.py
│   ├── pipeline.py
│   ├── retriever.py
│   └── ui.py
│
├── data/
│   └── products.json
│
├── embeddings/
│   ├── embeddings.npy
│   └── products.json
│
├── scripts/
│   ├── generate_dataset.py
│   ├── ingest.py
│   ├── test_filter.py
│   ├── test_groq.py
│   ├── test_loader.py
│   ├── test_pipeline.py
│   └── test_retriever.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/meghajujare/AI-Shopping-Assistant.git

cd AI-Shopping-Assistant
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_api_key
MODEL_NAME=llama-3.1-8b-instant
TOP_K=5
```

---

## Generate Embeddings

Run the ingestion script:

```bash
python -m scripts.ingest
```

This generates:

```text
embeddings/embeddings.npy
```

---

## Run the Application

```bash
streamlit run app/ui.py
```

---

## Streamlit Deployment

Add the following secrets in Streamlit Cloud:

```toml
GROQ_API_KEY = "your_api_key"
MODEL_NAME = "llama-3.1-8b-instant"
TOP_K = "5"
```

---

## Example Queries

- bottle warmer
- travel organizer
- stroller for newborn
- educational toys
- feeding bottle set
- diaper backpack

---

## Sample Recommendation Output

```json
{
  "primary_recommendation": {
    "name": "Johnson's Bottle Warmer",
    "price": 2981,
    "reason": "Highest semantic relevance to user query"
  },
  "alternatives": [
    {
      "name": "Munchkin Bottle Warmer",
      "price": 2157,
      "reason": "Lower price and high retrieval rank"
    }
  ],
  "confidence": 0.91
}
```

---

## AI Concepts Used

### Semantic Search

The system converts user queries and product descriptions into vector embeddings using Sentence Transformers.

### Vector Similarity

Cosine similarity is used to retrieve the most relevant products.

### Retrieval-Augmented Recommendation

Retrieved products are ranked and passed through the recommendation pipeline.

### LLM Integration

Groq-hosted LLMs generate intelligent recommendation reasoning.

---

## Future Improvements

- Image-based product search
- Personalized recommendations
- User login system
- Shopping cart integration
- Amazon / Flipkart API integration
- Hybrid search (keyword + semantic)
- FAISS vector database
- Advanced RAG pipeline

---

Live Application:  
https://ai-shopping-assistant-megha.streamlit.app/

---
