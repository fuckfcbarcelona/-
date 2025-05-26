import time
import threading
import feedparser
import requests
from flask import Flask

# === تنظیمات اصلی ===
BOT_TOKEN = "7239519330:AAFaVbAsE1V-jQ4wQN9-BGO4-dXluv1aus"
CHAT_ID = "-4665447944"
RSS_FEED_URLS = [
    "https://rss.app/feeds/UwEFld8FM84WyGkc.xml"
    "https://rss.app/feeds/ktIrhXzHl648lXd4.xml"
    "https://rss.app/feeds/5EZtkXHJhUIKZuJS.xml"
]
CHECK_INTERVAL = 30  # ثانیه

# === پست‌های ارسال‌شده ===
sent_posts = set()

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, data=payload)

def send_photo(chat_id, photo_url, caption):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    payload = {"chat_id": chat_id, "photo": photo_url, "caption": caption}
    requests.post(url, data=payload)

def check_feeds():
    while True:
        print("====== بررسی RSS ها شروع شد ======")
        for feed_url in FEEDS:
            try:
                print(f"بررسی: {feed_url}")
                feed = feedparser.parse(feed_url)
                # بررسی پست‌های جدید و ارسال پیام...
            except Exception as e:
                print(f"خطا در بررسی {feed_url}: {e}")
        time.sleep(CHECK_INTERVAL)

        for feed_url in RSS_FEED_URLS:
            print(f"بررسی: {feed_url}")
            feed = feedparser.parse(feed_url)

            for entry in feed.entries:
                link = entry.get("link")
                title = entry.get("title", "بدون عنوان")
                image_url = entry.get("media_content", [{}])[0].get("url")

                if link and link not in sent_posts:
                    print(f"ارسال پست جدید: {title}")

                    if image_url:
                        caption = f"{title}\n\n{link}"
                        send_photo(CHAT_ID, image_url, caption)
                    else:
                        message = f"{title}\n\n{link}"
                        send_message(CHAT_ID, message)

                    sent_posts.add(link)

        print(f"[+] منتظر {CHECK_INTERVAL} ثانیه بعدی...\n")
        time.sleep(CHECK_INTERVAL)

# اجرای موازی فیدخوان
threading.Thread(target=check_feeds, daemon=True).start()

# وب‌سرور ساده برای زنده نگه‌داشتن رندر
app = Flask(name)

@app.route('/')
def home():
    return 'Bot is running.'

if name == 'main':
    app.run(host='0.0.0.0', port=10000)
def check_feeds():
    while True:
        print("====== بررسی RSS ها شروع شد ======")
        for feed_url in RSS_FEED_URLS:
            print(f"بررسی: {feed_url}")
            feed = feedparser.parse(feed_url)

            new_entries = [entry for entry in feed.entries if entry.get("link") not in sent_posts]

            for entry in new_entries[:10]:  # محدود به ۱۰ پست
                link = entry.get("link")
                title = entry.get("title", "بدون عنوان")
                image_url = entry.get("media_content", [{}])[0].get("url")

                print(f"ارسال پست جدید: {title}")

                if image_url:
                    caption = f"{title}\n\n{link}"
                    send_photo(CHAT_ID, image_url, caption)
                else:
                    message = f"{title}\n\n{link}"
                    send_message(CHAT_ID, message)

                sent_posts.add(link)
                time.sleep(2)  # تأخیر ۲ ثانیه‌ای بین پست‌ها

        print(f"[+] منتظر {CHECK_INTERVAL} ثانیه...\n")
        time.sleep(CHECK_INTERVAL)

# اجرای موازی فیدخوان
threading.Thread(target=check_feeds, daemon=True).start()

# وب‌سرور ساده برای زنده نگه‌داشتن پروژه در Render یا Pydroid
app = Flask(__name__)

@app.route('/')
def home():
    return 'Bot is running.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
def check_feeds():
    while True:
        print("====== بررسی RSS ها شروع شد ======")
        for feed_url in FEEDS:
            try:
                print(f"بررسی: {feed_url}")
                feed = feedparser.parse(feed_url)
                # بررسی پست‌های جدید و ارسال پیام...
            except Exception as e:
                print(f"خطا در بررسی {feed_url}: {e}")
        time.sleep(CHECK_INTERVAL)
git add .
git commit -m "Update feeds and bot config"
git push origin main
