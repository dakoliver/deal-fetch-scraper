from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

app = Flask(__name__)

LOWES_URL = "https://www.lowes.com/pl/Deals/4294857984"

def scrape_lowes():
    # Set up Chrome options to run in headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Start WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Open Lowe's deals page
    driver.get(LOWES_URL)
    time.sleep(5)  # Wait for page to load

    deals = []
    
    # Select all product cards
    products = driver.find_elements(By.CLASS_NAME, "product-card")
    
    for product in products:
        try:
            name = product.find_element(By.CLASS_NAME, "product-title").text
            price = product.find_element(By.CLASS_NAME, "price").text
            original_price_elem = product.find_element(By.CLASS_NAME, "original-price")
            original_price = original_price_elem.text if original_price_elem else None

            if original_price:
                # Convert price strings to numbers
                original_price_num = float(original_price.replace("$", "").replace(",", ""))
                price_num = float(price.replace("$", "").replace(",", ""))
                
                # Calculate discount percentage
                discount_percentage = round(((original_price_num - price_num) / original_price_num) * 100, 2)
                
                if discount_percentage >= 15:  # Only include items with 15%+ discounts
                    deals.append({
                        "store": "Lowe's",
                        "name": name,
                        "price": f"${price_num}",
                        "original_price": f"${original_price_num}",
                        "discount": f"{discount_percentage}%",
                        "url": LOWES_URL
                    })
        except:
            continue

    driver.quit()
    return deals

@app.route('/api/deals', methods=['GET'])
def get_deals():
    lowes_deals = scrape_lowes()
    return jsonify(lowes_deals)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)