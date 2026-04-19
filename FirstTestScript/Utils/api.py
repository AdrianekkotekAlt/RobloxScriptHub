from flask import Flask, request, jsonify
import time, json, os

@app.route("/")
def home():
    return "API is running"

app = Flask(__name__)
DB_FILE = "FirstTestScript/Utils/keys.json"

def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=4)

@app.route("/validate", methods=["POST"])
def validate():
    data = request.json
    key = data.get("key")
    userId = data.get("userId")

    db = load_db()

    if key not in db:
        return jsonify({"valid": False})

    entry = db[key]

    if time.time() > entry["expires"]:
        return jsonify({"valid": False})

    if not entry["activated"]:
        entry["activated"] = True
        entry["userId"] = userId
        save_db(db)
        return jsonify({"valid": True})

    if entry["userId"] == userId:
        return jsonify({"valid": True})

    return jsonify({"valid": False})

# IMPORTANT for Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
