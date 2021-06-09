import requests
from requests import get, Session
from os import environ
import asyncio
from time import sleep
from pymongo import MongoClient
import time, datetime
import threading
import os, signal
import logging
from typing import Dict
import Colorer
from telegram import Bot, ParseMode, ReplyKeyboardMarkup, Update, ReplyKeyboardRemove, KeyboardButton, ForceReply, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    Defaults,
    ExtBot,
    ConversationHandler,
    CallbackContext,
    CallbackQueryHandler,
)

mpass = os.environ['MONGOPASS']
mongo = f"os.environ["MONGO_URI"]"

pid = os.getpid()
open("pid.txt", "w").write(str(pid))
print(pid)

cluster = MongoClient(mongo)
db = cluster["OtoPost"]
collection = db["Kanallar"]
OzelCol = db["Özel Kaynaklar"]
karaliste = collection.find_one({"_id": 0})
bottoken = karaliste['bottoken']
bot = ExtBot(bottoken, defaults=Defaults(parse_mode=ParseMode.HTML, run_async=True))

sahip = 1302980840
fixer = 1687646994
adminlist = [1687646994,1302980840]

def bildir(neyi='Boş Bildirim Testi !'):
    for i in adminlist:
        try:
            bot.send_message(i,neyi)
        except:
            pass

kaynaklar = [-1001190898326, -1001190898326, -1001190898326, -1001190898326, -1001190898326, -1001190898326, -1001190898326]

for i in kaynaklar:
    index = int(kaynaklar.index(i))
    if index == 0:
        try:
            mahzen = bot.get_chat(kaynaklar[0]) 
        except:
            bildir('Link Mahzeni kaynağına bot ulaşamıyor')
    elif index == 1:
        try:
            bedava = bot.get_chat(kaynaklar[1])
        except:
            bildir('Bedava Linkler kaynağına bot ulaşamıyor')
    elif index == 2:
        try:
            evi = bot.get_chat(kaynaklar[2])
        except:
            bildir('Link Evi kaynağına bot ulaşamıyor')
    elif index == 3:
        try:
           bashub = bot.get_chat(kaynaklar[3])
        except:
           bildir('Başhub kaynağına bot ulaşamıyor')
    elif index == 4:
        try:
            acikmi = bot.get_chat(kaynaklar[4])
        except:
            bildir('Açık mı kaynağına bot ulaşamıyor')
    elif index == 5:
        try:
            muho = bot.get_chat(kaynaklar[5])
        except:
            bildir('Muho kaynağına bot ulaşamıyor')
    elif index == 6:
        try:
            tutan = bot.get_chat(kaynaklar[6])
        except:
            bildir('Tutan kaynağına bot ulaşamıyor')
    else:
        qqq = 'Bu ne ? : {}'.format(i)
        bildir(qqq)


kara = karaliste['kara']

ALTMENU, APIDEGISTIR, KANALKAYDET = range(3)

OZELKAYNAK = range(1)

ALTAPI = range(1)

SABLON = range(1)

PATPOST = range(1)

markup = ForceReply(selective=False)

def dugme():
    dugme = ReplyKeyboardMarkup(keyboard=[['⚙️ Menü'], ['🔧 Kaynak', '📏 Şablon'], ['▶️ SFS Modu', '🥰 Bağış'], ['⛓️ Elle Post Paylaş']], resize_keyboard=True)
    
    return dugme

def markupp():
    markupp = ReplyKeyboardMarkup(keyboard=[['🔶 Yeni Kanal Ekle', '🗑️ Kanal Sil'], ['♻️ API değiştir', '🔗 Site değiştir'], ['🤖 Alternatif Ekle'], ['↩️ Ana Menü']], row_width=2, one_time_keyboard=True, resize_keyboard=True)

    return markupp

def imark():
    imark = ReplyKeyboardMarkup(keyboard=[['❌ İptal']], one_time_keyboard=True, resize_keyboard=True, selective=True)

    return imark

def dagme():
    dagme = ReplyKeyboardMarkup(keyboard=[['📝 Kaydet']], row_width=2, one_time_keyboard=True, resize_keyboard=True, selective=True)
    butonbir = KeyboardButton('📝 Kaydet')
    dagme.add(butonbir)
    return dagme

zaman = datetime.datetime.now()
saat = zaman.hour 
dakika = zaman.minute
logd = "{}.{}.{} - {}.{}".format(zaman.year, zaman.month, zaman.day, saat, dakika)

class patc:
    def __init__(self, sira, psablon, fid, ptip):
        self.sira = 0
        self.psablon = None
        self.fid = None
        self.ptip = None

def setup_logger():
    global logger
    file_handler = logging.FileHandler(f'Loglar/{logd}.txt', 'w', 'utf-8')
    stream_handler = logging.StreamHandler()
    logger = logging.getLogger("main_log")
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

#logger = getLogger(__name__)

setup_logger()

logger.info(f"Saat: {saat}:{dakika}")

def start(update, context):
    user = update.message.from_user.id
    chat = update.message.chat.id
    bot = context.bot
    if user in kara:
        bot.send_message(chat, "🤓 Üzgünüm senin gibi aptal birisi için çalışmıyorum")
        return
    kat = collection.find_one({"_id": user})
    ref = update.message.text.split()[1] if len(update.message.text.split()) > 1 else None
    kyn = str(ref.split('k')[-1]) if len(update.message.text.split()) > 1 else None
    key = {"_id": user, "kanal": [], "sablon": "1", "kaynak": [kyn], "site": "1", "altapi": "None", "altsite": "None", "sira": "0", "ozel": False}
    if ref == "Kaynak1":
        if kat == None:
            collection.insert_one(key)
            bot.send_message(chat, "🏋🏻 {} referansı ile geldiniz!".format(mahzen.title))
        else:
            if not kat['ozel']:
                collection.update_one({"_id": user}, {"$push": {"kaynak": "1"}})
                bot.send_message(chat, "Kaynağınız Eklendi!")
            else:
                bot.send_message(chat, "Özel kaynağınız olduğu için başka kaynak kullanamazsınız!")
            return
    if ref == "Kaynak2":
        if kat == None:
            collection.insert_one(key)
            bot.send_message(chat, "🏋🏻 {} referansı ile geldiniz!".format(bedava.title))
        else:
            if not kat['ozel']:
                collection.update_one({"_id": user}, {"$push": {"kaynak": "2"}})
                bot.send_message(chat, "Kaynağınız Eklendi!")
            else:
                bot.send_message(chat, "Özel kaynağınız olduğu için başka kaynak kullanamazsınız!")
            return
    if ref == "Kaynak3":
        if kat == None:
            collection.insert_one(key)
            bot.send_message(chat, "🏋🏻 {} referansı ile geldiniz!".format(evi.title))
        else:
            if not kat['ozel']:
                collection.update_one({"_id": user}, {"$push": {"kaynak": "3"}})
                bot.send_message(chat, "Kaynağınız Eklendi!")
            else:
                bot.send_message(chat, "Özel kaynağınız olduğu için başka kaynak kullanamazsınız!")
            return
    if ref == "Kaynak4":
        if kat == None:
            collection.insert_one(key)
            bot.send_message(chat, "🏋🏻 {} referansı ile geldiniz!".format(bashub.title))
        else:
            if not kat['ozel']:
                collection.update_one({"_id": user}, {"$push": {"kaynak": "4"}})
                bot.send_message(chat, "Kaynağınız Eklendi!")
            else:
                bot.send_message(chat, "Özel kaynağınız olduğu için başka kaynak kullanamazsınız!")
            return
    if ref == "Kaynak5":
        if kat == None:
            collection.insert_one(key)
            bot.send_message(chat, "🏋🏻 {} referansı ile geldiniz!".format(acikmi.title))
        else:
            if not kat['ozel']:
                collection.update_one({"_id": user}, {"$push": {"kaynak": "5"}})
                bot.send_message(chat, "Kaynağınız Eklendi!")
            else:
                bot.send_message(chat, "Özel kaynağınız olduğu için başka kaynak kullanamazsınız!")
            return
    if ref == "Kaynak6":
        if kat == None:
            collection.insert_one(key)
            bot.send_message(chat, "🏋🏻 {} referansı ile geldiniz!".format(tutan.title))
        else:
            if not kat['ozel']:
                collection.update_one({"_id": user}, {"$push": {"kaynak": "6"}})
                bot.send_message(chat, "Kaynağınız Eklendi!")
            else:
                bot.send_message(chat, "Özel kaynağınız olduğu için başka kaynak kullanamazsınız!")
            return
    if ref == "Kaynak7":
        if kat == None:
            collection.insert_one(key)
            bot.send_message(chat, "🏋🏻 {} referansı ile geldiniz!".format(muho.title))
        else:
            if not kat['ozel']:
                collection.update_one({"_id": user}, {"$push": {"kaynak": "7"}})
                bot.send_message(chat, "Kaynağınız Eklendi!")
            else:
                bot.send_message(chat, "Özel kaynağınız olduğu için başka kaynak kullanamazsınız!")
            return
    
    mention = "@"+update.message.from_user.username if update.message.from_user.username else update.message.from_user.first_name
    if kat == None:
        bot.send_message(chat, """
✨ <b>Merhaba {}!</b>

❔<b>Ne İşe Yarıyor? </b>
<i>Bu update.message sizin seçtiğiniz kaynak kanalında paylaşılan postların linklerini otomatik olarak kısaltıp sizin kanalınızda paylaşır.</i>

❔<b>Nasıl Kullanılır?</b>
<i>1. Adım: Botu kanlınıza yönetici olarak ekleyin.
2. Adım: Kaydet butonunu kullanarak bilgilerinizi kaydedin.
3. Adım: <b>KANALINIZDA</b> /onayla yazın.
4. Adım: Keyfini çıkarın.</i>

<b>❤️ Geliştirici & Sahip : @Pharex
👨🏻‍🔧 Fix & Eklentiler : @berce</b>


📔        <b>@OtoPosterBotLog</b>
""".format(mention), disable_web_page_preview=True, reply_markup=dagme())
    else:
        bot.send_message(chat, """
✨ <b>Merhaba {}!</b>

❔<b>Ne İşe Yarıyor? </b>
<i>Bu update.message sizin seçtiğiniz kaynak kanalında paylaşılan postların linklerini otomatik olarak kısaltıp sizin kanalınızda paylaşır.</i>

❔<b>Nasıl Kullanılır?</b>
<i>1. Adım: Botu kanlınıza yönetici olarak ekleyin.
2. Adım: Kaydet butonunu kullanarak bilgilerinizi kaydedin.
3. Adım: <b>KANALINIZDA</b> /onayla yazın.
4. Adım: Keyfini çıkarın.</i>

<b>❤️ Geliştirici & Sahip : @Pharex
👨🏻‍🔧 Fix & Eklentiler : @berce</b>

  📔        <b>@OtoPosterBotLog</b>
""".format(mention), disable_web_page_preview=True, reply_markup=dugme())

def stats(message):
    kanals = 0
    users = 0
    toplam = 0
    chat = update.message.chat.id
    user = update.message.from_user.id
    kum = []
    kulkum = []
    if not user in [sahip,fixer]:
        bot.send_message(chat, "Sen benim sahibim değilsin!")
        return
    msg = bot.send_message(chat, "<code> Veriler toplanıyor...</code>")
    kullanicilar = collection.find({})
    for kullanici in kullanicilar:
        if not kullanici in kulkum:
            kulkum.append(kullanici)
            users += 1
        for kul in kullanici['kanal']:
            if not kul in kum:
                kum.append(kul)
                time.sleep(1)
                kanals += 1
                try:
                    uye = bot.get_chat_members_count(kul)
                    print(uye)
                except Exception as e:
                    logger.error(e)
                    time.sleep(60)
                toplam += uye
          
    toplam = toplam / 1000
    toplam = round(toplam, 1)
    bot.edit_message_text("Toplam Kullanıcı Sayısı: {}\nToplam Kayıtlı Kanal Sayısı: {}\nToplam Kitle: {}K".format(users, kanals, toplam), chat, msg.message_id)

def bul(message):
    cnt = update.message.text.split()[1] if len(update.message.text.split()) > 1 else int(update.message.from_user.id)
    if not update.message.from_user.id in adminlist:
        bot.send_message(update.message.chat.id, "Sie")
        return
    try:
        cnt = collection.find({"_id": int(cnt)})
        for c in cnt:
            bot.send_message(update.message.chat.id, 'ID: {}\nToken: {} \nKaynak: {} \nSite: {} \nKanal: {} \nAlt Token: {} \n Alt Site: {} \n Özel Kaynak: {}'.format(c['_id'], c['token'], c['kaynak'], c['site'], c['kanal'], c['altapi'], c['altsite'], c['ozel']))
    except:
        pass
    try:
        cnt = collection.find({"token": cnt})
        for c in cnt:
            bot.send_message(update.message.chat.id, 'ID: {}\nToken: {} \nKaynak: {} \nSite: {} \nKanal: {} \nAlt Token: {} \n Alt Site: {} \n Özel Kaynak: {}'.format(c['_id'], c['token'], c['kaynak'], c['site'], c['kanal'], c['altapi'], c['altsite'], c['ozel']))
    except:
        pass
    try:
        cnt = collection.find({"altapi": cnt})
        for c in cnt:
            bot.send_message(update.message.chat.id, 'ID: {}\nToken: {} \nKaynak: {} \nSite: {} \nKanal: {} \nAlt Token: {} \n Alt Site: {} \n Özel Kaynak: {}'.format(c['_id'], c['token'], c['kaynak'], c['site'], c['kanal'], c['altapi'], c['altsite'], c['ozel']))
    except:
        pass
    try:
        cnt = collection.find({"kanal": [str(cnt)]})
        for c in cnt:
            bot.send_message(update.message.chat.id, 'ID: {}\nToken: {} \nKaynak: {} \nSite: {} \nKanal: {} \nAlt Token: {} \n Alt Site: {} \n Özel Kaynak: {}'.format(c['_id'], c['token'], c['kaynak'], c['site'], c['kanal'], c['altapi'], c['altsite'], c['ozel']))
    except:
        pass
    try:
        cnt = collection.find({"site": str(cnt)})
        for c in cnt:
            bot.send_message(update.message.chat.id, 'ID: {}\nToken: {} \nKaynak: {} \nSite: {} \nKanal: {} \nAlt Token: {} \n Alt Site: {} \n Özel Kaynak: {}'.format(c['_id'], c['token'], c['kaynak'], c['site'], c['kanal'], c['altapi'], c['altsite'], c['ozel']))
    except:
        pass

