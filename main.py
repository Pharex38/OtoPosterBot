import pyrogram
import requests
from pyrogram import *
from requests import get
from os import environ
import pymongo
from pymongo import MongoClient
from pyrogram.raw import functions
from pyrogram.raw.types import ChatAdminRights

api_id = environ['API_ID']
api_hash = environ['API_HASH']
botapi = environ['BOT_TOKEN'] 
mongo = environ['MONGO']
bot = Client("bot", api_id, api_hash, bot_token=botapi)
cluster = pymongo.MongoClient(mongo)
db = cluster["OtoPost"]
collection = db["Kanallar"]

print("Başlıyor")
    
@bot.on_message(filters.command(['start']))
def start(client, message):
    chat = message.chat.id
    bot.send_message(chat, "Merhaba!\n\n**Ne İşe Yarıyor?**\nBu bot [Link Mahzeni'nde](https://t.me/joinchat/UYu8q0gBTUdUudDL) paylaşılan postların linklerini otomatik olarak kısaltıp sizin kanalınıza iletir.\n\n**Nasıl Kullanılır?**\n1. Adım: Botu kanlınıza yönetici olarak ekleyin. \n2. Adım: API adresinizi ve Kanal ID girin. \n-/kaydet TRLINK_API KANAL_ID \n3. Adım: Kanalınzda /onayla yazın.\n4. Adım: Keyfini çıkarın.\n\n__NOT: Kanalınızın ID numarasını bilmiyorsanız kanaldan bota bir post iletin bot size söyleyecek.__", disable_web_page_preview=True)

@bot.on_message(filters.channel)
def post(client, message):
    chat = message.chat.id
    print(chat)
    if chat == -1001368112299 or chat == -1001352123979:
        mesaj = message.caption
        mesaj = mesaj.split("KTE: ")
        mesaja = mesaj[1].split("\n\n")
        mesajb = mesaja[0]
        s = requests.Session()
        link = s.get("https://ay.live/api")
        cookies = dict(link.cookies)
        binb = collection.find({})
        print(binb)
        try:
            medya = message.video
            medya = medya['file_id']
        except:
            medya = message.photo
            medya = medya['file_id']
            for hesap in binb:
                print(hesap)
                token = hesap['token']
                kanal = hesap['kanal']
                json = s.get(f"https://ay.live/api/?api={token}&url={mesajb}&alias=&ct=1", cookies=cookies).json()
                link = json['shortenedUrl']
                try:
                    bot.send_photo(kanal, medya, caption=f"{mesaj[0]}KTE: {link}\n\n {mesaja[1]}\n\n{mesaja[2]}{mesaja[3]}")
                except Exception as e:
                    print(e)
                    pass
        else:
            for hesap in binb:
                print(hesap)
                token = hesap['token']
                kanal = hesap['kanal']
                json = s.get(f"https://ay.live/api/?api={token}&url={mesajb}&alias=&ct=1", cookies=cookies).json()
                link = json['shortenedUrl']
                try:
                    bot.send_video(kanal, medya, caption=f"{mesaj[0]}KTE: {link}\n\n {mesaja[1]}\n\n{mesaja[2]}{mesaja[3]}")
                except Exception as e:
                    print(e)
                    print(kanal)
        bot.send_message(chat, "Başarılı!")
    elif message.text == "/onayla":
        new_rights = ChatAdminRights(post_messages=True, add_admins=True,
                                 invite_users=True,
                                 change_info=True,
                                 ban_users=True,
                                 delete_messages=True)
    
        yetki = bot.send(functions.channels.EditAdmin(channel=chat, user_id=1671239079, admin_rights=new_rights, rank="otopost"))
        print(yetki)
        bot.send_message(chat, "Tamamdır!")

@bot.on_message(filters.private)
def aydialma(client, message):
    print(message.text)
    if not message.text == None and message.text.startswith("/kaydet"):
        mesaj = message.text.split(None, 2)[1:]
        cid = message.chat.id
        user = message.from_user.id
        print(mesaj)
        if len(mesaj) < 2:
            bot.send_message(cid, "Yanlış kullanım! \n\n-/kaydet TRLINK_API KANAL_ID")
            return
        key = {"_id": user, "token": mesaj[0], "kanal": mesaj[1]}
        bnb = collection.find_one({"_id": user})
        if bnb == None:
            collection.insert_one(key)
        else:
            collection.update_one({"_id": user}, {"$set":{"token": mesaj[0], "kanal": mesaj[1]}})
    
        bot.send_message(cid, "Kaydedildi!")
    else:
        chat = message.chat.id
        ileti = message.forward_from_chat
        ileti = ileti['id']
        bot.send_message(chat, f"Kanal ID: `{ileti}`")

"""@bot.on_message(filters.command(['kaydet']))
def kaydet(client, message):
    mesaj = message.text.split(None, 2)[1:]
    cid = message.chat.id
    user = message.from_user.id
    
    key = {"_id": user, "token": mesaj[0], "kanal": mesaj[1]}
    if len(mesaj) < 2:
        bot.send_message(chat, "Yanlış kullanım! \n\n-/kaydet {TRLINK_API} {KANAL_ID}")
        return
    bnb = collection.find_one({"_id": user})
    if bnb == None:
        collection.insert_one(key)
    else:
        collection.update_one({"_id": user}, {"$set":{"token": mesaj[0], "kanal": mesaj[1]}})
    
    bot.send_message(cid, "Kaydedildi!")"""


bot.run()