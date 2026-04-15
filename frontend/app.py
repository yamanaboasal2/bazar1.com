from flask import Flask, jsonify
import requests

app = Flask(__name__)

CATALOG_URL = "http://catalog:5001"
ORDER_URL   = "http://order:5002"
//front
@app.route("/")
def home():
    return "Frontend working 🚀"

@app.route('/search/<topic>')
def search(topic):
    resp = requests.get(f"{CATALOG_URL}/search/{topic}")
    return jsonify(resp.json())

@app.route('/info/<int:id>')
def info(id):
    resp = requests.get(f"{CATALOG_URL}/info/{id}")
    return jsonify(resp.json())

@app.route('/purchase/<int:id>', methods=['POST'])
def purchase(id):
    resp = requests.post(f"{ORDER_URL}/purchase/{id}")
    return resp.json()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)