from playwright.async_api import async_playwright
from config import URL, DEFAULT_HEADLESS, SELECTOR_TIMEOUT, PAGE_TIMEOUT
from models.product import Product
from logger import setup_logger

logger = setup_logger()

class ScraperError(Exception):
    """Error base del scraper"""
    pass

async def scrape_ebay(query: str, max_pages: int, max_results: int) -> list[Product]:
    logger.info(f"Iniciando scraping en eBay | query='{query}'")
    data = []

    try: 

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=DEFAULT_HEADLESS)
            page = await browser.new_page()

            page.set_default_timeout(SELECTOR_TIMEOUT)
            page.set_default_navigation_timeout(PAGE_TIMEOUT)

            await page.goto(URL)
            logger.info("Pagina principal cargada")

            buscador = page.get_by_placeholder("Buscar artículos")
            await buscador.fill(query)
            await buscador.press("Enter")

            await page.wait_for_selector(".srp-results", state="visible")
            logger.info("Resultados visibles, comenzando paginacion")

            page_number = 1
            stop_scraping = False

            while True:
                if page_number > max_pages:
                    logger.info("Limite de paginas alcanzado")
                    break

                logger.info(f"Scrapeando página {page_number}")
                productos = page.locator(".srp-results > li")
                cant_productos = await productos.count()

                for i in range(cant_productos):
                    product = productos.nth(i)

                    if len(data) >= max_results:
                        logger.info("Limite de resultados alcanzado")
                        stop_scraping = True
                        break

                    try:
                        title_locator = product.locator(".s-card__title span.primary").filter(visible=True).first

                        if await title_locator.count() == 0:
                            continue

                        title = await title_locator.text_content()

                        price_locator = product.locator(".s-card__price")
                        price = None

                        if await price_locator.count() > 0:
                            price_text = await price_locator.first.text_content()
                            if price_text:
                                price = price_text

                        data.append(Product(
                            title=title,
                            price=price
                        ))
                        logger.debug("Producto agregado")

                    except TimeoutError:
                        logger.warning("Timeout al procesar un producto")
                        continue

                if stop_scraping:
                    break
                    
                btn_next = page.locator("a.pagination__next")
                if await btn_next.count() == 0:
                    logger.info("No hay mas paginas")
                    break

                await btn_next.click()
                await page.wait_for_selector(".srp-results", state="visible")
                page_number += 1

            await browser.close()
            logger.info("Browser cerrado correctamente")

    except TimeoutError as e:
        logger.error("Timeout general durante el scraping", exc_info=True)
        raise ScraperError("Timeout general al scraper ebay") from e

    except Exception as e:
        logger.error("Error inesperado en el scraper", exc_info=True)
        raise ScraperError("Error inesperado en el scraper") from e 

    logger.info(f"Scraping finalizado | productos obtenidos: {len(data)}")
    return data
