from pyrogram import *
from pyrogram.handlers import MessageHandler
from os import environ
import os
import subprocess
from pytgcalls import *
from mega import Mega

api_id = 1702217
api_hash = "227747362d2538b4c7694da4bf04e627"
BOT_TOKEN = "1762080925:AAGqS8tM8AW9PP1sFABWctHaQqnWCbxBmZM"
app = Client("RadyoBot", api_id, api_hash, bot_token=BOT_TOKEN)
email = "falperenkocakaplan@gmail.com"
password = "54545621a"
mega = Mega()
m = mega.login(email, password)
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

@app.on_message(filters.command(['hesap']))
def hesap(client, message):
    cid = message.chat.id
    bulut = m.get_storage_space(kilo=True)
    alan = bulut['total']
    quota = m.get_quota()
    details = m.get_user()
    dosyalar = m.get_files()
    isim = details['name']
    print(dosyalar)
    print(details)
    app.send_message(cid, f"**Hesap Bilgileriniz;**\n\nİsim: {isim} \nE-mail: {details['email']} \nBoşta bulut Alanı: {alan}\nQuota: {quota}")


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
