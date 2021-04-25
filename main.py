import pyrogram
from pyrogram import *
import requests
from os import environ

api_id = ***REMOVED-API-ID***
api_hash = "***REMOVED-API-HASH***"
botapi = "***REMOVED-BOT-TOKEN***"
token = "***REMOVED-SHORTENER-KEY***"
bot = Client("bot", api_id, api_hash, bot_token=botapi)
print("Başlıyor")

@bot.on_message(~filters.channel)
def post(client, message):
    chat = message.chat.id
    mesaj = message.caption
    medya = message.photo
    medya = medya['file_id']
    print(medya)
    mesaj = mesaj.split("http")
    mesaja = mesaj[1]
    json = get(f"https://ay.live/api/?api={token}&url=http{mesaja}&alias=&format=text&ct=1").json()
    link = json['shortenedUrl']
    bot.send_photo(chat, medya, caption=f"{mesaj[0]} {link}")


bot.run()