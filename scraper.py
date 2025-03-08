from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

LOWES_URL = "https://www.lowes.com/pl/Deals/4294857984"

def scrape_lowes():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(LOWES_URL, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    deals = []

    for product in soup.select(".product-card"):
        name_elem = product.select_one(".product-title")
        price_elem = product.select_one(".price")
        original_price_elem = product.select_one(".original-price")

        if name_elem and price_elem and original_price_elem:
            name = name_elem.text.strip()
            price = float(price_elem.text.replace("$", "").replace(",", "").strip())
            original_price = float(original_price_elem.text.replace("$", "").replace(",", "").strip())

            discount_percentage = round(((original_price - price) / original_price) * 100, 2)

            if discount_percentage >= 15:  # Only store deals with 15%+ discount
                deals.append({
                    "store": "Lowe's",
                    "name": name,
                    "price": f"${price:.2f}",
                    "original_price": f"${original_price:.2f}",
                    "discount": f"{discount_percentage}%",
                    "url": LOWES_URL
                })

    return deals

@app.route('/api/deals', methods=['GET'])
def get_deals():
    lowes_deals = scrape_lowes()
    return jsonify(lowes_deals)

if __name__ == '__main__':
    app.run(debug=True)