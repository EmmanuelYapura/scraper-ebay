import json

def crear_json(datos: list[dict], filename: str) -> None:
    with open(f"{filename}.json", "w", encoding="utf-8") as file :
        json.dump(datos, file, indent=3, ensure_ascii=False)