import os
import time
import requests
from flask import Flask
from threading import Thread

app = Flask(__name__)
@app.route("/")
def home():
    return "Bot Aing Jalan"
FONNTE_TOKEN = os.environ.get("FONNTE_TOKEN")
print(f"TOKEN TERBACA: {FONNTE_TOKEN}")
last_message_id = None

def kirim_pesan(nomor, pesan):
    requests.post("https://api.fonnte.com/send", headers={"Authorization": FONNTE_TOKEN}, data={"target": nomor, "message": pesan})

def poller():
    global last_message_id
    print("Poller dimulai...")
    while True:
        try:
            res = requests.get(f"https://api.fonnte.com/getMessages?token={FONNTE_TOKEN}").json()
            if res.get("status") and res.get("data"):
                pesan_terbaru = res["data"][0]
                if pesan_terbaru.get("id")!= last_message_id:
                    last_message_id = pesan_terbaru.get("id")
                    nomor = pesan_terbaru.get("from")
                    teks = pesan_terbaru.get("message")
                    print(f"PESAN MASUK: {nomor} {teks}")
                    if teks.startswith("!id aing|"):
                        kirim_pesan(nomor, f"Siap aing! ID {teks.split('|')[1]} terdaftar ✅")
        except: pass
        time.sleep(3)

def keep_alive():
    while True:
        try:
            requests.get("https://web-production-52a5b.up.railway.app")
            print("PING RAILWAY OK")
        except: print("PING GAGAL")
        time.sleep(300)

if __name__ == '__main__':
    Thread(target=poller, daemon=False).start()
Thread(target=keep_alive, daemon=False).start()
    import os
port = int(os.environ.get("PORT", 8080))
app.run(host='0.0.0.0', port=port)
