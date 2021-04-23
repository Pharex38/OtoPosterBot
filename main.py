from pyrogram import *
from pyrogram.handlers import MessageHandler
from os import environ
import subprocess
import Py-TgCalls

api_id = 1702217
api_hash = "227747362d2538b4c7694da4bf04e627"
BOT_TOKEN = "1762080925:AAGqS8tM8AW9PP1sFABWctHaQqnWCbxBmZM"
app = Client("RadyoBot", api_id, api_hash, bot_token=BOT_TOKEN)
pytgcalls = PyTgCalls(app, log_mode=PyLogs.verbose)
print("Başlıyor")

@app.on_message(filters.command(['start']))
def echo(client, message):
    chat = message.chat.id
    app.send_message(chat, "Merhaba!")

@app.on_message(filters.command(['oynat']))
def oynat(client, o):
    chat = o.chat.id
    subprocess.call('ffmpeg -y -i http://stream2.taksimbilisim.com:8010/ -f s16le -ac 1 -acodec pcm_s16le -ar 128 /yayin.raw', shell=True)
    pytgcalls.join_group_call(-1001391561285, 'yayin.raw')




app.run()  # Automatically start() and idle()
