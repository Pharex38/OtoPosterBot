import telebot
from mega import Mega
from os import environ
import requests

mega = Mega()
email = "falperenkocakaplan@gmail.com"
password = "54545621a"
m = mega.login(email, password)
details = m.get_user()
print(details)

API_KEY = environ['BOT_TOKEN']
bot = telebot.TeleBot(API_KEY)

den = m.download_url("https://mega.nz/file/DfoxyArC#jfgaNkO-AnKY69c59UtP5rw24treol-hmcq4JzPPGew")
indir = m.download(file, '/home/john-smith/Desktop', den)
print(den)

@bot.message_handler(commands=['start'])
def start(s):
    email = details['email']
    isim = details['name']
    chat = s.chat.id
    bot.send_message(chat, f"Mail: {email}\nİsim: {isim}")

@bot.message_handler(func=lambda message: True, content_types=["text"])
def dosya(d):
    chat = d.chat.id
    mesaj = d.text
    if mesaj.startswith("https://mega"):
        dosya = get(mesaj)
        
        m.download_url(link)
    

bot.polling()