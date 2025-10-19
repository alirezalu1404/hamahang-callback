from flask import Flask, jsonify, request
import os
import requests

app = Flask(__name__)

# 🔐 خواندن کلید از Secrets گیت‌هاب
DIVAR_SERVICE_TOKEN = os.getenv("DIVAR_SERVICE_TOKEN")

@app.route("/")
def home():
    return jsonify({
        "message": "✅ Hamahang Service Connected to Divar",
        "note": "This app uses Service Token for secure access."
    })

@app.route("/test", methods=["GET"])
def test_connection():
    """تست ارتباط مستقیم با API دیوار"""
    url = "https://api.divar.ir/v1/public/search/post"
    headers = {
        "Authorization": f"Bearer {DIVAR_SERVICE_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json={"q": "تهران"}, headers=headers)
    return jsonify({
        "status_code": response.status_code,
        "text": response.text
    })

@app.route("/kenar", methods=["POST"])
def receive_event():
    """دریافت پیام از Kenar و پاسخ خودکار"""
    payload = request.get_json()
    print("📩 دریافت پیام از Kenar:", payload)
    return jsonify({"received": True, "payload": payload})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
