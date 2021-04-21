from pyrogram import *
from pyrogram.handlers import MessageHandler

api_id = 4826651
api_hash = "ddd27540833843f8196318096eeaff5e"

app = Client("my_account", api_id, api_hash)
print("Başlıyor")
app.start()


app.send_message("me", "Greetings from **Pyrogram**!")

@app.on_message()
def my_handler(client, message):
    message.forward("me")


