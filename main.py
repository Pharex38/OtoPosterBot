import requests
from requests import get
from os import environ
import asyncio
from time import sleep
from pymongo import MongoClient
import telebot
from telebot import types
import time, datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import threading


#botapi = environ['BOT_TOKEN'] 
mongo = "os.environ["MONGO_URI"]"

cluster = MongoClient(mongo)
db = cluster["OtoPost"]
collection = db["Kanallar"]
karaliste = collection.find_one({"_id": 0})
botapi = karaliste['bottoken']
bot = telebot.TeleBot(botapi,parse_mode='html')
print("Başlıyor")

kara = karaliste['kara']

sahip = 1302980840
botlog = -1001352123979
kaynaklar = [-1001368112299, -1001122395785, -1001423365614, -1001251394039, -1001405966343, -1001368008488]
markup = types.ForceReply(selective=False)

dugme = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True, selective=True)
butonbir = types.KeyboardButton('📝 Kaydet')
butoniki = types.KeyboardButton('🔧 Kaynak')
butonuc = types.KeyboardButton('📏 Şablon')
butondort = types.KeyboardButton('▶️ SFS Modu')
butonbes = types.KeyboardButton('⛓️ Elle Post Paylaş')
butonalti = types.KeyboardButton('🥰 Bağış')
dugme.add(butonbir, butoniki, butonuc, butondort, butonbes)
dugme.row(butonalti)

markupp = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True, selective=True)
buton1 = types.KeyboardButton('🔶 Yeni Kanal Ekle')
buton2 = types.KeyboardButton('❌ İptal')
buton3 = types.KeyboardButton('🗑️ Kanal Sil')
buton4 = types.KeyboardButton('♻️ API değiştir')
buton5 = types.KeyboardButton('🔗 Site değiştir')
buton6 = types.KeyboardButton('🤖 Alternatif Ekle')
markupp.add(buton1, buton2, buton3, buton4, buton5, buton6)

imark = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True, selective=True)
batinbir = types.KeyboardButton('❌ İptal')
imark.add(batinbir)

amark = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True, selective=True)
batiniki = types.KeyboardButton('⛔ Alternatif Kaldır')
amark.add(batinbir, batiniki)

zaman = datetime.datetime.now()
saat = zaman.hour 
dakika = zaman.minute
print(f"Saat: {saat}:{dakika}")


@bot.message_handler(commands=['start'])
def start(message):
    user = message.from_user.id
    chat = message.chat.id
    if user in kara:
        bot.send_message(chat, "🤓 Üzgünüm senin gibi aptal birisi için çalışmıyorum")
        return
    kat = collection.find_one({"_id": user})
    dagme = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True, selective=True)
    dagme.add(butonbir)
    mention = "@"+message.from_user.username if message.from_user.username else message.from_user.first_name
    if kat == None:
        bot.send_message(chat, """
✨ <b>Merhaba {}!</b>

❔<b>Ne İşe Yarıyor? </b>
<i>Bu bot sizin seçtiğiniz kaynak kanalında paylaşılan postların linklerini otomatik olarak kısaltıp sizin kanalınıza iletir.</i>

❔<b>Nasıl Kullanılır?</b>
<i>1. Adım: Botu kanlınıza yönetici olarak ekleyin.
2. Adım: Kaydet butonunu kullanarak bilgilerinizi kaydedin.
3. Adım: <b>KANALINIZDA</b> /onayla yazın.
4. Adım: Keyfini çıkarın.</i>

<b>❤️ Geliştirici & Sahip : @Pharex
👨🏻‍🔧 Fix & Eklentiler : @bberc</b>


        <b>@OtoPosterBotLog</b>
""".format(mention), disable_web_page_preview=True, reply_markup=dagme)
    else:
        bot.send_message(chat, """
✨ <b>Merhaba {}!</b>

❔<b>Ne İşe Yarıyor? </b>
<i>Bu bot sizin seçtiğiniz kaynak kanalında paylaşılan postların linklerini otomatik olarak kısaltıp sizin kanalınıza iletir.</i>

❔<b>Nasıl Kullanılır?</b>
<i>1. Adım: Botu kanlınıza yönetici olarak ekleyin.
2. Adım: Kaydet butonunu kullanarak bilgilerinizi kaydedin.
3. Adım: <b>KANALINIZDA</b> /onayla yazın.
4. Adım: Keyfini çıkarın.</i>

<b>❤️ Geliştirici & Sahip : @Pharex
👨🏻‍🔧 Fix & Eklentiler : @bberc</b>

          <b>@OtoPosterBotLog</b>
""".format(mention), disable_web_page_preview=True, reply_markup=dugme)

@bot.message_handler(commands=['stats'])
def stats(message):
    kanals = 0
    users = 0
    chat = message.chat.id
    user = message.from_user.id
    if user != sahip:
        bot.send_message(chat, "Sen benim sahibim değilsin!")
        return
    kullanicilar = collection.find({})
    for kullanici in kullanicilar:
        users += 1
        for kul in kullanici['kanal']:
            kanals += 1
    bot.send_message(chat, "Toplam Kullanıcı Sayısı: {}\nToplam Kayıtlı Kanal Sayısı: {}".format(users, kanals))

@bot.message_handler(commands=['onayla'])
def ona(m):
    cid = m.chat.id
    bot.send_message(cid, "Bu komutu kanalınızda kullanmalısınız.")

@bot.message_handler(commands=['sil'])
def durdur(message):
    chat = message.chat.id
    user = message.from_user.id
    if user in kara:
        bot.send_message(chat, "🤓 Üzgünüm senin gibi aptal birisi için çalışmıyorum")
        return
    print(chat)
    try:
        collection.delete_one({"_id": user})
    except:
        bot.reply_to(message, "<b>Henüz bir kanal kaydetmemişsiniz.</b>")
    else:
        bot.reply_to(message, "<b>Kanalınız Silindi!</b>")

@bot.channel_post_handler(commands=['onayla'])
def post(message):
    chat = message.chat.id
    mid = message.id
    mids = mid+1
    print(chat)
    bot.reply_to(message, "Tamamdır!")
    sleep(1)
    try:
        bot.delete_message(chat, mid)
        bot.delete_message(chat, mids)
    except:
        pass

