from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

def setup_driver():
    """ Set up Chrome WebDriver with the required options. """
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Install Chrome WebDriver automatically
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def scrape_lowes():
    """ Scrapes Lowe's deals and returns JSON data. """
    LOWES_URL = "https://www.lowes.com/pl/Deals/4294857984"
    
    driver = setup_driver()
    driver.get(LOWES_URL)

    # Wait for page to load (increase time if necessary)
    driver.implicitly_wait(5)
    
    # Extract deals (modify the logic based on the actual page structure)
    products = driver.find_elements("css selector", ".product-card")
    deals = []

    for product in products:
        try:
            name = product.find_element("css selector", ".product-title").text
            price = product.find_element("css selector", ".price").text
            original_price = product.find_element("css selector", ".original-price").text
            
            discount_percentage = round(((float(original_price.strip("$")) - float(price.strip("$"))) / float(original_price.strip("$"))) * 100, 2)
            
            if discount_percentage >= 15:  # Only include deals >= 15% off
                deals.append({
                    "store": "Lowe's",
                    "name": name,
                    "price": price,
                    "original_price": original_price,
                    "discount": f"{discount_percentage}%",
                    "url": LOWES_URL
                })
        except Exception:
            pass  # Skip if any issue occurs in parsing

    driver.quit()
    return deals

@app.route('/api/deals', methods=['GET'])
def get_deals():
    """ API endpoint to return scraped deals in JSON format. """
    lowes_deals = scrape_lowes()
    return jsonify(lowes_deals)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)