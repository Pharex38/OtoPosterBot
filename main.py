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
    bot.send_message(chat, "Başladı")
    url = d.text
    den = m.download_url(url)
    dosya = open(f"{den}", "rb")
    bot.send_document(chat, dosya)

bot.polling()