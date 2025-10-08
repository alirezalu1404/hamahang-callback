import json
from datetime import datetime
import jdatetime

INPUT_FILE = "ads_latest.json"   # خروجی ads_runner.py
OUTPUT_FILE = "notification_message.txt"  # فایل آماده برای ارسال

def generate_message(data):
    lines = []
    for user, info in data.items():
        ads = info.get("ads", [])
        if not ads:
            continue

        # عنوان و زمان
        date_shamsi = jdatetime.datetime.now().strftime("%Y/%m/%d %H:%M")
        header = f"📢 به‌روزرسانی آگهی‌های جدید برای نشان شما ({user}) — {date_shamsi}\n"
        lines.append(header)

        # فهرست آگهی‌ها
        for ad in ads:
            title = ad.get("title", "بدون عنوان")
            url = ad.get("url", "#")
            lines.append(f"🔸 {title}\n🔗 {url}\n")

        # جداکننده بین کاربران
        lines.append("—" * 40 + "\n")

    return "\n".join(lines)

def main():
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("⚠ فایل ads_latest.json پیدا نشد. ابتدا ads_runner را اجرا کنید.")
        return

    message = generate_message(data)

    # ذخیره پیام آماده ارسال
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write(message)

    print("✅ پیام آماده ارسال برای کاربران در فایل notification_message.txt ذخیره شد.")

if __name__ == "__main__":
    main()
