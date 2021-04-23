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
    gosterge = current * 100 / total:.1f
    print(f"{gosterge}%")
 
@app.on_message(filters.command(['start']))
def echo(client, message):
    chat = message.chat.id
    app.send_message(chat, "Merhaba!")

@app.on_message(filters.command(['oynat']))
def oynat(client, o):
    chat = o.chat.id
    komut = subprocess.call(f'ffmpeg -y -i http://stream2.taksimbilisim.com:8010/ -f s16le -ac 1 -acodec pcm_s16le -ar 128 {yol}/yayin.raw', shell=True)
    print(komut)
    app.send_message(chat, "Oynatılıyor.")
    pytgcalls.join_group_call(-1001391561285, 'yayin.raw')
    app.send_message(chat, "Çalıyor.")

@app.on_message(filters.document)
def dosya(client, message):
    chat = message.chat.id
    indir = message.download(progress=progress)
    print(indir)
    while 
    app.send_message(chat, "sa")


app.run()  # Automatically start() and idle()
