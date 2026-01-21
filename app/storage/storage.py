import json
from typing import Iterable
from models.product import Product

def crear_json(datos: Iterable[Product], filename: str) -> None:
    data = [dato.model_dump() for dato in datos]

    with open(f"{filename}.json", "w", encoding="utf-8") as file :
        json.dump(data, file, indent=3, ensure_ascii=False)