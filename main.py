from pyrogram import *
from pyrogram.handlers import MessageHandler
from os import environ

api_id = 4826651
api_hash = "ddd27540833843f8196318096eeaff5e"
BOT_TOKEN = environ['BOT_TOKEN']
app = Client("RadyoBot", BOT_TOKEN)
print("Başlıyor")

@app.on_message(filters.text)
def echo(client, message):
    chat = message.chat.id
    app.send_message(chat, message.text)


app.run()  # Automatically start() and idle()
