import json, time, datetime, requests

def load_users():
    with open("data/user_bookmarks.json", "r", encoding="utf-8") as f:
        return json.load(f)

def fetch_ads(url):
    try:
        r = requests.get(url, timeout=10)
        return {"url": url, "status": r.status_code}
    except Exception as e:
        return {"url": url, "error": str(e)}

def main():
    data = load_users()
    fetch_interval = data["settings"]["fetch_interval_minutes"]
    print(f"Starting Hamahang fetch loop every {fetch_interval} min")

    while True:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        for user in data["users"]:
            for bm in user["bookmarks"]:
                result = fetch_ads(bm)
                print(f"[{now}] {user['username']} → {result}")
        time.sleep(fetch_interval * 60)

if __name__ == "__main__":
    main()
