import json
import re
from datetime import datetime

DATA_FILE = "data/user_bookmarks.json"

def load_bookmarks():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_bookmarks(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def extract_divar_link(message):
    """یافتن لینک معتبر دیوار از متن پیام"""
    pattern = r"(https:\/\/divar\.ir\/s\/[^\s]+)"
    match = re.search(pattern, message)
    return match.group(1) if match else None

def simulate_chat_messages():
    """شبیه‌سازی پیام‌های کاربر از چت دیوار (در فاز بعدی از API چت خوانده می‌شود)"""
    return [
        {"user": "user1", "message": "سلام، این نشان من است: https://divar.ir/s/tehran/buy-apartment/mirdamad?bbox=51.420204%2C35.736675%2C51.44881%2C35.770737&floor=3-6&rooms=%D8%B3%D9%87"},
        {"user": "user2", "message": "https://divar.ir/s/tehran/rent-apartment/vanak"},
        {"user": "user3", "message": "سلام افزونه هماهنگ! 👋"}
    ]

def main():
    bookmarks = load_bookmarks()
    messages = simulate_chat_messages()
    new_links = 0

    for msg in messages:
        user = msg["user"]
        link = extract_divar_link(msg["message"])

        if link:
            if user not in bookmarks or bookmarks[user]["url"] != link:
                bookmarks[user] = {
                    "url": link,
                    "added_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                new_links += 1
                print(f"✅ لینک جدید برای {user} ثبت شد: {link}")
            else:
                print(f"ℹ️ لینک تکراری از {user} دریافت شد.")
        else:
            print(f"⚠️ هیچ لینک معتبری در پیام {user} یافت نشد.")

    if new_links > 0:
        save_bookmarks(bookmarks)
        print(f"📁 {new_links} لینک جدید در فایل user_bookmarks.json ذخیره شد.")
    else:
        print("ℹ️ هیچ لینک جدیدی شناسایی نشد.")

if __name__ == "__main__":
    main()
