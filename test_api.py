import os
import requests

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

def main():
    print("🚀 Starting Hamahang API test...")

    if not ACCESS_TOKEN:
        print("❌ No access token found. Please set it in GitHub Secrets.")
        return

    url = "https://kenar.divar.dev/oauth/get_user"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

    try:
        response = requests.get(url, headers=headers)
        print(f"✅ Status Code: {response.status_code}")
        print("Response:")
        print(response.text[:500])
    except Exception as e:
        print("❌ Error:", e)

if __name__ == "__main__":
    main()
