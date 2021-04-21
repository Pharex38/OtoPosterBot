from pyrogram import *
from pyrogram.handlers import MessageHandler

api_id = ***REMOVED-API-ID***
api_hash = "***REMOVED-API-HASH***"

app = Client("my_account", api_id, api_hash)
print("Başlıyor")

@app.on_message(filters.text & filters.channel)
def echo(client, message):
    app.send_message(-1001196621427, message.text)


app.run()  # Automatically start() and idle()
