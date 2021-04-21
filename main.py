from pyrogram import Client

api_id = 4826651
api_hash = "ddd27540833843f8196318096eeaff5e"

app = Client("my_account", api_id, api_hash)
print("Başlıyor")


app.send_message("me", "Greetings from **Pyrogram**!")

my_handler = MessageHandler(my_function)
app.add_handler(my_handler)

app.start()