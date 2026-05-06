from app.data_loader import DataLoader
from app.filter import ProductFilter

loader = DataLoader()
products = loader.load()

filter_engine = ProductFilter(products)

results = filter_engine.filter(
    age=2,
    budget=2000,
    category="toys"
)

print(f"Filtered results: {len(results)}")
for r in results:
    print(r.name, r.price, r.age_range)