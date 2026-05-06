from app.data_loader import DataLoader
from app.pipeline import RecommendationPipeline


def main():
    # Load data
    loader = DataLoader()
    products = loader.load()

    # Initialize pipeline
    pipeline = RecommendationPipeline(products)

    # Sample test input
    result = pipeline.run(
        query="learning toys for brain development",
        age=2,
        budget=2000,
        category="toys"
    )

    print("\n=== RESULT ===")
    print(result)


if __name__ == "__main__":
    main()