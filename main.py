import telebot
from mega import Mega
from os import environ

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
    chat = s.chat.id
    bot.send_message(chat, email)


bot.polling()