import asyncio
from services.scraper import scrape_ebay, ScraperError
from storage.storage import crear_json
from logger import setup_logger

logger = setup_logger()

async def main():
    try:
        products = await scrape_ebay("ps4 2tb")
        crear_json(products, "ps4_2tb")
        logger.info(f"Archivo JSON generado correctamente")

    except ScraperError as e:
        logger.error(f"Fallo el scraping: {e}")

if __name__ == "__main__":
    asyncio.run(main())