def ona(m, context):
    cid = m.message.chat.id
    bot.send_message(cid, "Bu komutu kanalınızda kullanmalısınız.")

def durdur(update, context):
    chat = update.message.chat.id
    user = update.message.from_user.id
    if user in kara:
        bot.send_message(chat, "🤓 Üzgünüm senin gibi aptal birisi için çalışmıyorum")
        return
    try:
        collection.delete_one({"_id": user})
    except:
        update.message.reply_text("<b>Henüz bir kanal kaydetmemişsiniz.</b>")
    else:
        update.message.reply_text("<b>Kanalınız Silindi!</b>")

def kpostsil(update, context):
    chat = update.message.chat.id
    if not chat in kaynaklar:
        return
    data = db[str(chat)].find({})
    spcount = 0
    for d in data:
        try:
            bot.delete_message(d['_id'], d['pid'])
        except Exception as e:
            logger.error(e)
        else:
            spcount += 1
    bot.send_message(chat, f"{spcount} Post Silindi.")

def cpostsil(message):
    chat = update.message.chat.id
    if chat != sahip:
        return
    hedef = update.message.text.split()[1]
    data = db[str(hedef)].find({})
    spcount = 0
    for d in data:
        try:
            bot.delete_message(d['_id'], d['pid'])
        except Exception as e:
            logger.error(e)
        else:
            spcount += 1
    bot.send_message(chat, f"{spcount} Post Silindi.")
    
def duy(m, context):
    chat = m.chat.id
    if chat != sahip:
        return
    duyurus = 0
    if m.message.reply_to_message:
        duyurumsg = m.reply_text_update.message.text
        kullanicilar = collection.find({})
        for kullanici in kullanicilar:
            try:
                dmsg = bot.send_message(kullanici['_id'], duyurumsg)
                duyurus += 1
            except Exception as e:
                logger.error(e)
            else:
                kont = db[str(chat)].find_one({"_id": kullanici['_id']})
                if kont == None:
                    db[str(chat)].insert_one({"_id": kullanici['_id'], "mid": dmsg.message_id})
                else:
                    db[str(chat)].update_one({"_id": kullanici['_id']}, {"$set": {"mid": dmsg.message_id}})
                    
        bot.send_message(chat, "{} Kişiye Duyuru Mesajı Gönderildi!".format(duyurus))

def dsil(m, context):
    chat = m.message.chat.id
    if chat != sahip:
        return
    sd = 0
    tumks = db[str(chat)].find({})
    for t in tumks:
        try:
            bot.delete_message(t['_id'], t['mid'])
        except Exception as e:
            logger.error(e)
        else:
            sd += 1
    bot.send_message(chat, "{} Duyuru Mesajı Silindi!".format(sd))
        
def post(update, context):
    chat = update.channel_post.chat.id
    mid = update.channel_post.message_id
    msj = update.channel_post.reply_text("Tamamdır!")
    sleep(1)
    mids = msj.message_id
    try:
        bot.delete_message(chat, mid)
        bot.delete_message(chat, mids)
    except:
        pass

def zaman(update, context):
    chat = update.message.chat.id
    msj = update.message.reply_to_message.text if update.message.reply_to_message else None
    if msj == None:
        bot.send_message(chat, "Bu komut bir mesajı yanıtlayarak kullanılmalıdır.")
        return
    if chat == 822071585 or chat == 1302980840:
        collection.update_one({"_id": 0}, {"$set": {"mahzen": msj}})
    if chat == 755051086:
        collection.update_one({"_id": 0}, {"$set": {"bedava": msj}})
    if chat == 818136673:
        collection.update_one({"_id": 0}, {"$set": {"evi": msj}})
    if chat == 1082754978:
        collection.update_one({"_id": 0}, {"$set": {"bashub": msj}})
    if chat == 1573589253:
        collection.update_one({"_id": 0}, {"$set": {"acikmi": msj}})
    if chat == 814887530:
        collection.update_one({"_id": 0}, {"$set": {"tutan": msj}})
    if chat == 1613760981:
        collection.update_one({"_id": 0}, {"$set": {"muho": msj}})
    bot.send_message(chat, "Kaydedildi.")

import html
import json
import traceback
def error_handler(update: object, context: CallbackContext) -> None:
    logger.error(msg="Bir Hata oluştu:", exc_info=context.error)
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = ''.join(tb_list)
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        f'An exception was raised while handling an update\n'
        f'<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}'
        '</pre>\n\n'
        f'<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n'
        f'<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n'
        f'<pre>{html.escape(tb_string)}</pre>'
    )

    context.bot.send_message(chat_id=1302980840, text=message, parse_mode=ParseMode.HTML)

def sabloncall(call, context):
    user = call.effective_user.id
    chat = call.effective_chat.id
    mesajid = call.effective_message.message_id
    bot.delete_message(user, mesajid)
    if collection.find_one({"_id": user})['sira'] == "1":
        msz = bot.send_message(chat, "<i>Oluşturduğunuz şablonda</i> <b>{aciklama}, {alink}</b> ve <b>{link}</b> <i>kelimelerinin bulunduğundan emin olun yoksa şablon çalışmaz</i>", reply_markup=imark())
        return SABLON
    else:
        msz = bot.send_message(chat, "<i>Oluşturduğunuz şablonda</i> <b>{aciklama}</b> ve <b>{link}</b> <i>kelimelerinin bulunduğundan emin olun yoksa şablon çalışmaz</i>", reply_markup=imark())
        return SABLON

def altcall(call, context):
    user = call.effective_user.id
    chat = call.effective_chat.id
    mesajid = call.effective_message.message_id
    smesaj = str(call.callback_query.data.split("-")[1])
    sss = str(call.callback_query.data.split("-")[2])
    context.user_data['asite'] = smesaj
    context.user_data['sistem'] = sss
    call.callback_query.answer(call.callback_query.id, "✅ Site Kaydedildi!")
    bot.edit_message_text("✅ Alternatif site kaydedildi.", user, mesajid)
    bot.send_message(chat, "📝 Alternatif API adresinizi gönderin.", reply_markup=imark())
    return ALTAPI

def kaynakcall(call, context):
    user = call.effective_user.id
    chat = call.effective_chat.id
    kkul = collection.find_one({"_id": user})
    if kkul['ozel']:
        call.callback_query.edit_message_text(text="<b>Özel kaynak kullandığınız için kaynak başka kaynak kullanamazsınız!</b>")
        return
    mesajid = call.effective_message.message_id
    kys = str(call.callback_query.data.split("-")[1])
    if kys in kkul['kaynak']:
        collection.update_one({"_id": user}, {"$pull": {"kaynak": kys}})
        call.callback_query.answer(text="❌ Kaynak Kaldırıldı")
    else:
        collection.update_one({"_id": user}, {"$push": {"kaynak": kys}})
        call.callback_query.answer(text="✅ Kaynak Eklendi")
    call.callback_query.edit_message_text(text="<b>Kullanmak istediğiniz kaynak kanalını seçin.</b>", reply_markup=kaynakmark(user))

def ozelkaynakcall(call, context):
    user = call.effective_user.id
    chat = call.effective_chat.id
    mesajid = call.effective_message.message_id
    if OzelCol.find_one({"_id": user}) == None:
        OzelCol.insert_one({"_id": user}) 
    bot.delete_message(chat, mesajid)
    bot.send_message(chat, """<b>Yapmanız Gerekenler</b>
<i>
1 - Kaynak yapacağınız kanal oluşturun.
2 - Oluşturduğunuz kanaldan update.messagea bir mesaj iletin.</i>""", reply_markup=imark())
    return OZELKAYNAK


def callback_query(call, context):
    user = call.effective_user.id
    chat = call.effective_chat.id
    mesajid = call.callback_query.message.message_id
    """ İptal """
    if call.callback_query.data == "akaldır":
        collection.update_one({"_id": user}, {"$set": {"altsite": "None", "altapi": "None", "sira": "0", "sablon": "1"}})
        msg = bot.edit_message_text("⛔ Alternatif Kaldırıldı.", user, mesajid)
        call.callback_query.answer("⛔ Alternatif Kaldırıldı.")
    if call.callback_query.data == "aiptal":
        bot.edit_message_text("<i>İptal Edildi</i>", user, mesajid)
    if call.callback_query.data == "iptal":
        bot.edit_message_text("<i>İptal Edildi</i>", user, mesajid)
    """ Kanal Sil """
    if call.callback_query.data.startswith("sil"):
        kul = collection.find_one({"_id": user})
        s = int(call.callback_query.data.split("-")[1])
        collection.update_one({"_id": user}, {"$pull": {"kanal": kul['kanal'][s]}})
        bot.edit_message_text("Kanalınız Silindi!", user, mesajid)
        call.callback_query.answer(call.callback_query.id, "Kanalınız Silindi!")
    """ Site Değiştir """
    if call.callback_query.data.startswith("site"):
        skul = collection.find_one({"_id": user})
        ss = str(call.callback_query.data.split("-")[1])
        collection.update_one({"_id": user}, {"$set": {"site": ss}})
        bot.edit_message_text("Site Kaydedildi!\n\nAPI adresinizi seçtiğiniz siteye göre değiştirmeyi unutmayın.", user, mesajid)
        call.callback_query.answer(call.callback_query.id, "Site Kaydedildi!")
    """ Alternatif """
    if call.callback_query.data.startswith("sistem"):

        sss = str(call.callback_query.data.split("-")[1])
        collection.update_one({"_id": user}, {"$set": {"sira": sss}})
        call.callback_query.answer(call.callback_query.id, "✅ Site Kaydedildi!")
        bot.edit_message_text("Alternatif olarak kullanmak istediğiniz siteyi seçin.", user, mesajid)
        bot.edit_message_reply_markup(chat_id=chat, message_id=mesajid, reply_markup=altsitemarkup(sss))
    """ Kaynak """
    if call.callback_query.data.startswith("zaman"):
        saat = collection.find_one({"_id": 0})
        dgr = int(call.callback_query.data.split("-")[1])
        if dgr == 1:
            call.callback_query.answer(show_alert=True, text=saat['mahzen'])
        if dgr == 2:
            call.callback_query.answer(show_alert=True, text=saat['bedava'])
        if dgr == 3:
            call.callback_query.answer(show_alert=True, text=saat['evi'])
        if dgr == 4:
            call.callback_query.answer(show_alert=True, text=saat['bashub'])
        if dgr == 5:
            call.callback_query.answer(show_alert=True, text=saat['acikmi'])
        if dgr == 6:
            call.callback_query.answer(show_alert=True, text=saat['tutan'])
        if dgr == 7:
            call.callback_query.answer(show_alert=True, text=saat['muho'])
    if call.callback_query.data == "okay":
        bot.edit_message_text("""<b>Özel Kaynak Hakkında Bilmeniz Gerekenler</b>\n\n<i>- Özel kaynak ayarlarsanız başka kaynak seçemezsiniz.\n- Sadece size özeldir başkası kullanamaz.\n- Özel kaynağa kısaltılmamış link atmanız gerekiyor. Kısaltılmış linkli post atarsanız update.message linki geçmez direkt olarak kısaltılmış linki tekrar kısaltır.</i>\n\n<b>Alttaki butona bastığınız zaman işlem iptal edilemez!</b>""", chat, mesajid)
        bot.edit_message_reply_markup(chat, mesajid, reply_markup=ozelmark())
    if call.callback_query.data == "okayk":
        collection.update_one({"_id": user}, {"$set": {"ozel": False}})
        OzelCol.delete_one({"_id": user})
        bot.edit_message_text("Özel Kaynak Kaldırıldı.", chat, mesajid)
    """ PAT """
    if call.callback_query.data.startswith("pat"):
        back = call.callback_query.data.split("-")
        o = int(back[1]) - 1
        ptip = context.user_data['ptip']
        psablon = context.user_data['psablon']
        fid = context.user_data['fid']
        
        kanal = collection.find_one({"_id": user})['kanal']
        if o == -1:
            for kan in kanal:
                if ptip == 'photo':
                    bot.send_photo(kan, fid, caption=psablon)
                if ptip == 'video':
                    bot.send_video(kan, fid, caption=psablon)
                if ptip == 'animation':
                    bot.send_animation(kan, fid, caption=psablon)
            bot.edit_message_text("✅<b>Postunuz Tüm Kanallarınıza Gönderildi!</b>", user, mesajid)
            context.user_data.clear()
            return ConversationHandler.END
        if ptip == 'photo':
            bot.send_photo(kanal[o], fid, caption=psablon)
        if ptip == 'video':
            bot.send_video(kanal[o], fid, caption=psablon)
        if ptip == 'animation':
            bot.send_animation(kanal[o], fid, caption=psablon)
        bot.edit_message_text("✅<b>Postunuz  Kanalınıza Gönderildi!</b>", user, mesajid)
        context.user_data.clear()
        return ConversationHandler.END
    """ Şablon """
    if call.callback_query.data == "vsablon":
        if collection.find_one({"_id": user})['sira'] == "1":
            collection.update_one({"_id": user}, {"$set": {"sablon": "9"}})
        else:
            collection.update_one({"_id": user}, {"$set": {"sablon": "1"}})
        bot.edit_message_text("Varsayılana döndürüldü.", chat, mesajid)

def sitemarkup():
    skey = []
    smark = InlineKeyboardMarkup([[InlineKeyboardButton("TRLink", callback_data="site-1")], [InlineKeyboardButton("PND.TL", callback_data="site-2")], [InlineKeyboardButton("Exe.io", callback_data="site-3")], [InlineKeyboardButton("Ouo.io", callback_data="site-4")], [InlineKeyboardButton("Pubiza", callback_data="site-5")], [InlineKeyboardButton("❌ İptal ❌", callback_data="iptal")]])
    return smark

def altsitemarkup(sss):
    asmark = InlineKeyboardMarkup([[InlineKeyboardButton("TRLink", callback_data="asite-1-{}".format(sss))], [InlineKeyboardButton("PND.TL", callback_data="asite-2-{}".format(sss))], [InlineKeyboardButton("Exe.io", callback_data="asite-3-{}".format(sss))], [InlineKeyboardButton("Ouo.io", callback_data="asite-4-{}".format(sss))], [InlineKeyboardButton("Pubiza", callback_data="asite-5-{}".format(sss))], [InlineKeyboardButton("❌ İptal ❌", callback_data="iptal")]])

    return asmark

