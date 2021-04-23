from pyrogram import *
from pyrogram.handlers import MessageHandler
from os import environ
import os
import subprocess
from pytgcalls import *
from mega.py import Mega

api_id = ***REMOVED-API-ID***
api_hash = "***REMOVED-API-HASH***"
BOT_TOKEN = "***REMOVED-BOT-TOKEN***"
app = Client("RadyoBot", api_id, api_hash, bot_token=BOT_TOKEN)
email = "falperenkocakaplan@gmail.com"
password = "54545621a"
mega = Mega()
m = mega.login(email, password)
print("Başlıyor")

def progress(current, total):
    islems = current * 100 / total
    islem = int(islems)
    print(islem)
    sayac(islem, chat)
 
def sayac(islem, chat):
    app.send_message(chat, f"{islem}%")
 
@app.on_message(filters.command(['start']))
def echo(client, message):
    chat = message.chat.id
    app.send_message(chat, "Merhaba!")


@app.on_message(filters.document)
def dosya(client, message):
    global chat
    sayi = 0
    chat = message.chat.id
    indirilen = message.download(progress=progress)
    print(indirilen)
    yuklenen = m.upload(indirilen)
    print(yuklenen)
    link = m.get_upload_link(yuklenen)
    print(link)
    app.send_message(chat, f"Bitti: \nLinkiniz: {link}")


app.run()
