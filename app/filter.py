from typing import List
from app.models import Product


class ProductFilter:

    def __init__(self, products: List[Product]):
        self.products = products

    def filter(
        self,
        age: int,
        budget: int,
        category: str = None
    ) -> List[Product]:

        filtered = []

        for product in self.products:

            # CATEGORY FILTER
            if category:
                if product.category.lower() != category.lower():
                    continue

            # BUDGET FILTER
            if product.price > budget:
                continue

            # AGE FILTER
            try:
                min_age, max_age = map(
                    int,
                    product.age_range.split("-")
                )

                # overlap logic
                if age < min_age or age > max_age:
                    continue

            except:
                pass

            filtered.append(product)

        print(f"\nFiltered products: {len(filtered)}")

        for p in filtered[:10]:
            print(
                p.name,
                "|",
                p.category,
                "|",
                p.age_range,
                "|",
                p.price
            )

        return filtered