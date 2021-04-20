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
    open("sonhaber.txt", "w+").write(baslik)
    deger = True
    chat = h.chat.id
    sonhaber = open("sonhaber.txt", "r+").read()
    while deger:
        if baslik == sonhaber:
            pass
        else:
            open("sonhaber.txt", "w+").write(baslik)
            bot.send_message(chat, baslik)

@bot.message_handler(commands=['dur'])
def dur(d):
    chat = d.chat.id
    deger = False

bot.polling()