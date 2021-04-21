from pyrogram import *
from pyrogram.handlers import MessageHandler

api_id = 4826651
api_hash = "ddd27540833843f8196318096eeaff5e"

app = Client("my_account", api_id, api_hash)
print("Başlıyor")

@app.on_message(filters.channel & filters.create(lambda c,m: m.chat.id == -1001204665413))
def echo(client, message):
    app.send_message("-1001196621427", message.text)


app.run()  # Automatically start() and idle()
