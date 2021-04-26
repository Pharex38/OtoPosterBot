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
cluster = pymongo.MongoClient("mongodb+srv://Pharex:545456@cluster0.teii1.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["OtoPost"]
collection = db["Kanallar"]
kanallar = ['-1001352123979', '-1001444935707']
print("Başlıyor")

user = collection.find({"id": 1})
for usre in user:
    token = usre['token']
    xat = usre['kanal']
    json = s.get(f"https://ay.live/api/?api={token}&url={mesajb}&alias=&ct=1", cookies=cookies).json()
    bot.send_photo(xat, medya, caption=f"{mesaj[0]}KTE: {link}\n\n {mesaja[1]}\n\n{mesaja[2]}{mesaja[3]}")
    

@bot.on_message(~filters.group)
def post(client, message):
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
            try:
                bot.send_photo(xat, medya, caption=f"{mesaj[0]}KTE: {link}\n\n {mesaja[1]}\n\n{mesaja[2]}{mesaja[3]}")
            except:
                pass
    else:
        for xat in kanallar:
            try:
                bot.send_video(xat, medya, caption=f"{mesaj[0]}KTE: {link}\n\n {mesaja[1]}\n\n{mesaja[2]}{mesaja[3]}")
            except:
                pass
    bot.send_message(chat, "Başarılı!")

@bot.on_message(filters.command(['kaydet']))
def kaydet(client, message):
    mesaj = message.text.split(None, 2)[1:]
    cid = message.chat.id
    user = message.from_user.id
    kanal = f"-100{mesaj[2]}"
    key = {"_id": user, "token": mesaj[1], "kanal": kanal}
    if len(mesaj) < 2:
        bot.send_message(chat, "Yanlış kullanım! -/kaydet (tokeniniz) (kanal_id)")
        return
    if bnb == None:
        collection.insert_one(key)
    else:
        collection.update_one({"_id": user}, {"$set":{"token": mesaj[1], "kanal": kanal}})
    
    bot.send_message(cid, "Kaydedildi!")


bot.run()