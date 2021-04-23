from pyrogram import *
from pyrogram.handlers import MessageHandler
from os import environ
import os
import subprocess
from pytgcalls import *

api_id = ***REMOVED-API-ID***
api_hash = "***REMOVED-API-HASH***"
BOT_TOKEN = "***REMOVED-BOT-TOKEN***"
app = Client("RadyoBot", api_id, api_hash, bot_token=BOT_TOKEN)
pytgcalls = PyTgCalls(app, log_mode=PyLogs.verbose)
print("Başlıyor")

yol = os.getcwd()
print(yol)

    
def progress(current, total):
    islem = current * 100 / total
    global islem
    print(islem)
    
 
@app.on_message(filters.command(['start']))
def echo(client, message):
    chat = message.chat.id
    app.send_message(chat, "Merhaba!")


@app.on_message(filters.document)
def dosya(client, message):
    chat = message.chat.id
    indir = message.download(progress=progress)
    print(indir)
    islem = open("islem.txt", "r").read()
    goster = int(islem)
    app.send_message(chat, f"{goster}%")
        
    app.send_message(chat, "Bitti")


app.run()
