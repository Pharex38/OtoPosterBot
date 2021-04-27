
import requests
from requests import get
from os import environ
import asyncio
import time
from asyncio import sleep
from pymongo import MongoClient
import telebot
from telegram import ParseMode

api_id = environ['API_ID']
api_hash = environ['API_HASH']
botapi = environ['BOT_TOKEN'] 
mongo = environ['MONGO']

cluster = MongoClient(mongo)
db = cluster["OtoPost"]
collection = db["Kanallar"]
bot = telebot.TeleBot(botapi)
print("Başlıyor")
    
@bot.message_handler(commands=['start'])
def start(message):
    chat = message.chat.id
    bot.send_message(chat, "Merhaba!\n\n*Ne İşe Yarıyor?*\nBu bot [Link Mahzeni'nde](https://t.me/joinchat/UYu8q0gBTUdUudDL) paylaşılan postların linklerini otomatik olarak kısaltıp sizin kanalınıza iletir.\n\n*Nasıl Kullanılır?*\n1. Adım: Botu kanlınıza yönetici olarak ekleyin. \n2. Adım: API adresinizi ve Kanal ID girin. \n-/kaydet TRLINK_API KANAL_ID \n3. Adım: Kanalınzda /onayla yazın.\n4. Adım: Keyfini çıkarın.\n\n_NOT: Kanalınızın ID numarasını bilmiyorsanız kanaldan bota bir post iletin bot size söyleyecek._", parse_mode=ParseMode.MARKDOWN)

@bot.channel_post_handler(commands=['onayla'])
def post(message):
    chat = message.chat.id
    print(chat)
    bot.send_message(chat, "Tamamdır!")

@bot.message_handler(commands=['kaydet'])
def kaydet (message):
    mesaj = message.text.split(None, 2)[1:]
    cid = message.chat.id
    user = message.sender_id
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

@bot.message_handler(func=lambda message: True)
def aydialma(message):
    if message.chat.type == "private":
        chat = message.chat.id
        try:
            ileti = message.forward_from_chat.id
        except:
            pass
        else:
            bot.send_message(chat, f"Kanal ID: `{ileti}`", parse_mode=ParseMode.MARKDOWN)
    else:
        pass

@bot.channel_post_handler(content_types=['photo'])
def poster(message):
    chat = message.chat.id
    print(chat)
    if chat == -1001368112299 or chat == -1001352123979:
        print(f"başlıyor ")
        mesaj = message.caption
        mesaj = mesaj.split("KTE: ")
        mesaja = mesaj[1].split("\n\n")
        mesajb = mesaja[0]
        s = requests.Session()
        link = s.get("https://ay.live/api")
        cookies = dict(link.cookies)
        binb = collection.find({})
        print(binb)
        medya = message.photo.file_id
        
        for hesap in binb:
            token = hesap['token']
            kanal = hesap['kanal']
            json = s.get(f"https://ay.live/api/?api={token}&url={mesajb}&alias=&ct=1", cookies=cookies).json()
            link = json['shortenedUrl']
            try:
                time.sleep(1)
                bot.send_photo(kanal, medya, caption=f"{mesaj[0]}KTE: {link}\n\n {mesaja[1]}\n\n{mesaja[2]}{mesaja[3]}")
            except Exception as e:
                print(e)
                print(f"Hata {kanal}")
        print("Başarılı!")
        
        bot.send_message(chat, "Başarılı!")

@bot.channel_post_handler(content_types=['video'])
def poster(message):
    chat = message.chat.id
    print(chat)
    if chat == -1001368112299 or chat == -1001352123979:
        print(f"başlıyor ")
        mesaj = message.caption
        mesaj = mesaj.split("KTE: ")
        mesaja = mesaj[1].split("\n\n")
        mesajb = mesaja[0]
        s = requests.Session()
        link = s.get("https://ay.live/api")
        cookies = dict(link.cookies)
        binb = collection.find({})
        print(binb)
        
        medya = message.video.file_id
        
        for hesap in binb:
            token = hesap['token']
            kanal = hesap['kanal']
            json = s.get(f"https://ay.live/api/?api={token}&url={mesajb}&alias=&ct=1", cookies=cookies).json()
            link = json['shortenedUrl']
            try:
                time.sleep(1)
                bot.send_video(kanal, medya, caption=f"{mesaj[0]}KTE: {link}\n\n {mesaja[1]}\n\n{mesaja[2]}{mesaja[3]}")
            except Exception as e:
                print(f"Hata: {kanal}")
            print("Başarılı!")
        

bot.polling()
