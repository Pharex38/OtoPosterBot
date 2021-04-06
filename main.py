import telebot
from os import environ
from telebot import *
from telegram import *
from logging import basicConfig, getLogger, INFO

LOGS = getLogger(__name__)

LOGS.info("Bot Çalışıyor...")

API_KEY = environ['BOT_TOKEN']

basicConfig(format="%(asctime)s - @TRLinkShortener - %(levelname)s - %(message)s",
            level=INFO)

bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['start'])
def start(m):
    mesajlar = []
    sayi = 0
    chat = m.chat.id
    try:
        msg = m.reply_to_message.message_id
    except:
        bot.send_message(chat, f"Lütfen bir mesajı yanıtlayın.")
    while 250 > len(mesajlar):
        msg += 1
        mesajlar.append(msg)
        print(mesajlar)
        try:
            bot.delete_message(chat, msg)
            bot.send_message(chat, f"Mesaj Temizlendi.")
        except:
            pass
        else:
            sayı += 1
        bot.send_message(chat, f"{sayı} adet mesaj temizlendi.")


bot.polling()