# oauth_receiver.py
from flask import Flask, request, jsonify
import requests
import json
import os

app = Flask(__name__)

# ⚙️ اطلاعات اپلیکیشن در کنار دیوار
CLIENT_ID = "bloom-pine-jester"   # شناسه اپلیکیشن (slug)
CLIENT_SECRET = os.getenv("DIVAR_CLIENT_SECRET")  # خواندن از GitHub Secret
REDIRECT_URI = "https://alirezalu1404.github.io/hamahang-callback/index.html"

TOKEN_FILE = "data/divar_token.json"

@app.route("/callback")
def oauth_callback():
    code = request.args.get("code")
    state = request.args.get("state")

    if not code:
        return jsonify({"error": "Missing authorization code"}), 400

    # 🎯 تبادل code با access_token
    token_url = "https://api.divar.ir/oauth/token"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(token_url, json=payload, headers=headers)

    if response.status_code == 200:
        token_data = response.json()

        # ذخیره توکن در پوشه data
        os.makedirs("data", exist_ok=True)
        with open(TOKEN_FILE, "w", encoding="utf-8") as f:
            json.dump(token_data, f, indent=2, ensure_ascii=False)

        return jsonify({
            "message": "✅ OAuth access token received successfully!",
            "token": token_data
        })
    else:
        return jsonify({
            "error": "Failed to get token",
            "status_code": response.status_code,
            "response": response.text
        }), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
