from pyrogram import *
from pyrogram.handlers import MessageHandler

api_id = 4826651
api_hash = "ddd27540833843f8196318096eeaff5e"

app = Client("my_account", api_id, api_hash)
print("Başlıyor")

@app.on_message(filters.text & filters.private)
def echo(client, message):
    message.reply_text(message.text)


app.run()  # Automatically start() and idle()