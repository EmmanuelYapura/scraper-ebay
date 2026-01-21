from fastapi import FastAPI, HTTPException
from services.scraper import scrape_ebay, ScraperError
from models.product import Product
import asyncio
import sys

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

app = FastAPI(
    title="Ebay Scraper API",
    description="API para scrapear productos de eBay",
    version="1.0.0"
)

@app.get(
    "/scrape",
    response_model=list[Product],
    summary="Scrapear productos de eBay"
)
async def scrape(query: str):
    try:
        products = await scrape_ebay(query)
        return products

    except ScraperError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
