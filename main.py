from pyrogram import *

api_id = ***REMOVED-API-ID***
api_hash = "***REMOVED-API-HASH***"

app = Client("my_account", api_id, api_hash)
print("Başlıyor")
app.start()


app.send_message("me", "Greetings from **Pyrogram**!")

@app.on_message()
def my_handler(client, message):
    message.forward("me")


