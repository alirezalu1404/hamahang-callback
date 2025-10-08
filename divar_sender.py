import json
import requests

# فایل خروجی مرحله‌ی notifier
INPUT_FILE = "notification_message.txt"

# آدرس API چت دیوار
CHAT_API = "https://api.divar.ir/v1/chat/send_message/"

# توکن دسترسی هماهنگ (فعلاً در secrets نگهداری می‌شود)
ACCESS_TOKEN = "${{ secrets.ACCESS_TOKEN }}"

def send_message_to_divar(text):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "chat_id": "USER_CHAT_ID",   # موقت تا بعداً به‌صورت خودکار گرفته شود
        "message": {"text": text}
    }
    try:
        res = requests.post(CHAT_API, headers=headers, json=payload)
        print("📨 ارسال شد:", res.status_code)
        print(res.text)
    except Exception as e:
        print("⚠️ خطا در ارسال پیام:", e)

def main():
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print("⚠ فایل notification_message.txt پیدا نشد.")
        return
    send_message_to_divar(text)

if __name__ == "__main__":
    main()
