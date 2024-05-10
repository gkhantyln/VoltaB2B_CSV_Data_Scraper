import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

email = "YOURUSER"
password = "YOURPASSWORD"
login_url = "https://b2b.siteadi.com/Account/Login?"
products_url = "https://b2b.siteadi.com/Users/SparePartsDetails?ParentItemCode=M.APT4"

def login_session(email, password, login_url):
    try:
       
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Headless modu etkinleştirir
        chrome_options.add_argument("--disable-gpu")  # GPU'yu devre dışı bırakır
        chrome_options.add_argument("--no-sandbox")  # Güvenli çalışmayı devre dışı bırakır (bazı ortamlarda gerekli)
        service = ChromeService(executable_path="chromedriver.exe")
        driver = webdriver.Chrome(service=service, options=chrome_options)

       
        driver.get(login_url)

        
        wait = WebDriverWait(driver, 10)

        
        email_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='MainContent_Email']")))
        email_input.send_keys(email)

        
        password_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='MainContent_Password']")))
        password_input.send_keys(password)

        
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Giriş Yap / Login']")))
        login_button.click()

        return driver
    except (TimeoutException, NoSuchElementException) as e:
        print("Giriş yapılırken bir hata oluştu:", e)
        return None

def get_products(driver, products_url):
    try:
        
        driver.get(products_url)

        
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".col-lg-3.col-md-6.mb-r")))
        products = driver.find_elements(By.CSS_SELECTOR, ".col-lg-3.col-md-6.mb-r")

        return products
    except Exception as e:
        print("Ürünler alınırken bir hata oluştu:", e)
        return None

def write_to_csv(products, filename):
    try:
        
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Ürün Barkod Kodu", "Ürün Adı", "Fiyat", "Ürün Resmi"])
            for product in products:
                try:
                    product_barcode = product.find_element(By.CSS_SELECTOR, '.card-title').text.strip()
                    product_name = product.find_element(By.CSS_SELECTOR, 'h5.card-title strong').text.strip()
                    product_price = product.find_element(By.CSS_SELECTOR, '.discount').text.strip()
                    product_image = product.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
                    writer.writerow([product_barcode, product_name, product_price, product_image])
                except NoSuchElementException as e:
                    print("Ürün bilgileri bulunamadı:", e)
    except Exception as e:
        print("CSV dosyasına yazılırken bir hata oluştu:", e)

def main():
    
    driver = login_session(email, password, login_url)
    if driver:
        
        products = get_products(driver, products_url)
        if products:
            write_to_csv(products, "urunler.csv")
            print("Veriler 'urunler.csv' dosyasına başarıyla kaydedildi.")
        else:
            print("Ürünler alınamadı.")
        driver.quit()
    else:
        print("Giriş yapma işlemi başarısız oldu.")

if __name__ == "__main__":
    main()
