from playwright.async_api import async_playwright
from config import URL, DEFAULT_HEADLESS

async def scrape_ebay(query: str) -> list[dict]:
    data = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=DEFAULT_HEADLESS)
        
        page = await browser.new_page()
        await page.goto(URL)

        buscador = page.get_by_placeholder("Buscar artículos")
        await buscador.fill(query)
        await buscador.press("Enter")

        await page.wait_for_selector(".srp-results", state="visible")

        while True:
            productos = page.locator(".srp-results > li")
            cant_productos = await productos.count()

            for i in range(cant_productos):
                product = productos.nth(i)

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

                data.append({
                    "title": title,
                    "price": price
                })

            btn_next = page.locator("a.pagination__next")
            if await btn_next.count() == 0:
                break

            await btn_next.click()
            await page.wait_for_selector(".srp-results", state="visible")

        await browser.close()

    return data
