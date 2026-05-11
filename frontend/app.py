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

cache = {}
search_cache = {}


@app.route("/")
def home():
    return "Frontend working correctly!"


# ---------------- SEARCH ----------------
@app.route('/search/<topic>')
def search(topic):
    global catalog_index

    print(f"\n[SEARCH REQUEST] topic = {topic}", flush=True)

    if topic in search_cache:
        print("[SEARCH CACHE HIT]", flush=True)
        return jsonify(search_cache[topic])

    print("[SEARCH CACHE MISS]", flush=True)

    server = catalog_servers[catalog_index]
    catalog_index = (catalog_index + 1) % len(catalog_servers)

    print(f"[FORWARDING] {server}", flush=True)

    resp = requests.get(f"{server}/search/{topic}")
    data = resp.json()

    search_cache[topic] = data

    print(f"[SEARCH DONE] found {len(data)} books", flush=True)

    return jsonify(data)


# ---------------- INFO ----------------
@app.route('/info/<int:id>')
def info(id):
    global catalog_index

    print(f"\n[INFO REQUEST] id = {id}", flush=True)

    if id in cache:
        print("[CACHE HIT]", flush=True)
        return jsonify(cache[id])

    print("[CACHE MISS]", flush=True)

    server = catalog_servers[catalog_index]
    catalog_index = (catalog_index + 1) % len(catalog_servers)

    print(f"[FORWARDING] {server}", flush=True)

    resp = requests.get(f"{server}/info/{id}")
    data = resp.json()

    cache[id] = data

    print(f"[CACHE STORE] id {id} cached", flush=True)

    return jsonify(data)


# ---------------- PURCHASE ----------------
@app.route('/purchase/<int:id>', methods=['POST'])
def purchase(id):
    global order_index

    print(f"\n[PURCHASE REQUEST] id = {id}", flush=True)

    server = order_servers[order_index]
    order_index = (order_index + 1) % len(order_servers)

    print(f"[FORWARDING] {server}", flush=True)

    resp = requests.post(f"{server}/purchase/{id}")

    # invalidate caches
    if id in cache:
        print("[CACHE INVALIDATED: INFO]", flush=True)
        cache.pop(id, None)

    print("[CACHE INVALIDATED: SEARCH]", flush=True)
    search_cache.clear()

    return jsonify(resp.json())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)