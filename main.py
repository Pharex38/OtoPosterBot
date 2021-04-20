import feedparser
import telebot
from os import environ

afeed = feedparser.parse("https://www.aa.com.tr/tr/rss/default?cat=guncel")

entry = afeed.entries[1]
baslik = entry.title

API_KEY = environ['BOT_TOKEN']
bot = telebot.TeleBot(API_KEY)
open("sonhaber.txt", "w+").write("0")
print(baslik)

@bot.message_handler(commands=['basla'])
def haber(h):
    deger = True
    chat = h.chat.id
    sonhaber = open("sonhaber.txt", "r+").read()
    while deger:
        if baslik != sonhaber:
            open("sonhaber.txt", "w+").write(baslik)
            bot.send_message(chat, baslik)
        else:
            pass


bot.polling()