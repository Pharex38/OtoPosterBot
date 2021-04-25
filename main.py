import pyrogram
from pyrogram import *

api_id = 1702217
api_hash = "227747362d2538b4c7694da4bf04e627"
botapi = "1718645974:AAHbjtjhWcRn0RZfhyrsKB-1hO4jYpNDgoQ"
bot = Client("bot", api_id, api_hash, bot_token=botapi)
print("Başlıyor")

metin = "Eve attıkları kızlara arkalı önlü döşüyorlar https://streamtape.com/e/1dM4xp48LQseqe8"
metin = metin.split("http")
print(metin)
metin = metin[1]
print(metin)

@bot.on_message(~filters.channel)
def post(client, message):
    chat = message.chat.id
    mesaj = message.caption
    print(mesaj)
    mesaj = mesaj.split("http")
    mesaj = mesaj[1]
    bot.send_message(chat, mesaj)


bot.run()