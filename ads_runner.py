import requests
import json
from datetime import datetime
import os

BOOKMARK_FILE = "data/user_bookmarks.json"   # محل ذخیره آدرس نشان کاربران
OUTPUT_FILE = "ads_latest.json"              # خروجی نهایی

def fetch_ads(url):
    """دریافت لیست آگهی‌ها از آدرس نشان"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        html = response.text

        # استخراج لینک آگهی‌ها از HTML (با فیلتر divar.ir)
        ads = []
        for part in html.split('"'):
            if part.startswith("https://divar.ir/v/") and part not in ads:
                ads.append({"url": part, "title": "آگهی جدید"})

        print(f"✅ {len(ads)} آگهی از {url} یافت شد.")
        return ads

    except Exception as e:
        print(f"⚠ خطا در دریافت آگهی‌ها از {url}: {e}")
        return []

def main():
    # بررسی وجود فایل نشان‌ها
    if not os.path.exists(BOOKMARK_FILE):
        print(f"⚠ فایل {BOOKMARK_FILE} پیدا نشد.")
        return

    # خواندن نشان‌های کاربران
    with open(BOOKMARK_FILE, "r", encoding="utf-8") as f:
        bookmarks = json.load(f)

    all_results = {}
    for user, data in bookmarks.items():
        url = data.get("url")
        if not url:
            print(f"⚠ برای {user} هیچ URL ثبت نشده است.")
            continue

        print(f"👤 بررسی کاربر: {user}")
        ads = fetch_ads(url)
        all_results[user] = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ads": ads[:10]  # فقط ۱۰ آگهی اول ذخیره می‌شود
        }

    # ذخیره خروجی در مسیر اصلی ریپازیتوری
    output_path = os.path.join(os.getcwd(), OUTPUT_FILE)
    with open(output_path, "w", encoding="utf-8") as out:
        json.dump(all_results, out, ensure_ascii=False, indent=2)

    print(f"✅ بررسی انجام شد و خروجی در {output_path} ذخیره گردید.")

if __name__ == "__main__":
    main()
