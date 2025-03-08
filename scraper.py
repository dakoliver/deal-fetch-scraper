from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import undetected_chromedriver as uc

app = Flask(__name__)

def get_deals():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize undetected ChromeDriver
    driver = uc.Chrome(options=chrome_options)

    try:
        driver.get("https://www.lowes.com/pl/Deals/4294857984")
        time.sleep(5)  # Allow time for page to load

        deals = []
        products = driver.find_elements(By.CLASS_NAME, "product-card")
        
        for product in products:
            try:
                name = product.find_element(By.CLASS_NAME, "product-title").text
                price = product.find_element(By.CLASS_NAME, "price").text
                deals.append({"name": name, "price": price})
            except:
                continue  # Skip products without name or price

        return deals

    finally:
        driver.quit()

@app.route('/api/deals', methods=['GET'])
def api_get_deals():
    return jsonify(get_deals())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)