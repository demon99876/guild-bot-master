import requests
import time
import os
from threading import Thread

FONNTE_TOKEN = os.getenv("FONNTE_TOKEN")
DEVICE = "6288225622133"
CHECK_INTERVAL = 3

last_message_id = None

def get_messages():
    global last_message_id
    url = "https://api.fonnte.com/message"
    headers = {"Authorization": FONNTE_TOKEN}
    data = {"device": DEVICE}
    
    try:
        res = requests.post(url, headers=headers, data=data)
        res.raise_for_status()
        messages = res.json().get("data", [])
        
        for msg in messages:
            msg_id = msg.get("id")
            if msg_id!= last_message_id:
                last_message_id = msg_id
                sender = msg.get("sender")
                text = msg.get("message")
                
                print(f"PESAN DARI: {sender} ISI: {text}")
                process_command(sender, text)
                
    except Exception as e:
        print(f"Error poller: {e}")

def process_command(sender, text):
    if text.startswith("!id"):
        parts = text.split("|")
        if len(parts) == 2:
            nama = parts[0].replace("!id ", "")
            id_game = parts[1]
            print(f"DAFTAR BARU: {nama} - {id_game}")
            send_message(sender, f"Siap {nama}! ID {id_game} sudah terdaftar ✅")
    elif text == "!help":
        send_message(sender, "Ketik:!id Nama|ID_Game")

def send_message(to, message):
    url = "https://api.fonnte.com/send"
    headers = {"Authorization": FONNTE_TOKEN}
    data = {"target": to, "message": message}
    requests.post(url, headers=headers, data=data)

def start_poller():
    print("Poller Fonnte dimulai...")
    while True:
        get_messages()
        time.sleep(CHECK_INTERVAL)

Thread(target=start_poller, daemon=True).start()
