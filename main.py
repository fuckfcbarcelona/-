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
CHECK_INTERVAL = 30  # هر چند ثانیه یک بار بررسی شود

sent_entries = set()

# ---------- تنظیم لاگر ----------
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s'
)

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
    while True:
        try:
            for url in RSS_FEED_URLS:
                feed = feedparser.parse(url)
                for entry in reversed(feed.entries):
                    entry_id = entry.get('id') or entry.get('link')
                    if entry_id not in sent_entries:
                        title = entry.title
                        link = entry.link
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
    port = int(os.environ.get('PORT', 5000))  # مخصوص Render
    app.run(host='0.0.0.0', port=port)