@bot.message_handler(content_types=['text'])
def menu(message):
    chat = message.chat.id
    user = message.from_user.id
    mesaj = message.text
    mj = collection.find_one({"_id": user})
    if user in kara:
        bot.send_message(chat, "🤓 Üzgünüm senin gibi aptal birisi için çalışmıyorum")
        return
    if mesaj == "🔧 Kaynak":
        mahzen = bot.get_chat(kaynaklar[0])
        bedava = bot.get_chat(kaynaklar[1])
        evi = bot.get_chat(kaynaklar[2])
        bashub = bot.get_chat(kaynaklar[3])
        acikmi = bot.get_chat(kaynaklar[4])
        muho = bot.get_chat(kaynaklar[5])
        if mj == None:
            bot.send_message(chat, "Lütfen önce bir API kaydedin.")
            return
        msg = bot.send_message(chat, """<b>Kullanmak istediğiniz kaynak kanalınının numarasını gönderin:
    
    Kaynak No:1</b>
    <a href="{}">{}</a>
    
    <b>Kaynak No:2</b>
    <a href="{}">{}</a>
    
    <b>Kaynak No:3</b>
    <a href="{}">{}</a>
    
    <b>Kaynak No:4</b>
    <a href="{}">{}</a>
    
    <b>Kaynak No:5</b>
    <a href="{}">{}</a>
    
    <b>Kaynak No:6</b>
    <a href="{}">{}</a>

<b>❗Birden fazla kaynak seçmek isterseniz  seçmek istediğiniz kaynakların numaralarının arasına virgül koyarak gönderin.
Örnek: "1,2,3"</b>
    
    
    """.format(mahzen.invite_link, mahzen.title, bedava.invite_link, bedava.title, evi.invite_link, evi.title, bashub.invite_link, bashub.title, acikmi.invite_link, acikmi.title, muho.invite_link, muho.title), disable_web_page_preview=True, reply_markup=imark)
        bot.register_next_step_handler(msg, kaynake)
        return
    if mesaj == "📏 Şablon":
        if mj == None:
            bot.send_message(chat, "Lütfen önce bir API kaydedin.")
            return
        if mj['sira'] == "1":
            bot.send_message(chat, """<b>Şablon No:9</b>
----------------
{aciklama} 

𝙇𝙄𝙉𝙆🔗 {link} 


  𝙇𝙄𝙉𝙆🔗 {alink}

🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.

📌 Link Nasıl Açılır Bilmiyorsanız
👉 @linkk_gecmee
----------------

Üstteki şablonlardan kullanmak isterseniz, istediğiniz şablonun numarasını gönderin.""", reply_markup=markup)
            msg = bot.send_message(chat, "<i>Eğer kendi şablonunuzu oluşturmak isterseniz üstteki şablonlardaki gibi</i> <b>{aciklama}, {alink}</b> ve <b>{link}</b> <i>kelimelerinin bulunduğundan emin olun yoksa şablon çalışmaz</i>", reply_markup=imark)
            bot.register_next_step_handler(msg, sabloniki)
            return
        else:
            bot.send_message(chat, """<b>Şablon No:1</b>
    ----------------
🔥{aciklama}

🔱 TIKLA 👉 {link}

📛 SESİ AÇ 'a tıklamayı unutma
----------------

<b>Şablon No:2</b>
----------------
{aciklama} 

𝙇𝙄𝙉𝙆🔗 {link}

🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.

📌 Link Nasıl Açılır Bilmiyorsanız

👉 @linkgec06
----------------

Üstteki şablonlardan kullanmak isterseniz, istediğiniz şablonun numarasını gönderin.""", reply_markup=markup)
            msg = bot.send_message(chat, "<i>Eğer kendi şablonunuzu oluşturmak isterseniz üstteki şablonlardaki gibi</i> <b>{aciklama}</b> ve <b>{link}</b> <i>kelimelerinin bulunduğundan emin olun yoksa şablon çalışmaz</i>", reply_markup=imark)
            bot.register_next_step_handler(msg, sabloniki)
            return
    if mesaj == "📝 Kaydet":
        kayitli = 0
        chat = message.chat.id
        bina = collection.find_one({"_id": chat})
        try:
            for chan in bina['kanal']:
                try:
                    kbilgi = bot.get_chat(chan)
                except Exception as e:
                    print(e)
                    collection.update_one({"_id": chat}, {"$pull": {"kanal": chan}})
                    kayitli = kayitli - 1
                    print("Kanal silindi")
                else:    
                    bot.send_message(chat, """Kayit No: {}\n\nKanalınız: <a href="{}">{}</a>""".format(kayitli+1, kbilgi.invite_link, kbilgi.title))
                kayitli = kayitli + 1
        except Exception as e:
            print(e)
            pass
        try:
            tokenn = bina['token']
        except:
            msg = bot.send_message(chat, """📝 <i>Lütfen</i> <a href="https://tr.link/member/tools/quick">burdan</a> <i>aldığınız API adresinizi gönderin</i>""", reply_markup=imark)
            bot.register_next_step_handler(msg, apikayit)
            return
        else:
            site = bina['site']
            if site == "1":
                site = "TRLink"
            if site == "2":
                site = "PND.TL"
            if site == "3":
                site = "Exe.io"
            if site == "4":
                site = "Ouo.io"
            if site == "5":
                site = "Pubiza"
            if bina['altsite'] == "None":
                msg = bot.send_message(chat, "<i>♦️Kayıtlı API: {}\nSite: {}\nToplam Kanal: {}</i>".format(tokenn, site, kayitli), reply_markup=markupp)
            else:
                altsite = bina['altsite']
                if altsite == "1":
                    altsite = "TRLink"
                if altsite == "2":
                    altsite = "PND.TL"
                if altsite == "3":
                    altsite = "Exe.io"
                if altsite == "4":
                    altsite = "Ouo.io"
                if altsite == "5":
                    altsite = "Pubiza"
                msg = bot.send_message(chat, "<i>♦️Birincil API: {}\n  Birincil Site: {}\n  Alternatif API: {}\n  Alternatif Site: {}\n  Toplam Kanal: {}</i>".format(tokenn, site, bina['altapi'], altsite, kayitli), reply_markup=markupp)
                
            bot.register_next_step_handler(msg, kayitapi)
            return
    if mesaj == "▶️ SFS Modu":
        if mj == None:
            bot.send_message(chat, "Lütfen önce bir API kaydedin.")
            return
        try:
            mod = collection.find_one({"_id": user})
        except:
            pass
        if mod['kaynak'] == "9" or mod['kaynak'] == None:
            try:
                collection.update_one({"_id": user}, {"$set": {"kaynak": mod['eski']}})
            except:
                pass
            bot.send_message(chat, "SFS modu durduruldu", reply_markup=dugme)
            return
        else:
            collection.update_one({"_id": user}, {"$set": {"eski": mod['kaynak']}})
            collection.update_one({"_id": user}, {"$set": {"kaynak": "9"}})
            bot.send_message(chat, "Kanallarınız SFS moduna alındı. Siz modu kapatana kadar yeni post atılmayacak.", reply_markup=dugme)
            return
    if mesaj == "🥰 Bağış":
        bot.send_message(chat, "🥰Madem bu kadar çok istiyorsun. \n\n🏧Papara: <code>1666982412</code> \n🏦İninal: <code>4003140030544</code>")
        return
    if mesaj == "⛓️ Elle Post Paylaş":
        if mj == None:
            bot.send_message(chat, "Lütfen önce bir API kaydedin.")
            return
        if len(mj['kanal']) < 1:
            bot.send_message(chat, "Lütfen önce bir kanal kaydedin.")
            return
        msg = bot.send_message(chat, "Paylaşmamı istediğin hazır postu ilet.", reply_markup=imark)
        bot.register_next_step_handler(msg, pat)
        return
        
    kisi = collection.find_one({"_id": user})
    if kisi == None:
        bot.send_message(chat, "<i>Lütfen alttaki butonları kullan</i>", reply_markup=dugme)
        return
    bot.send_message(chat, "<i>Lütfen alttaki butonları kullan</i>", reply_markup=dugme)
    
def kaynake(message):
    ktext = message.text
    chat = message.chat.id
    user = message.from_user.id
    ktext = ktext.split(",")
    if message.text == None:
        msg = bot.send_message(chat, "Lütfen istediğiniz kaynağın numarasını gönderin.")
        bot.register_next_step_handler(msg, kaynake)
        return
    if message.text == "❌ İptal":
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme)
        return
    bnb = collection.find_one({"_id": user})
    if bnb == None:
        bot.send_message(chat, "Lütfen kaynak seçmeden önce Kaydet butonu ile bilgilerinizi kaydedin.", reply_markup=dugme)
    else:
        collection.update_one({"_id": user}, {"$set":{"kaynak": ktext}})
        bot.send_message(chat, "Kaynak Kaydedildi!", reply_markup=dugme)

