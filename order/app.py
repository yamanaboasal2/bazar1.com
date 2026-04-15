from flask import Flask, jsonify
import requests
import time

app = Flask(__name__)

CATALOG_URL = "http://catalog:5001"

@app.route("/purchase/<int:id>", methods=["POST"])
def purchase(id):
    for i in range(5):
        try:
            response = requests.get(f"{CATALOG_URL}/info/{id}")
            break
        except:
            time.sleep(1)

    if response.status_code != 200:
        return jsonify({"error": "book not found"})

    book = response.json()

    if int(book['quantity']) > 0:
        requests.post(f"{CATALOG_URL}/update/{id}")
        return jsonify({"message": f"bought book {book['title']}"})
    else:
        return jsonify({"message": "out of stock"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)