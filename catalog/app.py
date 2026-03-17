from flask import Flask, jsonify
import csv
from urllib.parse import unquote

app = Flask(__name__)

# قراءة البيانات من CSV
def read_catalog():
    with open('catalog.csv', newline='') as file:
        return list(csv.DictReader(file))

# البحث حسب الموضوع
@app.route('/search/<topic>')
def search(topic):
    topic = unquote(topic)  # حل مشكلة %20
    data = read_catalog()
    result = []

    for book in data:
        if book['topic'] == topic:
            result.append({
                "id": book['id'],
                "title": book['title']
            })

    return jsonify(result)

# جلب معلومات كتاب
@app.route('/info/<int:id>')
def info(id):
    data = read_catalog()

    for book in data:
        if int(book['id']) == id:
            return jsonify({
                "title": book['title'],
                "quantity": book['stock'],
                "price": book['price']
            })

    return jsonify({"error": "not found"})

# تشغيل السيرفر
app.run(port=5001, debug=True)