def sabloniki(message):
    mesaj = message.text
    chat = message.chat.id
    user = message.from_user.id
    bnb = collection.find_one({"_id": user})
    if message.text == None:
        if mesaj.find("{link}") == -1 or mesaj.find("{aciklama}") == -1:
            msg = bot.send_message(chat, """ ❌<i> Lütfen mesajınızda "{link}" ve "{aciklama}" bulunduğudan emin olun.</i> """)
            bot.register_next_step_handler(msg, sabloniki)
            return
    if message.text == "❌ İptal":
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme)
        return
    if not mesaj.isdigit() and bnb['sira'] == "1":
        if mesaj.find("{link}") == -1 or mesaj.find("{aciklama}") == -1 or mesaj.find("{alink}") == -1:
            msg = bot.send_message(chat, """ ❌<i> Lütfen mesajınızda "{link}", "{alink}" ve "{aciklama}" bulunduğudan emin olun.</i> """)
            bot.register_next_step_handler(msg, sabloniki)
            return
    if not mesaj.isdigit():
        if mesaj.find("{link}") == -1 or mesaj.find("{aciklama}") == -1:
            msg = bot.send_message(chat, """ ❌<i> Lütfen mesajınızda "{link}" ve "{aciklama}" bulunduğudan emin olun.</i> """)
            bot.register_next_step_handler(msg, sabloniki)
            return
    if bnb == None:
        bot.send_message(chat, "Lütfen şablon kaydetmeden önce Kaydet butonu ile bilgilerinizi girin!", reply_markup=dugme)
    else:
        collection.update_one({"_id": user}, {"$set":{"sablon": mesaj}})
        bot.send_message(chat, "Şablon kaydedildi!", reply_markup=dugme)

def kayitapi(message):
    chat = message.chat.id
    mesaj = message.text
    user = message.from_user.id
    if mesaj == "🗑️ Kanal Sil":
        msg = bot.send_message(chat, "Silmek istediğiniz kanalın kayıt numarasını girin.", reply_markup=imark)
        bot.register_next_step_handler(msg, ksil)
        return
    if mesaj == "♻️ API değiştir":
        msg = bot.send_message(chat, "Yeni API adresinizi girin.", reply_markup=imark)
        bot.register_next_step_handler(msg, apikayit)
        return
    if mesaj == "❌ İptal":
        msg = bot.send_message(chat, "İptal Edildi.", reply_markup=dugme)
        return
    if mesaj == "🔗 Site değiştir":
        user = message.from_user.id
        msg = bot.send_message(chat, "<i>Kullanmak istediğiniz sitenin numarasını girin:\n\n<b>    No:1</b>\n    TRLink (Varsayılan)\n\n<b>    No:2</b>\n    PND.TL\n\n<b>    No:3</b>\n    Exe.io\n\n<b>    No:4</b>\n    Ouo.io\n\n<b>    No:5</b>\n    Pubiza</i>\n \nㅤ", reply_markup=imark)
        bot.register_next_step_handler(msg, sitekayit)
        return
    if mesaj == "🤖 Alternatif Ekle":
        msg = bot.send_message(chat, "<i>ALTERNATİF olarak Kullanmak istediğiniz sitenin numarasını girin:\n\n<b>    No:1</b>\n    TRLink (Varsayılan)\n\n<b>    No:2</b>\n    PND.TL\n\n<b>    No:3</b>\n    Exe.io\n\n<b>    No:4</b>\n    Ouo.io\n\n<b>    No:5</b>\n    Pubiza</i>\n \nㅤ", reply_markup=amark)
        bot.register_next_step_handler(msg, altkayit)
        return
    if mesaj == "🔶 Yeni Kanal Ekle":
        bol = collection.find_one({"_id": chat})
        if len(bol['kanal']) > 2:
            bot.send_message(chat, "<i>Üzgünüm en fazla 3 kanal kaydedebilirsiniz.</i>", reply_markup=imark)
            return
        msg = bot.send_message(chat, """📝 <i>Lütfen kanalınızdan bir gönderi iletin.</i>""", reply_markup=imark)
        bot.register_next_step_handler(msg, kanalkayit)
        return
    msg = bot.send_message(chat, "Lütfen alttaki butonları kullanın.", reply_markup=markupp)
    bot.register_next_step_handler(msg, kayitapi)

def ksil(message):
    user = message.from_user.id
    chat = message.chat.id
    if message.text == None:
        msg = bot.send_message(chat, "Lütfen geçerli bir numara verin")
        bot.register_next_step_handler(msg, ksil)
        return
    if message.text == "❌ İptal":
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme)
        return
    mesaj = int(message.text) - 1
    if not message.text.isdigit():
        bot.send_message(chat, "Lütfen geçerli bir numara verin")
        return
    bul = collection.find_one({"_id": user})
    x = bul['kanal']
    try:
        collection.update_one({"_id": user}, {"$pull": {"kanal": x[mesaj]}})
    except:
        bot.send_message(chat, "Yanlış bir numara girdiniz.", reply_markup=dugme)
    else:
        bot.send_message(chat, "Kanalınız silindi.", reply_markup=dugme)

def altkayit(message):
    chat = message.chat.id
    user = message.from_user.id
    smesaj = message.text
    if message.text == None:
        msg = bot.send_message(chat, "Lütfen geçerli bir numara verin")
        bot.register_next_step_handler(msg, ksil)
        return
    if message.text == "❌ İptal":
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme)
        return
    if message.text == "⛔ Alternatif Kaldır":
        collection.update_one({"_id": user}, {"$set": {"altsite": "None", "altapi": "None", "sablon": "1", "sira": "0"}})
        bot.send_message(chat, "Alternatif kaldırıldı, artık postlarınız alternatif linksiz paylaşılacak.", reply_markup=dugme)
        return
    msg = bot.send_message(chat, "✅ Site kaydedildi!\n\nAlternatif sitenizin API adresinizi gönderin.")
    bot.register_next_step_handler(msg, altakayit, smesaj, user, chat)

def altakayit(message, smesaj, user, chat):
    amesaj = message.text
    if message.text == "❌ İptal":
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme)
        return
    if message.text == "⛔ Alternatif Kaldır":
        collection.update_one({"_id": user}, {"$set": {"altsite": "None", "altapi": "None", "sablon": "1", "sira": "0"}})
        bot.send_message(chat, "Alternatif kaldırıldı, artık postlarınız alternatif linksiz paylaşılacak.", reply_markup=dugme)
        return
    collection.update_one({"_id": user}, {"$set": {"altsite": smesaj, "altapi": amesaj}})
    msg = bot.send_message(chat, "✅ Alternatif kaydedildi\n\n<b>Alternatif Nasıl Kullanılsın.\n\n No:1</b>\n <i>Aynı post iki link</i> \n\n<b>No:2</b>\n <i>Bir post birinci servis, bir post alternatif servis.</i>\n\n<b>İstediğiniz sistemin numarasını gönderin.</b>")
    bot.register_next_step_handler(msg, sirasistem)

