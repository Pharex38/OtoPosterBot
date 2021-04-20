import feedparser
import telebot

afeed = feedparser.parse("https://www.aa.com.tr/tr/rss/default?cat=guncel")

haber = afeed.keys
entry = afeed.entries[1]

print(entry.keys())
print(entry.title())