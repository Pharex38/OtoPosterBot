from pyrogram import *
from pyrogram.handlers import MessageHandler
from os import environ
import subprocess
from pytgcalls import *

api_id = ***REMOVED-API-ID***
api_hash = "***REMOVED-API-HASH***"
BOT_TOKEN = "***REMOVED-BOT-TOKEN***"
app = Client("RadyoBot", api_id, api_hash, bot_token=BOT_TOKEN)
pytgcalls = PyTgCalls(app, log_mode=PyLogs.verbose)
print("Başlıyor")

komut = subprocess.call('ffmpeg -y -i http://yayin.yayindakiler.com:4010/;stream.mp3 -f s16le -ac 1 -acodec pcm_s16le -ar 144 yayin.mp3', shell=True)
print(komut)


@app.on_message(filters.command(['start']))
def echo(client, message):
    chat = message.chat.id
    app.send_message(chat, "Merhaba!")

@app.on_message(filters.command(['oynat']))
def oynat(client, o):
    chat = o.chat.id
    app.send_message(chat, "Oynatılıyor.")
    pytgcalls.join_group_call(-1001391561285, 'yayin.raw')




app.run()
