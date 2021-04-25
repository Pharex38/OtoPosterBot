from pyrogram import Client

api_id = 3489775
api_hash = "***REMOVED-API-HASH***"
strings = 
app = Client( strings, api_id, api_hash)
print("Başlıyor")
app.start()

metin = "Eve attıkları kızlara arkalı önlü döşüyorlar https://streamtape.com/e/1dM4xp48LQseqe8"
metin = metin.strip("://")
print(metin)
metin = metin[1]
print(metin)

app.send_message("me", "Greetings from **Pyrogram**!")

