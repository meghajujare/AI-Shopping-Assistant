from app.data_loader import DataLoader

loader = DataLoader()
products = loader.load()

print(f"Loaded {len(products)} products")
print(products[0].dict())