import asyncio
from scraper import scrape_ebay
from storage import crear_json

async def main():
    products = await scrape_ebay("ps4 2tb")
    crear_json(products, "ps4_2tb")

if __name__ == "__main__":
    asyncio.run(main())