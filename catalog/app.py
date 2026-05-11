from flask import Flask, jsonify
import csv

app = Flask(__name__)

FILE = "catalog.csv"


def read_catalog():
    data = []
    try:
        with open(FILE, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                row["id"] = int(row["id"])
                row["quantity"] = int(row["quantity"])
                row["price"] = str(row["price"])
                data.append(row)
    except:
        return []
    return data


def write_catalog(data):
    with open(FILE, 'w', newline='') as f:
        fieldnames = ['id', 'title', 'topic', 'quantity', 'price']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


@app.route("/")
def home():
    return "Catalog working correctly"


# SEARCH 
@app.route('/search/<topic>')
def search(topic):
    data = read_catalog()
    result = []

    for book in data:
        if book['topic'].lower() == topic.lower():
            result.append({
                "id": book["id"],
                "title": book["title"],
                "quantity": book["quantity"],
                "price": book["price"]
            })

    return jsonify(result)


# INFO 
@app.route('/info/<int:id>')
def info(id):
    data = read_catalog()

    for book in data:
        if book['id'] == id:
            return jsonify({
                "id": book["id"],
                "title": book["title"],
                "topic": book["topic"],
                "quantity": book["quantity"],
                "price": book["price"]
            })

    return jsonify({"error": "not found"}), 404


# UPDATE STOCK
@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    data = read_catalog()

    for book in data:
        if book['id'] == id:

            if book['quantity'] > 0:
                book['quantity'] -= 1
                write_catalog(data)
                return jsonify({"message": "updated", "new_quantity": book["quantity"]})

            return jsonify({"message": "out of stock"}), 400

    return jsonify({"error": "not found"}), 404


# GET ALL BOOKS
@app.route('/books')
def books():
    return jsonify(read_catalog())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)