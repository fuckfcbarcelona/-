import requests

bot_token = '8124991049:AAHW-FH8gBIR8fBn2jvJh2ww3tuBuGtdktA'
chat_id = '7757886535'
message = 'سلام! این یه تست از main.py هست.'

url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

payload = {
    'chat_id': chat_id,
    'text': message
}

response = requests.post(url, data=payload)

print(f"Status Code: {response.status_code}")
print(response.text)
