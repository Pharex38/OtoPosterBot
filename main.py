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
kanallar = ['-1001352123979', '-1001444935707']
print("Başlıyor")

@bot.on_message(~filters.group)
def post(client, message):
    print(message)
    chat = message.chat.id
    mesaj = message.caption
    
    mesaj = mesaj.split("KTE: ")
    mesaja = mesaj[1].split("\n\n")
    mesajb = mesaja[0]
    s = requests.Session()
    link = s.get("https://ay.live/api")
    cookies = dict(link.cookies)
    json = s.get(f"https://ay.live/api/?api={token}&url={mesajb}&alias=&ct=1", cookies=cookies).json()
    link = json['shortenedUrl']
    try:
        medya = message.video
        medya = medya['file_id']
    except:
        medya = message.photo
        medya = medya['file_id']
        for xat in kanallar:
            bot.send_photo(xat, medya, caption=f"{mesaj[0]}KTE: {link}\n\n {mesaja[1]}\n\n{mesaja[2]}{mesaja[3]}")
    else:
        for xat in kanallar:
            bot.send_photo(xat, medya, caption=f"{mesaj[0]}KTE: {link}\n\n {mesaja[1]}\n\n{mesaja[2]}{mesaja[3]}")
    bot.send_message(chat, "Başarılı!")


bot.run()