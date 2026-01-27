from fastapi import FastAPI, HTTPException, Query
from services.scraper import scrape_ebay, ScraperError
from logger import setup_logger
from models.product import Product
import asyncio
import sys

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

logger = setup_logger()

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
async def scrape(query: str = Query(..., min_length=3, description="Texto a buscar en eBay")):


    if not query.strip():
        logger.warning("Query invalida: solo espacios")
        raise HTTPException(status_code=400, detail="La query no puede estar vacia") 
    
    logger.info(f"Request recibido / scrape | query={query}")
    
    try:
        products = await scrape_ebay(query)

        if not products: 
            logger.info(f"No se encontraron productos | query={query}")
            raise HTTPException(status_code=400, detail="No se encontraron productos para la busqueda")
        
        logger.info(f"Scraping exitoso | query={query} | productos={len(products)}")

        return products

    except ScraperError as e:
        logger.error(f"Error de scrping | query={query} | error={e}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
    except Exception as e:
        logger.exception(f"Error inesperado | query={query}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")
