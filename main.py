import os
import json
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

FONNTE_TOKEN = os.environ.get('FONNTE_TOKEN')
ADMIN = "6288225622133" # GANTI INI PAKE NOMER KAMU YA
DATA_FILE = "data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"list": {}, "absen": []}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

data = load_data()

def kirim_pesan(target, pesan):
    url = "https://api.fonnte.com/send"
    payload = {"target": target, "message": pesan}
    headers = {"Authorization": FONNTE_TOKEN}
    requests.post(url, data=payload, headers=headers)

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        return "OK", 200
        
    req = request.get_json()
    sender = req.get('sender')
    message = req.get('message', '').strip()

    if message.startswith('!help'):
        balasan = """*BOT GUILD AING*
!id Nama|IDFF - Daftar ID
!list - Lihat daftar
!absen - Absen
!resetabsen - Reset absen [Admin]"""
        kirim_pesan(sender,balasan) 

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
