import pyrogram
import requests
from pyrogram import *
from requests import get
from os import environ

api_id = 1702217
api_hash = "227747362d2538b4c7694da4bf04e627"
botapi = "1718645974:AAHbjtjhWcRn0RZfhyrsKB-1hO4jYpNDgoQ"
token = "13c86bc3b625bf15995d018810d38737e6e70197"
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
    mesaja = mesaj[1].split("🔔")
    print(mesaj)
    print(mesaja)
    mesaja = mesaja[0]
    print(mesaja)
    s = requests.Session()
    link = s.get("https://ay.live/api")
    cookies = dict(link.cookies)
    json = s.get(f"https://ay.live/api/?api={token}&url=http{mesaja}&alias=&ct=1", cookies=cookies).json()
    link = json['shortenedUrl']
    bot.send_photo(-1001444935707, medya, caption=f"{mesaj[0]} {link}")
    bot.send_message(chat, "Başarılı!")


bot.run()