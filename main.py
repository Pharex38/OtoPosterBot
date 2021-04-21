from pyrogram import Client

api_id = ***REMOVED-API-ID***
api_hash = "***REMOVED-API-HASH***"

app = Client("my_account", api_id, api_hash)
print("Başlıyor")
app.start()


app.send_message("me", "Greetings from **Pyrogram**!")

def my_function(client, message):
    message.forward("me")

my_handler = MessageHandler(my_function)
app.add_handler(my_handler)

