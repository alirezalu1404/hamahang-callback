import os
import json
import requests
import jdatetime

# ===== تنظیمات پایه =====
MESSAGE_FILE = "notification_message.txt"   # خروجی تولیدشده از notifier.py
DIVAR_CHAT_API = "https://kenar.divar.dev/chat/send_message"  # مسیر ارسال پیام به چت دیوار
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")    # توکن از GitHub Secrets خوانده می‌شود
BOOKMARK_FILE = "data/user_bookmarks.json"  # فایل نشان‌های کاربران


# ===== بخش 1: خواندن پیام =====
def load_message():
    """خواندن پیام آماده ارسال از فایل"""
    if not os.path.exists(MESSAGE_FILE):
        print("⚠ فایل پیام پیدا نشد. ابتدا notifier.py را اجرا کنید.")
        return None
    with open(MESSAGE_FILE, "r", encoding="utf-8") as f:
        return f.read().strip()


# ===== بخش 2: ارسال پیام به چت دیوار =====
def send_to_divar_chat(message: str, chat_id: str):
    """ارسال پیام به چت دیوار با استفاده از API کنار"""
    if not ACCESS_TOKEN:
        print("⚠ ACCESS_TOKEN در GitHub Secrets تنظیم نشده است.")
        return False

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "chat_id": chat_id,
        "message": message,
    }

    try:
        response = requests.post(DIVAR_CHAT_API, json=payload, headers=headers)
        if response.status_code == 200:
            print(f"✅ پیام با موفقیت به چت {chat_id} ارسال شد.")
            return True
        else:
            print(f"❌ خطا در ارسال پیام ({chat_id}): {response.status_code} — {response.text}")
            return False
    except Exception as e:
        print(f"⚠ خطا در اتصال به API دیوار: {e}")
        return False


# ===== بخش 3: اجرای خودکار برای همه کاربران =====
def main():
    message = load_message()
    if not message:
        return

    if not os.path.exists(BOOKMARK_FILE):
        print("⚠ فایل user_bookmarks.json پیدا نشد.")
        return

    with open(BOOKMARK_FILE, "r", encoding="utf-8") as f:
        users = json.load(f)

    for user, info in users.items():
        chat_id = info.get("chat_id")
        if not chat_id:
            print(f"⚠ کاربر {user} شناسه چت ندارد، پیام ارسال نشد.")
            continue

        print(f"📨 در حال ارسال پیام برای کاربر {user} ...")
        send_to_divar_chat(message, chat_id)

    print(f"\n✅ تمام پیام‌ها در {jdatetime.datetime.now().strftime('%Y/%m/%d %H:%M')} بررسی شدند.")


if __name__ == "__main__":
    main()
