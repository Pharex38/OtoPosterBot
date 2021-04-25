from pyrogram import Client
import pyrogram

api_id = ***REMOVED-API-ID***
api_hash = "***REMOVED-API-HASH***"
botapi = "***REMOVED-BOT-TOKEN***"
bot = Client("bot", api_id, api_hash, bot_token=botapi)
print("Başlıyor")

metin = "Eve attıkları kızlara arkalı önlü döşüyorlar https://streamtape.com/e/1dM4xp48LQseqe8"
metin = metin.split("http")
print(metin)
metin = metin[1]
print(metin)

@bot.on_message(~filters.channel)
def post(client, message):
    mesaj = message.text
    print(mesaj)



bot.run()