def apikayit(message):
    token = message.text
    mid = message.id
    user = message.from_user.id
    chat = message.chat.id
    bnb = collection.find_one({"_id": user})
    if message.text == None:
        msg = bot.send_message(chat, "Lütfen geçerli bir API verin.")
        bot.register_next_step_handler(msg, apikayit)
        return
    if message.text == "❌ İptal":
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme)
        return
    if bnb == None:
        kontrol = requests.get("https://ay.live/api/?api={}&url=www.zort.com&format=text&alias=&ct=2".format(token)).text
        if kontrol == "":
            mso = bot.send_message(chat, "❌ Geçersiz bir API verdiniz! Lütfen doğru bir API adresi verin.")
            bot.register_next_step_handler(mso, apikayit)
            return
    key = {"_id": user, "token": token, "kanal": [], "sablon": "1", "kaynak": ["1"], "site": "1", "altapi": "None", "altsite": "None", "sira": "0"}
    if bnb == None:
        collection.insert_one(key)
    else:
        collection.update_one({"_id": user}, {"$set": {"token": token}})
    bot.send_message(chat, "<b>🟢 API kaydedildi!</b>", reply_markup=dugme)

def kanalkayit(message):
    chat = message.chat.id
    user = message.from_user.id
    y = collection.find_one({"_id": user})
    if message.text == "❌ İptal":
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme)
        return
    if not message.forward_from_chat:
        msg = bot.send_message(chat, "↪️ Bunun ne olduğu hakkında bir fikrim yok! Lütfen kanaldan herhangi bir gönderi iletin.")
        bot.register_next_step_handler(msg, kanalkayit)
        return
    kanal = message.forward_from_chat.id
    if kanal in kaynaklar:
        mst = bot.send_message(chat, "Kaynak kanalını nasıl kaydedebilirim ki?")
        bot.register_next_step_handler(mst, kanalkayit)
        return
    if str(kanal) in y['kanal']:
        msl = bot.send_message(chat, "Bu kanalı zaten kaydetmişsiniz")
        bot.register_next_step_handler(chat, kanalkayit)
        return
    try:
        kanalbilgi = bot.get_chat(kanal)
    except:
        msg = bot.send_message(chat, "Botu kanalınızda yönetici eklememişsiniz.")
        bot.register_next_step_handler(msg, kanalkayit)
        return
    yetkiler = bot.get_chat_administrators(kanal)
    for y in yetkiler:
        if y.user.id == user:
            collection.update_one({"_id": user}, {"$push":{"kanal": str(kanal)}})
            bot.reply_to(message,"<b>🟢Kanalınız Kaydedildi.</b>", reply_markup=dugme)
            return
            break
    msz = bot.send_message(chat, "Bu kanal sizin değil 😠")
    bot.register_next_step_handler(msz, kanalkayit)

def pat(message):
    chat = message.chat.id
    user = message.from_user.id
    ptip = message.content_type 
    if message.text == "❌ İptal":
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme)
        return
    if message.content_type == "text":
        msg = bot.send_message(chat, "Lütfen paylaşmamı istediğin postu at")
        bot.register_next_step_handler(msg, pat)
        return
    if message.caption == None:
        msg = bot.send_message(chat, "Lütfen paylaşmamı istediğin postu at")
        bot.register_next_step_handler(msg, pat)
        return
    mesaj = message.caption
    if message.content_type == "video":
        fid = message.video.file_id
    if message.content_type == "photo":
        fid = message.photo[0].file_id
    if message.content_type == "animation":
        fid = message.animation.file_id
    """Açıklama Tespit"""
    pson = mesaj.find("\n")
    paciklama = mesaj[:pson]
    """Link Tespit"""
    psol = mesaj.find("http")
    psag = mesaj.find("\n", psol)
    plink = mesaj[psol:psag].strip()
    pathesap = collection.find_one({"_id": user})
    s = requests.Session()
    link = s.get("https://ay.live/api")
    cookies = dict(link.cookies)
    ptoken = pathesap['token']
    psablon = pathesap['sablon']
    psite = pathesap['site']
    paltapi = pathesap['altapi']
    paltsite = pathesap['altsite']
    psira = pathesap['sira']
    if psira == "2":
        ptoken = paltapi
        psite = paltsite
        collection.update_one({"_id": user}, {"$set": {"sira": "3"}})
    if psira == "3":
        collection.update_one({"_id": user}, {"$set": {"sira": "2"}})
    if not paltapi == "None":
        if paltsite == "1":
            pjson = s.get(f"https://ay.live/api/?api={paltapi}&url={plink}&alias=&ct=1", cookies=cookies).json()
            palink = pjson['shortenedUrl']
        if paltsite == "2":
            pjson = s.get(f"https://www.pnd.tl/api?api={paltapi}&url={plink}&category=6").json()
            palink = pjson['shortenedUrl']
        if paltsite == "3":
            pjson = s.get(f"https://exe.io/api?api={paltapi}&url={plink}").json()
            palink = pjson['shortenedUrl']
        if paltsite == "4":
            palink = s.get(f"http://ouo.io/api/{paltapi}?s={plink}").text
        if paltsite == "5":
            palink = s.get(f"http://pubiza.com/api.php?token={paltapi}&url={plink}&ads_type=adult").text
    if psite == "1":
        pjson = s.get(f"https://ay.live/api/?api={ptoken}&url={plink}&alias=&ct=1", cookies=cookies).json()
        plink = pjson['shortenedUrl']
    if psite == "2":
        pjson = s.get(f"https://www.pnd.tl/api?api={ptoken}&url={plink}&category=6").json()
        plink = pjson['shortenedUrl']
    if psite == "3":
        pjson = s.get(f"https://exe.io/api?api={ptoken}&url={plink}").json()
        plink = pjson['shortenedUrl']
    if psite == "4":
        plink = s.get(f"http://ouo.io/api/{ptoken}?s={plink}").text
    if psite == "5":
        plink = s.get(f"http://pubiza.com/api.php?token={ptoken}&url={plink}&ads_type=adult").text
    if psablon == "1":
        psablon = f"🔥{paciklama}\n\n🔱 TIKLA 👉 {plink}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
    elif psablon == "2" or psablon == "3":
        psablon = f"{paciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {plink}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 @linkgec06"
    elif psablon == "9":
        psablon = f"{paciklama} \n\n𝙇𝙄𝙉𝙆🔗 {plink} \n\n     𝙇𝙄𝙉𝙆🔗 {palink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 @linkk_gecmee"
    elif psablon.find('{alink}') != -1:
                    pasol = psablon.split("{link}")
                    paort = pasol[1].split("{alink}")
                    pasal = pasol[0].split("{aciklama}")
                    psablon = f"{pasal[0]}{paciklama}{pasal[1]}{plink}{paort[0]}{palink}{paort[1]}"
                    
                
    else:
        psablon = psablon.replace("aciklama", "").replace("{link}", "{}").format(paciklama, plink)
    pkanallar = pathesap['kanal']
    pcount = 0
    for pkan in pkanallar:
        pcount = pcount + 1
        knl = bot.get_chat(pkan)
        bot.send_message(chat, "No: {}\n{}".format(pcount, knl.title))
    msg = bot.send_message(chat, "<i>Postun gönderilmesini istediğin kanalın numarasını gönder.\n\n(Tüm kanallarına gönderilmesini istiyorsan <b>0</b> yaz</i>)")
    bot.register_next_step_handler(msg, patiki, psablon, pathesap, fid, ptip)

