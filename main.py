import asyncio
import json
from playwright.async_api import async_playwright

def crear_json(datos, producto):
    with open(f"{producto}.json", "w", encoding="utf-8") as file :
        json.dump(datos, file, indent=3, ensure_ascii=False)

async def extraer_info(productos, cant):
    data = []    
    for i in range(cant):
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

        product_info = {
            "title": title,
            "price": price
        }

        print(product_info)

        data.append(product_info)        

    return data

async def main():
    data = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto("https://www.ebay.com/")

        buscador = page.get_by_placeholder("Buscar artículos")
        await buscador.fill("ps4 2tb")
        await buscador.press("Enter")

        await page.wait_for_selector(".srp-results", state="visible")

        while True:
            print("########## Scrapeando paginación ##########")

            productos = page.locator(".srp-results > li")
            cant_productos = await productos.count()

            data_pagination = await extraer_info(productos, cant_productos)
            data += data_pagination

            btn_next = page.locator("a.pagination__next")

            if await btn_next.count() == 0:
                print("Se acabó la paginación")
                break

            await btn_next.click()
            await page.wait_for_selector(".srp-results", state="visible")

        crear_json(data, "ps4_2tb")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())