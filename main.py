from pyrogram import *
from pyrogram.handlers import MessageHandler
from os import environ

api_id = 1762080925
api_hash = "***REMOVED-BOT-TOKEN***"
BOT_TOKEN = environ['BOT_TOKEN']
app = Client("RadyoBot", api_id, api_hash)
print("Başlıyor")

@app.on_message(filters.text)
def echo(client, message):
    chat = message.chat.id
    app.send_message(chat, message.text)


app.run()  # Automatically start() and idle()
