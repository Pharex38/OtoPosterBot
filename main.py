import feedparser
import telebot
from os import environ

afeed = feedparser.parse("https://www.aa.com.tr/tr/rss/default?cat=guncel")

entry = afeed.entries[1]
baslik = entry.title

API_KEY = environ['BOT_TOKEN']
bot = telebot.TeleBot(API_KEY)

print(baslik)

@bot.message_handler(commands=['basla'])
def haber(h):
    chat = h.chat.id
    bot.send_message(chat, baslik)


bot.polling()