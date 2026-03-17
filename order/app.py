from flask import Flask, jsonify
import requests

app = Flask(__name__)


CATALOG_URL = "http://localhost:5001"


@app.route('/purchase/<int:id>', methods=['GET', 'POST'])
def purchase(id):
   
    response = requests.get(f"{CATALOG_URL}/info/{id}")
    
    if response.status_code != 200:
        return jsonify({"error": "book not found"})

    book = response.json()

    
    if int(book['quantity']) > 0:
        
        print(f"bought book {book['title']}")

        return jsonify({
            "message": f"bought book {book['title']}"
        })
    else:
        print("out of stock")  # برضو مفيد للتقرير

        return jsonify({
            "message": "out of stock"
        })


app.run(port=5002, debug=True)