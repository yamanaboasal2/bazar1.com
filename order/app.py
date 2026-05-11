from flask import Flask, jsonify
import requests
import time

app = Flask(__name__)

CATALOG_URL = "http://127.0.0.1:5001"

orders = []


# Purchase a book
@app.route("/purchase/<int:id>", methods=["POST"])
def purchase(id):

    # Try connecting to catalog service
    for i in range(5):
        try:
            response = requests.get(f"{CATALOG_URL}/info/{id}")
            break
        except:
            time.sleep(1)

    # Check if book exists
    if response.status_code != 200:
        return jsonify({"error": "book not found"})

    book = response.json()

    # Check stock availability
    if int(book['quantity']) > 0:

        # Update quantity in catalog service
        requests.post(f"{CATALOG_URL}/update/{id}")

        # Create order object
        order = {
            "book_id": id,
            "title": book['title'],
            "price": book['price'],
            "status": "completed"
        }

        # Save order
        orders.append(order)

        return jsonify({
            "message": f"bought book {book['title']}",
            "order": order
        })

    else:
        return jsonify({"message": "out of stock right now!"})


# Get all orders
@app.route("/orders")
def get_orders():
    return jsonify(orders)

# Get order by ID
@app.route('/orders/<int:id>')
def get_order(id):

    for order in orders:
        if order['book_id'] == id:
            return jsonify(order)

    return jsonify({"error": "order not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)