def altmarkup(user):

    altkey = [[InlineKeyboardButton("Sıralı", callback_data="sistem-2")], [InlineKeyboardButton("Tek Post İki Link", callback_data="sistem-1")], [InlineKeyboardButton("❌ İptal ❌", callback_data="iptal")]]
    if collection.find_one({"_id": user})['altapi'] != "None":
        altkey.append([InlineKeyboardButton("⛔ Alternatif Kaldır", callback_data="akaldır")])
    altmark = InlineKeyboardMarkup(altkey)
    return altmark

def inmark():
    inmark = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton("❌ İptal ❌", callback_data="aiptal")]])

    return inmark

def ozelmark():
    omark = InlineKeyboardMarkup([[InlineKeyboardButton("➕ Oluştur ➕", callback_data="okayt")], [InlineKeyboardButton("❌ İptal ❌", callback_data="aiptal")]])

    return omark

def kaynakmark(user):
    u = collection.find_one({"_id": user})
    saatbut = InlineKeyboardButton("⏳", callback_data="zaman-1")
    bsaatbut = InlineKeyboardButton("⏳", callback_data="zaman-2")
    csaatbut = InlineKeyboardButton("⏳", callback_data="zaman-3")
    dsaatbut = InlineKeyboardButton("⏳", callback_data="zaman-4")
    esaatbut = InlineKeyboardButton("⏳", callback_data="zaman-5")
    fsaatbut = InlineKeyboardButton("⏳", callback_data="zaman-6")
    gsaatbut = InlineKeyboardButton("⏳", callback_data="zaman-7")
    
    ubut =InlineKeyboardButton("{}".format(mahzen.title), url="{}".format(mahzen.invite_link))
    bbut =InlineKeyboardButton("{}".format(bedava.title), url="{}".format(bedava.invite_link))
    cbut =InlineKeyboardButton("{}".format(evi.title), url="{}".format(evi.invite_link))
    dbut =InlineKeyboardButton("{}".format(bashub.title), url="{}".format(bashub.invite_link))
    ebut =InlineKeyboardButton("{}".format(acikmi.title), url="{}".format(acikmi.invite_link))
    fbut =InlineKeyboardButton("{}".format(tutan.title), url="{}".format(tutan.invite_link))
    gbut =InlineKeyboardButton("{}".format(muho.title), url="{}".format(muho.invite_link))
    if u['ozel']:
        kmark = InlineKeyboardMarkup([[InlineKeyboardButton("🟣 Özel Kaynağı Kaldır 🟣", callback_data="okayk")], [InlineKeyboardButton("❌ İptal ❌", callback_data="aiptal")]])
        return kmark        

    if "1" in u['kaynak']:
        kb1 = InlineKeyboardButton("✅", callback_data="kaynak-1")
    else:
        kb1 = InlineKeyboardButton("⚫", callback_data="kaynak-1")
    if "2" in u['kaynak']:
        kb2 = InlineKeyboardButton("✅", callback_data="kaynak-2")
    else:
        kb2 = InlineKeyboardButton("⚫", callback_data="kaynak-2")
    if "3" in u['kaynak']:
        kb3 = InlineKeyboardButton("✅", callback_data="kaynak-3")
    else:
        kb3 = InlineKeyboardButton("⚫", callback_data="kaynak-3")
    if "4" in u['kaynak']:
        kb4 = InlineKeyboardButton("✅", callback_data="kaynak-4")
    else:
        kb4 = InlineKeyboardButton("⚫", callback_data="kaynak-4")
    if "5" in u['kaynak']:
        kb5 = InlineKeyboardButton("✅", callback_data="kaynak-5")
    else:
        kb5 = InlineKeyboardButton("⚫", callback_data="kaynak-5")
    if "6" in u['kaynak']:
        kb6 = InlineKeyboardButton("✅", callback_data="kaynak-6")
    else:
        kb6 = InlineKeyboardButton("⚫", callback_data="kaynak-6")
    if "7" in u['kaynak']:
        kb7 = InlineKeyboardButton("✅", callback_data="kaynak-7")
    else:
        kb7 = InlineKeyboardButton("⚫", callback_data="kaynak-7")
    
    kmark = InlineKeyboardMarkup(inline_keyboard=[[ubut], [kb1, saatbut], [bbut], [kb2, bsaatbut], [cbut], [kb3, csaatbut], [dbut], [kb4, dsaatbut], [ebut], [kb5, esaatbut], [gbut], [kb6, gsaatbut], [fbut], [kb7, fsaatbut], [InlineKeyboardButton("❌ İptal ❌", callback_data="aiptal")], [InlineKeyboardButton("♋️ Özel Kaynak Oluştur ♋️", callback_data="okay")]])
    
    return kmark

def sablonmark(user):
    if collection.find_one({"_id": user})['sablon'] in ["1", "2", "3", "9"]:
        buts = InlineKeyboardButton("➕ Şablon Oluştur ➕", callback_data="sablon")
        samark = InlineKeyboardMarkup(inline_keyboard=[[buts]], row_width=2)
        return samark
    else:
        buts = InlineKeyboardButton("➕ Şablon Değiştir ➕", callback_data="sablon")
        buts2 = InlineKeyboardButton("🔁 Varsayılan Şablonu Kullan 🔁", callback_data="vsablon")
        buts3 = InlineKeyboardButton("❌ İptal ❌", callback_data="aiptal")
        samark = InlineKeyboardMarkup(inline_keyboard=[[buts], [buts2], [buts3]], row_width=2)
        return samark

def patmark(user):
    zero = 0
    pkeyb = [[InlineKeyboardButton("Hepsine Gönder", callback_data="pat-0")]]
    pkul = collection.find_one({"_id": user})

    for k in pkul['kanal']:
        kn = bot.get_chat(k)
        zero += 1
        pkeyb.append([InlineKeyboardButton("{}".format(kn.title), callback_data="pat-{}".format(zero))])
    pkeyb.append([InlineKeyboardButton("❌ İptal ❌", callback_data="aiptal")])

    pmark = InlineKeyboardMarkup(pkeyb)
    return pmark
    
def gen_markup(user):
    keyb = []
    kayd = collection.find_one({"_id": user})
    butonno = 0
    for k in kayd['kanal']:
        ismi = bot.get_chat(k)
        keyb.append([InlineKeyboardButton("{}".format(ismi.title), callback_data="sil-{}".format(butonno))])
        butonno += 1
    keyb.append([InlineKeyboardButton("❌ İptal ❌", callback_data="iptal")])
    silkey = InlineKeyboardMarkup(keyb)
    
    return silkey


def menu(update, context):
    chat = update.message.chat.id
    user = update.message.from_user.id
    mesaj = update.message.text
    bot = context.bot
    mj = collection.find_one({"_id": user})
    if user in kara:
        bot.send_message(chat, "🤓 Üzgünüm senin gibi aptal birisi için çalışmıyorum")
        return
    if mesaj == "🔧 Kaynak":
        global mahzen, bedava, evi, bashub, acikmi, muho, tutan
        mahzen = bot.get_chat(kaynaklar[0])
        bedava = bot.get_chat(kaynaklar[1])
        evi = bot.get_chat(kaynaklar[2])
        bashub = bot.get_chat(kaynaklar[3])
        acikmi = bot.get_chat(kaynaklar[4])
        muho = bot.get_chat(kaynaklar[5])
        tutan = bot.get_chat(kaynaklar[6])
        if mj == None:
            bot.send_message(chat, "Lütfen önce bir API kaydedin.")
            return
        if mj['ozel']:
            bot.send_message(chat, """<b>Özel Kaynak Kullandığınız için başka kaynak seçemezsiniz.</b>""", reply_markup=kaynakmark(user))
            return
        bot.send_message(chat, """<b>Kullanmak istediğiniz kaynak kanalını seçin.</b>""", reply_markup=kaynakmark(user))
        return
    if mesaj == "📏 Şablon":
        link = "https://ay.live/vRpKVx"
        aciklama = "Pharex, lord adminin karısını sikerken lord adminn basıyor."
        alink = "https://pgg.fyi/X0DK3"
        if mj == None:
            bot.send_message(chat, "Lütfen önce bir API kaydedin.")
            return
        if mj['sablon'] == "1":
            bot.send_message(chat, "<b>Varsayılan Şablon:</b>\n\n🔥{aciklama} \n\n🔱 TIKLA 👉 {link} \n\n📛 SESİ AÇ 'a tıklamayı unutma", reply_markup=sablonmark(user))
        elif mj['sablon'] == "2":
            bot.send_message(chat, "<b>Varsayılan Şablon:</b>\n\n{aciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {link}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 #linkgec06", reply_markup=sablonmark(user))
        elif mj['sablon'] == "9":
            bot.send_message(chat, "<b>Varsayılan Şablon:</b>\n\n{aciklama} \n\n𝙇𝙄𝙉𝙆🔗 {link} \n\n     𝙇𝙄𝙉𝙆🔗 {alink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 #linkk_gecmee", reply_markup=sablonmark(user))
        else:
            if mj['sira'] == "1":
                pst = mj['sablon'].replace("{aciklama}", "{}").replace("{link}", "{}").replace("{alink}", "{}").format(aciklama, link, alink)
            else:
                pst = mj['sablon'].replace("{aciklama}", "{}").replace("{link}", "{}").replace("{alink}", "").format(aciklama, link)
            bot.send_message(chat, f"<b>Şablonunuz böyle gözükecek:</b>\n\n{pst}", reply_markup=sablonmark(user))
        return
    if mesaj == "📝 Kaydet":
        try:
            tokenn = bina['token']
        except:
            msg = bot.send_message(chat, """📝 <i>Lütfen</i> <a href="https://tr.link/member/tools/quick">burdan</a> <i>aldığınız API adresinizi gönderin</i>""", reply_markup=imark())
            
            return APIDEGISTIR
    if mesaj == "⚙️ Menü":
        kayitli = 0
        chat = update.message.chat.id
        bina = collection.find_one({"_id": chat})
        try:
            for chan in bina['kanal']:
                try:
                    kbilgi = bot.get_chat(chan)
                except Exception as e:
                    logger.error(e)
                    collection.update_one({"_id": chat}, {"$pull": {"kanal": chan}})
                    kayitli = kayitli - 1
                    logger.debug("Kanal silindi")
                else:    
                    bot.send_message(chat, """Kanalınız: <a href="{}">{}</a>""".format(kbilgi.invite_link, kbilgi.title))
                kayitli = kayitli + 1
        except Exception as e:
            pass
        try:
            tokenn = bina['token']
        except:
            msg = bot.send_message(chat, """⛔ Henüz bir API kaydetmemişsiniz!
            
📝 <i></i> <a href="https://tr.link/member/tools/quick">buraya tıklayarak</a> <i>aldığınız API adresinizi gönderin</i>""", reply_markup=imark())
            
            return APIDEGISTIR
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
                msg = bot.send_message(chat, "<i>♦️Kayıtlı API: {}\nSite: {}\nToplam Kanal: {}</i>".format(tokenn, site, kayitli), reply_markup=markupp())
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
                msg = bot.send_message(chat, "<i>♦️Birincil API: {}\n  Birincil Site: {}\n  Alternatif API: {}\n  Alternatif Site: {}\n  Toplam Kanal: {}</i>".format(tokenn, site, bina['altapi'], altsite, kayitli), reply_markup=markupp())
                
        return ALTMENU
    if mesaj == "▶️ SFS Modu":
        if mj == None:
            bot.send_message(chat, "Lütfen önce bir API kaydedin.")
            return
        try:
            mod = collection.find_one({"_id": user})
        except:
            pass
        if "31" in mod['kaynak'] or mod['kaynak'] == None:
            try:
                collection.update_one({"_id": user}, {"$set": {"kaynak": mod['eski']}})
            except:
                pass
            bot.send_message(chat, "SFS modu durduruldu", reply_markup=dugme())
            return
        else:
            collection.update_one({"_id": user}, {"$set": {"eski": mod['kaynak']}})
            collection.update_one({"_id": user}, {"$set": {"kaynak": ['31']}})
            bot.send_message(chat, "Kanallarınız SFS moduna alındı. Siz modu kapatana kadar yeni post atılmayacak.", reply_markup=dugme())
            return
    if mesaj == "🥰 Bağış":
        if user != sahip:
            bot.send_message(chat, "Bu komut bakımda.")
            return
        bot.send_message(chat, "🥰Madem bu kadar çok istiyorsun. \n\n🏧Papara: <code>1666982412</code> \n🏦İninal: <code>4003140030544</code>")
        return
    if mesaj == "⛓️ Elle Post Paylaş":
        if mj == None:
            bot.send_message(chat, "Lütfen önce bir API kaydedin.")
            return
        if len(mj['kanal']) < 1:
            bot.send_message(chat, "Lütfen önce bir kanal kaydedin.")
            return
        msg = bot.send_message(chat, "Paylaşmamı istediğin hazır postu ilet.", reply_markup=imark())
        
        return PATPOST
        
    kisi = collection.find_one({"_id": user})
    if kisi == None:
        bot.send_message(chat, "<i>Lütfen alttaki butonları kullan</i>", reply_markup=dagme())
        return
    bot.send_message(chat, "<i>Lütfen alttaki butonları kullan</i>", reply_markup=dugme())
    
def ozelk(update, context):
    user = update.message.from_user.id
    chat = update.message.chat.id
    if update.message.text == "❌ İptal":
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme())
        return ConversationHandler.END
    if not update.message.forward_from_chat:
        msz = bot.send_message(update.message.chat.id, "Lütfen bana oluşturduğun kanaldan bir mesaj ilet.")
        return OZELKAYNAK
    kanal = update.message.forward_from_chat.id
    if kanal in kaynaklar:
        mst = bot.send_message(chat, "Kaynak kanalını nasıl kaydedebilirim ki?")
        return OZELKAYNAK
    try:
        yetkiler = bot.get_chat_administrators(kanal)
    except:
        msg = bot.send_message(chat, "Botu kanalınızda yönetici eklememişsiniz.")
        return OZELKAYNAK
    if update.message.forward_from_chat:
        ileti = update.message.forward_from_chat.id
        OzelCol.update_one({"_id": user}, {"$set": {"okaynak": ileti}})
        collection.update_one({"_id": user}, {"$set": {"ozel": True, "kaynak": ["32"]}})
        bot.send_message(update.message.chat.id, "<b>Özel Kaynak Oluşturuldu!</b>", reply_markup=dugme())
        return ConversationHandler.END

