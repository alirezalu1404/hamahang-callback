import json, re, os
from datetime import datetime

BOOKMARK_FILE = "data/user_bookmarks.json"

def save_bookmark(user_id, url):
    try:
        with open(BOOKMARK_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    data[user_id] = {"url": url, "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    os.makedirs("data", exist_ok=True)
    with open(BOOKMARK_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    p = os.getenv("GITHUB_EVENT_PATH")
    if not p or not os.path.exists(p):
        print("no_event")
        return
    with open(p, "r", encoding="utf-8") as f:
        ev = json.load(f)
    if "event_type" not in ev:
        ev = {"event_type": "kenar_message_created", "client_payload": ev}
    payload = ev.get("client_payload", {})
    user_id = payload.get("sender_id", "user_unknown")
    blob = json.dumps(payload, ensure_ascii=False)
    m = re.search(r"https:\/\/divar\.ir\/s\/[^\s\"']+", blob)
    if not m:
        print("no_url")
        return
    url = m.group(0)
    save_bookmark(user_id, url)
    print("saved")

if __name__ == "__main__":
    main()
