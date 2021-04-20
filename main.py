import feedparser
import telebot

afeed = feedparser.parse("https://www.aa.com.tr/tr/rss/default?cat=guncel")

entry = afeed.entries[1]
baslik = entry.title

API_KEY = environ['BOT_TOKEN']
bot = telebot.TeleBot(API_KEY)

print(baslik)
