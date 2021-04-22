from pyrogram import *
from pyrogram.handlers import MessageHandler
from os import environ

api_id = 1702217
api_hash = "227747362d2538b4c7694da4bf04e627"
BOT_TOKEN = "1762080925:AAGqS8tM8AW9PP1sFABWctHaQqnWCbxBmZM"
app = Client("RadyoBot", api_id, api_hash, bot_token=BOT_TOKEN)
print("Başlıyor")

@app.on_message(filters.text)
def echo(client, message):
    chat = message.chat.id
    app.send_message(chat, message.text)


app.run()  # Automatically start() and idle()
