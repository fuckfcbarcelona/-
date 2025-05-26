import time
import threading
import feedparser
import requests
from flask import Flask

# === تنظیمات اصلی ===
BOT_TOKEN = "7239519330:AAFaVbAsE1V-jQ4wQN9-BGO4-dXluv1aus"
CHAT_ID = "-4665447944"
RSS_FEED_URLS = [
    "https://rss.app/feeds/UwEFld8FM84WyGkc.xml",
    "https://rss.app/feeds/ktIrhXzHl648lXd4.xml",
    "https://rss.app/feeds/5EZtkXHJhUIKZuJS.xml"
]
CHECK_INTERVAL = 30  # ثانیه

app = Flask(__name__)
sent_links = set()

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=data)

def check_rss():
    while True:
        for feed_url in RSS_FEED_URLS:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries:
                if entry.link not in sent_links:
                    message = f"{entry.title}\n{entry.link}"
                    send_to_telegram(message)
                    sent_links.add(entry.link)
        time.sleep(CHECK_INTERVAL)

@app.route('/')
def index():
    return "RSS to Telegram bot is running."

if __name__ == '__main__':
    threading.Thread(target=check_rss, daemon=True).start()
    app.run(host='0.0.0.0', port=10000)
