from pydantic import BaseModel, Field, validator
from typing import Optional


class Product(BaseModel):
    id: str = Field(..., description="Unique product ID")
    name: str
    category: str
    age_range: str
    price: int = Field(..., ge=0)
    description: str
    reviews: Optional[str] = ""
    safety_info: Optional[str] = ""

    @validator("category")
    def validate_category(cls, v):
        allowed = {"toys", "stroller", "feeding", "care", "travel"}
        if v.lower() not in allowed:
            raise ValueError(f"Invalid category: {v}")
        return v.lower()

    @validator("age_range")
    def validate_age_range(cls, v):
        try:
            low, high = map(int, v.split("-"))
            if low < 0 or high < low:
                raise ValueError
        except:
            raise ValueError(f"Invalid age_range format: {v}")
        return v