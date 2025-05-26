import threading
import time
import feedparser
import requests
from flask import Flask

BOT_TOKEN = "7239519330:AAFaVbAsE1V-jQ4wQN9-BGO4-dXluv1aus"
CHAT_ID = "-4665447944"
RSS_FEED_URLS = [
    "https://rss.app/feeds/UwEFld8FM84WyGkc.xml",
    "https://rss.app/feeds/ktIrhXzHl648lXd4.xml",
    "https://rss.app/feeds/5EZtkXHJhUIKZuJS.xml"
]

app = Flask(__name__)
sent_links = set()

def send_telegram_message(text, image_url=None):
    if image_url:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        payload = {
            "chat_id": CHAT_ID,
            "caption": text,
            "photo": image_url
        }
    else:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": text
        }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Error sending message:", e)

def extract_image(entry):
    try:
        if 'media_content' in entry:
            return entry.media_content[0]['url']
        elif 'enclosures' in entry and entry.enclosures:
            return entry.enclosures[0].href
        elif 'image' in entry:
            return entry.image.href
    except:
        return None
    return None

def check_rss():
    while True:
        for url in RSS_FEED_URLS:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                link = getattr(entry, "link", None)
                if link and link not in sent_links:
                    title = getattr(entry, "title", "بدون عنوان")
                    image = extract_image(entry)
                    message = f"{title}\n{link}"
                    send_telegram_message(message, image)
                    sent_links.add(link)
        time.sleep(60)

@app.route('/')
def home():
    return "Bot is running!"

if __name__ == '__main__':
    threading.Thread(target=check_rss, daemon=True).start()
    app.run(host="0.0.0.0", port=10000)
