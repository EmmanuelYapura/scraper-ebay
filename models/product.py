from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    title: str
    price: Optional[str] = None