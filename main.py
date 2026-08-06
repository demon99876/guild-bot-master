import poller
import os
import json
import requests
from flask import Flask

app = Flask(__name__)

FONNTE_TOKEN = os.environ.get('FONNTE_TOKEN')
ADMIN = "6288225622133"
DATA_FILE = "data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"list": {}, "absen": []}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

def kirim_pesan(target, pesan):
    target = target.replace("@c.us", "").replace("@s.whatsapp.net", "")
    url = "https://api.fonnte.com/send"
    payload = {"target": target, "message": pesan}
    headers = {"Authorization": FONNTE_TOKEN}
    r = requests.post(url, data=payload, headers=headers)
    print("STATUS KIRIM:", r.status_code)

@app.route('/')
def home():
    return "Bot Jalan"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
