import os
import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# 🔐 از Secrets گیت‌هاب برای امنیت
GITHUB_TOKEN = os.environ.get("ACCESS_TOKEN")
REPO = "alirezalu1404/hamahang-callback"

@app.route("/", methods=["POST"])
def handle_event():
    """دریافت پیام از Kenar و ارسال آن به GitHub Dispatch"""
    try:
        payload = request.get_json()
        print("📩 دریافت از Kenar:", payload)

        event_type = "kenar_message_created"
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {GITHUB_TOKEN}",
        }

        data = {
            "event_type": event_type,
            "client_payload": payload,
        }

        response = requests.post(
            f"https://api.github.com/repos/{REPO}/dispatches",
            headers=headers,
            data=json.dumps(data),
        )

        if response.status_code == 204:
            print("✅ پیام به GitHub ارسال شد.")
            return jsonify({"status": "success"}), 200
        else:
            print("❌ خطا در ارسال:", response.text)
            return jsonify({"status": "error", "response": response.text}), 400

    except Exception as e:
        print("⚠️ خطای داخلی:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
