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

@bot.on_message(~filters.group)
def post(client, message):
    chat = message.chat.id
    mesaj = message.caption
    medya = message.photo
    medya = medya['file_id']
    print(medya)
    mesaj = mesaj.split("KTE: ")
    mesaja = mesaj[1].split("\n\n")
    print(mesaj)
    mesajb = mesaja[0]
    print(mesaja)
    
    print(mesajb)
    s = requests.Session()
    link = s.get("https://ay.live/api")
    cookies = dict(link.cookies)
    json = s.get(f"https://ay.live/api/?api={token}&url={mesajb}&alias=&ct=1", cookies=cookies).json()
    link = json['shortenedUrl']
    bot.send_photo(-1001444935707, medya, caption=f"{mesaj[0]}KTE: {link} {mesaja[0]}{mesaja[1]}{mesaja[2]}")
    bot.send_message(chat, "Başarılı!")


bot.run()