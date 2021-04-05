import telebot
from os import environ
from telebot import *
from telegram import *
from logging import basicConfig, getLogger, INFO

LOGS = getLogger(__name__)

LOGS.info("Bot Çalışıyor...")

API_KEY = environ['BOT_TOKEN']


@bot.message_handler(commands=['start'])
def start(m):
    chat = m.chat.id
    msg = message.message.id
    print(msg)


bot.polling()