import time
import feedparser
import requests

# === تنظیمات اصلی ===
BOT_TOKEN = "7239519330:AAFaVbAsE1V-jQX4wQN9-BGO4-dXluv1aus"
CHAT_ID = "-4665447944"  # آی‌دی گروه
RSS_FEED_URLS = [
    "https://rss.app/feeds/UwEFld8FM84WyGkc.xml",
    "https://rss.app/feeds/ktIrhXzHl648lXd4.xml",
    "https://rss.app/feeds/5EZtkXHJhUIKZuJS.xml"
]
CHECK_INTERVAL = 30  # ثانیه بین هر چک

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

while True:
    print("====== بررسی RSS ها شروع شد ======")

    for feed_url in RSS_FEED_URLS:
        print(f"بررسی: {feed_url}")
        feed = feedparser.parse(feed_url)

        for entry in feed.entries:
            link = entry.link
            title = entry.title
            image_url = entry.get("media_content", [{}])[0].get("url")

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
