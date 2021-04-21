from pyrogram import Client

api_id = ***REMOVED-API-ID***
api_hash = "***REMOVED-API-HASH***"

app = Client("my_account", api_id, api_hash)
print("Başlıyor")

app.send_message("me", "Greetings from **Pyrogram**!")

