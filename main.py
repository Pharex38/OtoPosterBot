from pyrogram import *
from pyrogram.handlers import MessageHandler
from os import environ
import os
import subprocess
from pytgcalls import *
from mega import Mega
import pymongo

api_id = os.environ['API_ID']
api_hash = os.environ['API_HASH']
BOT_TOKEN = os.environ['BOT_TOKEN']
mongo = os.environ['MONGO']
mega = Mega()

cluster = pymongo.MongoClient(mongo)
db = cluster["Mega"]
collection = db["Hesaplar"]
app = Client("RadyoBot", api_id, api_hash, bot_token=BOT_TOKEN)

print("Başlıyor")

def progress(current, total):
    islems = current * 100 / total
    islem = int(islems)
    print(islem)
    sayac(islem, chat, mids)
 
def sayac(islem, chat, mids):
    app.edit_message_text(chat, mids, f"{islem}%")
 
@app.on_message(filters.command(['start']))
def echo(client, message):
    chat = message.chat.id
    app.send_message(chat, "Merhaba!")

@app.on_message(filters.command(['indir']))
def linkten(client, message):
    mesaj = message.text.split(None, 2)[1:]
    cid = message.chat.id
    mid = message.message_id
    mids = mid+1
    if mesaj[0].startswith("https://mega") or mesaj[0].startswith("http://mega"):
        m.send_message(cid, f"`Dosya indiriliyor...`")
        m = mega.login()
        indirilen = m.download_url(mesaj)
        app.edit_message_text(cid, mids, f"`Dosya indirildi, Telegrama Yükleniyor...`")
        app.send_document(cid, indirilen)
        app.edit_message_text(cid, mids, f"__**Başarılı!**__")
    else:
        app.send_message(cid, "**Hatalı kullanım!**")
    

@app.on_message(filters.command(['giris']))
def giris(client, message):
    user = message.from_user.id
    mesaj = message.text.split(None, 2)[1:]
    cid = message.chat.id
    if len(mesaj) < 2:
        print(len(mesaj))
        app.send_message(cid, "Yanlış kullanım")
        return
    email = mesaj[0]
    sifre = mesaj[1]
    print(mesaj)
    try:
        mega.login(email, sifre)
    except:
        app.send_message(cid, "Email veya şifreniz hatalı!")
    else:
        bnb = collection.find_one({"_id": user})
        if bnb == None:
            key = {"_id": user, "email": email, "sifre": sifre}
            collection.insert_one(key)
            app.send_message(cid, "Giriş Yapıldı!")
        else:
            collection.update_one({"_id": user}, {"$set":{"email": email, "sifre": sifre}})
            app.send_message(cid, "Giriş Yapıldı!")


@app.on_message(filters.command(['hesap']))
def hesap(client, message):
    user = message.from_user.id
    cid = message.chat.id
    mid = message.message_id
    mids = mid+1
    app.send_message(cid, "`Yükleniyor...`")
    hbilgi = collection.find_one({"_id": user})
    if hbilgi == None:
        app.send_message(cid, "Bu özelliği kullanabilmek için önce giriş yapmanız gerekiyor. /giris komutu ile giriş yapabilirsiniz.")
    else:
        email = hbilgi['email']
        sifre = hbilgi['sifre']
        m = mega.login(email, sifre)
        bulut = m.get_storage_space(giga=True)
        alan = round(bulut['used'],2)
        quota = m.get_quota()
        details = m.get_user()
        dosyalar = m.get_files()
        isim = details['name']
        print(dosyalar)
        print(details)
        app.edit_message_text(cid, mids,f"**Hesap Bilgileriniz;**\n\nİsim: {isim} \nE-mail: {details['email']} \nKullanımda bulut Alanı: {alan}GB")


@app.on_message(filters.document)
def dosya(client, message):
    global chat
    global mids
    user = message.from_user.id
    chat = message.chat.id
    mid = message.message_id
    mids = mid+1
    app.send_message(chat, "Dosya indirliyor...")
    indirilen = message.download(progress=progress)
    app.edit_message_text(chat, mids, "`Dosya Mega'ya yükleniyor...`")
    hbilgi = collection.find_one({"_id": user})
    if hbilgi == None:
        app.send_message(chat, "Bu özelliği kullanabilmek için önce giriş yapmanız gerekiyor. /giris komutu ile giriş yapabilirsiniz.")
    else:
        email = hbilgi['email']
        sifre = hbilgi['sifre']
        m = mega.login(email, sifre)
        yuklenen = m.upload(indirilen)
        print(yuklenen)
        link = m.get_upload_link(yuklenen)
        print(link)
        app.edit_message_text(chat, mids, f"**İşlem Tamamlandı:** \n\nDosya: {indirilen}\nLinkiniz: {link}")


app.run()
