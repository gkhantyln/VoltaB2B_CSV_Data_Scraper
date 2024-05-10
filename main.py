import csv
import asyncio
from pyppeteer import launch

email = ""
password = ""
login_url = "LOGIN_URL"
products_url = "Users/SparePartsDetails?ParentItemCode=" #Product URL

login_data = {
    "ctl00$MainContent$Email": email,
    "ctl00$MainContent$Password": password
}

async def main():
    browser = await launch()
    page = await browser.newPage()

    await page.goto(login_url)
    await page.type('#MainContent_Email', email)
    await page.type('#MainContent_Password', password)
    await page.click('input[type="submit"]')
    await page.waitForNavigation()

    
    await page.goto(products_url)

    
    products = await page.querySelectorAll('.col-lg-3.col-md-6.mb-r')

    with open("urunler.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Ürün Barkod Kodu", "Ürün Adı", "Fiyat", "Ürün Resmi"])

        for product in products:
            product_name = await product.querySelectorEval('.card-title', '(element) => element.textContent')
            product_barcode = await product.querySelectorEval('.text-muted', '(element) => element.textContent')
            product_price = await product.querySelectorEval('.discount', '(element) => element.textContent')
            product_image = await product.querySelectorEval('img', '(element) => element.getAttribute("src")')

            writer.writerow([product_barcode.strip(), product_name.strip(), product_price.strip(), product_image])

    print("Veriler 'products.csv' dosyasına kaydedildi.")

    await browser.close()

asyncio.get_event_loop().run_until_complete(main())

