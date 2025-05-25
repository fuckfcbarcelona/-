import feedparser
import requests
import time

# تنظیمات اصلی
RSS_FEED_URLS = [
    "https://rss.app/feeds/UwEFld8FM84WyGkc.xml",
    "https://rss.app/feeds/ktIrhXzHl648lXd4.xml",
    "https://rss.app/feeds/5EZtkXHJhUIKZuJS.xml"
]  # ← آدرس فید RSS رو اینجا بذار
TELEGRAM_TOKEN = "YOUR_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"

last_sent_link = None

def get_latest_post():
    feed = feedparser.parse(RSS_FEED_URL)
    if not feed.entries:
        return None
    return feed.entries[0]

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    requests.post(url, data=data)

while True:
    latest = get_latest_post()
    if latest and latest.link != last_sent_link:
        message = f"<b>{latest.title}</b>\n{latest.link}"
        send_to_telegram(message)
        last_sent_link = latest.link
    time.sleep(30)  
