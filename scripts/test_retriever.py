from app.data_loader import DataLoader
from app.retriever import Retriever


def main():

    loader = DataLoader()

    products = loader.load()

    retriever = Retriever()

    query = "Travel Organizer"

    results = retriever.retrieve(
        query=query,
        products=products,
        top_k=5
    )

    print("\n=========== RESULTS ===========\n")

    for i, p in enumerate(results, start=1):

        print(
            f"{i}. {p.name} | {p.category}"
        )

    print("\n===============================\n")


if __name__ == "__main__":
    main()