import telebot
from telebot import *
from telegram import *
from logging import basicConfig, getLogger, INFO

LOGS = getLogger(__name__)

LOGS.info("Bot Çalışıyor...")

API_KEY = os.environ['BOT_TOKEN']


@bot.message_handler(commands=['start'])
def start(m):
    chat = m.chat.id
    msg = message.message.id
    print(msg)