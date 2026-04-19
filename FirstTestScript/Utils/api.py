from flask import Flask, request, jsonify
import secrets
import time, json, os

sessions = {}

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

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    admin = data.get("admin")

    if admin != "YOUR_SECRET_PASSWORD":
        return jsonify({"error": "unauthorized"}), 403

    import random, string, time

    key = '-'.join(
        ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
        for _ in range(4)
    )

    db = load_db()

    db[key] = {
        "expires": int(time.time() + 86400),
        "activated": False,
        "userId": None
    }

    save_db(db)

    return jsonify({"key": key})

@app.route("/create-session", methods=["POST"])
def create_session():
    data = request.json
    key = data.get("key")
    userId = data.get("userId")

    db = load_db()

    if key not in db:
        return jsonify({"valid": False}), 403

    entry = db[key]

    if time.time() > entry["expires"]:
        return jsonify({"valid": False}), 403

    import secrets
    token = secrets.token_hex(16)

    # session expires when key expires OR 1 hour max
    session_expiry = min(
        time.time() + 3600,
        entry["expires"]
    )

    sessions[token] = {
        "userId": userId,
        "expires": session_expiry
    }

    return jsonify({
        "valid": True,
        "token": token,
        "expires": session_expiry
    })

@app.route("/validate", methods=["POST"])
def validate():
    try:
        data = request.json
        key = data.get("key")
        userId = data.get("userId")

        db = load_db()

        # key does not exist
        if key not in db:
            return jsonify({"valid": False})

        entry = db[key]

        # expired check
        if time.time() > entry["expires"]:
            return jsonify({"valid": False})

        # first activation
        if not entry.get("activated", False):
            entry["activated"] = True
            entry["userId"] = userId
            save_db(db)
            return jsonify({"valid": True})

        # same user allowed
        if entry.get("userId") == userId:
            return jsonify({"valid": True})

        return jsonify({"valid": False})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"valid": False})

@app.route("/validate-session", methods=["POST"])
def validate_session():
    data = request.json
    token = data.get("token")
    userId = data.get("userId")

    if token not in sessions:
        return jsonify({"valid": False})

    session = sessions[token]

    if time.time() > session["expires"]:
        return jsonify({"valid": False})

    if session["userId"] != userId:
        return jsonify({"valid": False})

    return jsonify({"valid": True})

# IMPORTANT for Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
