# kenar_receiver.py
from flask import Flask, request, jsonify
import requests, os, json

app = Flask(__name__)

# 📌 Secrets خوانده‌شده از GitHub
DIVAR_SECRET = os.getenv("DIVAR_SECRET", "")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", "")

GITHUB_DISPATCH_URL = "https://api.github.com/repos/alirezalu1404/hamahang-callback/dispatches"

@app.route("/events/bloom-pine-jester", methods=["POST"])
def handle_event():
    """دریافت رویدادهای کنار دیوار و ارسال به GitHub Dispatch"""
    
    auth_header = request.headers.get("Authorization", "")
    if not auth_header or DIVAR_SECRET not in auth_header:
        print("❌ Unauthorized request.")
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json(silent=True) or {}
    print("📩 Event received:", json.dumps(data, ensure_ascii=False, indent=2))

    text = data.get("text", "")
    sender_id = data.get("sender_id", "unknown")

    if "divar.ir" in text:
        payload = {
            "event_type": "kenar_message_created",
            "client_payload": {"sender_id": sender_id, "text": text}
        }

        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }

        print("🚀 Dispatching to GitHub...")
        r = requests.post(GITHUB_DISPATCH_URL, json=payload, headers=headers)
        print("📤 Status:", r.status_code, r.text)

        if r.status_code in (200, 204):
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"error": "GitHub dispatch failed", "response": r.text}), 422

    return jsonify({"status": "ignored"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
