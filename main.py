from flask import Flask
import feedparser
import time
import threading
import requests
import logging
import os

# ---------- تنظیمات ----------
TELEGRAM_TOKEN = '7239519330:AAFaVbAsE1V-jQX4wQN9-BGO4-dXluv1aus'
CHAT_ID = '7757886535'
RSS_FEED_URLS = [
    'https://rss.app/feeds/UwEFld8FM84WyGkc.xml',
    'https://rss.app/feeds/ktIrhXzHl648lXd4.xml',
    'https://rss.app/feeds/5EZtkXHJhUIKZuJS.xml',
]
CHECK_INTERVAL = 30  # هر چند ثانیه یک‌بار بررسی شود

SENT_FILE = 'sent.txt'
sent_entries = set()

# ---------- تنظیم لاگر ----------
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s'
)

# ---------- بارگذاری ارسال‌شده‌ها ----------
def load_sent_entries():
    if os.path.exists(SENT_FILE):
        with open(SENT_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                sent_entries.add(line.strip())

# ---------- ذخیره یک آی‌دی در فایل ----------
def save_sent_entry(entry_id):
    with open(SENT_FILE, 'a', encoding='utf-8') as f:
        f.write(entry_id + '\n')

# ---------- ارسال به تلگرام ----------
def send_to_telegram(title, link, image_url=None):
    try:
        if image_url:
            data = {
                'chat_id': CHAT_ID,
                'caption': f'<b>{title}</b>\n{link}',
                'parse_mode': 'HTML'
            }
            response = requests.post(
                f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto',
                data=data,
                files={'photo': requests.get(image_url).content}
            )
        else:
            text = f'<b>{title}</b>\n{link}'
            response = requests.post(
                f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage',
                data={'chat_id': CHAT_ID, 'text': text, 'parse_mode': 'HTML'}
            )

        logging.info(f'پیام ارسال شد: {title} | Status: {response.status_code}')
    except Exception as e:
        logging.error(f'خطا در ارسال پیام: {e}')

# ---------- بررسی فیدها ----------
def check_feed():
    global sent_entries
    load_sent_entries()
    while True:
        try:
            for url in RSS_FEED_URLS:
                feed = feedparser.parse(url)
                for entry in reversed(feed.entries):
                    entry_id = (entry.get('id') or entry.get('link') or '') + entry.get('title', '')
                    if not entry_id or entry_id in sent_entries:
                        continue

                    title = entry.get('title', 'بدون عنوان')
                    link = entry.get('link', '')
                    image_url = None

                    if 'media_content' in entry:
                        image_url = entry.media_content[0]['url']
                    elif 'links' in entry:
                        for l in entry.links:
                            if l.type.startswith('image'):
                                image_url = l.href
                                break

                    send_to_telegram(title, link, image_url)
                    sent_entries.add(entry_id)
                    save_sent_entry(entry_id)

            logging.info('فیدها بررسی شدند.')
        except Exception as e:
            logging.error(f'خطا در بررسی فید: {e}')

        time.sleep(CHECK_INTERVAL)

# ---------- اجرای Flask ----------
app = Flask(__name__)

@app.route('/')
def home():
    return 'ربات فید RSS در حال اجراست.'

# ---------- شروع Thread و اجرای برنامه ----------
if __name__ == '__main__':
    threading.Thread(target=check_feed, daemon=True).start()
    port = int(os.environ.get('PORT', 5000))  # مخصوص render.com
    app.run(host='0.0.0.0', port=port)
