from mega import Mega
import telethon
from os import environ

mega = Mega()
hesap = mega.login(falperenkocakaplan@gmail.com, 54545621a)
API_KEY = environ['BOT_TOKEN']

bot = telebot.TeleBot("API_KEY")

@bot.message_handler(commands=['start'])
def start(m):
    chat = m.chat.id
    detay = hesap.get_user()
    bot.send_message(chat, gui)


bot.polling()