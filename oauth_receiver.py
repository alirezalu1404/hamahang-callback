# oauth_receiver.py (auto-mode)
import requests
import json
import os

# تنظیمات اپلیکیشن در کنار دیوار
CLIENT_ID = "bloom-pine-jester"
CLIENT_SECRET = os.getenv("DIVAR_CLIENT_SECRET")  # خواندن از secret
REDIRECT_URI = "https://alirezalu1404.github.io/hamahang-callback/index.html"
TOKEN_FILE = "data/divar_token.json"

def fetch_token():
    token_url = "https://api.divar.ir/oauth/token"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials",
        "redirect_uri": REDIRECT_URI,
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(token_url, json=payload, headers=headers)

    if response.status_code == 200:
        token_data = response.json()
        os.makedirs("data", exist_ok=True)
        with open(TOKEN_FILE, "w", encoding="utf-8") as f:
            json.dump(token_data, f, indent=2, ensure_ascii=False)
        print("✅ Token fetched successfully")
        return token_data
    else:
        print("❌ Failed to fetch token:", response.status_code, response.text)
        return None


if __name__ == "__main__":
    fetch_token()