def sabloniki(update, context):
    mesaj = update.message.text
    chat = update.message.chat.id
    user = update.message.from_user.id
    bnb = collection.find_one({"_id": user})
    if update.message.text == None:
        msg = bot.send_message(chat, """ ❌<i> Lütfen mesajınızda "{link}" ve "{aciklama}" bulunduğudan emin olun.</i> """)

        return SABLON
    if update.message.text == "❌ İptal":
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme())
        return ConversationHandler.END
    if not mesaj.isdigit() and bnb['sira'] == "1":
        if mesaj.find("{link}") == -1 or mesaj.find("{aciklama}") == -1 or mesaj.find("{alink}") == -1:
            msg = bot.send_message(chat, """ ❌<i> Lütfen mesajınızda "{link}", "{alink}" ve "{aciklama}" bulunduğudan emin olun.</i> """)
            return SABLON
        if mesaj.find("{link}") > mesaj.find("{alink}"):
            msg = bot.send_message(chat, """ ❌<i> Şablonunuzda {link} kelimesi {alink}'ten önde olmak zorundadır</i> """)
            return SABLON
    if not mesaj.isdigit():
        if mesaj.find("{link}") == -1 or mesaj.find("{aciklama}") == -1:
            msg = bot.send_message(chat, """ ❌<i> Lütfen mesajınızda "{link}" ve "{aciklama}" bulunduğudan emin olun.</i> """)
            return SABLON
        if mesaj.find("{link}") != mesaj.rfind("{link}"):
            msg = bot.send_message(chat, """ ❌<i> Lütfen mesajınızda bir tane "{link}" bulunduğudan emin olun.</i> """)
            return SABLON
        if mesaj.find("{aciklama}") != mesaj.rfind("{aciklama}"):
            msg = bot.send_message(chat, """ ❌<i> Lütfen mesajınızda bir tane "{aciklama}" bulunduğudan emin olun.</i> """)
            return SABLON
    if bnb == None:
        bot.send_message(chat, "Lütfen şablon kaydetmeden önce Kaydet butonu ile bilgilerinizi girin!", reply_markup=dugme())
    else:
        collection.update_one({"_id": user}, {"$set":{"sablon": mesaj}})
        bot.send_message(chat, "Şablon kaydedildi!", reply_markup=dugme())
        return ConversationHandler.END

def kayitapi(update, context):
    chat = update.message.chat.id
    mesaj = update.message.text
    user = update.message.from_user.id
    ka = collection.find_one({"_id": user})
    vip_uyeler = collection.find_one({"_id": 0})['vipuye']
    if mesaj == "🗑️ Kanal Sil":
        if len(ka['kanal']) < 1:
            msg = bot.send_message(chat, "Henüz bir kanal kaydetmemişsiniz!", reply_markup=markupp())
            return 
        msg = bot.send_message(chat, "Silmek istediğiniz kanalı seçin.", reply_markup=gen_markup(user))
        return 
    if mesaj == "♻️ API değiştir":
        msg = bot.send_message(chat, "Yeni API adresinizi girin.", reply_markup=imark())
        return APIDEGISTIR
    if mesaj == "↩️ Ana Menü" or mesaj == "❌ İptal":
        msg = bot.send_message(chat, "İptal Edildi.", reply_markup=dugme())
        return ConversationHandler.END
    if mesaj == "🔗 Site değiştir":
        msg = bot.send_message(chat, "<i>Kullanmak istediğiniz siteyi seçin</i>", reply_markup=sitemarkup())
        
        return
    if mesaj == "🤖 Alternatif Ekle":
        msg = bot.send_message(chat, "<b>Alternatif Nasıl Kullanılsın.\n\n Tek Post İki Link</b>\n <i>Aynı post iki link</i> \n\n<b>Sıralı</b>\n <i>Bir post birinci servis, bir post alternatif servis.</i>\n\n<b>Kullanmak istediğiniz sistemi seçin.</b>", reply_markup=altmarkup(user))
        
        return
    if mesaj == "🔶 Yeni Kanal Ekle":
        bol = collection.find_one({"_id": chat})
        if len(bol['kanal']) > 2 and not user in vip_uyeler:
            bot.send_message(chat, "<i>Üzgünüm en fazla 3 kanal kaydedebilirsiniz.</i>")
            return 
        bot.send_message(chat, """📝 <i>Lütfen kanalınızdan bir gönderi iletin.</i>""", reply_markup=imark())

        return KANALKAYDET
    bot.send_message(chat, "Lütfen alttaki butonları kullanıns.", reply_markup=markupp())

def cancel(update, context):
    chat = update.message.chat.id
    bot.send_message(chat, "İptal Edildi.", reply_markup=dugme())
    return

def altakayit(update, context):
    amesaj = update.message.text
    user = update.message.from_user.id
    chat = update.message.chat.id
    if update.message.text == "❌ İptal" or update.message.text == None:
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme())
        return ConversationHandler.END
    if update.message.text == "⛔ Alternatif Kaldır":
        collection.update_one({"_id": user}, {"$set": {"altsite": "None", "altapi": "None", "sablon": "1", "sira": "0"}})
        bot.send_message(chat, "Alternatif kaldırıldı, artık postlarınız alternatif linksiz paylaşılacak.", reply_markup=dugme())
        return ConversationHandler.END
    smesaj = context.user_data['asite']
    sss = context.user_data['sistem']
    collection.update_one({"_id": user}, {"$set": {"altsite": str(smesaj), "altapi": str(amesaj), "sira": str(sss)}})
    bot.send_message(chat, "✅ Alternatif API kaydedildi", reply_markup=dugme())
    return ConversationHandler.END

def apikayit(update, context):
    token = update.message.text
    user = update.message.from_user.id
    chat = update.message.chat.id
    bnb = collection.find_one({"_id": user})
    if update.message.text == None:
        msg = bot.send_message(chat, "Lütfen geçerli bir API verin.")
        return
    if update.message.text == "❌ İptal":
        if bnb == None:
            bot.send_message(chat, "İptal Edildi.", reply_markup=dagme())
        else:
            bot.send_message(chat, "İptal Edildi.", reply_markup=dugme())
        return ConversationHandler.END
    if bnb == None:
        kontrol = get("https://ay.live/api/?api={}&url=www.zort.com&format=text&alias=&ct=2".format(token)).text
        if kontrol == "":
            mso = bot.send_message(chat, "❌ Geçersiz bir API verdiniz! Lütfen doğru bir API adresi verin.")
            return APIDEGISTIR
    key = {"_id": user, "token": token, "kanal": [], "sablon": "1", "kaynak": ["1"], "site": "1", "altapi": "None", "altsite": "None", "sira": "0", "ozel": False}
    if bnb == None:
        collection.insert_one(key)
    else:
        collection.update_one({"_id": user}, {"$set": {"token": token}})
    bot.send_message(chat, "<b>🟢 API kaydedildi!</b>", reply_markup=dugme())
    return ConversationHandler.END

def kanalkayit(update, context):
    chat = update.message.chat.id
    user = update.message.from_user.id
    y = collection.find_one({"_id": user})
    if update.message.text == "❌ İptal":
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme())
        return ConversationHandler.END
    if not update.message.forward_from_chat:
        msg = bot.send_message(chat, "↪️ Bunun ne olduğu hakkında bir fikrim yok! Lütfen kanaldan herhangi bir gönderi iletin.", reply_markup=imark())
        
        return KANALKAYDET
    kanal = update.message.forward_from_chat.id
    if kanal in kaynaklar:
        mst = bot.send_message(chat, "Kaynak kanalını nasıl kaydedebilirim ki?", reply_markup=imark())
        return KANALKAYDET
    if str(kanal) in y['kanal']:
        msl = bot.send_message(chat, "Bu kanalı zaten kaydetmişsiniz")
        return KANALKAYDET
    try:
        kanalbilgi = bot.get_chat(kanal)
    except:
        msg = bot.send_message(chat, "Botu kanalınızda yönetici eklememişsiniz.")
        
        return KANALKAYDET
    try:
        yetkiler = bot.get_chat_administrators(kanal)
    except:
        msg = bot.send_message(chat, "Botu kanalınızda yönetici eklememişsiniz.")
        
        return KANALKAYDET
    for y in yetkiler:
        if y.user.id == user:
            collection.update_one({"_id": user}, {"$push":{"kanal": str(kanal)}})
            update.message.reply_text("<b>🟢Kanalınız Kaydedildi.</b>", reply_markup=dugme())
            return ConversationHandler.END
            break
    msz = bot.send_message(chat, "Bu kanal sizin değil 😠")
    update.message.register_next_step_handler(msz, kanalkayit)



def pat(update, context):
    chat = update.message.chat.id
    user = update.message.from_user.id
    if update.message.text == "❌ İptal":
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme())
        return ConversationHandler.END
    if update.message.text:
        msg = bot.send_message(chat, "Lütfen paylaşmamı istediğin postu at")
        return PATPOST
    if update.message.caption == None:
        msg = bot.send_message(chat, "Lütfen paylaşmamı istediğin postu at")
        return PATPOST
    mesaj = update.message.caption
    if update.message.video:
        fid = update.message.video.file_id
        ptip = "video"
    if update.message.photo:
        fid = update.message.photo[0].file_id
        ptip = "photo"
    if update.message.animation:
        fid = update.message.animation.file_id
        ptip = "animation"
    """Açıklama Tespit"""
    pson = mesaj.find("\n")
    paciklama = mesaj[:pson]
    """Link Tespit"""
    psol = mesaj.find("http")
    psag = mesaj.find("\n", psol)
    plink = mesaj[psol:psag].strip()
    if mesaj.find("\n", psol) == -1:
        plink = mesaj[psol:].strip()
    pathesap = collection.find_one({"_id": user})
    s = Session()
    link = s.get("https://ay.live/api")
    cookies = dict(link.cookies)
    pret = True
    try:
        ptoken = pathesap['token']
    except:
        pret = False
        bot.send_message(chat, "API adresinizi yeniden kaydedin.")
    psablon = pathesap['sablon']
    psite = pathesap['site']
    paltapi = pathesap['altapi']
    paltsite = pathesap['altsite']
    psira = pathesap['sira']
    palink = " "
    if psira == "2":
        ptoken = paltapi
        psite = paltsite
        collection.update_one({"_id": user}, {"$set": {"sira": "3"}})
    if psira == "3":
        collection.update_one({"_id": user}, {"$set": {"sira": "2"}})
    try:
        if not paltapi == "None":
            if paltsite == "1":
                pjson = s.get(f"https://ay.live/api/?", params={"api": paltapi, "url": plink, "ct": 1}, cookies=cookies).json()
                palink = pjson['shortenedUrl']
            if paltsite == "2":
                pjson = s.get(f"https://www.pnd.tl/api?", params={'api': paltapi, 'url': plink, 'category': 6}).json()
                palink = pjson['shortenedUrl']
            if paltsite == "3":
                pjson = s.get(f"https://exe.io/api?", params={"api": paltapi, "url": plink}).json()
                palink = pjson['shortenedUrl']
            if paltsite == "4":
                palink = s.get(f"http://ouo.io/api/{paltapi}", params={"s": plink}).text
            if paltsite == "5":
                palink = s.get(f"http://pubiza.com/api.php?", params={"token": paltapi, "url": plink, "ads_type": "adult"}).text
        if psite == "1":
            pjson = s.get(f"https://ay.live/api/?", params={"api": ptoken, "url": plink, "ct": 1}, cookies=cookies).json()
            plink = pjson['shortenedUrl']
        if psite == "2":
            pjson = get(f"https://www.pnd.tl/api?", params={'api': ptoken, 'url': plink, 'category': 6}).json()
            plink = pjson['shortenedUrl']
        if psite == "3":
            pjson = s.get(f"https://exe.io/api?", params={"api": ptoken, "url": plink}).json()
            plink = pjson['shortenedUrl']
        if psite == "4":
            plink = s.get(f"http://ouo.io/api/{ptoken}?", params={"s": plink}).text
        if psite == "5":
            plink = s.get(f"http://pubiza.com/api.php?", params={"token": ptoken, "url": plink, "ads_type": "adult"}).text
        if psablon == "1":
            psablon = f"🔥{paciklama}\n\n🔱 TIKLA 👉 {plink}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
        elif psablon == "2" or psablon == "3":
            psablon = f"{paciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {plink}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 #linkgec06"
        elif psablon == "9":
            psablon = f"{paciklama} \n\n𝙇𝙄𝙉𝙆🔗 {plink} \n\n     𝙇𝙄𝙉𝙆🔗 {palink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 #linkk_gecmee"
        elif psablon.find('{alink}') != -1:
            psablon = psablon.replace("{aciklama}", "{}").replace("{link}", "{}").replace("{alink}", "{}").format(paciklama, plink, palink)
        else:
            psablon = psablon.replace("aciklama", "").replace("{link}", "{}").format(paciklama, plink)
        pkanallar = pathesap['kanal']
        pcount = 0
    except Exception as e:
        bot.send_message(chat, f"Bir sorun oluştu: \n\n{e}")
        logger.error(e)
        pret = False
    if len(pathesap['kanal']) < 2 and pret:
        pmesaj = 0
        if ptip == "video":
            bot.send_video(pkanallar[0], fid, caption=psablon)
        if ptip == "photo":
            bot.send_photo(pkanallar[0], fid, caption=psablon)
        if ptip == "animation":
            bot.send_animation(pkanallar[0], fid, caption=psablon)
        bot.send_message(chat, "Postunuz gönderildi.", reply_markup=dugme())
        return ConversationHandler.END
    
    context.user_data['psablon'] = psablon
    context.user_data['ptip'] = ptip
    context.user_data['fid'] = fid
    if pret:
        bot.send_message(chat, "Post Hazırlandı!", reply_markup=dugme())
        bot.send_message(chat, "<i>Postun gönderilmesini istediğin kanalı seç.</i>", reply_markup=patmark(user))
        return ConversationHandler.END
    else:
        bot.send_message(chat, "Bir hata oluştu")

