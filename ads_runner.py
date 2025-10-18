import json
import requests
from datetime import datetime

# مسیر فایل نشان‌ها (بوکمارک‌های کاربران)
BOOKMARK_FILE = "data/user_bookmarks.json"
OUTPUT_FILE = "data/ads_latest.json"

def fetch_ads(bookmark_url):
    """گرفتن آگهی‌ها از نشان کاربر"""
    try:
        response = requests.get(bookmark_url, timeout=15)
        if response.status_code == 200:
            # فقط لینک‌های آگهی را نگه می‌داریم
            data = response.text
            ads = []
            for part in data.split('"token"'):
                if "divar.ir/v/" in part:
                    start = part.find("https://divar.ir/v/")
                    end = part.find('"', start)
                    url = part[start:end]
                    if url and url not in ads:
                        ads.append(url)
            return ads
        else:
            print(f"⚠ خطا در دریافت ({response.status_code}) برای {bookmark_url}")
            return []
    except Exception as e:
        print(f"❌ خطا در اتصال به {bookmark_url}: {e}")
        return []

def main():
    """اجرای خودکار برای همه کاربران"""
    try:
        with open(BOOKMARK_FILE, "r", encoding="utf-8") as f:
            bookmarks = json.load(f)
    except FileNotFoundError:
        print("⚠ فایل user_bookmarks.json پیدا نشد.")
        return

    all_results = {}
    for user, data in bookmarks.items():
        print(f"👤 بررسی کاربر: {user}")
        ads = fetch_ads(data["url"])
        all_results[user] = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ads": ads[:10]  # فقط ۱۰ لینک اول ذخیره می‌شود
        }

    # ذخیره خروجی
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        json.dump(all_results, out, ensure_ascii=False, indent=2)
    print("✅ بررسی انجام شد و خروجی در ads_latest.json ذخیره گردید.")

if __name__ == "__main__":
    main()
