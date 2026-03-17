from flask import Flask, jsonify
import requests

app = Flask(__name__)

CATALOG_URL = "http://localhost:5001"
ORDER_URL = "http://localhost:5002"

# search من خلال frontend
@app.route('/search/<topic>')
def search(topic):
    response = requests.get(f"{CATALOG_URL}/search/{topic}")
    return jsonify(response.json())

# info من خلال frontend
@app.route('/info/<int:id>')
def info(id):
    response = requests.get(f"{CATALOG_URL}/info/{id}")
    return jsonify(response.json())

# purchase من خلال frontend
@app.route('/purchase/<int:id>')
def purchase(id):
    response = requests.get(f"{ORDER_URL}/purchase/{id}")
    return jsonify(response.json())

# تشغيل السيرفر
app.run(port=5000, debug=True)