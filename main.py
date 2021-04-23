from pyrogram import *
from pyrogram.handlers import MessageHandler
from os import environ
import os
import subprocess
from pytgcalls import *
from mega import Mega
import pymongo

api_id = 1702217
api_hash = "227747362d2538b4c7694da4bf04e627"
BOT_TOKEN = "1762080925:AAGqS8tM8AW9PP1sFABWctHaQqnWCbxBmZM"
app = Client("RadyoBot", api_id, api_hash, bot_token=BOT_TOKEN)
email = "falperenkocakaplan@gmail.com"
password = "54545621a"
mega = Mega()
m = mega.login(email, password)


cluster = pymongo.MongoClient("mongodb+srv://Pharex:545456@cluster0.teii1.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["Mega"]
collection = db["Hesaplar"]

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

@app.on_message(filters.command(['giris']))
def giris(client, message):
    user = message.from_user.id
    mesaj = message.text.split(None, 2)[1:]
    cid = message.chat.id
    if len(mesaj) < 3:
        app.send_message(cid, "Yanlış kullanım")
        return
    email = mesaj[0]
    sifre = mesaj[1]
    print(mesaj)
    try:
        m.login(email, sifre)
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
    cid = message.chat.id
    mid = message.message_id
    mids = mid+1
    app.send_message(cid, "`Yükleniyor...`")
    bulut = m.get_storage_space(giga=True)
    alan = round(bulut['used'],2)
    quota = m.get_quota()
    details = m.get_user()
    dosyalar = m.get_files()
    isim = details['name']
    print(dosyalar)
    print(details)
    app.edit_message_text(cid, mids,f"**Hesap Bilgileriniz;**\n\nİsim: {isim} \nE-mail: {details['email']} \nKullanımda bulut Alanı: {alan}GB\nQuota: {quota}")


@app.on_message(filters.document)
def dosya(client, message):
    global chat
    global mids
    sayi = 0
    chat = message.chat.id
    mid = message.message_id
    mids = mid+1
    app.send_message(chat, "Dosya indirliyor...")
    indirilen = message.download(progress=progress)
    app.edit_message_text(chat, mids, "`Dosya Mega'ya yükleniyor...`")
    yuklenen = m.upload(indirilen)
    print(yuklenen)
    link = m.get_upload_link(yuklenen)
    print(link)
    app.send_message(chat, f"**İşlem Tamamlandı:** \n\nLinkiniz: {link}")


app.run()
