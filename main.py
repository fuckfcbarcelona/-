import feedparser
import time
import threading
import json
import os
import requests
from flask import Flask

# تنظیمات ربات
RSS_FEED_URL = 'https://rss.app/feeds/5EZtkXHJhUIKZuJS.xml'
TELEGRAM_BOT_TOKEN = 'توکن رباتت اینجا'
TELEGRAM_CHAT_ID = 'آیدی عددی یا @کانالت'

# فایل ذخیره‌ی شناسه‌ها
SENT_FILE = 'sent.json'

# Flask برای زنده نگه داشتن
app = Flask(__name__)

@app.route('/')
def index():
    return 'Bot is running'

# بارگذاری پست‌های ارسال‌شده قبلی
def load_sent_entries():
    if os.path.exists(SENT_FILE):
        with open(SENT_FILE, 'r') as f:
            return set(json.load(f))
    return set()

# ذخیره‌سازی پست‌های ارسال‌شده
def save_sent_entries(sent_entries):
    with open(SENT_FILE, 'w') as f:
        json.dump(list(sent_entries), f)

# چک کردن فید و ارسال پست‌های جدید
def check_feeds():
    sent_entries = load_sent_entries()
    while True:
        try:
            feed = feedparser.parse(RSS_FEED_URL)
            for entry in reversed(feed.entries):
                entry_id = entry.get('id', entry.get('link'))
                if entry_id and entry_id not in sent_entries:
                    title = entry.get('title', 'بدون عنوان')
                    message = f"ارسال پست جدید: {title}"
                    send_to_telegram(message)
                    sent_entries.add(entry_id)
                    save_sent_entries(sent_entries)
                    time.sleep(2)  # فاصله بین پیام‌ها برای جلوگیری از بن
            time.sleep(30)  # فاصله بین هر چک فید
        except Exception as e:
            print(f'خطا در چک کردن فید: {e}')
            time.sleep(60)

# ارسال به تلگرام
def send_to_telegram(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    data = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }
    requests.post(url, data=data)

# اجرای چک فید در ترد جدا
threading.Thread(target=check_feeds, daemon=True).start()

# اجرای Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
