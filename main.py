from pyrogram import Client

api_id = 3489775
api_hash = "ddd27540833843f8196318096eeaff5e"
botapi = "1718645974:AAHbjtjhWcRn0RZfhyrsKB-1hO4jYpNDgoQ"
bot = Client("bot", api_id, api_hash, bot_token=botapi)
print("Başlıyor")

metin = "Eve attıkları kızlara arkalı önlü döşüyorlar https://streamtape.com/e/1dM4xp48LQseqe8"
metin = metin.split("http")
print(metin)
metin = metin[1]
print(metin)

@bot.on_message(filters.private)
def post(client, message):
    mesaj = message.text
    print(mesaj)



bot.run()