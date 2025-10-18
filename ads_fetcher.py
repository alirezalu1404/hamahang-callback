import requests, json, time, datetime

DATA_FILE = "ads_log.json"
CHECK_INTERVAL = 900  # 15 دقیقه (قابل تغییر توسط مدیر افزونه)

def fetch_ads(search_url):
    try:
        r = requests.get(search_url, timeout=10)
        if r.status_code != 200:
            return []
        # در نسخه نهایی لینک‌های واقعی از HTML استخراج می‌شوند
        links = [f"{search_url}?ad={i}" for i in range(5)]
        return links
    except Exception as e:
        print("⚠️ خطا در دریافت آگهی‌ها:", e)
        return []

def save_to_json(links):
    ts = datetime.datetime.now().isoformat()
    record = {"timestamp": ts, "ads": links}
    try:
        with open(DATA_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        print(f"✅ {len(links)} آگهی در زمان {ts} ذخیره شد.")
    except Exception as e:
        print("⚠️ خطا در ذخیره‌سازی:", e)

if __name__ == "__main__":
    search_url = input("https://divar.ir/s/tehran/buy-apartment/zafar?districts=74%2C86").strip()
    while True:
        ads = fetch_ads(search_url)
        if ads:
            save_to_json(ads)
        time.sleep(CHECK_INTERVAL)