def poster(update, context):
    okaynak = None
    chat = update.channel_post.chat.id
    # Link Mahzeni
    if chat == kaynaklar[0] and mahzen:
        count = 0
        mesaj = update.channel_post.caption
        if mesaj == None:
            return
        """  Link tespit  """
        solx = mesaj.rfind("http")
        sol = mesaj.find("http")
        if sol == -1:
            return
        if sol != solx:
            return
        sag = mesaj.find("\n", sol)
        kynk = bot.get_chat(chat)
        mesajb = mesaj[sol:sag].strip()
        if mesaj.find("\n", sol) == -1:
            mesajb = mesaj[sol:].strip()
        if mesajb.startswith("https://t.me/"):
            return
        logger.warning("{} postu atılıyor... ".format(kynk.title))
        """  Açıklama tespit  """
        ason = mesaj.rfind("\n", 0, sol)
        aciklama = mesaj[:ason].strip()
        """  Cookies  """
        s = Session()
        link = s.get("https://ay.live/")
        cookies = dict(link.cookies)
        """  Veri Tabanı  """
        postdata = db[str(chat)]
        binb = collection.find({})
        """ Dosya tespit """
        if update.channel_post.photo:
            medya = update.channel_post.photo[0].file_id
        if update.channel_post.animation:
            medya = update.channel_post.animation.file_id
        if update.channel_post.video:
            medya = update.channel_post.video.file_id
        for hesap in binb:
            ret = True
            kaynak = hesap['kaynak']
            try:
                token = hesap['token']
            except:
                ret = False
            kanal = hesap['kanal']
            sablon = hesap['sablon']
            user = hesap['_id']
            site = hesap["site"]
            altapi = hesap['altapi']
            altsite = hesap['altsite']
            sira = hesap['sira']
            if "1" in kaynak and len(kanal) > 0 and ret:
                link = " "
                alink = " "
                json = " "
                try:
                    if sira == "2":
                        token = altapi
                        site = altsite
                        collection.update_one({"_id": user}, {"$set": {"sira": "3"}})
                    if sira == "3":
                        collection.update_one({"_id": user}, {"$set": {"sira": "2"}})
                    if not altapi == "None":
                        if altsite == "1":
                            json = s.get(f"https://ay.live/api/?", params={'api': altapi, 'url': mesajb, 'ct': 1}, cookies=cookies).json()
                            alink = json['shortenedUrl']
                        if altsite == "2":
                            json = s.get(f"https://www.pnd.tl/api?", params={'api': altapi, 'url': mesajb, 'category': 6}).json()
                            alink = json['shortenedUrl']
                        if altsite == "3":
                            json = s.get(f"https://exe.io/api?", params={'api': altapi, 'url': mesajb}).json()
                            alink = json['shortenedUrl']
                        if altsite == "4":
                            alink = s.get(f"http://ouo.io/api/{altapi}?", params={'s': mesajb}).text
                        if altsite == "5":
                            alink = s.get(f"http://pubiza.com/api.php?", params={'token': altapi, 'url': mesajb, 'ads_type': "adult"}).text
                    if site == "1":
                        json = s.get(f"https://ay.live/api/?", params={'api': token, 'url': mesajb, 'ct': 1}, cookies=cookies).json()
                        link = json['shortenedUrl']
                    if site == "2":
                        json = s.get(f"https://www.pnd.tl/api?", params={'api': token, 'url': mesajb, 'category': 6}).json()
                        link = json['shortenedUrl']
                    if site == "3":
                        json = s.get(f"https://exe.io/api?", params={'api': token, 'url': mesajb}).json()
                        link = json['shortenedUrl']
                    if site == "4":
                        link = s.get(f"http://ouo.io/api/{token}?", params={'s': mesajb}).text
                    if site == "5":
                        link = s.get(f"http://pubiza.com/api.php?", params={'token': token, 'url': mesajb, 'ads_type': "adult"}).text
                    logger.info(f"{kanal} + {link} + {token}")
                except Exception as e:
                    bot.send_message(user, "Son postunuz gönderilemedi;\n\n<code>API adresiniz sıkıntılı veya sitenize ulaşılamıyor. API adresinizi kontrol edin, bir sıkıntı yoksa bu mesajı görmezden gelin muhtemelen seçtiğiniz site ile ilgili bir sorun vardır.</code>")
                    logger.error(e)
                    logger.debug(json)
                    ret = False
                if sablon == "1":
                    sablon = f"🔥{aciklama}\n\n🔱 TIKLA 👉 {link}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
                elif sablon == "2" or sablon == "3":
                    sablon = f"{aciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {link}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 #linkgec06"
                elif sablon == "9":
                    sablon = f"{aciklama} \n\n𝙇𝙄𝙉𝙆🔗 {link} \n\n     𝙇𝙄𝙉𝙆🔗 {alink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 #linkk_gecmee"
                elif sablon.find('{alink}') != -1:
                    sablon = sablon.replace("{aciklama}", "{}").replace("{alink}", "{}").replace("{link}", "{}").format(aciklama, link, alink)
                else:
                    sablon = sablon.replace("{aciklama}", "{}").replace("{link}", "{}").format(aciklama, link)
                sleep(1)
                for kan in kanal:
                    try:
                        if update.channel_post.photo and ret:
                            post = bot.send_photo(kan, medya, caption=sablon)
                        if update.channel_post.video and ret:
                            post = bot.send_video(kan, medya, caption=sablon)
                        if update.channel_post.animation and ret:
                            post = bot.send_animation(kan, medya, caption=sablon)
                        postkayit = postdata.find_one({"_id": kan})
                        if postkayit == None:
                            postdata.insert_one({"_id": kan, "pid": post.message_id})
                        else:
                            postdata.update_one({"_id": kan}, {"$set": {"pid": post.message_id}})
                        count = count + 1
                    except Exception as e:
                        logger.debug(f"Hatalı kanal: {kanal}")
                        e = str(e)
                        if e.find("update.message is") != -1:
                            collection.update_one({"_id": user}, {"$pull": {"kanal": kan}})
                            try:
                                bot.send_message(user, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                            except: #Hem update.messageu engelleyip hemde kanaldan sildiyse
                                pass   
                            logger.debug(f"{kanal} kayıtlardan silindi.")
                logger.info("Başarılı!")
            else:
                pass
        basari = "{} kaynağından, {} Kanalda Post Paylaşıldı.".format(kynk.title, count)
        logger.warning(basari)
        bot.send_message(update.messagelog, basari)
    # Bedava Link
    elif chat == kaynaklar[1] and bedava:
        bcount = 0
        bmesaj = update.channel_post.caption
        if bmesaj == None:
            return
        """ Link tespit """
        bsolx = bmesaj.rfind("http")
        bsol = bmesaj.find("http")
        if bsol == -1:
            return
        bsag = bmesaj.find("\n", bsol)
        if bsol != bsolx:
            return
        bmesajb = bmesaj[bsol:bsag].strip()
        if bmesaj.find("\n", bsol) == -1:
            bmesajb = bmesaj[bsol:].strip()
        if bmesajb.startswith("https://t.me/"):
            return
        bkynk = bot.get_chat(chat)
        logger.warning("{} postu atılıyor... ".format(bkynk.title))
        """ Açıklama tespit """
        bason = bmesaj.rfind("\n", 0, bsol)
        baciklama = bmesaj[:bason].strip()
        """    Cookies    """
        s = Session()
        link = s.get("https://ay.live/api")
        cookies = dict(link.cookies)
        """  Veri Tabanı  """
        bpostdata = db[str(chat)]
        bbinb = collection.find({})
        """ Dosya tespit """
        if update.channel_post.photo:
            bmedya = update.channel_post.photo[0].file_id
        if update.channel_post.animation:
            medya = update.channel_post.animation.file_id
        if update.channel_post.video:
            bmedya = update.channel_post.video.file_id
        for bhesap in bbinb:
            bret = True
            bkaynak = bhesap['kaynak']
            bsablon = bhesap['sablon']
            bsablon = str(bsablon)
            try:
                btoken = bhesap['token']
            except:
                bret = False
            bkanal = bhesap['kanal']
            buser = bhesap['_id']
            bsite = bhesap['site']
            baltapi = bhesap['altapi']
            baltsite = bhesap['altsite']
            bsira = bhesap['sira']
            if "2" in bkaynak and len(bkanal) > 0 and bret:
                balink = " "
                blink = " "
                bjson = " "
                if bsira == "2":
                    btoken = baltapi
                    bsite = baltsite
                    collection.update_one({"_id": buser}, {"$set": {"sira": "3"}})
                if bsira == "3":
                    collection.update_one({"_id": buser}, {"$set": {"sira": "2"}})
                try:
                    if not baltapi == "None":
                        if baltsite == "1":
                            bjson = s.get(f"https://ay.live/api/?", params={'api': baltapi, 'url': bmesajb, 'ct': 1}, cookies=cookies).json()
                            balink = bjson['shortenedUrl']
                        if baltsite == "2":
                            bjson = s.get(f"https://www.pnd.tl/api?", params={'api': baltapi, 'url': bmesajb, 'category': 6}).json()
                            balink = bjson['shortenedUrl']
                        if baltsite == "3":
                            bjson = s.get(f"https://exe.io/api?", params={'api': baltapi, 'url': bmesajb}).json()
                            balink = bjson['shortenedUrl']
                        if baltsite == "4":
                            balink = s.get(f"http://ouo.io/api/{baltapi}?", params={'s': bmesajb}).text
                        if baltsite == "5":
                            balink = s.get(f"http://pubiza.com/api.php?", params={'token': baltapi, 'url': bmesajb, 'ads_type': "adult"}).text
                    sleep(1)
                    if bsite == "1":
                        bjson = s.get(f"https://ay.live/api/?", params={'api': btoken, 'url': bmesajb, 'ct': 1}, cookies=cookies).json()
                        blink = bjson['shortenedUrl']
                    if bsite == "2":
                        bjson = s.get(f"https://www.pnd.tl/api?", params={'api': btoken, 'url': bmesajb, 'category': 6}).json()
                        blink = bjson['shortenedUrl']
                    if bsite == "3":
                        bjson = s.get(f"https://exe.io/api?", params={'api': btoken, 'url': bmesajb}).json()
                        blink = bjson['shortenedUrl']
                    if bsite == "4":
                        blink = s.get(f"http://ouo.io/api/{btoken}?", params={'s': bmesajb}).text
                    if bsite == "5":
                        blink = s.get(f"http://pubiza.com/api.php?", params={'token': btoken, 'url': bmesajb, 'ads_type': "adult"}).text
                    logger.info(f"{bkanal} + {blink} + {btoken}")
                except Exception as e:
                    bot.send_message(buser, "Son postunuz gönderilemedi;\n\n<code>API adresiniz sıkıntılı veya sitenize ulaşılamıyor. API adresinizi kontrol edin, bir sıkıntı yoksa bu mesajı görmezden gelin muhtemelen seçtiğiniz site ile ilgili bir sorun vardır.</code>")
                    logger.error(e)
                    logger.debug(bjson)
                    bret = False
                if bsablon == "1":
                    bsablon = f"🔥{baciklama}\n\n🔱 TIKLA 👉 {blink}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
                elif bsablon == "2" or bsablon == "3":
                    bsablon = f"{baciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {blink}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 #linkgec06"
                elif bsablon == "9":
                    bsablon = f"{baciklama} \n\n𝙇𝙄𝙉𝙆🔗 {blink} \n\n     𝙇𝙄𝙉𝙆🔗 {balink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 #linkk_gecmee"
                elif bsablon.find('{alink}') != -1:
                    bsablon = bsablon.replace("{aciklama}", "{}").replace("{alink}","{}").replace("{link}", "{}").format(baciklama, blink, balink)
                    
                else:
                    bsablon = bsablon.replace("{aciklama}", "{}").replace("{link}", "{}")
                    bsablon = str(bsablon).format(baciklama, blink)
                sleep(1)
                for bkan in bkanal:
                    try:
                        if update.channel_post.photo and bret:
                            bpost = bot.send_photo(bkan, bmedya, caption=bsablon)
                        if update.channel_post.video and bret:
                            bpost = bot.send_video(bkan, bmedya, caption=bsablon)
                        if update.channel_post.animation and bret:
                            bpost = bot.send_animation(bkan, bmedya, caption=bsablon)
                        bpostkayit = bpostdata.find_one({"_id": bkan})
                        if bpostkayit == None:
                            bpostdata.insert_one({"_id": bkan, "pid": bpost.message_id})
                        else:
                            bpostdata.update_one({"_id": bkan}, {"$set": {"pid": bpost.message_id}})
                        bcount = bcount + 1
                    except Exception as e:
                        logger.debug(f"Hatalı kanal: {bkanal}")
                        e = str(e)
                        if e.find("update.message is") != -1:
                            collection.update_one({"_id": buser}, {"$pull": {"kanal": bkan}})
                            try:
                                bot.send_message(buser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                            except: #Hem update.messageu engelleyip hemde kanaldan sildiyse
                                pass   
                            logger.debug(f"{bkanal} kayıtlardan silindi.")
                    
                logger.info("Başarılı!")
        bbasari = "{} kaynağından, {} Kanalda Post Paylaşıldı.".format(bkynk.title, bcount)
        logger.warning(bbasari)
        bot.send_message(update.messagelog, bbasari)
    # Link Evi
    elif chat == kaynaklar[2] and evi:
        ccount = 0
        cmesaj = update.channel_post.caption
        if cmesaj == None:
            return
        """ Link tespit """
        csolx = cmesaj.rfind("http")
        csol = cmesaj.find("http")
        if csol == -1:
            return
        if csol != csolx:
            return
        csag = cmesaj.find("\n", csol)
        cmesajb = cmesaj[csol:csag].strip()
        if cmesaj.find("\n", csol) == -1:
            cmesajb = cmesaj[csol:].strip()
        if cmesajb.startswith("https://t.me/"):
            return
        ckynk = bot.get_chat(chat)
        logger.warning("{} postu atılıyor... ".format(ckynk.title))
        """ Açıklama tespit """
        cason = cmesaj.find("\n", 0, csol)
        caciklama = cmesaj[:cason].strip()
        """    Cookies    """
        s = Session()
        link = s.get("https://ay.live/api")
        cookies = dict(link.cookies)
        """  Veri Tabanı  """
        cpostdata = db[str(chat)]
        cbinb = collection.find({})
        """ Dosya tespit """
        if update.channel_post.photo:
            cmedya = update.channel_post.photo[0].file_id
        if update.channel_post.animation:
            cmedya = update.channel_post.animation.file_id
        if update.channel_post.video:
            cmedya = update.channel_post.video.file_id
        for chesap in cbinb:
            cret = True
            ckaynak = chesap['kaynak']
            csablon = chesap['sablon']
            csablon = str(csablon)
            try:
                ctoken = chesap['token']
            except:
                cret = False
            ckanal = chesap['kanal']
            cuser = chesap['_id']
            csite = chesap['site']
            caltapi = chesap['altapi']
            caltsite = chesap['altsite']
            csira = chesap['sira']
            if "3" in ckaynak and len(ckanal) > 0 and cret:
                clink = " "
                calink = " "
                cjson = " "
                if csira == "2":
                    ctoken = caltapi
                    csite = caltsite
                    collection.update_one({"_id": cuser}, {"$set": {"sira": "3"}})
                if csira == "3":
                    collection.update_one({"_id": cuser}, {"$set": {"sira": "2"}})
                try:
                    if not caltapi == "None":
                        if caltsite == "1":
                            cjson = s.get(f"https://ay.live/api/?", params={'api': caltapi, 'url': cmesajb, 'ct': 1}, cookies=cookies).json()
                            calink = cjson['shortenedUrl']
                        if caltsite == "2":
                            cjson = s.get(f"https://www.pnd.tl/api?", params={'api': caltapi, 'url': cmesajb, 'category': 6}).json()
                            calink =     cjson['shortenedUrl']
                        if caltsite == "3":
                            cjson = s.get(f"https://exe.io/api?", params={'api': caltapi, 'url': cmesajb}).json()
                            calink = cjson['shortenedUrl']
                        if caltsite == "4":
                            calink = s.get(f"http://ouo.io/api/{caltapi}?", params={'s': cmesajb}).text
                        if caltsite == "5":
                            calink = s.get(f"http://pubiza.com/api.php?", params={'token': caltapi, 'url': cmesajb, 'ads_type': "adult"}).text
                    sleep(0.5)
                    if csite == "1":
                        cjson = s.get(f"https://ay.live/api/?", params={'api': ctoken, 'url': cmesajb, 'ct': 1},
                                      cookies=cookies).json()
                        clink = cjson['shortenedUrl']
                    if csite == "2":
                        cjson = s.get(f"https://www.pnd.tl/api?", params={'api': ctoken, 'url': cmesajb, 'category': 6}).json()
                        clink = cjson['shortenedUrl']
                    if csite == "3":
                        cjson = s.get(f"https://exe.io/api?", params={'api': ctoken, 'url': cmesajb}).json()
                        clink = cjson['shortenedUrl']
                    if csite == "4":
                        clink = s.get(f"http://ouo.io/api/{ctoken}?", params={'s': cmesajb}).text
                    if csite == "5":
                        clink = s.get(f"http://pubiza.com/api.php?", params={'token': ctoken, 'url': cmesajb, 'ads_type': "adult"}).text
                    logger.info(f"{ckanal} + {clink} + {ctoken}")
                except Exception as e:
                    bot.send_message(cuser, "Son postunuz gönderilemedi;\n\n<code>API adresiniz sıkıntılı veya sitenize ulaşılamıyor. API adresinizi kontrol edin, bir sıkıntı yoksa bu mesajı görmezden gelin muhtemelen seçtiğiniz site ile ilgili bir sorun vardır.</code>")
                    logger.error(e)
                    logger.debug(cjson)
                    cret = False
                    
                if csablon == "1":
                    csablon = f"🔥{caciklama}\n\n🔱 TIKLA 👉 {clink}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
                elif csablon == "2" or csablon == "3":
                    csablon = f"{caciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {clink}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 #linkgec06"
                elif csablon == "9":
                    csablon = f"{caciklama} \n\n𝙇𝙄𝙉𝙆🔗 {clink} \n\n     𝙇𝙄𝙉𝙆🔗 {calink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 #linkk_gecmee"
                elif csablon.find('{alink}') != -1:
                    csablon = csablon.replace("{link}", "{}").replace("{aciklama}", "{}").replace("{alink}","{}").format(caciklama, clink, calink)
                    
                else:
                    csablon = csablon.replace("{link}", "{}").replace("aciklama", "").format(caciklama, clink)
                sleep(1)
                for ckan in ckanal:
                    try:
                        if update.channel_post.photo and cret:
                            cpost = bot.send_photo(ckan, cmedya, caption=csablon)
                        if update.channel_post.video and cret:
                            cpost = bot.send_video(ckan, cmedya, caption=csablon)
                        if update.channel_post.animation and cret:
                            cpost = bot.send_animation(ckan, cmedya, caption=csablon)
                        cpostkayit = cpostdata.find_one({"_id": ckan})
                        if cpostkayit == None:
                            cpostdata.insert_one({"_id": ckan, "pid": cpost.message_id})
                        else:
                            cpostdata.update_one({"_id": ckan}, {"$set": {"pid": cpost.message_id}})
                        ccount = ccount + 1
                    except Exception as e:
                        logger.debug(f"Hatalı kanal: {ckanal}")
                        e = str(e)
                        if e.find("update.message is") != -1:
                            collection.update_one({"_id": cuser}, {"$pull": {"kanal": ckan}})
                            try:
                                bot.send_message(cuser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                            except: #Hem update.messageu engelleyip hemde kanaldan sildiyse
                                pass   
                            logger.debug(f"{ckanal} kayıtlardan silindi.")

                logger.info("Başarılı!")
        cbasari = "{} kaynağından, {} Kanalda Post Paylaşıldı.".format(ckynk.title, ccount)
        logger.warning(cbasari)
        bot.send_message(update.messagelog, cbasari)
    # BAŞHUB
    elif chat == kaynaklar[3] and bashub:
        dcount = 0
        dmesaj = update.channel_post.caption
        if dmesaj == None:
            return
        """ Link tespit """
        dsolx = dmesaj.rfind("http")
        dsol = dmesaj.find("http")
        if dsol == -1:
            return
        if dsol != dsolx:
            return
        dsag = dmesaj.find("\n", dsol)
        dmesajb = dmesaj[dsol:dsag].strip()
        if dmesaj.find("\n", dsol) == -1:
            dmesajb = dmesaj[dsol:].strip()
        if dmesajb.startswith("https://t.me/"):
            return
        dkynk = bot.get_chat(chat)
        logger.warning("{} postu atılıyor... ".format(dkynk.title))
        """ Açıklama tespit """
        dason = dmesaj.find("\n", 0, dsol)
        daciklama = dmesaj[:dason].strip()
        """    Cookies    """
        s = Session()
        link = s.get("https://ay.live/api")
        cookies = dict(link.cookies)
        """  Veri Tabanı  """
        dpostdata = db[str(chat)]
        dbinb = collection.find({})
        """ Dosya tespit """
        if update.channel_post.photo:
            dmedya = update.channel_post.photo[0].file_id
        if update.channel_post.animation:
            dmedya = update.channel_post.animation.file_id
        if update.channel_post.video:
            dmedya = update.channel_post.video.file_id
        for dhesap in dbinb:
            dret = True
            dkaynak = dhesap['kaynak']
            dsablon = dhesap['sablon']
            dsablon = str(dsablon)
            try:
                dtoken = dhesap['token']
            except:
                dret = False
            dkanal = dhesap['kanal']
            duser = dhesap['_id']
            dsite = dhesap['site']
            daltapi = dhesap['altapi']
            daltsite = dhesap['altsite']
            dsira = dhesap['sira']
            if "4" in dkaynak and len(dkanal) > 0 and dret:
                dalink = " "
                dlink = " "
                djson = " "
                if dsira == "2":
                    dtoken = daltapi
                    dsite = daltsite
                    collection.update_one({"_id": duser}, {"$set": {"sira": "3"}})
                if dsira == "3":
                    collection.update_one({"_id": duser}, {"$set": {"sira": "2"}})
                try:
                    if not daltapi == "None":
                        if daltsite == "1":
                            djson = s.get(f"https://ay.live/api/?", params={'api': daltapi, 'url': dmesajb, 'ct': 1}, cookies=cookies).json()
                            dalink = djson['shortenedUrl']
                        if daltsite == "2":
                            djson = s.get(f"https://www.pnd.tl/api?", params={'api': daltapi, 'url': dmesajb, 'category': 6}).json()
                            dalink = djson['shortenedUrl']
                        if daltsite == "3":
                            djson = s.get(f"https://exe.io/api?", params={'api': daltapi, 'url': dmesajb}).json()
                            dalink = djson['shortenedUrl']
                        if daltsite == "4":
                            dalink = s.get(f"http://ouo.io/api/{daltapi}?", params={'s': dmesajb}).text
                        if daltsite == "5":
                            dalink = s.get(f"http://pubiza.com/api.php?", params={'token': daltapi, 'url': dmesajb, 'ads_type': "adult"}).text
                    sleep(0.5)
                    if dsite == "1":
                        djson = s.get(f"https://ay.live/api/?", params={'api': dtoken, 'url': dmesajb, 'ct': 1}, cookies=cookies).json()
                        dlink = djson['shortenedUrl']
                    if dsite == "2":
                        djson = s.get(f"https://www.pnd.tl/api?", params={'api': dtoken, 'url': dmesajb, 'category': 6}).json()
                        dlink = djson['shortenedUrl']
                    if dsite == "3":
                        djson = s.get(f"https://exe.io/api?", params={'api': dtoken, 'url': dmesajb}).json()
                        dlink = djson['shortenedUrl']
                    if dsite == "4":
                        dlink = s.get(f"http://ouo.io/api/{dtoken}?", params={'s': dmesajb}).text
                    if dsite == "5":
                        dlink = s.get(f"http://pubiza.com/api.php?", params={'token': dtoken, 'url': dmesajb, 'ads_type': "adult"}).text
                    logger.info(f"{dkanal} + {dlink} + {dtoken}")
                except Exception as e:
                    bot.send_message(duser, "Son postunuz gönderilemedi;\n\n<code>API adresiniz sıkıntılı veya sitenize ulaşılamıyor. API adresinizi kontrol edin, bir sıkıntı yoksa bu mesajı görmezden gelin muhtemelen seçtiğiniz site ile ilgili bir sorun vardır.</code>")
                    logger.error(e)
                    logger.debug(djson)
                    dret = False
                    
                if dsablon == "1":
                    dsablon = f"🔥{daciklama}\n\n🔱 TIKLA 👉 {dlink}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
                elif dsablon == "2" or dsablon == "3":
                    dsablon = f"{daciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {dlink}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 #linkgec06"
                elif dsablon == "9":
                    dsablon = f"{daciklama} \n\n𝙇𝙄𝙉𝙆🔗 {dlink} \n\n     𝙇𝙄𝙉𝙆🔗 {dalink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 #linkk_gecmee"
                elif dsablon.find('{alink}') != -1:
                    dsablon = dsablon.replace("{link}", "{}").replace("{aciklama}", "{}").replace("{alink}", "{}").format(daciklama, dlink, dalink)
                else:
                    dsablon = dsablon.replace("{link}", "{}").replace("{aciklama}", "{}").format(daciklama, dlink)
                sleep(0.5)
                for dkan in dkanal:
                    try: 
                        if update.channel_post.photo and dret:
                            dpost = bot.send_photo(dkan, dmedya, caption=dsablon)
                        if update.channel_post.video and dret:
                            dpost = bot.send_video(dkan, dmedya, caption=dsablon)
                        if update.channel_post.animation and dret:
                            dpost = bot.send_animation(dkan, dmedya, caption=dsablon)
                        dpostkayit = dpostdata.find_one({"_id": dkan})
                        if dpostkayit == None:
                            dpostdata.insert_one({"_id": dkan, "pid": dpost.message_id})
                        else:
                            dpostdata.update_one({"_id": dkan}, {"$set": {"pid": dpost.message_id}})
                        dcount = dcount + 1
                    except Exception as e:
                        logger.debug(f"Hatalı kanal: {dkanal}")
                        e = str(e)
                        if e.find("update.message is") != -1:
                            collection.update_one({"_id": duser}, {"$pull": {"kanal": dkan}})
                            try:
                                bot.send_message(duser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                            except: #Hem update.messageu engelleyip hemde kanaldan sildiyse
                                pass   
                            logger.debug(f"{dkanal} kayıtlardan silindi.")

                logger.info("Başarılı!")
        dbasari = "{} kaynağından, {} Kanalda Post Paylaşıldı.".format(dkynk.title, dcount)
        logger.warning(dbasari)
        bot.send_message(update.messagelog, dbasari)
    # Açık mı link
    elif chat == kaynaklar[4] and acikmi:
        ecount = 0
        emesaj = update.channel_post.caption
        """ Link tespit """
        esolx = emesaj.rfind("http")
        esol = emesaj.find("http")
        if esol == -1:
            return
        if esol != esolx:
            return
        esag = emesaj.find("\n", esol)
        emesajb = emesaj[esol:esag].strip()
        if emesaj.find("\n", esol) == -1:
            emesajb = emesaj[esol:].strip()
        if emesajb.startswith("https://t.me/"):
            return
        ekynk = bot.get_chat(chat)
        logger.warning("{} postu atılıyor... ".format(ekynk.title))
        """ Açıklama tespit """
        eason = emesaj.find("\n", 0, esol)
        eaciklama = emesaj[:eason].strip()
        """    Cookies    """
        s = Session()
        link = s.get("https://ay.live/api")
        cookies = dict(link.cookies)
        """  Veri Tabanı  """
        epostdata = db[str(chat)]
        ebinb = collection.find({})
        """ Dosya tespit """
        if update.channel_post.photo:
            emedya = update.channel_post.photo[0].file_id
        if update.channel_post.animation:
            emedya = update.channel_post.animation.file_id
        if update.channel_post.video:
            emedya = update.channel_post.video.file_id
        for ehesap in ebinb:
            eret = True
            ekaynak = ehesap['kaynak']
            esablon = ehesap['sablon']
            esablon = str(esablon)
            try:
                etoken = ehesap['token']
            except:
                eret = False
            ekanal = ehesap['kanal']
            euser = ehesap['_id']
            esite = ehesap['site']
            ealtapi = ehesap['altapi']
            ealtsite = ehesap['altsite']
            esira = ehesap['sira']
            if "5" in ekaynak and len(ekanal) > 0 and eret:
                elink = " "
                ealink = " "
                ejson = " "
                if esira == "2":
                    etoken = ealtapi
                    esite = ealtsite
                    collection.update_one({"_id": euser}, {"$set": {"sira": "3"}})
                if esira == "3":
                    collection.update_one({"_id": euser}, {"$set": {"sira": "2"}})
                try:
                    if not ealtapi == "None":
                        if ealtsite == "1":
                            ejson = s.get(f"https://ay.live/api/?", params={'api': ealtapi, 'url': emesajb, 'ct': 1}, cookies=cookies).json()
                            ealink = ejson['shortenedUrl']
                        if ealtsite == "2":
                            ejson = s.get(f"https://www.pnd.tl/api?", params={'api': ealtapi, 'url': emesajb, 'category': 6}).json()
                            ealink = ejson['shortenedUrl']
                        if ealtsite == "3":
                            ejson = s.get(f"https://exe.io/api?", params={'api': ealtapi, 'url': emesajb}).json()
                            ealink = ejson['shortenedUrl']
                        if ealtsite == "4":
                            ealink = s.get(f"http://ouo.io/api/{ealtapi}?", params={'s': emesajb}).text
                        if ealtsite == "5":
                            ealink = s.get(f"http://pubiza.com/api.php?", params={'token': ealtapi, 'url': emesajb, 'ads_type': "adult"}).text
                    if esite == "1":
                        ejson = s.get(f"https://ay.live/api/?", params={'api': etoken, 'url': emesajb, 'ct': 1}, cookies=cookies).json()
                        elink = ejson['shortenedUrl']
                    if esite == "2":
                        ejson = s.get(f"https://www.pnd.tl/api?", params={'api': etoken, 'url': emesajb, 'category': 6}).json()
                        elink = ejson['shortenedUrl']
                    if esite == "3":
                        ejson = s.get(f"https://exe.io/api?", params={'api': etoken, 'url': emesajb}).json()
                        elink = ejson['shortenedUrl']
                    if esite == "4":
                        elink = s.get(f"http://ouo.io/api/{etoken}?", params={'s': emesajb}).text
                    if esite == "5":
                        elink = s.get(f"http://pubiza.com/api.php?", params={'token': etoken, 'url': emesajb, 'ads_type': "adult"}).text
                    logger.info(f"{ekanal} + {elink} + {etoken}")
                except Exception as e:
                    bot.send_message(euser, "Son postunuz gönderilemedi;\n\n<code>API adresiniz sıkıntılı veya sitenize ulaşılamıyor. API adresinizi kontrol edin, bir sıkıntı yoksa bu mesajı görmezden gelin muhtemelen seçtiğiniz site ile ilgili bir sorun vardır.</code>")
                    logger.error(e)
                    logger.debug(ejson)
                    eret = False
                if esablon == "1":
                    esablon = f"🔥{eaciklama}\n\n🔱 TIKLA 👉 {elink}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
                elif esablon == "2" or esablon == "3":
                    esablon = f"{eaciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {elink}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 #linkgec06"
                elif esablon == "9":
                    esablon = f"{eaciklama} \n\n𝙇𝙄𝙉𝙆🔗 {elink} \n\n     𝙇𝙄𝙉𝙆🔗 {ealink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 #linkk_gecmee"
                elif esablon.find('{alink}') != -1:
                    esablon = esablon.replace("{link}", "{}").replace("{aciklama}", "{}").replace("{alink}", "{}").format(eaciklama, elink, ealink)
                else:
                    esablon = esablon.replace("{link}", "{}").replace("{aciklama}", "{}").format(eaciklama, elink)
                sleep(0.5)
                for ekan in ekanal:
                    try:
                        if update.channel_post.photo and eret:
                            epost = bot.send_photo(ekan, emedya, caption=esablon)
                        if update.channel_post.video and eret:
                            epost = bot.send_video(ekan, emedya, caption=esablon)
                        if update.channel_post.animation and eret:
                            epost = bot.send_animation(ekan, emedya, caption=esablon)
                        epostkayit = epostdata.find_one({"_id": ekan})
                        if epostkayit == None:
                            epostdata.insert_one({"_id": ekan, "pid": epost.message_id})
                        else:
                            epostdata.update_one({"_id": ekan}, {"$set": {"pid": epost.message_id}})
                        ecount = ecount + 1
                    except Exception as e:
                        logger.debug(f"Hatalı kanal: {ekanal}")
                        e = str(e)
                        if e.find("update.message is") != -1:
                            collection.update_one({"_id": euser}, {"$pull": {"kanal": ekan}})
                            try:
                                bot.send_message(euser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                            except: #Hem update.messageu engelleyip hemde kanaldan sildiyse
                                pass   
                            logger.debug(f"{ekanal} kayıtlardan silindi.")

                logger.info("Başarılı!")
        ebasari = "{} kaynağından, {} Kanalda Post Paylaşıldı.".format(ekynk.title, ecount)
        logger.warning(ebasari)
        bot.send_message(update.messagelog, ebasari)
    # MuhoVip
    elif chat == kaynaklar[5] and muho:
        gcount = 0
        gmesaj = update.channel_post.caption
        if gmesaj == None:
           return
        """ Link tespit """
        gsolx = gmesaj.rfind("http")
        gsol = gmesaj.find("http")
        if gsol == -1:
            return
        if gsol != gsolx:
            return
        gkynk = bot.get_chat(chat)
        gsag = gmesaj.find("\n", gsol)
        gmesajb = gmesaj[gsol:gsag].strip()
        if gmesaj.find("\n", gsol) == -1:
            gmesajb = gmesaj[gsol:].strip()
        if gmesajb.startswith("https://t.me/"):
            return
        logger.warning("{} postu atılıyor... ".format(gkynk.title))
        """ Açıklama tespit """
        gason = gmesaj.find("\n", 0, gsol)
        gaciklama = gmesaj[:gason].strip()
        """    Cookies    """
        s = Session()
        link = s.get("https://ay.live/api")
        cookies = dict(link.cookies)
        """  Veri Tabanı  """
        gpostdata = db[str(chat)]
        gbinb = collection.find({})
        """ Dosya tespit """
        if update.channel_post.photo:
            gmedya = update.channel_post.photo[0].file_id
        if update.channel_post.animation:
            gmedya = update.channel_post.animation.file_id
        if update.channel_post.video:
            gmedya = update.channel_post.video.file_id
        for ghesap in gbinb:
            gret = True
            gkaynak = ghesap['kaynak']
            gsablon = ghesap['sablon']
            gsablon = str(gsablon)
            try:
                gtoken = ghesap['token']
            except:
                gret = False
            gkanal = ghesap['kanal']
            guser = ghesap['_id']
            gsite = ghesap['site']
            galtapi = ghesap['altapi']
            galtsite = ghesap['altsite']
            gsira = ghesap['sira']
            if "6" in gkaynak and len(gkanal) > 0 and gret:
                glink = " "
                galink = " "
                gjson = " "
                if gsira == "2":
                    gtoken = galtapi
                    gsite = galtsite
                    collection.update_one({"_id": guser}, {"$set": {"sira": "3"}})
                if gsira == "3":
                    collection.update_one({"_id": guser}, {"$set": {"sira": "2"}})
                try:
                    if not galtapi == "None":
                        if galtsite == "1":
                            gjson = s.get(f"https://ay.live/api/?", params={'api': galtapi, 'url': gmesajb, 'ct': 1}, cookies=cookies).json()
                            galink = gjson['shortenedUrl']
                        if galtsite == "2":
                            gjson = s.get(f"https://www.pnd.tl/api?", params={'api': galtapi, 'url': gmesajb, 'category': 6}).json()
                            galink = gjson['shortenedUrl']
                        if galtsite == "3":
                            gjson = s.get(f"https://exe.io/api?", params={'api': galtapi, 'url': gmesajb}).json()
                            galink = gjson['shortenedUrl']
                        if galtsite == "4":
                            galink = s.get(f"http://ouo.io/api/{galtapi}?", params={'s': gmesajb}).text
                        if galtsite == "5":
                            galink = s.get(f"http://pubiza.com/api.php?", params={'token': galtapi, 'url': gmesajb, 'ads_type': "adult"}).text
                    if gsite == "1":
                        gjson = s.get(f"https://ay.live/api/?", params={'api': gtoken, 'url': gmesajb, 'ct': 1},
                                      cookies=cookies).json()
                        glink = gjson['shortenedUrl']
                    if gsite == "2":
                        gjson = s.get(f"https://www.pnd.tl/api?", params={'api': gtoken, 'url': gmesajb, 'category': 6}).json()
                        glink = gjson['shortenedUrl']
                    if gsite == "3":
                        gjson = s.get(f"https://exe.io/api?", params={'api': gtoken, 'url': gmesajb}).json()
                        glink = gjson['shortenedUrl']
                    if gsite == "4":
                      glink = s.get(f"http://ouo.io/api/{gtoken}?", params={'s': gmesajb}).text
                    if gsite == "5":
                        glink = s.get(f"http://pubiza.com/api.php?", params={'token': gtoken, 'url': gmesajb, 'ads_type': "adult"}).text
                    logger.info(f"{gkanal} + {glink} + {gtoken}")
                except Exception as e:
                    bot.send_message(guser, "Son postunuz gönderilemedi;\n\n<code>API adresiniz sıkıntılı veya sitenize ulaşılamıyor. API adresinizi kontrol edin, bir sıkıntı yoksa bu mesajı görmezden gelin muhtemelen seçtiğiniz site ile ilgili bir sorun vardır.</code>")
                    logger.error(e)
                    logger.debug(gjson)
                    gret = False
                if gsablon == "1":
                    gsablon = f"🔥{gaciklama}\n\n🔱 TIKLA 👉 {glink}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
                elif gsablon == "2" or gsablon == "3":
                    gsablon = f"{gaciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {glink}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 #linkgec06"
                elif gsablon == "9":
                    gsablon = f"{gaciklama} \n\n𝙇𝙄𝙉𝙆🔗 {glink} \n\n     𝙇𝙄𝙉𝙆🔗 {galink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 #linkk_gecmee"
                elif gsablon.find('{alink}') != -1:
                    gsablon = gsablon.replace("{link}", "{}").replace("{aciklama}", "{}").replace("{alink}", "{}").format(gaciklama, glink, galink)
                else:
                    gsablon = gsablon.replace("{link}", "{}").replace("aciklama", "").format(gaciklama, glink)
                sleep(0.5)
                for gkan in gkanal:
                    try:
                        if update.channel_post.photo and gret:
                            gpost = bot.send_photo(gkan, gmedya, caption=gsablon)
                        if update.channel_post.video and gret:
                            gpost = bot.send_video(gkan, gmedya, caption=gsablon)
                        if update.channel_post.animation and gret:
                            gpost = bot.send_animation(gkan, gmedya, caption=gsablon)
                        gpostkayit = gpostdata.find_one({"_id": gkan})
                        if gpostkayit == None:
                            gpostdata.insert_one({"_id": gkan, "pid": gpost.message_id})
                        else:
                            gpostdata.update_one({"_id": gkan}, {"$set": {"pid": gpost.message_id}})
                        gcount = gcount + 1
                    except Exception as e:
                        logger.debug(f"Hatalı kanal: {gkanal}")
                        e = str(e)
                        if e.find("update.message is") != -1:
                            collection.update_one({"_id": guser}, {"$pull": {"kanal": gkan}})
                            try:
                                bot.send_message(guser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                            except: #Hem update.messageu engelleyip hemde kanaldan sildiyse
                                pass   
                            logger.debug(f"{gkanal} kayıtlardan silindi.")

                logger.info("Başarılı!")
        gbasari = "{} kaynağından, {} Kanalda Post Paylaşıldı.".format(gkynk.title, gcount)
        logger.warning(gbasari)
        bot.send_message(update.messagelog, gbasari)
    # Tutan Linkler
    elif chat == kaynaklar[6] and tutan:
        fcount = 0
        fmesaj = update.channel_post.caption
        if fmesaj == None:
            return
        """ Link tespit """
        fsolx = fmesaj.rfind("http")
        fsol = fmesaj.find("http")
        if fsol == -1:
            return
        if fsol != fsolx:
            return
        fsag = fmesaj.find("\n", fsol)
        fmesajb = fmesaj[fsol:fsag].strip()
        if fmesaj.find("\n", fsol) == -1:
            fmesajb = fmesaj[fsol:].strip()
        if fmesajb.startswith("https://t.me/"):
            return
        fkynk = bot.get_chat(chat)
        logger.warning("{} postu atılıyor... ".format(fkynk.title))
        """ Açıklama tespit """
        fason = fmesaj.find("\n", 0, fsol)
        faciklama = fmesaj[:fason].strip()
        """    Cookies    """
        s = Session()
        link = s.get("https://ay.live/api")
        cookies = dict(link.cookies)
        """  Veri Tabanı  """
        fpostdata = db[str(chat)]
        fbinb = collection.find({})
        """ Dosya tespit """
        if update.channel_post.photo:
            fmedya = update.channel_post.photo[0].file_id
        if update.channel_post.animation:
            fmedya = update.channel_post.animation.file_id
        if update.channel_post.video:
            fmedya = update.channel_post.video.file_id
        for fhesap in fbinb:
            fret = True
            fkaynak = fhesap['kaynak']
            fsablon = fhesap['sablon']
            fsablon = str(fsablon)
            try:
                ftoken = fhesap['token']
            except:
                fret = False
            fkanal = fhesap['kanal']
            fuser = fhesap['_id']
            fsite = fhesap['site']
            faltapi = fhesap['altapi']
            faltsite = fhesap['altsite']
            fsira = fhesap['sira']
            if "7" in fkaynak and len(fkanal) > 0 and fret:
                falink = " "
                flink = " "
                fjson = " "
                if fsira == "2":
                    ftoken = faltapi
                    fsite = faltsite
                    collection.update_one({"_id": fuser}, {"$set": {"sira": "3"}})
                if fsira == "3":
                    collection.update_one({"_id": fuser}, {"$set": {"sira": "2"}})
                try:
                    if not faltapi == "None":
                        if faltsite == "1":
                            fjson = s.get(f"https://ay.live/api/?", params={'api': faltapi, 'url': fmesajb, 'ct': 1}, cookies=cookies).json()
                            falink = fjson['shortenedUrl']
                        if faltsite == "2":
                            fjson = s.get(f"https://www.pnd.tl/api?", params={'api': faltapi, 'url': fmesajb, 'category': 6}).json()
                            falink = fjson['shortenedUrl']
                        if faltsite == "3":
                            fjson = s.get(f"https://exe.io/api?", params={'api': faltapi, 'url': fmesajb}).json()
                            falink = fjson['shortenedUrl']
                        if faltsite == "4":
                            falink = s.get(f"http://ouo.io/api/{faltapi}?", params={'s': fmesajb}).text
                        if faltsite == "5":
                            falink = s.get(f"http://pubiza.com/api.php?", params={'token': faltapi, 'url': fmesajb, 'ads_type': "adult"}).text
                    sleep(1)
                    if fsite == "1":
                        fjson = s.get(f"https://ay.live/api/?", params={'api': ftoken, 'url': fmesajb, 'ct': 1}, cookies=cookies).json()
                        flink = fjson['shortenedUrl']
                    if fsite == "2":
                        fjson = s.get(f"https://www.pnd.tl/api?", params={'api': ftoken, 'url': fmesajb, 'category': 6}).json()
                        flink = fjson['shortenedUrl']
                    if fsite == "3":
                        fjson = s.get(f"https://exe.io/api?", params={'api': ftoken, 'url': fmesajb}).json()
                        flink = fjson['shortenedUrl']
                    if fsite == "4":
                        flink = s.get(f"http://ouo.io/api/{ftoken}?", params={'s': fmesajb}).text
                    if fsite == "5":
                        flink = s.get(f"http://pubiza.com/api.php?", params={'token': faltapi, 'url': fmesajb, 'ads_type': "adult"}).text
                    logger.info(f"{fkanal} + {flink} + {ftoken}")
                except Exception as e:
                    bot.send_message(fuser, "Son postunuz gönderilemedi;\n\n<code>API adresiniz sıkıntılı veya sitenize ulaşılamıyor. API adresinizi kontrol edin, bir sıkıntı yoksa bu mesajı görmezden gelin muhtemelen seçtiğiniz site ile ilgili bir sorun vardır.</code>")
                    logger.error(e)
                    logger.debug(fjson)
                    fret = False
                if fsablon == "1":
                    fsablon = f"🔥{faciklama}\n\n🔱 TIKLA 👉 {flink}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
                elif fsablon == "2" or fsablon == "3":
                    fsablon = f"{faciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {flink}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 #linkgec06"
                elif fsablon == "9":
                    fsablon = f"{faciklama} \n\n𝙇𝙄𝙉𝙆🔗 {flink} \n\n     𝙇𝙄𝙉𝙆🔗 {falink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 #linkk_gecmee"
                elif fsablon.find('{alink}') != -1:
                    fsablon = fsablon.replace("{aciklama}", "{}").replace("{alink}", "{}").replace("{link}", "{}").format(faciklama, flink, falink)
                else:
                    fsablon = fsablon.replace("{aciklama}", "{}").replace("{link}", "{}")
                    fsablon = str(fsablon).format(faciklama, flink)
                sleep(1)
                for fkan in fkanal:
                    try:
                        if update.channel_post.photo and fret:
                            fpost = bot.send_photo(fkan, fmedya, caption=fsablon)
                        if update.channel_post.video and fret:
                            fpost = bot.send_video(fkan, fmedya, caption=fsablon)
                        if update.channel_post.animation and fret:
                            fpost = bot.send_animation(fkan, fmedya, caption=fsablon)
                        fpostkayit = fpostdata.find_one({"_id": fkan})
                        if fpostkayit == None:
                            fpostdata.insert_one({"_id": fkan, "pid": fpost.message_id})
                        else:
                            fpostdata.update_one({"_id": fkan}, {"$set": {"pid": fpost.message_id}})
                        fcount = fcount + 1
                    except Exception as e:
                        logger.debug(f"Hatalı kanal: {fkanal}")
                        e = str(e)
                        if e.find("update.message is") != -1:
                            collection.update_one({"_id": fuser}, {"$pull": {"kanal": fkan}})
                            try:
                                bot.send_message(fuser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                            except: #Hem update.messageu engelleyip hemde kanaldan sildiyse
                                pass   
                            logger.debug(f"{fkanal} kayıtlardan silindi.")
                    
                logger.info("Başarılı!")
        fbasari = "{} kaynağından, {} Kanalda Post Paylaşıldı.".format(fkynk.title, fcount)
        bot.send_message(update.messagelog, fbasari)
        logger.warning(fbasari)
    # Özel Kaynaklar
    else:
        okaynak = OzelCol.find_one({"okaynak": chat})
    if okaynak != None:
        ocount = 0
        omesaj = update.channel_post.caption
        if omesaj == None:
            return
        """  Link tespit  """
        osolx = omesaj.rfind("http")
        osol = omesaj.find("http")
        if osol == -1:
            return
        if osol != osolx:
            return
        osag = omesaj.find("\n", osol)
        okynk = bot.get_chat(chat)
        omesajb = omesaj[osol:osag].strip()
        if omesaj.find("\n", osol) == -1:
            omesajb = omesaj[osol:].strip()
        if omesajb.startswith("https://t.me/"):
            return
        logger.warning("[ÖZEL] {} postu atılıyor... ".format(okynk.title))
        """  Açıklama tespit  """
        oason = omesaj.rfind("\n", 0, osol)
        oaciklama = omesaj[:oason].strip()
        """  Cookies  """
        s = Session()
        link = s.get("https://ay.live/api")
        cookies = dict(link.cookies)
        """  Veri Tabanı  """
        ohesap = collection.find_one({"_id": okaynak['_id']})
        """ Dosya tespit """
        if update.channel_post.photo:
            omedya = update.channel_post.photo[0].file_id
        if update.channel_post.animation:
            omedya = update.channel_post.animation.file_id
        if update.channel_post.video:
            omedya = update.channel_post.video.file_id
        oret = True
        try:
            otoken = ohesap['token']
        except:
            oret = False
        okanal = ohesap['kanal']
        osablon = ohesap['sablon']
        ouser = ohesap['_id']
        osite = ohesap["site"]
        oaltapi = ohesap['altapi']
        oaltsite = ohesap['altsite']
        osira = ohesap['sira']
        if len(okanal) > 0 and oret:
            oalink = " "
            olink = " "
            if osira == "2":
                otoken = oaltapi
                osite = oaltsite
                collection.update_one({"_id": ouser}, {"$set": {"sira": "3"}})
            if osira == "3":
                collection.update_one({"_id": ouser}, {"$set": {"sira": "2"}})
            try:
                if not oaltapi == "None":
                    if oaltsite == "1":
                        ojson = s.get(f"https://ay.live/api/?", params={'api': oaltapi, 'url': omesajb, 'ct': 1}, cookies=cookies).json()
                        oalink = ojson['shortenedUrl']
                    if oaltsite == "2":
                        ojson = s.get(f"https://www.pnd.tl/api?", params={'api': oaltapi, 'url': omesajb, 'category': 6}).json()
                        oalink = ojson['shortenedUrl']
                    if oaltsite == "3":
                        ojson = s.get(f"https://exe.io/api?", params={'api': oaltapi, 'url': omesajb}).json()
                        oalink = ojson['shortenedUrl']
                    if oaltsite == "4":
                        oalink = s.get(f"http://ouo.io/api/{oaltapi}?", params={'s': omesajb}).text
                    if oaltsite == "5":
                        oalink = s.get(f"http://pubiza.com/api.php?", params={'token': oaltapi, 'url': omesajb, 'ads_type': "adult"}).text
                if osite == "1":
                    ojson = s.get(f"https://ay.live/api/?", params={'api': otoken, 'url': omesajb, 'ct': 1}, cookies=cookies).json()
                    olink = ojson['shortenedUrl']
                if osite == "2":
                    ojson = s.get(f"https://www.pnd.tl/api?", params={'api': otoken, 'url': omesajb, 'category': 6}).json()
                    olink = ojson['shortenedUrl']
                if osite == "3":
                    ojson = s.get(f"https://exe.io/api?", params={'api': otoken, 'url': omesajb}).json()
                    olink = ojson['shortenedUrl']
                if osite == "4":
                    olink = s.get(f"http://ouo.io/api/{otoken}?", params={'s': omesajb}).text
                if osite == "5":
                    olink = s.get(f"http://pubiza.com/api.php?", params={'token': etoken, 'url': omesajb, 'ads_type': "adult"}).text
                logger.info(f"{okanal} + {olink} + {otoken}")
            except:
                bot.send_message(ouser, "Son postunuz gönderilemedi;\n\n<code>API adresiniz sıkıntılı veya sitenize ulaşılamıyor. API adresinizi kontrol edin, bir sıkıntı yoksa bu mesajı görmezden gelin muhtemelen seçtiğiniz site ile ilgili bir sorun vardır.</code>")
                logger.error(e)
                oret = False
                
            if osablon == "1":
                osablon = f"🔥{oaciklama}\n\n🔱 TIKLA 👉 {olink}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
            elif osablon == "2" or osablon == "3":
                osablon = f"{oaciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {olink}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 #linkgec06"
            elif osablon == "9":
                osablon = f"{oaciklama} \n\n𝙇𝙄𝙉𝙆🔗 {olink} \n\n     𝙇𝙄𝙉𝙆🔗 {oalink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 #linkk_gecmee"
            elif osablon.find('{alink}') != -1:
                osablon = osablon.replace("{aciklama}", "{}").replace("{alink}", "{}").replace("{link}", "{}").format(oaciklama, olink, oalink)
            else:
                osablon = osablon.replace("{aciklama}", "{}").replace("{link}", "{}").format(oaciklama, olink)
            sleep(1)
            for okan in okanal:
                try:
                    if update.channel_post.photo and oret:
                        opost = bot.send_photo(okan, omedya, caption=osablon)
                    if update.channel_post.video and oret:
                        opost = bot.send_video(okan, omedya, caption=osablon)
                    if update.channel_post.animation and oret:
                        opost = bot.send_animation(okan, omedya, caption=osablon)
                except Exception as e:
                    logger.debug(f"Hatalı kanal: {okanal}")
                    e = str(e)
                    if e.find("update.message is") != -1:
                        collection.update_one({"_id": ouser}, {"$pull": {"kanal": okan}})
                        try:
                            bot.send_message(ouser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                        except: #Hem update.messageu engelleyip hemde kanaldan sildiyse
                            pass                        
                        logger.debug(f"{okanal} kayıtlardan silindi.")
            logger.info("Başarılı!")
        obasari = "[ÖZEL] {} kaynağından post Paylaşıldı.".format(okynk.title)
        logger.warning(obasari)

def gunluk():
    while 0 < 1:
        zaman = datetime.datetime.now()
        if zaman.hour == 11 and zaman.minute == 50:
            msg = bot.send_message(update.messagelog, "<code>Günlük veriler hesaplanıyor...</code>")
            toplam = 0
            kum = []
            kanals = 0
            users = 0
            kullanicilar = collection.find({})
            for kullanici in kullanicilar:
                users += 1
                for kul in kullanici['kanal']:
                    if not kul in kum:
                        kum.append(kul)
                        time.sleep(0.5)
                        try:
                            uye = bot.get_chat_members_count(kul)
                            print(uye)
                        except Exception as e:
                            logger.error(e)
                            time.sleep(30)
                        else:
                            toplam += uye
                            kanals += 1
          
            toplam = toplam / 1000
            toplam = round(toplam, 1)
            msg = bot.edit_message_text("👥 Toplam Kullanıcı Sayısı: {}\n📢 Toplam Kayıtlı Kanal Sayısı: {}\n🙋 Toplam Kitle: {}K\n\nHer gün saat 22:00'da otomatik olarak güncel veriler paylaşılacak.".format(users, kanals, toplam), update.messagelog, msg.message_id)
            update.message.pin_chat_message(update.messagelog, msg.message_id)
        time.sleep(60)
    
threading.Thread(target=gunluk).start()

logger.info("Bot Çalışıyor...")
bildir('Bot Başladı 🍕')

def main() -> None:
    updater = Updater(bot=bot)

    dispatcher = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.text & ~Filters.command, menu)],
        states={ 
            ALTMENU: [MessageHandler(Filters.text, kayitapi)], 
            APIDEGISTIR: [MessageHandler(Filters.text, apikayit)],
            KANALKAYDET: [MessageHandler(~Filters.command, kanalkayit)],
            SABLON: [MessageHandler(Filters.text, sabloniki)],
            PATPOST: [MessageHandler(~Filters.command, pat)]
            },
        fallbacks=[MessageHandler(Filters.regex('^(↩️ Ana Menü)$'), cancel)], 
        )

    conver = ConversationHandler(
        entry_points=[CallbackQueryHandler(sabloncall, pattern="^(sablon)$")],
        states={
            SABLON: [MessageHandler(Filters.text, sabloniki)]
            },
        fallbacks=[MessageHandler(Filters.regex('^(↩️ Ana Menü)$'), cancel)],
        per_message=False)
    altconver = ConversationHandler(
        entry_points=[CallbackQueryHandler(altcall, pattern="^asite(.*)")],
        states={
            ALTAPI: [MessageHandler(Filters.text, altakayit)]
            },
        fallbacks=[MessageHandler(Filters.regex('^(↩️ Ana Menü)$'), cancel)],
        per_message=False)
    ozelkconver = ConversationHandler(
        entry_points=[CallbackQueryHandler(ozelkaynakcall, pattern="^okayt(.*)")],
        states={
            OZELKAYNAK: [MessageHandler(~Filters.command, ozelk)]
            },
        fallbacks=[MessageHandler(Filters.regex('^(↩️ Ana Menü)$'), cancel)],
        per_message=False)
    dispatcher.add_handler(conver)
    dispatcher.add_handler(altconver)
    dispatcher.add_handler(ozelkconver)

    dispatcher.add_handler(conv_handler)

    dispatcher.add_handler(CommandHandler('start', start, Filters.chat_type.private))
    dispatcher.add_handler(MessageHandler(Filters.command('onayla') & Filters.chat_type.channel, post))
    dispatcher.add_handler(MessageHandler(Filters.command('postsil') & Filters.chat_type.channel, kpostsil))
    dispatcher.add_handler(CommandHandler('bul', bul, Filters.chat_type.private))
    dispatcher.add_handler(CommandHandler('onayla', ona, Filters.chat_type.private))
    dispatcher.add_handler(CommandHandler('sil', durdur, Filters.chat_type.private))
    dispatcher.add_handler(CommandHandler('duyuru', duy, Filters.chat_type.private))
    dispatcher.add_handler(CommandHandler('postsil', cpostsil, Filters.chat_type.private))
    dispatcher.add_handler(CommandHandler('dsil', dsil, Filters.chat_type.private))
    dispatcher.add_handler(CommandHandler('stats', stats, Filters.chat_type.private))
    dispatcher.add_handler(CommandHandler('zaman', zaman, Filters.chat_type.private))

    dispatcher.add_handler(MessageHandler(Filters.photo & Filters.chat_type.channel | Filters.video & Filters.chat_type.channel | Filters.animation & Filters.chat_type.channel, poster))

    dispatcher.add_handler(CallbackQueryHandler(kaynakcall, pattern="^kaynak(.*)"))
    dispatcher.add_handler(CallbackQueryHandler(callback_query))

    dispatcher.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
