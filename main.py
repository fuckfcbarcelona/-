import time
import requests
import feedparser
from flask import Flask

# تنظیمات
BOT_TOKEN = "7239519330:AAFaVbAsE1V-jQ4wQN9-BGO4-dXluv1aus"
CHAT_ID = "-4665447944"
RSS_FEED_URLS = [
    "https://rss.app/feeds/UwEFld8FM84WyGkc.xml",
    "https://rss.app/feeds/ktIrhXzHl648lXd4.xml",
    "https://rss.app/feeds/5EZtkXHJhUIKZuJS.xml"
]

# ذخیره لینک خبرهای ارسال شده
sent_links = set()

# تابع ارسال پیام به تلگرام
def send_to_telegram(title, link, image_url=None):
    message = f"<b>{title}</b>\n<a href='{link}'>مطالعه خبر</a>"
    
    if image_url:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        data = {
            "chat_id": CHAT_ID,
            "caption": message,
            "photo": image_url,
            "parse_mode": "HTML"
        }
    else:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }

    try:
        r = requests.post(url, data=data, timeout=10)
        print("ارسال پست:", title)
    except Exception as e:
        print(f"خطا در ارسال پیام: {e}")

# تابع بررسی فیدها
def check_feeds():
    for feed_url in RSS_FEED_URLS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            title = getattr(entry, "title", "بدون عنوان")
            link = getattr(entry, "link", None)
            if not link:
                continue

            image_url = None
            if "media_content" in entry:
                media = entry.media_content
                if media and "url" in media[0] and media[0]["url"]:
                    image_url = media[0]["url"]
            elif "image" in entry and entry.image:
                image_url = entry.image

            if link not in sent_links:
                send_to_telegram(title, link, image_url)
                sent_links.add(link)

# اجرای دائم
app = Flask(__name__)

@app.route('/')
def home():
    return "RSS to Telegram bot is running!"

def run_bot_loop():
    while True:
        check_feeds()
        time.sleep(30)

if __name__ == "__main__":
    import threading
    threading.Thread(target=run_bot_loop).start()
    app.run(host="0.0.0.0", port=10000)
