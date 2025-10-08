import json
import re
from datetime import datetime
import os

BOOKMARKS_FILE = "data/user_bookmarks.json"

def validate_divar_url(url: str) -> bool:
    """
    بررسی می‌کند که لینک از دیوار است و ساختار جستجو دارد
    """
    pattern = r"^https://divar\.ir/s/[a-z]+/.+"
    return bool(re.match(pattern, url.strip()))

def add_bookmark(user_id: str, url: str):
    """
    افزودن نشان کاربر به فایل bookmarks
    """
    if not validate_divar_url(url):
        print("❌ لینک معتبر دیوار نیست.")
        return

    # اگر فایل وجود ندارد، ایجادش می‌کنیم
    if not os.path.exists(BOOKMARKS_FILE):
        os.makedirs(os.path.dirname(BOOKMARKS_FILE), exist_ok=True)
        with open(BOOKMARKS_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f, ensure_ascii=False, indent=2)

    # خواندن فایل موجود
    with open(BOOKMARKS_FILE, "r", encoding="utf-8") as f:
        bookmarks = json.load(f)

    # افزودن نشان جدید یا بروزرسانی
    bookmarks[user_id] = {
        "url": url.strip(),
        "added_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # ذخیره فایل
    with open(BOOKMARKS_FILE, "w", encoding="utf-8") as f:
        json.dump(bookmarks, f, ensure_ascii=False, indent=2)

    print(f"✅ نشان جدید برای کاربر «{user_id}» ذخیره شد.")
    print(f"🔗 {url}")

def main():
    print("📥 دریافت نشان از کاربر (خریدار)")
    user_id = input("🧑 شناسه کاربر را وارد کنید: ").strip()
    user_url = input("🔗 لینک نشان ذخیره‌شده در دیوار را وارد کنید: ").strip()

    add_bookmark(user_id, user_url)

if __name__ == "__main__":
    main()
