import requests

bot_token = '7239519330:AAFaVbAsE1V-jQX4wQN9-BGO4-dXluv1aus'
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
