import time
import feedparser
import requests

# === تنظیمات اصلی ===
BOT_TOKEN = "7239519330:AAFaVbAsE1V-jQ4wQN9-BGO4-dXluv1aus"
CHAT_ID = "-4665447944"  # آی‌دی گروه
RSS_FEED_URLS = [
    "https://rss.app/feeds/UwEFld8FM84WyGkc.xml",
    "https://rss.app/feeds/ktIrhXzHl648lXd4.xml",
    "https://rss.app/feeds/5EZtkXHJhUIKZuJS.xml"
]
CHECK_INTERVAL = 30  # فاصله زمانی چک کردن (ثانیه)

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

# اجرای بررسی فیدها در یک Thread جداگانه
def check_feeds():
    while True:
        print("====== بررسی RSS ها شروع شد ======")

        for feed_url in RSS_FEED_URLS:
            print(f"بررسی: {feed_url}")
            feed = feedparser.parse(feed_url)

            for entry in feed.entries:
                link = entry.link
                title = entry.title

                media = entry.get("media_content")
                if media and isinstance(media, list) and "url" in media[0]:
                    image_url = media[0]["url"]
                else:
                    image_url = None

                if link not in sent_posts:
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

# اگر از render یا replit استفاده می‌کنی و نیاز به پورت باز داری:
from threading import Thread
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'RSS Bot is running!'

# اجرای دو بخش:
if __name__ == "__main__":
    # اجرای بررسی RSS‌ها
    Thread(target=check_feeds).start()
    
    # اجرای وب سرور (برای زنده موندن در هاست‌های رایگان)
    app.run(host="0.0.0.0", port=10000)
