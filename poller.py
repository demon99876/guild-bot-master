import os
import time
import requests
import threading
from main import kirim_pesan, load_data, save_data

FONNTE_TOKEN = os.environ.get('FONNTE_TOKEN')

def proses_pesan(data):
    if data['sender'] == '6288225622133@c.us':
        return
    nomor = data['sender'].replace('@c.us','')
    pesan = data['message'].strip()
    data_bot = load_data()
    if pesan.startswith('!id '):
        try:
            _, isi = pesan.split('!id ', 1)
            nama, id_ = isi.split('|')
            data_bot['list'][nomor] = {'nama': nama, 'id': id_}
            save_data(data_bot)
            kirim_pesan(nomor, f"Siap {nama}! ID {id_} terdaftar ✅")
            print(f"DAFTAR BARU: {nama} - {id_}")
        except:
            kirim_pesan(nomor, "Format salah. Pakai:!id Nama|ID")

def cek_pesan():
    print("Poller Fonnte dimulai...")
    last_id = 0
    while True:
        try:
            r = requests.get(f"https://api.fonnte.com/inbox?token={FONNTE_TOKEN}")
            if r.status_code == 200:
                msgs = r.json().get('data', [])
                for msg in msgs:
                    if msg['id'] > last_id:
                        last_id = msg['id']
                        print("PESAN MASUK:", msg['sender'], msg['message'])
                        proses_pesan(msg)
        except Exception as e:
            print("ERROR:", e)
        time.sleep(2)

threading.Thread(target=cek_pesan, daemon=True).start()