def patiki(message, psablon, pathesap, fid, ptip):
    chat = message.chat.id
    if message.text == "❌ İptal":
        bot.send_message(chat, "İptal Edildi", reply_markup=dugme)
        return
    if message.text == None:
        msg = bot.send_message(chat, "Lütfen geçerli bir numara girin.")
        bot.register_next_step_handler(msg, patiki, psablon, pathesap, fid, ptip)
        return
    if not message.text.isdigit():
        msg = bot.send_message(chat, "Lütfen geçerli bir numara girin.")
        bot.register_next_step_handler(msg, patiki, psablon, pathesap, fid, ptip)
        return
    pmesaj = int(message.text) - 1
    pkan = pathesap['kanal'][pmesaj]
    if pmesaj == -1:
        for pk in pathesap['kanal']:
            if ptip == "video":
                bot.send_video(pk, fid, caption=psablon)
            if ptip == "photo":
                bot.send_photo(pk, fid, caption=psablon)
        bot.send_message(chat, "Postunuz gönderildi.")
        return
    if ptip == "video":
        bot.send_video(pkan, fid, caption=psablon)
    if ptip == "photo":
        bot.send_photo(pkan, fid, caption=psablon)
    if ptip == "animation":
        bot.send_animation(pkan, fid, caption=psablon)
    bot.send_message(chat, "Postunuz gönderildi.", reply_markup=dugme)

def sitekayit(message):
    chat = message.chat.id
    user = message.from_user.id
    if message.text == None:
        msg = bot.send_message(chat, "Lütfen doğru bir numara girin")
        bot.register_next_step_handler(msg, sitekayit)
        return
    if message.text == "❌ İptal":
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme)
        return
    mesaj = str(message.text)
    if not message.text.isdigit() or len(mesaj) > 1:
        msg = bot.send_message(chat, "Lütfen doğru bir numara girin")
        bot.register_next_step_handler(msg, sitekayit)
        return
    collection.update_one({"_id": user}, {"$set": {"site": mesaj}})
    bot.send_message(chat, "Site Kaydedildi\n\nAPI adresinizi seçtiğiniz siteye göre değiştirmeyi unutmayın.", reply_markup=dugme)

def sirasistem(message):
    user = message.from_user.id
    chat = message.chat.id
    if message.text == None:
        msg = bot.send_message(chat, "Lütfen doğru bir numara girin")
        bot.register_next_step_handler(msg, sitekayit)
        return
    if message.text != "1" and message.text != "2" and message.text != "❌ İptal" and message.text != "⛔ Alternatif Kaldır":  
        msg = bot.send_message(chat, "Lütfen doğru bir numara girin")
        bot.register_next_step_handler(msg, sitekayit)
        return
    if message.text == "⛔ Alternatif Kaldır":
        collection.update_one({"_id": user}, {"$set": {"altsite": "None", "altapi": "None", "sablon": "1", "sira": "0"}})
        bot.send_message(chat, "Alternatif kaldırıldı, artık postlarınız alternatif linksiz paylaşılacak.", reply_markup=dugme)
        return
    if message.text == "❌ İptal":
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme)
        return
    sistem = str(message.text)
    if sistem == "1":
        collection.update_one({"_id": user}, {"$set": {"sablon": "9"}})
    collection.update_one({"_id": user}, {"$set": {"sira": sistem}})
    bot.send_message(chat, "✅ Alternatif Kaydedildi", reply_markup=dugme)

