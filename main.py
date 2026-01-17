import asyncio
from scraper import scrape_ebay, ScraperError
from storage import crear_json

async def main():
    try:
        products = await scrape_ebay("ps4 2tb")
        crear_json(products, "ps4_2tb")

    except ScraperError as e:
        print(f"Error de scraping: {e}")

if __name__ == "__main__":
    asyncio.run(main())