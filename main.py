from pyrogram import *
from pyrogram.handlers import MessageHandler
from os import environ
import os
import subprocess
from pytgcalls import *

api_id = 1702217
api_hash = "227747362d2538b4c7694da4bf04e627"
BOT_TOKEN = "1762080925:AAGqS8tM8AW9PP1sFABWctHaQqnWCbxBmZM"
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
    sayi = 0
    chat = message.chat.id
    indir = message.download(progress=progress)
    print(indir)
    while sayi < 7:
        sayi += 1
        app.send_message(chat, f"{islem}%")
        
    app.send_message(chat, "Bitti")


app.run()
