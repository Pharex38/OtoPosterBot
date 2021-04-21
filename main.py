from pyrogram import *
from pyrogram.handlers import MessageHandler

api_id = ***REMOVED-API-ID***
api_hash = "***REMOVED-API-HASH***"

app = Client("my_account", api_id, api_hash)
print("Başlıyor")

@app.on_message(-1001204665413)
def echo(client, message):
    message.reply_text(message.text)


app.run()  # Automatically start() and idle()