from flask import Flask, jsonify
import requests

app = Flask(__name__)

catalog_servers = [
    "http://catalog:5001",
    "http://catalog_2:5001"
]

order_servers = [
    "http://order:5002",
    "http://order_2:5002"
]

catalog_index = 0
order_index = 0

# cache for info requests
cache = {}

# cache for search requests
search_cache = {}


@app.route("/")
def home():
    return "Frontend working correctly!"


@app.route('/search/<topic>')
def search(topic):

    global catalog_index

    # check search cache
    if topic in search_cache:
        print("SEARCH CACHE HIT", flush=True)
        return jsonify(search_cache[topic])

    print("SEARCH CACHE MISS", flush=True)

    # round robin load balancing
    server = catalog_servers[catalog_index]
    catalog_index = (catalog_index + 1) % 2

    print("FORWARDED TO:", server, flush=True)

    resp = requests.get(f"{server}/search/{topic}")

    data = resp.json()

    # save result in cache
    search_cache[topic] = data

    return jsonify(data)


@app.route('/info/<int:id>')
def info(id):

    global catalog_index

    # check info cache
    if id in cache:
        print("CACHE HIT", flush=True)
        return jsonify(cache[id])

    print("CACHE MISS", flush=True)

    # round robin load balancing
    server = catalog_servers[catalog_index]
    catalog_index = (catalog_index + 1) % 2

    print("FORWARDED TO:", server, flush=True)

    resp = requests.get(f"{server}/info/{id}")

    data = resp.json()

    # save result in cache
    cache[id] = data

    return jsonify(data)


@app.route('/purchase/<int:id>', methods=['POST'])
def purchase(id):

    global order_index

    # round robin load balancing
    server = order_servers[order_index]
    order_index = (order_index + 1) % 2

    print("FORWARDED TO:", server, flush=True)

    resp = requests.post(f"{server}/purchase/{id}")

    # invalidate info cache
    if id in cache:
        print("INVALIDATING INFO CACHE", flush=True)
        del cache[id]

    # invalidate search cache
    print("INVALIDATING SEARCH CACHE", flush=True)
    search_cache.clear()

    return jsonify(resp.json())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)