import telebot
from os import environ
from telebot import *
from telegram import *
from logging import basicConfig, getLogger, INFO

LOGS = getLogger(__name__)

LOGS.info("Bot Çalışıyor...")

API_KEY = environ['BOT_TOKEN']

bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['start'])
def start(m):
    mesajlar = []
    chat = m.chat.id
    try:
        msg = m.reply_to_message.message_id
    except:
        bot.send_message(chat, f"Lütfen bir mesajı yanıtlayın.")
    while 100 > len(mesajlar):
        msg += 1
        mesajlar.append(msg)
        if not msg == None:
            bot.delete_message(chat, msg)
        
    bot.send_message(chat, f"{msg}")


bot.polling()