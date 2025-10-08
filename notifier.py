import json
from datetime import datetime, timedelta
import jdatetime

INPUT_FILE = "ads_latest.json"      # خروجی ads_runner.py
USER_FILE = "data/user_bookmarks.json"  # اطلاعات کاربران و بازه ارسال
OUTPUT_FILE = "notification_message.txt"  # خروجی نهایی برای ارسال

def generate_message(user, ads):
    date_shamsi = jdatetime.datetime.now().strftime("%Y/%m/%d %H:%M")
    lines = [f"📢 به‌روزرسانی آگهی‌های جدید برای نشان شما ({user}) — {date_shamsi}\n"]
    for ad in ads:
        title = ad.get("title", "بدون عنوان")
        url = ad.get("url", "#")
        lines.append(f"🔸 {title}\n🔗 {url}\n")
    lines.append("—" * 40 + "\n")
    return "\n".join(lines)

def main():
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            ads_data = json.load(f)
    except FileNotFoundError:
        print("⚠ فایل ads_latest.json پیدا نشد. ابتدا ads_runner را اجرا کنید.")
        return

    try:
        with open(USER_FILE, "r", encoding="utf-8") as uf:
            users = json.load(uf)
    except FileNotFoundError:
        print("⚠ فایل user_bookmarks.json پیدا نشد.")
        return

    all_messages = []
    for user, info in users.items():
        notify_interval = info.get("notify_interval", 60)  # پیش‌فرض: 60 دقیقه
        ads = ads_data.get(user, {}).get("ads", [])
        if ads:
            message = generate_message(user, ads)
            all_messages.append(message)

    if not all_messages:
        print("ℹ️ آگهی جدیدی برای ارسال وجود ندارد.")
        return

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write("\n".join(all_messages))

    print("✅ پیام‌ها آماده و در notification_message.txt ذخیره شدند.")

if __name__ == "__main__":
    main()
