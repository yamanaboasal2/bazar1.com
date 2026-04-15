from flask import Flask, jsonify
import csv
//....
app = Flask(__name__)
FILE = "catalog.csv"

def read_catalog():
    data = []
    try:
        with open(FILE, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
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
    return "Catalog working ✅"

@app.route('/search/<topic>')
def search(topic):
    data = read_catalog()
    result = []
    for book in data:
        if book['topic'].lower() == topic.lower():
            result.append({"id": book['id'], "title": book['title']})
    return jsonify(result)

@app.route('/info/<int:id>')
def info(id):
    data = read_catalog()
    for book in data:
        if int(book['id']) == id:
            return jsonify(book)
    return jsonify({"error": "not found"}), 404

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    data = read_catalog()
    for book in data:
        if int(book['id']) == id:
            if int(book['quantity']) > 0:
                book['quantity'] = str(int(book['quantity']) - 1)
                write_catalog(data)
                return jsonify({"message": "updated"})
            else:
                return jsonify({"message": "out of stock"})
    return jsonify({"error": "not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)