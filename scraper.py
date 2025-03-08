from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

LOWES_URL = "https://www.lowes.com/pl/Deals/4294857984"

def scrape_lowes():
    options = Options()
    options.add_argument("--headless")  # Run Chrome in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-blink-features=AutomationControlled")

    # Set up WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Fetch webpage
    driver.get(LOWES_URL)
    time.sleep(5)  # Wait for the page to fully load

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()  # Close the browser after scraping

    deals = []

    # Extract product information
    for product in soup.select(".product-card"):
        name_elem = product.select_one(".product-title")
        price_elem = product.select_one(".price")

        if name_elem and price_elem:
            deals.append({
                "store": "Lowe's",
                "name": name_elem.text.strip(),
                "price": price_elem.text.strip(),
                "url": LOWES_URL
            })

    return deals

@app.route('/api/deals', methods=['GET'])
def get_deals():
    lowes_deals = scrape_lowes()
    return jsonify(lowes_deals)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)