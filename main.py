from playwright.sync_api import sync_playwright
import json

def crear_json(datos, producto):
    with open(f"{producto}.json", "w", encoding="utf-8") as file :
        json.dump(datos, file, indent=3, ensure_ascii=False)

def extraer_info(productos, cant):
    data = []    
    for i in range(cant):
        product = productos.nth(i)

        title_locator = product.locator(".s-card__title span.primary").filter(visible=True).first
        if title_locator.count() == 0:
            continue

        title = title_locator.text_content()

        price_locator = product.locator(".s-card__price")
        price = None 

        if price_locator.count() > 0:
            price_text = price_locator.first.text_content()
            if price_text:
                price = price_text

        product_info = {
            "title": title,
            "price": price
        }

        print(product_info)

        data.append(product_info)        

    return data


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.ebay.com/")

    buscador = page.get_by_placeholder("Buscar artículos")
    buscador.fill("ps4 2tb")
    buscador.press("Enter")

    page.wait_for_selector(".srp-results", state="visible")
    
    productos = page.locator(".srp-results > li")
    cant_productos = productos.count()

    paginacion = page.locator("ol.pagination__items > li")

    data = []

    while True:
        print("##########Scrapeando paginacion....##########")
        data_pagination = extraer_info(productos, cant_productos)
        data += data_pagination 
        btn_next = page.locator("a.pagination__next")
        
        if btn_next.count() == 0:
            print("Se acabo la paginacion")
            break
        
        btn_next.click()
        page.wait_for_selector(".srp-results", state="visible")
    
    crear_json(data, "ps4_2tb")   
    input("Click para cerrar la pagina")
    browser.close()
