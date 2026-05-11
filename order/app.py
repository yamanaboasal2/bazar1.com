from flask import Flask, jsonify
import requests
import time

app = Flask(__name__)


CATALOG_URL = "http://catalog:5001"

orders = []


@app.route("/purchase/<int:id>", methods=["POST"])
def purchase(id):

    response = None

    # Try to connect to catalog service
    for i in range(5):
        try:
            response = requests.get(f"{CATALOG_URL}/info/{id}", timeout=2)
            break
        except:
            time.sleep(1)

    # If still no response
    if response is None:
        return jsonify({"error": "catalog service not reachable"}), 500

    # Check if book exists
    if response.status_code != 200:
        return jsonify({"error": "book not found"}), 404

    book = response.json()

    # Check stock
    if int(book["quantity"]) <= 0:
        return jsonify({"message": "out of stock right now!"}), 400

    # Try update catalog (safe call)
    try:
        requests.post(f"{CATALOG_URL}/update/{id}", timeout=2)
    except:
        pass

    order = {
        "book_id": id,
        "title": book["title"],
        "price": book["price"],
        "status": "completed"
    }

    orders.append(order)

    return jsonify({
        "message": f"bought book {book['title']}",
        "order": order
    })


@app.route("/orders")
def get_orders():
    return jsonify(orders)


@app.route('/orders/<int:id>')
def get_order(id):

    for order in orders:
        if order["book_id"] == id:
            return jsonify(order)

    return jsonify({"error": "order not found"}), 404


@app.route("/")
def home():
    return "Order service working"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)