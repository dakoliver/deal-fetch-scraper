from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Target URL for scraping
LOWES_URL = "https://www.lowes.com/pl/Deals/4294857984"

def scrape_lowes():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    response = requests.get(LOWES_URL, headers=headers)
    
    # If request fails, return an empty list
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    deals = []

    # Extract deals from Lowe's HTML structure
    for product in soup.select(".product-card"):
        name = product.select_one(".product-title")
        price = product.select_one(".price")

        if name and price:
            deals.append({
                "store": "Lowe's",
                "name": name.text.strip(),
                "price": price.text.strip(),
                "url": LOWES_URL
            })

    return deals

@app.route('/api/deals', methods=['GET'])
def get_deals():
    lowes_deals = scrape_lowes()
    return jsonify(lowes_deals)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)