import json
import re
from datetime import datetime
import os

BOOKMARK_FILE = "data/user_bookmarks.json"

def save_bookmark(user_id, url):
    """ذخیره لینک نشان کاربر در فایل JSON"""
    try:
        with open(BOOKMARK_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    data[user_id] = {
        "url": url,
        "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    os.makedirs("data", exist_ok=True)
    with open(BOOKMARK_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ لینک نشان کاربر {user_id} ذخیره شد.")


def main():
    event_path = os.getenv("GITHUB_EVENT_PATH")
    if not event_path or not os.path.exists(event_path):
        print("⚠ هیچ event واقعی دریافت نشد.")
        return

    with open(event_path, "r") as f:
        event = json.load(f)

    payload = event.get("client_payload", {})
    user_id = payload.get("sender_id")
    text = payload.get("text", "")

    pattern = re.compile(r"https:\/\/divar\.ir\/s\/[^\s]+")

    match = pattern.search(text)
    if match:
        url = match.group(0)
        save_bookmark(user_id, url)
        print(f"✅ نشان جدید کاربر {user_id} ثبت شد: {url}")
    else:
        print(f"⚠ لینک معتبری در پیام کاربر {user_id} یافت نشد.")


if __name__ == "__main__":
    main()
