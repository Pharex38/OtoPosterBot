import telebot
from mega import Mega
from os import environ
import urllib.request
from pyrogram import *

mega = Mega()
email = "falperenkocakaplan@gmail.com"
password = "54545621a"
m = mega.login(email, password)
details = m.get_user()

API_KEY = environ['BOT_TOKEN']
bot = telebot.TeleBot(API_KEY)


@app.on_message(filters.command(['oynat']))
def oynat(client, o):
    chat = o.chat.id
    komut = subprocess.call(f'ffmpeg -y -i http://stream2.taksimbilisim.com:8010/ -f s16le -ac 1 -acodec pcm_s16le -ar 128 {yol}/yayin.raw', shell=True)
    print(komut)
    app.send_message(chat, "Oynatılıyor.")
    pytgcalls.join_group_call(-1001391561285, 'yayin.raw')
    app.send_message(chat, "Çalıyor.")

@bot.message_handler(commands=['start'])
def start(s):
    email = details['email']
    isim = details['name']
    chat = s.chat.id
    bot.send_message(chat, f"Mail: {email}\nİsim: {isim}")
    #

@bot.message_handler(func=lambda message: True, content_types=["text"])
def dosya(d):
    chat = d.chat.id
    bot.send_message(chat, "Başladı")
    url = d.text
    print(url)
    den = m.download_url(url)
    print(den)
    dosya = open(f"{den}", "rb")
    print(dosya)
    bot.send_document(chat, dosya)



bot.polling()