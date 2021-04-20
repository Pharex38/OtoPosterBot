import feedparser
import telebot

afeed = feedparser.parse("https://www.aa.com.tr/tr/rss/default?cat=guncel")

haber = afeed.keys
entry = afeed.entries[1]
baslik = entry.title()

print(baslik)