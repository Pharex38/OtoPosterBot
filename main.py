import pyrogram
import requests
from pyrogram import *
from requests import get
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
    s = requests.Session()
    link = s.get("https://ay.live/api")
    cookies = dict(link.cookies)
    json = s.get(f"https://ay.live/api/?api={token}&url=http{mesaja}&alias=&ct=1", cookies=cookies).text
    link = json['shortenedUrl']
    bot.send_photo(-1001444935707, medya, caption=f"{mesaj[0]} {link}")
    bot.send_message(chat, "Başarılı!")


bot.run()