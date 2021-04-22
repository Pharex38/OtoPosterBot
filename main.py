import telebot
from mega import Mega
from os import environ
import urllib.request

mega = Mega()
email = "falperenkocakaplan@gmail.com"
password = "54545621a"
m = mega.login(email, password)
details = m.get_user()
print(details)

API_KEY = environ['BOT_TOKEN']
bot = telebot.TeleBot(API_KEY)



@bot.message_handler(commands=['start'])
def start(s):
    email = details['email']
    isim = details['name']
    chat = s.chat.id
    bot.send_message(chat, f"Mail: {email}\nİsim: {isim}")

@bot.message_handler(func=lambda message: True, content_types=["text"])
def dosya(d):
    chat = d.chat.id
    url = d.text
    den = m.download_url(url)
    m.import_public_url(url)
    file = m.find(den)
    m.download(file, '/Dosyalar')
    dosya = open(f"/Dosyalar/{den}", "rb")
    bot.send_document(chat, dosya)

bot.polling()