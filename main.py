import os
import json
import requests
import time
from flask import Flask
from threading import Thread

app = Flask(__name__)

FONNTE_TOKEN = os.environ.get('FONNTE_TOKEN')
print("TOKEN TERBACA:", FONNTE_TOKEN)
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
    target = target.replace("@c.us", "")
    url = "https://api.fonnte.com/send"
    payload = {"target": target, "message": pesan}
    headers = {"Authorization": FONNTE_TOKEN}
    requests.post(url, data=payload, headers=headers)

def cek_pesan():
    url = "https://api.fonnte.com/get-message" # <-- INI TADI url1 kamu benerin jadi url
    headers = {"Authorization": FONNTE_TOKEN}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            data = r.json()
            if data.get("status") and data.get("data"):
                for msg in data["data"]:
                    sender = msg["sender"]
                    text = msg["message"]
                    print("PESAN MASUK:", sender, text)
                    
                    if text.startswith("!id"):
                        try:
                            nama, id_guild = text.split("|")
                            nama = nama.replace("!id ", "")
                            data = load_data()
                            data["list"][sender] = {"nama": nama, "id": id_guild}
                            save_data(data)
                            kirim_pesan(sender, f"Siap {nama}! ID {id_guild} terdaftar ✅")
                        except:
                            kirim_pesan(sender, "Format salah. Pake:!id nama|ID")
    except: 
        pass

@app.route('/')
def home():
    return "Bot Jalan"

def poller(): # <-- INI MESIN BIAR GA MATI
    while True:
        cek_pesan()
        time.sleep(2)

if __name__ == '__main__':
    Thread(target=poller, daemon=True).start() # <-- JALANIN POLLER
    app.run(host='0.0.0.0', port=8080) # <-- JALANIN FLASK
