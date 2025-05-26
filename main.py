from flask import Flask
import feedparser
import time
import threading
import requests
import logging

# ---------- تنظیمات ----------
TELEGRAM_TOKEN = '7239519330:AAFaVbAsE1V-jQX4wQN9-BGO4-dXluv1aus'
CHAT_ID = '7757886535'
RSS_FEED_URL = 'https://example.com/rss.xml'
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
            files = {'photo': requests.get(image_url).content}
            response = requests.post(f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto', data=data, files={'photo': files['photo']})
        else:
            text = f'<b>{title}</b>\n{link}'
            response = requests.post(f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage', data={
                'chat_id': CHAT_ID,
                'text': text,
                'parse_mode': 'HTML'
            })

        logging.info(f'پیام ارسال شد: {title} | Status: {response.status_code}')
    except Exception as e:
        logging.error(f'خطا در ارسال پیام: {e}')

# ---------- بررسی فید ----------
def check_feed():
    global sent_entries
    while True:
        try:
            feed = feedparser.parse(RSS_FEED_URL)
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

            logging.info('فید بررسی شد.')

        except Exception as e:
            logging.error(f'خطا در بررسی فید: {e}')

        time.sleep(CHECK_INTERVAL)

# ---------- اجرای Flask ----------
app = Flask(__name__)

@app.route('/')
def home():
    return 'ربات فید RSS در حال اجراست.'

# ---------- شروع Thread پس‌زمینه ----------
if __name__ == '__main__':
    threading.Thread(target=check_feed, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
