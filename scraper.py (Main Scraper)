import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

app = Flask(__name__)

LOWES_URL = "https://www.lowes.com/pl/Deals/4294857984"

def scrape_lowes():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(LOWES_URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    deals = []
    
    for product in soup.select(".product-card"):
        name = product.select_one(".product-title").text.strip()
        price = product.select_one(".price").text.strip().replace("$", "")
        original_price_elem = product.select_one(".original-price")
        
        if original_price_elem:
            original_price = original_price_elem.text.strip().replace("$", "")
            discount_percentage = round(((float(original_price) - float(price)) / float(original_price)) * 100, 2)
            
            if discount_percentage >= 15:  # Only show deals with 15%+ discount
                deals.append({
                    "store": "Lowe's",
                    "name": name,
                    "price": f"${price}",
                    "original_price": f"${original_price}",
                    "discount": f"{discount_percentage}% Off",
                    "url": LOWES_URL
                })
    
    return deals

@app.route('/api/deals', methods=['GET'])
def get_deals():
    lowes_deals = scrape_lowes()
    return jsonify(lowes_deals)

if __name__ == '__main__':
    app.run(debug=True)