@bot.channel_post_handler(content_types=['photo', 'animation', 'video'])
def poster(message):
    count = 0
    bcount = 0
    ccount = 0
    dcount = 0
    ecount = 0
    mahzen = bot.get_chat(kaynaklar[0])
    bedava = bot.get_chat(kaynaklar[1])
    evi = bot.get_chat(kaynaklar[2])
    bashub = bot.get_chat(kaynaklar[3])
    acikmi = bot.get_chat(kaynaklar[4])
    muho = bot.get_chat(kaynaklar[5])
    chat = message.chat.id
    # Link Mahzeni
    if chat == kaynaklar[0]:
        print("{} postu atılıyor... ".format(mahzen.title))
        mesaj = message.caption
        """  Link tespit  """
        sol = mesaj.find("http")
        sag = mesaj.find("\n", sol)
        mesajb = mesaj[sol:sag].strip()
        if mesajb.startswith("https://t.me/"):
            return
        """  Açıklama tespit  """
        ason = mesaj.find("\n")
        aciklama = mesaj[:ason]
        """  Cookies  """
        s = requests.Session()
        link = s.get("https://ay.live/api")
        cookies = dict(link.cookies)
        binb = collection.find({})
        """ Dosya tespit """
        if message.content_type == "photo":
            medya = message.photo[0].file_id
        if message.content_type == "animation":
            medya = message.animation.file_id
        if message.content_type == "video":
            medya = message.video.file_id
        for hesap in binb:
            kaynak = hesap['kaynak']
            token = hesap['token']
            kanal = hesap['kanal']
            sablon = hesap['sablon']
            user = hesap['_id']
            site = hesap["site"]
            altapi = hesap['altapi']
            altsite = hesap['altsite']
            sira = hesap['sira']
            if sira == "2":
                token = altapi
                site = altsite
                collection.update_one({"_id": user}, {"$set": {"sira": "3"}})
            if sira == "3":
                collection.update_one({"_id": user}, {"$set": {"sira": "2"}})
            if not altapi == "None":
                if altsite == "1":
                    json = s.get(f"https://ay.live/api/?api={altapi}&url={mesajb}&alias=&ct=1", cookies=cookies).json()
                    alink = json['shortenedUrl']
                if altsite == "2":
                    json = s.get(f"https://www.pnd.tl/api?api={altapi}&url={mesajb}&category=6").json()
                    alink = json['shortenedUrl']
                if altsite == "3":
                    json = s.get(f"https://exe.io/api?api={altapi}&url={mesajb}").json()
                    alink = json['shortenedUrl']
                if altsite == "4":
                    alink = s.get(f"http://ouo.io/api/{altapi}?s={mesajb}").text
                if altsite == "5":
                    alink = s.get(f"http://pubiza.com/api.php?token={altapi}&url={mesajb}&ads_type=adult").text
            if "1" in kaynak:
                if site == "1":
                    json = s.get(f"https://ay.live/api/?api={token}&url={mesajb}&alias=&ct=1", cookies=cookies).json()
                    link = json['shortenedUrl']
                if site == "2":
                    json = s.get(f"https://www.pnd.tl/api?api={token}&url={mesajb}&category=6").json()
                    link = json['shortenedUrl']
                if site == "3":
                    json = s.get(f"https://exe.io/api?api={token}&url={mesajb}").json()
                    link = json['shortenedUrl']
                if site == "4":
                    link = s.get(f"http://ouo.io/api/{token}?s={mesajb}").text
                if site == "5":
                    link = s.get(f"http://pubiza.com/api.php?token={token}&url={mesajb}&ads_type=adult").text
                print(f"{kanal} + {link} + {token}")
                if sablon == "1":
                    sablon = f"🔥{aciklama}\n\n🔱 TIKLA 👉 {link}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
                elif sablon == "2" or sablon == "3":
                    sablon = f"{aciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {link}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 @linkgec06"
                elif sablon == "9":
                    sablon = f"{aciklama} \n\n𝙇𝙄𝙉𝙆🔗 {link} \n\n     𝙇𝙄𝙉𝙆🔗 {alink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 @linkk_gecmee"
                elif sablon.find('{alink}') != -1:
                    asol = sablon.split("{link}")
                    aort = asol[1].split("{alink}")
                    asal = asol[0].split("{aciklama}")
                    sablon = f"{asal[0]}{aciklama}{asal[1]}{link}{aort[0]}{alink}{aort[1]}"
                else:
                    sablon = sablon.replace("aciklama", "").replace("{link}", "{}").format(aciklama, link)
                sleep(1)
                for kan in kanal:
                    try:
                        if message.content_type == "photo":
                            bot.send_photo(kan, medya, caption=sablon)
                        if message.content_type == "video":
                            bot.send_video(kan, medya, caption=sablon)
                        if message.content_type == "animation":
                            bot.send_animation(kan, medya, caption=sablon)
                        count = count + 1
                    except Exception as e:
                        print(f"Hatalı kanal: {kanal}")
                        e = str(e)
                        if e.find("bot is not a member") != -1:
                            collection.update_one({"_id": user}, {"$pull": {"kanal": kan}})
                            bot.send_message(user, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                            print(f"{kanal} kayıtlardan silindi.")
                print("Başarılı!")
            else:
                pass
        basari = "{} kaynağından, {} Kanalda Post Paylaşıldı.".format(mahzen.title, count)
        print(basari)
        bot.send_message(botlog, basari)
    # Bedava Link
    elif chat == kaynaklar[1]:
        print("{} postu atılıyor... ".format(bedava.title))
        bmesaj = message.caption
        """ Link tespit """
        bsol = bmesaj.find("http")
        bsag = bmesaj.find("\n", bsol)
        bmesajb = bmesaj[bsol:bsag].strip()
        if bmesajb.startswith("https://t.me/"):
            return
        """ Açıklama tespit """
        bason = bmesaj.find("\n")
        baciklama = bmesaj[:bason]
        """    Cookies    """
        s = requests.Session()
        link = s.get("https://ay.live/api")
        cookies = dict(link.cookies)
        bbinb = collection.find({})
        """ Dosya tespit """
        if message.content_type == "photo":
            bmedya = message.photo[0].file_id
        if message.content_type == "animation":
            medya = message.animation.file_id
        if message.content_type == "video":
            bmedya = message.video.file_id
        for bhesap in bbinb:
            bkaynak = bhesap['kaynak']
            bsablon = bhesap['sablon']
            bsablon = str(bsablon)
            btoken = bhesap['token']
            bkanal = bhesap['kanal']
            buser = bhesap['_id']
            bsite = bhesap['site']
            baltapi = bhesap['altapi']
            baltsite = bhesap['altsite']
            bsira = bhesap['sira']
            if bsira == "2":
                btoken = baltapi
                bsite = baltsite
                collection.update_one({"_id": buser}, {"$set": {"sira": "3"}})
            if bsira == "3":
                collection.update_one({"_id": buser}, {"$set": {"sira": "2"}})
            if not baltapi == "None":
                if baltsite == "1":
                    bjson = s.get(f"https://ay.live/api/?api={baltapi}&url={bmesajb}&alias=&ct=1", cookies=cookies).json()
                    balink = bjson['shortenedUrl']
                if baltsite == "2":
                    bjson = s.get(f"https://www.pnd.tl/api?api={baltapi}&url={bmesajb}&category=6").json()
                    balink = bjson['shortenedUrl']
                if baltsite == "3":
                    bjson = s.get(f"https://exe.io/api?api={baltapi}&url={bmesajb}").json()
                    balink = bjson['shortenedUrl']
                if baltsite == "4":
                    balink = s.get(f"http://ouo.io/api/{baltapi}?s={bmesajb}").text
                if baltsite == "5":
                    balink = s.get(f"http://pubiza.com/api.php?token={baltapi}&url={bmesajb}&ads_type=adult").text
            sleep(1)
            if "2" in bkaynak:
                if bsite == "1":
                    bjson = s.get(f"https://ay.live/api/?api={btoken}&url={bmesajb}&alias=&ct=1", cookies=cookies).json()
                    blink = bjson['shortenedUrl']
                if bsite == "2":
                    bjson = s.get(f"https://www.pnd.tl/api?api={btoken}&url={bmesajb}&category=6").json()
                    blink = bjson['shortenedUrl']
                if bsite == "3":
                    bjson = s.get(f"https://exe.io/api?api={btoken}&url={bmesajb}").json()
                    blink = bjson['shortenedUrl']
                if bsite == "4":
                    blink = s.get(f"http://ouo.io/api/{btoken}?s={bmesajb}").text
                if bsite == "5":
                    blink = s.get(f"http://pubiza.com/api.php?token={btoken}&url={bmesajb}&ads_type=adult").text
                print(f"{bkanal} + {blink} + {btoken}")
                if bsablon == "1":
                    bsablon = f"🔥{baciklama}\n\n🔱 TIKLA 👉 {blink}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
                elif bsablon == "2" or bsablon == "3":
                    bsablon = f"{baciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {blink}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 @linkgec06"
                elif bsablon == "9":
                    bsablon = f"{baciklama} \n\n𝙇𝙄𝙉𝙆🔗 {blink} \n\n     𝙇𝙄𝙉𝙆🔗 {balink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 @linkk_gecmee"
                elif bsablon.find('{alink}') != -1:
                    basol = bsablon.split("{link}")
                    baort = basol[1].split("{alink}")
                    basal = basol[0].split("{aciklama}")
                    bsablon = f"{basal[0]}{baciklama}{basal[1]}{blink}{baort[0]}{balink}{baort[1]}"
                else:
                    bsablon = bsablon.replace("aciklama", "").replace("{link}", "{}").format(baciklama, blink)
                sleep(1)
                for bkan in bkanal:
                    try:
                        if message.content_type == "photo":
                            bot.send_photo(bkan, bmedya, caption=bsablon)
                        if message.content_type == "video":
                            bot.send_video(bkan, bmedya, caption=bsablon)
                        if message.content_type == "animation":
                            bot.send_animation(bkan, bmedya, caption=bsablon)
                        bcount = bcount + 1
                    except Exception as e:
                        print(e)
                        print(f"Hatalı kanal: {bkanal}")
                        e = str(e)
                        print(e)
                        if e.find("bot is not a member") != -1:
                            collection.update_one({"_id": buser}, {"$pull": {"kanal": bkan}})
                            bot.send_message(buser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                            print(f"{bkanal} kayıtlardan silindi.")
                    
                print("Başarılı!")
        bbasari = "{} kaynağından, {} Kanalda Post Paylaşıldı.".format(bedava.title, bcount)
        print(bbasari)
        bot.send_message(botlog, bbasari)
    # Link Evi
    elif chat == kaynaklar[2]:
        print("{} postu atılıyor... ".format(evi.title))
        cmesaj = message.caption
        """ Link tespit """
        csol = cmesaj.find("http")
        csag = cmesaj.find("\n", csol)
        cmesajb = cmesaj[csol:csag].strip()
        if cmesajb.startswith("https://t.me/"):
            return
        """ Açıklama tespit """
        cason = cmesaj.find("\n")
        caciklama = cmesaj[:cason]
        """    Cookies    """
        s = requests.Session()
        link = s.get("https://ay.live/api")
        cookies = dict(link.cookies)
        cbinb = collection.find({})
        """ Dosya tespit """
        if message.content_type == "photo":
            cmedya = message.photo[0].file_id
        if message.content_type == "animation":
            cmedya = message.animation.file_id
        if message.content_type == "video":
            cmedya = message.video.file_id
        for chesap in cbinb:
            ckaynak = chesap['kaynak']
            csablon = chesap['sablon']
            csablon = str(csablon)
            ctoken = chesap['token']
            ckanal = chesap['kanal']
            cuser = chesap['_id']
            csite = chesap['site']
            caltapi = chesap['altapi']
            caltsite = chesap['altsite']
            csira = chesap['sira']
            if csira == "2":
                ctoken = caltapi
                csite = caltsite
                collection.update_one({"_id": cuser}, {"$set": {"sira": "3"}})
            if csira == "3":
                collection.update_one({"_id": cuser}, {"$set": {"sira": "2"}})
            if not caltapi == "None":
                if caltsite == "1":
                    cjson = s.get(f"https://ay.live/api/?api={caltapi}&url={cmesajb}&alias=&ct=1", cookies=cookies).json()
                    calink = cjson['shortenedUrl']
                if caltsite == "2":
                    cjson = s.get(f"https://www.pnd.tl/api?api={caltapi}&url={cmesajb}&category=6").json()
                    calink = cjson['shortenedUrl']
                if caltsite == "3":
                    cjson = s.get(f"https://exe.io/api?api={caltapi}&url={cmesajb}").json()
                    calink = cjson['shortenedUrl']
                if caltsite == "4":
                    calink = s.get(f"http://ouo.io/api/{caltapi}?s={cmesajb}").text
                if caltsite == "5":
                    calink = s.get(f"http://pubiza.com/api.php?token={caltapi}&url={cmesajb}&ads_type=adult").text
            sleep(1)
            if "3" in ckaynak:
                if csite == "1":
                    bjson = s.get(f"https://ay.live/api/?api={ctoken}&url={cmesajb}&alias=&ct=1",
                                  cookies=cookies).json()
                    clink = bjson['shortenedUrl']
                if csite == "2":
                    bjson = s.get(f"https://www.pnd.tl/api?api={ctoken}&url={cmesajb}&category=6").json()
                    clink = bjson['shortenedUrl']
                if csite == "3":
                    bjson = s.get(f"https://exe.io/api?api={ctoken}&url={cmesajb}").json()
                    clink = bjson['shortenedUrl']
                if csite == "4":
                    clink = s.get(f"http://ouo.io/api/{ctoken}?s={cmesajb}").text
                if csite == "5":
                    clink = s.get(f"http://pubiza.com/api.php?token={ctoken}&url={cmesajb}&ads_type=adult").text
                print(f"{ckanal} + {clink} + {ctoken}")
                if csablon == "1":
                    csablon = f"🔥{caciklama}\n\n🔱 TIKLA 👉 {clink}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
                elif csablon == "2" or csablon == "3":
                    csablon = f"{caciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {clink}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 @linkgec06"
                elif csablon == "9":
                    csablon = f"{caciklama} \n\n𝙇𝙄𝙉𝙆🔗 {clink} \n\n     𝙇𝙄𝙉𝙆🔗 {calink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 @linkk_gecmee"
                elif csablon.find('{alink}') != -1:
                    casol = csablon.split("{link}")
                    caort = casol[1].split("{alink}")
                    casal = casol[0].split("{aciklama}")
                    csablon = f"{casal[0]}{caciklama}{casal[1]}{clink}{caort[0]}{calink}{caort[1]}"
                    
                else:
                    csablon = csablon.replace("{link}", "{}").replace("aciklama", "").format(caciklama, clink)
                sleep(1)
                for ckan in ckanal:
                    try:
                        if message.content_type == "photo":
                            bot.send_photo(ckan, cmedya, caption=csablon)
                        if message.content_type == "video":
                            bot.send_video(ckan, cmedya, caption=csablon)
                        if message.content_type == "animation":
                            bot.send_animation(ckan, cmedya, caption=csablon)
                        ccount = ccount + 1
                    except Exception as e:
                        print(e)
                        print(f"Hatalı kanal: {ckanal}")
                        e = str(e)
                        print(e)
                        if e.find("bot is not a member") != -1:
                            collection.update_one({"_id": cuser}, {"$pull": {"kanal": ckan}})
                            bot.send_message(cuser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                            print(f"{ckanal} kayıtlardan silindi.")

                print("Başarılı!")
        cbasari = "{} kaynağından, {} Kanalda Post Paylaşıldı.".format(evi.title, ccount)
        print(evi.title, cbasari)
        bot.send_message(botlog, cbasari)
    # BAŞHUB
    elif chat == kaynaklar[3]:
        print("{} postu atılıyor... ".format(bashub.title))
        dmesaj = message.caption
        """ Link tespit """
        dsol = dmesaj.find("http")
        dsag = dmesaj.find("\n", dsol)
        dmesajb = dmesaj[dsol:dsag].strip()
        if dmesajb.startswith("https://t.me/"):
            return
        """ Açıklama tespit """
        dason = dmesaj.find("\n")
        daciklama = dmesaj[:dason]
        """    Cookies    """
        s = requests.Session()
        link = s.get("https://ay.live/api")
        cookies = dict(link.cookies)
        dbinb = collection.find({})
        """ Dosya tespit """
        if message.content_type == "photo":
            dmedya = message.photo[0].file_id
        if message.content_type == "animation":
            dmedya = message.animation.file_id
        if message.content_type == "video":
            dmedya = message.video.file_id
        for dhesap in dbinb:
            dkaynak = dhesap['kaynak']
            dsablon = dhesap['sablon']
            dsablon = str(dsablon)
            dtoken = dhesap['token']
            dkanal = dhesap['kanal']
            duser = dhesap['_id']
            dsite = dhesap['site']
            daltapi = dhesap['altapi']
            daltsite = dhesap['altsite']
            dsira = dhesap['sira']
            if dsira == "2":
                dtoken = daltapi
                dsite = daltsite
                collection.update_one({"_id": duser}, {"$set": {"sira": "3"}})
            if dsira == "3":
                collection.update_one({"_id": duser}, {"$set": {"sira": "2"}})
            if not daltapi == "None":
                if daltsite == "1":
                    djson = s.get(f"https://ay.live/api/?api={daltapi}&url={dmesajb}&alias=&ct=1", cookies=cookies).json()
                    dalink = djson['shortenedUrl']
                if daltsite == "2":
                    djson = s.get(f"https://www.pnd.tl/api?api={daltapi}&url={dmesajb}&category=6").json()
                    dalink = djson['shortenedUrl']
                if daltsite == "3":
                    djson = s.get(f"https://exe.io/api?api={daltapi}&url={dmesajb}").json()
                    dalink = djson['shortenedUrl']
                if daltsite == "4":
                    dalink = s.get(f"http://ouo.io/api/{daltapi}?s={dmesajb}").text
                if daltsite == "5":
                    dalink = s.get(f"http://pubiza.com/api.php?token={daltapi}&url={dmesajb}&ads_type=adult").text
            sleep(1)
            if "4" in dkaynak:
                if dsite == "1":
                    djson = s.get(f"https://ay.live/api/?api={dtoken}&url={dmesajb}&alias=&ct=1",
                                  cookies=cookies).json()
                    dlink = djson['shortenedUrl']
                if dsite == "2":
                    djson = s.get(f"https://www.pnd.tl/api?api={dtoken}&url={dmesajb}&category=6").json()
                    dlink = djson['shortenedUrl']
                if dsite == "3":
                    djson = s.get(f"https://exe.io/api?api={dtoken}&url={dmesajb}").json()
                    dlink = djson['shortenedUrl']
                if dsite == "4":
                    dlink = s.get(f"http://ouo.io/api/{dtoken}?s={dmesajb}").text
                if dsite == "5":
                    dlink = s.get(f"http://pubiza.com/api.php?token={dtoken}&url={dmesajb}&ads_type=adult").text
                print(f"{dkanal} + {dlink} + {dtoken}")
                if dsablon == "1":
                    dsablon = f"🔥{daciklama}\n\n🔱 TIKLA 👉 {dlink}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
                elif dsablon == "2" or dsablon == "3":
                    dsablon = f"{daciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {dlink}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 @linkgec06"
                elif dsablon == "9":
                    dsablon = f"{daciklama} \n\n𝙇𝙄𝙉𝙆🔗 {dlink} \n\n     𝙇𝙄𝙉𝙆🔗 {dalink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 @linkk_gecmee"
                elif dsablon.find('{alink}') != -1:
                    dasol = dsablon.split("{link}")
                    daort = dasol[1].split("{alink}")
                    dasal = dasol[0].split("{aciklama}")
                    dsablon = f"{dasal[0]}{daciklama}{dasal[1]}{dlink}{daort[0]}{dalink}{daort[1]}"
                else:
                    dsablon = dsablon.replace("{link}", "{}").replace("aciklama", "").format(daciklama, dlink)
                sleep(1)
                for dkan in dkanal:
                    try:
                        if message.content_type == "photo":
                            bot.send_photo(dkan, dmedya, caption=dsablon)
                        if message.content_type == "video":
                            bot.send_video(dkan, dmedya, caption=dsablon)
                        if message.content_type == "animation":
                            bot.send_animation(dkan, dmedya, caption=dsablon)
                        dcount = dcount + 1
                    except Exception as e:
                        print(f"Hatalı kanal: {dkanal}")
                        e = str(e)
                        if e.find("bot is not a member") != -1:
                            collection.update_one({"_id": duser}, {"$pull": {"kanal": dkan}})
                            bot.send_message(duser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                            print(f"{dkanal} kayıtlardan silindi.")

                print("Başarılı!")
        dbasari = "{} kaynağından, {} Kanalda Post Paylaşıldı.".format(bashub.title, dcount)
        print(dbasari)
        bot.send_message(botlog, dbasari)
    # Açık mı link
    elif chat == kaynaklar[4]:
        print("{} postu atılıyor... ".format(acikmi.title))
        emesaj = message.caption
        """ Link tespit """
        esol = emesaj.find("http")
        esag = emesaj.find("\n", esol)
        emesajb = emesaj[esol:esag].strip()
        if emesajb.startswith("https://t.me/"):
            return
        """ Açıklama tespit """
        eason = emesaj.find("\n")
        eaciklama = emesaj[:eason]
        """    Cookies    """
        s = requests.Session()
        link = s.get("https://ay.live/api")
        cookies = dict(link.cookies)
        ebinb = collection.find({})
        """ Dosya tespit """
        if message.content_type == "photo":
            emedya = message.photo[0].file_id
        if message.content_type == "animation":
            emedya = message.animation.file_id
        if message.content_type == "video":
            emedya = message.video.file_id
        for ehesap in ebinb:
            ekaynak = ehesap['kaynak']
            esablon = ehesap['sablon']
            esablon = str(esablon)
            etoken = ehesap['token']
            ekanal = ehesap['kanal']
            euser = ehesap['_id']
            esite = ehesap['site']
            ealtapi = ehesap['altapi']
            ealtsite = ehesap['altsite']
            esira = ehesap['sira']
            if esira == "2":
                etoken = ealtapi
                esite = ealtsite
                collection.update_one({"_id": euser}, {"$set": {"sira": "3"}})
            if esira == "3":
                collection.update_one({"_id": euser}, {"$set": {"sira": "2"}})
            if not ealtapi == "None":
                if ealtsite == "1":
                    ejson = s.get(f"https://ay.live/api/?api={ealtapi}&url={emesajb}&alias=&ct=1", cookies=cookies).json()
                    ealink = ejson['shortenedUrl']
                if ealtsite == "2":
                    ejson = s.get(f"https://www.pnd.tl/api?api={ealtapi}&url={emesajb}&category=6").json()
                    ealink = ejson['shortenedUrl']
                if ealtsite == "3":
                    ejson = s.get(f"https://exe.io/api?api={ealtapi}&url={emesajb}").json()
                    ealink = ejson['shortenedUrl']
                if ealtsite == "4":
                    ealink = s.get(f"http://ouo.io/api/{ealtapi}?s={emesajb}").text
                if ealtsite == "5":
                    ealink = s.get(f"http://pubiza.com/api.php?token={ealtapi}&url={emesajb}&ads_type=adult").text
            sleep(1)
            if "5" in ekaynak:
                if esite == "1":
                    ejson = s.get(f"https://ay.live/api/?api={etoken}&url={emesajb}&alias=&ct=1",
                                  cookies=cookies).json()
                    elink = ejson['shortenedUrl']
                if esite == "2":
                    ejson = s.get(f"https://www.pnd.tl/api?api={etoken}&url={emesajb}&category=6").json()
                    elink = ejson['shortenedUrl']
                if esite == "3":
                    ejson = s.get(f"https://exe.io/api?api={etoken}&url={emesajb}").json()
                    elink = ejson['shortenedUrl']
                if esite == "4":
                    elink = s.get(f"http://ouo.io/api/{etoken}?s={emesajb}").text
                if esite == "5":
                    elink = s.get(f"http://pubiza.com/api.php?token={etoken}&url={emesajb}&ads_type=adult").text
                print(f"{ekanal} + {elink} + {etoken}")
                if esablon == "1":
                    esablon = f"🔥{eaciklama}\n\n🔱 TIKLA 👉 {elink}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
                elif esablon == "2" or esablon == "3":
                    esablon = f"{eaciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {elink}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 @linkgec06"
                elif esablon == "9":
                    esablon = f"{eaciklama} \n\n𝙇𝙄𝙉𝙆🔗 {elink} \n\n     𝙇𝙄𝙉𝙆🔗 {ealink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 @linkk_gecmee"
                elif esablon.find('{alink}') != -1:
                    easol = esablon.split("{link}")
                    eaort = easol[1].split("{alink}")
                    easal = easol[0].split("{aciklama}")
                    esablon = f"{easal[0]}{eaciklama}{easal[1]}{elink}{eaort[0]}{ealink}{eaort[1]}"
                else:
                    esablon = esablon.replace("{link}", "{}").replace("aciklama", "").format(eaciklama, elink)
                sleep(1)
                for ekan in ekanal:
                    try:
                        if message.content_type == "photo":
                            bot.send_photo(ekan, emedya, caption=esablon)
                        if message.content_type == "video":
                            bot.send_video(ekan, emedya, caption=esablon)
                        if message.content_type == "animation":
                            bot.send_animation(ekan, emedya, caption=esablon)
                        ecount = ecount + 1
                    except Exception as e:
                        print(f"Hatalı kanal: {ekanal}")
                        e = str(e)
                        if e.find("bot is not a member") != -1:
                            collection.update_one({"_id": euser}, {"$pull": {"kanal": ekan}})
                            bot.send_message(euser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                            print(f"{ekanal} kayıtlardan silindi.")

                print("Başarılı!")
        ebasari = "{} kaynağından, {} Kanalda Post Paylaşıldı.".format(acikmi.title, ecount)
        print(ebasari)
        bot.send_message(botlog, ebasari)


def gunluk():
    while 0 < 1:
        zaman = datetime.datetime.now()
        if zaman.hour == 11 and zaman.minute == 50:
            kanals = 0
            users = 0
            kullanicilar = collection.find({})
            for kullanici in kullanicilar:
                users += 1
                for kul in kullanici['kanal']:
                    kanals += 1
            msg = bot.send_message(botlog, "👥 Toplam Kullanıcı Sayısı: {}\n📢 Toplam Kayıtlı Kanal Sayısı: {}\n\nHer gün saat 22:00'da otomatik olarak güncel veriler paylaşılacak.".format(users, kanals))
            bot.pin_chat_message(botlog, msg.message_id)
        time.sleep(60)
    
timThr = threading.Thread(target=gunluk)
timThr.start()

bot.polling(none_stop=True, interval=0)
