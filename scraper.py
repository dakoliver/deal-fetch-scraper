from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

app = Flask(__name__)

# Target URL for scraping
LOWES_URL = "https://www.lowes.com/pl/Deals/4294857984"

def get_html_with_requests():
    """Fetch HTML using requests"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    response = requests.get(LOWES_URL, headers=headers)
    
    # Debugging: Print status and response
    print(f"Status Code: {response.status_code}")
    print(response.text[:1000])  # Print first 1000 characters for debugging
    
    if response.status_code == 200:
        return response.text
    return None

def get_html_with_selenium():
    """Fetch HTML using Selenium (if requests gets blocked)"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(LOWES_URL)
    time.sleep(5)  # Give the page time to load

    html = driver.page_source
    driver.quit()
    
    return html

def scrape_lowes():
    """Extract deals from Lowe's"""
    html = get_html_with_requests()

    if not html:  # If requests fail, use Selenium
        print("Requests blocked, switching to Selenium...")
        html = get_html_with_selenium()

    if not html:
        return []  # No data available

    soup = BeautifulSoup(html, "html.parser")
    deals = []

    # Extract deals from Lowe’s page
    for product in soup.select(".product-card"):
        name_elem = product.select_one(".product-title")
        price_elem = product.select_one(".price")
        
        if name_elem and price_elem:
            name = name_elem.text.strip()
            price = price_elem.text.strip()
            
            deals.append({
                "store": "Lowe's",
                "name": name,
                "price": price,
                "url": LOWES_URL
            })

    return deals

@app.route('/api/deals', methods=['GET'])
def get_deals():
    """API endpoint for fetching deals"""
    lowes_deals = scrape_lowes()
    return jsonify(lowes_deals)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)