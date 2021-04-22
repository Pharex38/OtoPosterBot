from pyrogram import *
from pyrogram.handlers import MessageHandler
from os import environ

api_id = ***REMOVED-API-ID***
api_hash = "***REMOVED-API-HASH***"
BOT_TOKEN = "***REMOVED-BOT-TOKEN***"
app = Client("RadyoBot", api_id, api_hash, bot_token=BOT_TOKEN)
print("Başlıyor")

@app.on_message(filters.command=(['start']))
def echo(client, message):
    chat = message.chat.id
    app.send_message(chat, "Merhaba!")


app.run()  # Automatically start() and idle()
