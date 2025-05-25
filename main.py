import feedparser
import time
import requests

# لینک‌های RSS
RSS_FEED_URLS = [
    "https://rss.app/feeds/UwEFld8FM84WyGkc.xml",
    "https://rss.app/feeds/ktIrhXzHl648lXd4.xml",
    "https://rss.app/feeds/5EZtkXHJhUIKZuJS.xml"
]

# توکن ربات تلگرام
TELEGRAM_BOT_TOKEN = "7239519330:AAFaVbAsE1V-jQX4wQN9-BGO4-dXluv1aus"

# آی‌دی عددی گروه تلگرام
TELEGRAM_CHAT_ID = -4665447944

# ذخیره پست‌های ارسال‌شده
sent_links = set()

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "disable_web_page_preview": False
    }
    requests.post(url, data=data)

while True:
    for feed_url in RSS_FEED_URLS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            link = entry.link
            if link not in sent_links:
                sent_links.add(link)
                message = f"{entry.title}\n{link}"
                send_to_telegram(message)
    time.sleep(30)
