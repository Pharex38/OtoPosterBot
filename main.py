import requests
from requests import get, Session
from os import environ
import asyncio
from time import sleep
from pymongo import MongoClient
import telebot
from telebot import types
import time, datetime
import threading
import Colorer
import os, signal
import logging
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton 
#botapi = environ['BOT_TOKEN']  
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
botapi = karaliste['bottoken']
bot = telebot.TeleBot(botapi,parse_mode='html')

botlog = -1001352123979
sahip = 1302980840
fixer = 1687646994
adminlist = [1687646994,1302980840]

def bildir(neyi='Boş Bildirim Testi !'):
    global bot
    for i in adminlist:
        try:
            bot.send_message(i,neyi)
        except:
            pass
kaynaklar = [-1001368112299, -1001122395785, -1001423365614, -1001240514861, -1001405966343, -1001368008488, -1001379893661]
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


markup = types.ForceReply(selective=False)

def dugme():
    dugme = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True, selective=True)
    butonbir = types.KeyboardButton('⚙️ Menü')
    butoniki = types.KeyboardButton('🔧 Kaynak')
    butonuc = types.KeyboardButton('📏 Şablon')
    butondort = types.KeyboardButton('▶️ SFS Modu')
    butonbes = types.KeyboardButton('⛓️ Elle Post Paylaş')
    butonalti = types.KeyboardButton('🥰 Bağış')
    dugme.row(butonbir)
    dugme.add(butoniki, butonuc, butondort, butonalti, butonbes)
    return dugme

def markupp():
    markupp = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True, selective=True)
    buton1 = types.KeyboardButton('🔶 Yeni Kanal Ekle')
    buton7 = types.KeyboardButton('↩️ Ana Menü')
    buton2 = types.KeyboardButton('❌ İptal')
    buton3 = types.KeyboardButton('🗑️ Kanal Sil')
    buton4 = types.KeyboardButton('♻️ API değiştir')
    buton5 = types.KeyboardButton('🔗 Site değiştir')
    buton6 = types.KeyboardButton('🤖 Alternatif Ekle')
    markupp.add(buton1, buton3, buton4, buton5, buton6)
    markupp.add(buton7)
    return markupp

def imark():
    imark = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True, selective=True)
    batinbir = types.KeyboardButton('❌ İptal')
    imark.add(batinbir)
    return imark

def dagme():
    dagme = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True, selective=True)
    butonbir = types.KeyboardButton('📝 Kaydet')
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

@bot.message_handler(commands=['start'])
def start(message):
    user = message.from_user.id
    chat = message.chat.id
    if user in kara:
        bot.send_message(chat, "🤓 Üzgünüm senin gibi aptal birisi için çalışmıyorum")
        return
    kat = collection.find_one({"_id": user})
    ref = message.text.split()[1] if len(message.text.split()) > 1 else None
    kyn = str(ref.split('k')[-1]) if len(message.text.split()) > 1 else None
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
    
    mention = "@"+message.from_user.username if message.from_user.username else message.from_user.first_name
    if kat == None:
        bot.send_message(chat, """
✨ <b>Merhaba {}!</b>

❔<b>Ne İşe Yarıyor? </b>
<i>Bu bot sizin seçtiğiniz kaynak kanalında paylaşılan postların linklerini otomatik olarak kısaltıp sizin kanalınızda paylaşır.</i>

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
<i>Bu bot sizin seçtiğiniz kaynak kanalında paylaşılan postların linklerini otomatik olarak kısaltıp sizin kanalınızda paylaşır.</i>

❔<b>Nasıl Kullanılır?</b>
<i>1. Adım: Botu kanlınıza yönetici olarak ekleyin.
2. Adım: Kaydet butonunu kullanarak bilgilerinizi kaydedin.
3. Adım: <b>KANALINIZDA</b> /onayla yazın.
4. Adım: Keyfini çıkarın.</i>

<b>❤️ Geliştirici & Sahip : @Pharex
👨🏻‍🔧 Fix & Eklentiler : @berce</b>

  📔        <b>@OtoPosterBotLog</b>
""".format(mention), disable_web_page_preview=True, reply_markup=dugme())

@bot.message_handler(commands=['stats'])
def stats(message):
    kanals = 0
    users = 0
    toplam = 0
    chat = message.chat.id
    user = message.from_user.id
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

@bot.message_handler(commands=['bul'])
def bul(message):
    cnt = message.text.split()[1] if len(message.text.split()) > 1 else int(message.from_user.id)
    if not message.from_user.id in adminlist:
        bot.send_message(message.chat.id, "Sie")
        return
    try:
        cnt = collection.find({"_id": int(cnt)})
        for c in cnt:
            bot.send_message(message.chat.id, 'ID: {}\nToken: {} \nKaynak: {} \nSite: {} \nKanal: {} \nAlt Token: {} \n Alt Site: {} \n Özel Kaynak: {}'.format(c['_id'], c['token'], c['kaynak'], c['site'], c['kanal'], c['altapi'], c['altsite'], c['ozel']))
    except:
        pass
    try:
        cnt = collection.find({"token": cnt})
        for c in cnt:
            bot.send_message(message.chat.id, 'ID: {}\nToken: {} \nKaynak: {} \nSite: {} \nKanal: {} \nAlt Token: {} \n Alt Site: {} \n Özel Kaynak: {}'.format(c['_id'], c['token'], c['kaynak'], c['site'], c['kanal'], c['altapi'], c['altsite'], c['ozel']))
    except:
        pass
    try:
        cnt = collection.find({"altapi": cnt})
        for c in cnt:
            bot.send_message(message.chat.id, 'ID: {}\nToken: {} \nKaynak: {} \nSite: {} \nKanal: {} \nAlt Token: {} \n Alt Site: {} \n Özel Kaynak: {}'.format(c['_id'], c['token'], c['kaynak'], c['site'], c['kanal'], c['altapi'], c['altsite'], c['ozel']))
    except:
        pass
    try:
        cnt = collection.find({"kanal": [str(cnt)]})
        for c in cnt:
            bot.send_message(message.chat.id, 'ID: {}\nToken: {} \nKaynak: {} \nSite: {} \nKanal: {} \nAlt Token: {} \n Alt Site: {} \n Özel Kaynak: {}'.format(c['_id'], c['token'], c['kaynak'], c['site'], c['kanal'], c['altapi'], c['altsite'], c['ozel']))
    except:
        pass
    try:
        cnt = collection.find({"site": str(cnt)})
        for c in cnt:
            bot.send_message(message.chat.id, 'ID: {}\nToken: {} \nKaynak: {} \nSite: {} \nKanal: {} \nAlt Token: {} \n Alt Site: {} \n Özel Kaynak: {}'.format(c['_id'], c['token'], c['kaynak'], c['site'], c['kanal'], c['altapi'], c['altsite'], c['ozel']))
    except:
        pass

@bot.message_handler(commands=['onayla'])
def ona(m):
    cid = m.chat.id
    bot.send_message(cid, "Bu komutu kanalınızda kullanmalısınız.")

@bot.message_handler(commands=['sil'])
def durdur(message):
    chat = message.chat.id
    user = message.from_user.id
    kimi = message.text.split() if len(message.text.split()) > 1 and user in adminlist else message.from_user.id
    if user in kara:
        bot.send_message(chat, "🤓 Üzgünüm senin gibi aptal birisi için çalışmıyorum")
        return
    try:
        collection.delete_one({"_id": kimi})
    except:
        bot.reply_to(message, "<b>Henüz bir kanal kaydetmemişsiniz.</b>")
    else:
        bot.reply_to(message, "<b>Kanalınız Silindi!</b>")

@bot.channel_post_handler(commands=['postsil'])
def kpostsil(message):
    chat = message.chat.id
    if not chat in kaynaklar:
        return
    mesid = message.reply_to_message.message_id if message.reply_to_message else None
    if mesid == None:
        bot.send_message(chat, "Silmek istediğiniz postu yanıtlayın.")
        return
    data = db[str(chat)].find({"_id": mesid})
    spcount = 0
    for d in data:
        try:
            bot.delete_message(d['chat'], d['pid'])
        except Exception as e:
            logger.error(e)
        else:
            spcount += 1
    bot.send_message(chat, f"{spcount} Post Silindi.")

@bot.message_handler(commands=['postsil'])
def cpostsil(message):
    chat = message.chat.id
    if chat != sahip:
        return
    hedef = message.text.split()[1] if len(message.text.split()) > 1 else None
    mesid = int(message.text.split()[2]) if len(message.text.split()) > 2 else None
    if hedef == None or mesid == None:
        return
    data = db[str(hedef)].find({"_id": mesid})
    spcount = 0
    for d in data:
        try:
            bot.delete_message(d['_id'], d['pid'])
        except Exception as e:
            logger.error(e)
        else:
            spcount += 1
    bot.send_message(chat, f"{spcount} Post Silindi.")
    
@bot.message_handler(commands=['duyuru'])
def duy(m):
    chat = m.chat.id
    if chat != sahip:
        return
    duyurus = 0
    if m.reply_to_message:
        duyurumsg = m.reply_to_message.text
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

@bot.message_handler(commands=['dsil'])
def dsil(m):
    chat = m.chat.id
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
        
@bot.channel_post_handler(commands=['onayla'])
def post(message):
    chat = message.chat.id
    mid = message.id
    mids = mid+1
    bot.reply_to(message, "Tamamdır!")
    sleep(1)
    try:
        bot.delete_message(chat, mid)
        bot.delete_message(chat, mids)
    except:
        pass

@bot.message_handler(commands=['zaman'])
def zaman(message):
    chat = message.chat.id
    msj = message.reply_to_message.text if message.reply_to_message else None
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

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    col = call.message.json
    user = call.message.chat.id
    chat = user
    mesajid = call.message.id
    """ İptal """
    if call.data == "akaldır":
        try:
            collection.update_one({"_id": user}, {"$set": {"altsite": "None", "altapi": "None", "sira": "0", "sablon": "1"}})
            msg = bot.edit_message_text("⛔ Alternatif Kaldırıldı.", user, mesajid)
            bot.answer_callback_query("⛔ Alternatif Kaldırıldı.")
            bot.register_next_step_handler(msg, kayitapi)
        except Exception as e:
            bildir(e)
    if call.data == "aiptal":
        try:
            msg = bot.edit_message_text("<i>İptal Edildi</i>", user, mesajid)
        except Exception as e:
            bildir(e)
    if call.data == "iptal":
        try:
            bot.edit_message_text("<i>İptal Edildi</i>", user, mesajid)
        except Exception as e:
            bildir(e)
    """ Kanal Sil """
    if call.data.startswith("sil"):
        try:
            kul = collection.find_one({"_id": user})
            s = int(call.data.split("-")[1])
            collection.update_one({"_id": user}, {"$pull": {"kanal": kul['kanal'][s]}})
            bot.edit_message_text("Kanalınız Silindi!", user, mesajid)
            bot.answer_callback_query(call.id, "Kanalınız Silindi!")
        except Exception as e:
            bildir(e)
    """ Site Değiştir """
    if call.data.startswith("site"):
        try:
            skul = collection.find_one({"_id": user})
            ss = str(call.data.split("-")[1])
            collection.update_one({"_id": user}, {"$set": {"site": ss}})
            bot.edit_message_text("Site Kaydedildi!\n\nAPI adresinizi seçtiğiniz siteye göre değiştirmeyi unutmayın.", user, mesajid)
            bot.answer_callback_query(call.id, "Site Kaydedildi!")
        except Exception as e:
            bildir(e)
    """ Alternatif """
    if call.data.startswith("asite"):
        try:
            smesaj = str(call.data.split("-")[1])
            sss = str(call.data.split("-")[2])
            bot.answer_callback_query(call.id, "✅ Site Kaydedildi!")
            bot.edit_message_text("✅ Alternatif site kaydedildi.", user, mesajid)
            msg = bot.send_message(chat, "📝 Alternatif API adresinizi gönderin.", reply_markup=imark())
            bot.register_next_step_handler(msg, altakayit, smesaj, user, chat, sss)
        except Exception as e:
            bildir(e)
    if call.data.startswith("sistem"):
        try:
            sss = str(call.data.split("-")[1])
            collection.update_one({"_id": user}, {"$set": {"sira": sss}})
            bot.answer_callback_query(call.id, "✅ Site Kaydedildi!")
            bot.edit_message_text("Alternatif olarak kullanmak istediğiniz siteyi seçin.", user, mesajid)
            bot.edit_message_reply_markup(user, mesajid, reply_markup=altsitemarkup(sss))
        except Exception as e:
            bildir(e)
    """ Kaynak """
    if call.data.startswith("kaynak"):
        try:
            kys = str(call.data.split("-")[1])
            kkul = collection.find_one({"_id": user})
            if kys in kkul['kaynak']:
                collection.update_one({"_id": user}, {"$pull": {"kaynak": kys}})
                bot.answer_callback_query(call.id, "❌ Kaynak Kaldırıldı")
            else:
                collection.update_one({"_id": user}, {"$push": {"kaynak": kys}})
                bot.answer_callback_query(call.id, "✅ Kaynak Eklendi")
            bot.edit_message_reply_markup(chat, mesajid, reply_markup=kaynakmark(user))
        except Exception as e:
            bildir(e)
    if call.data.startswith("zaman"):
        try:
            saat = collection.find_one({"_id": 0})
            dgr = int(call.data.split("-")[1])
            if dgr == 1:
                bot.answer_callback_query(callback_query_id=call.id,show_alert=True, text=saat['mahzen'])
            if dgr == 2:
                bot.answer_callback_query(callback_query_id=call.id,show_alert=True, text=saat['bedava'])
            if dgr == 3:
                bot.answer_callback_query(callback_query_id=call.id,show_alert=True, text=saat['evi'])
            if dgr == 4:
                bot.answer_callback_query(callback_query_id=call.id,show_alert=True, text=saat['bashub'])
            if dgr == 5:
                bot.answer_callback_query(callback_query_id=call.id,show_alert=True, text=saat['acikmi'])
            if dgr == 6:
                bot.answer_callback_query(callback_query_id=call.id,show_alert=True, text=saat['tutan'])
            if dgr == 7:
                bot.answer_callback_query(callback_query_id=call.id,show_alert=True, text=saat['muho'])
        except Exception as e:
            bildir(e)
    if call.data == "okay":
        try:
            bot.edit_message_text("""<b>Özel Kaynak Hakkında Bilmeniz Gerekenler</b>\n\n<i>- Özel kaynak ayarlarsanız başka kaynak seçemezsiniz.\n- Sadece size özeldir başkası kullanamaz.\n- Özel kaynağa kısaltılmamış link atmanız gerekiyor. Kısaltılmış linkli post atarsanız bot linki geçmez direkt olarak kısaltılmış linki tekrar kısaltır.</i>\n\n<b>Alttaki butona bastığınız zaman işlem iptal edilemez!</b>""", chat, mesajid)
            bot.edit_message_reply_markup(chat, mesajid, reply_markup=ozelmark())
        except Exception as e:
            bildir(e)
    if call.data == "okayt":
        try:
            if OzelCol.find_one({"_id": user}) == None:
                OzelCol.insert_one({"_id": user})
        
            bot.delete_message(chat, mesajid)
            msg = bot.send_message(chat, """<b>Yapmanız Gerekenler</b>
<i>
1 - Kaynak yapacağınız kanal oluşturun.
2 - Oluşturduğunuz kanaldan bota bir mesaj iletin.</i>""", reply_markup=imark())
            bot.register_next_step_handler(msg, ozelk)
        except Exception as e:
            bildir(e)
    if call.data == "okayk":
        try:
            collection.update_one({"_id": user}, {"$set": {"ozel": False}})
            OzelCol.delete_one({"_id": user})
            bot.edit_message_text("Özel Kaynak Kaldırıldı.", chat, mesajid)
        except Exception as e:
            bildir(e)
    """ PAT """
    if call.data.startswith("pat"):
        try:
            back = call.data.split("-")
            o = int(back[1]) - 1
            ptip = patc.ptip
            psablon = patc.psablon
            fid = patc.fid
        
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
                return
            if ptip == 'photo':
                bot.send_photo(kanal[o], fid, caption=psablon)
            if ptip == 'video':
                bot.send_video(kanal[o], fid, caption=psablon)
            if ptip == 'animation':
                bot.send_animation(kanal[o], fid, caption=psablon)
            bot.edit_message_text("✅<b>Postunuz  Kanalınıza Gönderildi!</b>", user, mesajid)
        except Exception as e:
            bildir(e)
    """ Şablon """
    if call.data == "sablon":
        try:
            bot.delete_message(user, mesajid)
            if collection.find_one({"_id": user})['sira'] == "1":
                msz = bot.send_message(chat, "<i>Oluşturduğunuz şablonda</i> <b>{aciklama}, {alink}</b> ve <b>{link}</b> <i>kelimelerinin bulunduğundan emin olun yoksa şablon çalışmaz</i>", reply_markup=imark())
            else:
                msz = bot.send_message(chat, "<i>Oluşturduğunuz şablonda</i> <b>{aciklama}</b> ve <b>{link}</b> <i>kelimelerinin bulunduğundan emin olun yoksa şablon çalışmaz</i>", reply_markup=imark())
            bot.register_next_step_handler(msz, sabloniki)
        except Exception as e:
            bildir(e)
    if call.data == "vsablon":
        try:
            if collection.find_one({"_id": user})['sira'] == "1":
                collection.update_one({"_id": user}, {"$set": {"sablon": "9"}})
            else:
                collection.update_one({"_id": user}, {"$set": {"sablon": "1"}})
            bot.edit_message_text("Varsayılana döndürüldü.", chat, mesajid)
        except Exception as e:
            bildir(e)
        
def sitemarkup():
    smark = InlineKeyboardMarkup()
    smark.row_width = 2
    smark.add(InlineKeyboardButton("TRLink", callback_data="site-1"))
    smark.add(InlineKeyboardButton("PND.TL", callback_data="site-2"))
    smark.add(InlineKeyboardButton("Exe.io", callback_data="site-3"))
    smark.add(InlineKeyboardButton("Ouo.io", callback_data="site-4"))
    smark.add(InlineKeyboardButton("Pubiza", callback_data="site-5"))
    smark.row(InlineKeyboardButton("❌ İptal ❌", callback_data="iptal"))
    
    return smark

def altsitemarkup(sss):
    asmark = InlineKeyboardMarkup()
    asmark.row_width = 2
    asmark.add(InlineKeyboardButton("TRLink", callback_data="asite-1-{}".format(sss)))
    asmark.add(InlineKeyboardButton("PND.TL", callback_data="asite-2-{}".format(sss)))
    asmark.add(InlineKeyboardButton("Exe.io", callback_data="asite-3-{}".format(sss)))
    asmark.add(InlineKeyboardButton("Ouo.io", callback_data="asite-4-{}".format(sss)))
    asmark.add(InlineKeyboardButton("Pubiza", callback_data="asite-5-{}".format(sss)))
    asmark.row(InlineKeyboardButton("❌ İptal ❌", callback_data="iptal"))
    
    return asmark

def altmarkup(user):
    altmark = InlineKeyboardMarkup()
    altmark.row_width = 1
    altmark.add(InlineKeyboardButton("Sıralı", callback_data="sistem-2"))
    altmark.add(InlineKeyboardButton("Tek Post İki Link", callback_data="sistem-1"))
    altmark.add(InlineKeyboardButton("❌ İptal ❌", callback_data="iptal"))
    if collection.find_one({"_id": user})['altapi'] != "None":
        altmark.add(InlineKeyboardButton("⛔ Alternatif Kaldır", callback_data="akaldır"))
    return altmark

def inmark():
    inmark = InlineKeyboardMarkup(row_width = 1)
    inmark.row(InlineKeyboardButton("❌ İptal ❌", callback_data="aiptal"))

    return inmark

def ozelmark():
    omark = InlineKeyboardMarkup(row_width = 1)
    omark.add(InlineKeyboardButton("➕ Oluştur ➕", callback_data="okayt"))
    omark.row(InlineKeyboardButton("❌ İptal ❌", callback_data="aiptal"))

    return omark

def kaynakmark(user):
    u = collection.find_one({"_id": user})
    kmark = InlineKeyboardMarkup(row_width=2)
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
        kmark.row(InlineKeyboardButton("🟣 Özel Kaynağı Kaldır 🟣", callback_data="okayk"))
        kmark.row(InlineKeyboardButton("❌ İptal ❌", callback_data="aiptal"))
        return kmark        
    kmark.add(ubut)
    if "1" in u['kaynak']:
        kmark.add(InlineKeyboardButton("✅".format(mahzen.title), callback_data="kaynak-1"), saatbut)
    else:
        kmark.add(InlineKeyboardButton("⚫".format(mahzen.title), callback_data="kaynak-1"), saatbut)
    kmark.add(bbut)
    if "2" in u['kaynak']:
        kmark.add(InlineKeyboardButton("✅".format(bedava.title), callback_data="kaynak-2"), bsaatbut)
    else:
        kmark.add(InlineKeyboardButton("⚫".format(bedava.title), callback_data="kaynak-2"), bsaatbut)
    kmark.add(cbut)
    if "3" in u['kaynak']:
        kmark.add(InlineKeyboardButton("✅".format(evi.title), callback_data="kaynak-3"), csaatbut)
    else:
        kmark.add(InlineKeyboardButton("⚫".format(evi.title), callback_data="kaynak-3"), csaatbut)
    kmark.add(dbut)
    if "4" in u['kaynak']:
        kmark.add(InlineKeyboardButton("✅".format(bashub.title), callback_data="kaynak-4"), dsaatbut)
    else:
        kmark.add(InlineKeyboardButton("⚫".format(bashub.title), callback_data="kaynak-4"), dsaatbut)
    kmark.add(ebut)
    if "5" in u['kaynak']:
        kmark.add(InlineKeyboardButton("✅".format(acikmi.title), callback_data="kaynak-5"), esaatbut)
    else:
        kmark.add(InlineKeyboardButton("⚫".format(acikmi.title), callback_data="kaynak-5"), esaatbut)
    kmark.add(gbut)
    if "6" in u['kaynak']:
        kmark.add(InlineKeyboardButton("✅".format(muho.title), callback_data="kaynak-6"), gsaatbut)
    else:
        kmark.add(InlineKeyboardButton("⚫".format(muho.title), callback_data="kaynak-6"), gsaatbut)
    kmark.add(fbut)
    if "7" in u['kaynak']:
        kmark.add(InlineKeyboardButton("✅".format(tutan.title), callback_data="kaynak-7"), fsaatbut)
    else:
        kmark.add(InlineKeyboardButton("⚫".format(tutan.title), callback_data="kaynak-7"), fsaatbut)
    kmark.row(InlineKeyboardButton("❌ İptal ❌", callback_data="aiptal"))
    kmark.row(InlineKeyboardButton("♋️ Özel Kaynak Oluştur ♋️", callback_data="okay"))
        
    return kmark

def sablonmark(user):
    samark = InlineKeyboardMarkup(row_width=2)
    if collection.find_one({"_id": user})['sablon'] in ["1", "2", "3", "9"]:
        samark.add(InlineKeyboardButton("➕ Şablon Oluştur ➕", callback_data="sablon"))
    else:
        samark.add(InlineKeyboardButton("➕ Şablon Değiştir ➕", callback_data="sablon"))
        samark.add(InlineKeyboardButton("🔁 Varsayılan Şablonu Kullan 🔁", callback_data="vsablon"))
    samark.add(InlineKeyboardButton("❌ İptal ❌", callback_data="aiptal"))
    return samark

def patmark(user):
    zero = 0
    pmark = InlineKeyboardMarkup()
    pmark.row_width = 1
   
    pkul = collection.find_one({"_id": user})
    pmark.add(InlineKeyboardButton("Hepsine Gönder", callback_data="pat-0"))
    
    for k in pkul['kanal']:
        kn = bot.get_chat(k)
        zero += 1
        pmark.add(InlineKeyboardButton("{}".format(kn.title), callback_data="pat-{}".format(zero)))
    pmark.row(InlineKeyboardButton("❌ İptal ❌", callback_data="aiptal"))
    
    return pmark
    
def gen_markup(user):
    silkey = InlineKeyboardMarkup()
    silkey.row_width = 1
    kayd = collection.find_one({"_id": user})
    butonno = 0
    for k in kayd['kanal']:
        ismi = bot.get_chat(k)
        silkey.add(InlineKeyboardButton("{}".format(ismi.title), callback_data="sil-{}".format(butonno)))
        butonno += 1
    silkey.row(InlineKeyboardButton("❌ İptal ❌", callback_data="iptal"))
    
    return silkey

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
            bot.send_message(chat, "<b>Varsayılan Şablon:</b>\n\n{aciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {link}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 @linkgec06", reply_markup=sablonmark(user))
        elif mj['sablon'] == "9":
            bot.send_message(chat, "<b>Varsayılan Şablon:</b>\n\n{aciklama} \n\n𝙇𝙄𝙉𝙆🔗 {link} \n\n     𝙇𝙄𝙉𝙆🔗 {alink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 @linkk_gecmee", reply_markup=sablonmark(user))
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
            bot.register_next_step_handler(msg, apikayit)
            return
    if mesaj == "⚙️ Menü":
        kayitli = 0
        chat = message.chat.id
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
        bot.register_next_step_handler(msg, pat)
        return
        
    kisi = collection.find_one({"_id": user})
    if kisi == None:
        bot.send_message(chat, "<i>Lütfen alttaki butonları kullan</i>", reply_markup=dagme())
        return
    bot.send_message(chat, "<i>Lütfen alttaki butonları kullan</i>", reply_markup=dugme())
    
def ozelk(message):
    user = message.from_user.id
    chat = message.chat.id
    if message.text == "❌ İptal":
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme())
        return
    if not message.forward_from_chat:
        msz = bot.send_message(message.chat.id, "Lütfen bana oluşturduğun kanaldan bir mesaj ilet.")
        bot.register_next_step_handler(msz, ozelk)
        return
    kanal = message.forward_from_chat.id
    if kanal in kaynaklar:
        mst = bot.send_message(chat, "Kaynak kanalını nasıl kaydedebilirim ki?")
        bot.register_next_step_handler(mst, ozelk)
        return
    try:
        yetkiler = bot.get_chat_administrators(kanal)
    except:
        msg = bot.send_message(chat, "Botu kanalınızda yönetici eklememişsiniz.")
        bot.register_next_step_handler(msg, ozelk)
        return
    if message.forward_from_chat:
        ileti = message.forward_from_chat.id
        OzelCol.update_one({"_id": user}, {"$set": {"okaynak": ileti}})
        collection.update_one({"_id": user}, {"$set": {"ozel": True, "kaynak": ["32"]}})
        bot.send_message(message.chat.id, "<b>Özel Kaynak Oluşturuldu!</b>", reply_markup=dugme())

def kaynake(message):
    ktext = message.text
    chat = message.chat.id
    user = message.from_user.id
    if message.text == None:
        msg = bot.send_message(chat, "Lütfen istediğiniz kaynağın numarasını gönderin.")
        bot.register_next_step_handler(msg, kaynake)
        return
    if message.text == "❌ İptal":
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme())
        return
    ktext = ktext.split(",")
    bnb = collection.find_one({"_id": user})
    if bnb == None:
        bot.send_message(chat, "Lütfen kaynak seçmeden önce Kaydet butonu ile bilgilerinizi kaydedin.", reply_markup=dugme())
    else:
        collection.update_one({"_id": user}, {"$set":{"kaynak": ktext}})
        bot.send_message(chat, "Kaynak Kaydedildi!", reply_markup=dugme())

def sabloniki(message):
    mesaj = message.text
    chat = message.chat.id
    user = message.from_user.id
    bnb = collection.find_one({"_id": user})
    if message.text == None:
        msg = bot.send_message(chat, """ ❌<i> Lütfen mesajınızda "{link}" ve "{aciklama}" bulunduğudan emin olun.</i> """)
        bot.register_next_step_handler(msg, sabloniki)
        return
    if message.text == "❌ İptal":
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme())
        return
    if not mesaj.isdigit() and bnb['sira'] == "1":
        if mesaj.find("{link}") == -1 or mesaj.find("{aciklama}") == -1 or mesaj.find("{alink}") == -1:
            msg = bot.send_message(chat, """ ❌<i> Lütfen mesajınızda "{link}", "{alink}" ve "{aciklama}" bulunduğudan emin olun.</i> """)
            bot.register_next_step_handler(msg, sabloniki)
            return
        if mesaj.find("{link}") > mesaj.find("{alink}"):
            msg = bot.send_message(chat, """ ❌<i> Şablonunuzda {link} kelimesi {alink}'ten önde olmak zorundadır</i> """)
            bot.register_next_step_handler(msg, sabloniki)
            return
    if not mesaj.isdigit():
        if mesaj.find("{link}") == -1 or mesaj.find("{aciklama}") == -1:
            msg = bot.send_message(chat, """ ❌<i> Lütfen mesajınızda "{link}" ve "{aciklama}" bulunduğudan emin olun.</i> """)
            bot.register_next_step_handler(msg, sabloniki)
            return
        if mesaj.find("{link}") != mesaj.rfind("{link}"):
            msg = bot.send_message(chat, """ ❌<i> Lütfen mesajınızda bir tane "{link}" bulunduğudan emin olun.</i> """)
            bot.register_next_step_handler(msg, sabloniki)
            return
        if mesaj.find("{aciklama}") != mesaj.rfind("{aciklama}"):
            msg = bot.send_message(chat, """ ❌<i> Lütfen mesajınızda bir tane "{aciklama}" bulunduğudan emin olun.</i> """)
            bot.register_next_step_handler(msg, sabloniki)
            return
    if bnb == None:
        bot.send_message(chat, "Lütfen şablon kaydetmeden önce Kaydet butonu ile bilgilerinizi girin!", reply_markup=dugme())
    else:
        collection.update_one({"_id": user}, {"$set":{"sablon": mesaj}})
        bot.send_message(chat, "Şablon kaydedildi!", reply_markup=dugme())

def kayitapi(message):
    chat = message.chat.id
    mesaj = message.text
    user = message.from_user.id
    ka = collection.find_one({"_id": user})
    vip_uyeler = collection.find_one({"_id": 0})['vipuye']
    if mesaj == "🗑️ Kanal Sil":
        if len(ka['kanal']) < 1:
            msg = bot.send_message(chat, "Henüz bir kanal kaydetmemişsiniz!", reply_markup=markupp())
            bot.register_next_step_handler(msg, kayitapi)
            return
        msg = bot.send_message(chat, "Silmek istediğiniz kanalı seçin.", reply_markup=gen_markup(user))
        bot.register_next_step_handler(msg, kayitapi)
        return
    if mesaj == "♻️ API değiştir":
        msg = bot.send_message(chat, "Yeni API adresinizi girin.", reply_markup=imark())
        bot.register_next_step_handler(msg, apikayit)
        return
    if mesaj == "↩️ Ana Menü" or mesaj == "❌ İptal":
        msg = bot.send_message(chat, "İptal Edildi.", reply_markup=dugme())
        return
    if mesaj == "🔗 Site değiştir":
        msg = bot.send_message(chat, "<i>Kullanmak istediğiniz siteyi seçin</i>", reply_markup=sitemarkup())
        bot.register_next_step_handler(msg, kayitapi)
        return
    if mesaj == "🤖 Alternatif Ekle":
        msg = bot.send_message(chat, "<b>Alternatif Nasıl Kullanılsın.\n\n Tek Post İki Link</b>\n <i>Aynı post iki link</i> \n\n<b>Sıralı</b>\n <i>Bir post birinci servis, bir post alternatif servis.</i>\n\n<b>Kullanmak istediğiniz sistemi seçin.</b>", reply_markup=altmarkup(user))
        bot.register_next_step_handler(msg, kayitapi)
        return
    if mesaj == "🔶 Yeni Kanal Ekle":
        bol = collection.find_one({"_id": chat})
        if len(bol['kanal']) > 2 and not user in vip_uyeler:
            bot.send_message(chat, "<i>Üzgünüm en fazla 3 kanal kaydedebilirsiniz.</i>")
            return
        msg = bot.send_message(chat, """📝 <i>Lütfen kanalınızdan bir gönderi iletin.</i>""", reply_markup=imark())
        bot.register_next_step_handler(msg, kanalkayit)
        return
    msg = bot.send_message(chat, "Lütfen alttaki butonları kullanın.", reply_markup=markupp())
    bot.register_next_step_handler(msg, kayitapi)

def altakayit(message, smesaj, user, chat, sss):
    amesaj = message.text
    if message.text == "❌ İptal" or message.text == None:
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme())
        return
    if message.text == "⛔ Alternatif Kaldır":
        collection.update_one({"_id": user}, {"$set": {"altsite": "None", "altapi": "None", "sablon": "1", "sira": "0"}})
        bot.send_message(chat, "Alternatif kaldırıldı, artık postlarınız alternatif linksiz paylaşılacak.", reply_markup=dugme())
        return
    
    collection.update_one({"_id": user}, {"$set": {"altsite": smesaj, "altapi": amesaj, "sira": sss}})
    bot.send_message(chat, "✅ Alternatif API kaydedildi", reply_markup=dugme())

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
        if bnb == None:
            bot.send_message(chat, "İptal Edildi.", reply_markup=dagme())
        else:
            bot.send_message(chat, "İptal Edildi.", reply_markup=dugme())
        return
    if bnb == None:
        kontrol = get("https://ay.live/api/?api={}&url=www.zort.com&format=text&alias=&ct=2".format(token)).text
        if kontrol == "":
            mso = bot.send_message(chat, "❌ Geçersiz bir API verdiniz! Lütfen doğru bir API adresi verin.")
            bot.register_next_step_handler(mso, apikayit)
            return
    if token.startswith("http"):
        mso = bot.send_message(chat, "❌ Geçersiz bir API verdiniz! Lütfen doğru bir API adresi verin.")
        bot.register_next_step_handler(mso, apikayit)
        return
    key = {"_id": user, "token": token, "kanal": [], "sablon": "1", "kaynak": ["1"], "site": "1", "altapi": "None", "altsite": "None", "sira": "0", "ozel": False}
    if bnb == None:
        collection.insert_one(key)
    else:
        collection.update_one({"_id": user}, {"$set": {"token": token}})
    bot.send_message(chat, "<b>🟢 API kaydedildi!</b>", reply_markup=dugme())

def kanalkayit(message):
    chat = message.chat.id
    user = message.from_user.id
    y = collection.find_one({"_id": user})
    if message.text == "❌ İptal":
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme())
        return
    if not message.forward_from_chat:
        msg = bot.send_message(chat, "↪️ Bunun ne olduğu hakkında bir fikrim yok! Lütfen kanaldan herhangi bir gönderi iletin.", reply_markup=imark())
        bot.register_next_step_handler(msg, kanalkayit)
        return
    kanal = message.forward_from_chat.id
    if kanal in kaynaklar:
        mst = bot.send_message(chat, "Kaynak kanalını nasıl kaydedebilirim ki?", reply_markup=imark())
        bot.register_next_step_handler(mst, kanalkayit)
        return
    if str(kanal) in y['kanal']:
        msl = bot.send_message(chat, "Bu kanalı zaten kaydetmişsiniz")
        bot.register_next_step_handler(msl, kanalkayit)
        return
    try:
        kanalbilgi = bot.get_chat(kanal)
    except:
        msg = bot.send_message(chat, "Botu kanalınızda yönetici eklememişsiniz.")
        bot.register_next_step_handler(msg, kanalkayit)
        return
    try:
        yetkiler = bot.get_chat_administrators(kanal)
    except:
        msg = bot.send_message(chat, "Botu kanalınızda yönetici eklememişsiniz.")
        bot.register_next_step_handler(msg, kanalkayit)
        return
    for y in yetkiler:
        if y.user.id == user:
            collection.update_one({"_id": user}, {"$push":{"kanal": str(kanal)}})
            bot.reply_to(message,"<b>🟢Kanalınız Kaydedildi.</b>", reply_markup=dugme())
            return
            break
    msz = bot.send_message(chat, "Bu kanal sizin değil 😠")
    bot.register_next_step_handler(msz, kanalkayit)

def pat(message):
    chat = message.chat.id
    user = message.from_user.id
    ptip = message.content_type 
    if message.text == "❌ İptal":
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme())
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
    elif message.content_type == "photo":
        fid = message.photo[0].file_id
    elif message.content_type == "animation":
        fid = message.animation.file_id
    else:
        bot.send_message(chat, "Bu dosya türü desteklenmiyor. Lütfen bir video, fotoğraf veya gif gönderin.")
        return
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
            psablon = f"{paciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {plink}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 @linkgec06"
        elif psablon == "9":
            psablon = f"{paciklama} \n\n𝙇𝙄𝙉𝙆🔗 {plink} \n\n     𝙇𝙄𝙉𝙆🔗 {palink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 @linkk_gecmee"
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
        return
    
    patc.psablon = psablon
    patc.ptip = ptip
    patc.fid = fid
    if pret:
        bot.send_message(chat, "Post Hazırlandı!", reply_markup=dugme())
        bot.send_message(chat, "<i>Postun gönderilmesini istediğin kanalı seç.</i>", reply_markup=patmark(user))
    else:
        bot.send_message(chat, "Bir hata oluştu")
@bot.channel_post_handler(content_types=['photo', 'animation', 'video'])
def poster(message):
    okaynak = None
    chat = message.chat.id
    # Link Mahzeni
    if chat == kaynaklar[0] and mahzen:
        count = 0
        mesaj = message.caption
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
        mesjid = message.message_id
        """ Dosya tespit """
        if message.content_type == "photo":
            medya = message.photo[0].file_id
        if message.content_type == "animation":
            medya = message.animation.file_id
        if message.content_type == "video":
            medya = message.video.file_id
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
                    sablon = f"{aciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {link}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 @linkgec06"
                elif sablon == "9":
                    sablon = f"{aciklama} \n\n𝙇𝙄𝙉𝙆🔗 {link} \n\n     𝙇𝙄𝙉𝙆🔗 {alink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 @linkk_gecmee"
                elif sablon.find('{alink}') != -1:
                    sablon = sablon.replace("{aciklama}", "{}").replace("{alink}", "{}").replace("{link}", "{}").format(aciklama, link, alink)
                else:
                    sablon = sablon.replace("{aciklama}", "{}").replace("{link}", "{}").format(aciklama, link)
                sleep(1)
                for kan in kanal:
                    try:
                        if message.content_type == "photo" and ret:
                            post = bot.send_photo(kan, medya, caption=sablon)
                        if message.content_type == "video" and ret:
                            post = bot.send_video(kan, medya, caption=sablon)
                        if message.content_type == "animation" and ret:
                            post = bot.send_animation(kan, medya, caption=sablon)
                        count = count + 1
                    except Exception as e:
                        logger.debug(f"Hatalı kanal: {kanal}")
                        e = str(e)
                        if e.find("bot is") != -1:
                            collection.update_one({"_id": user}, {"$pull": {"kanal": kan}})
                            try:
                                bot.send_message(user, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                            except: #Hem botu engelleyip hemde kanaldan sildiyse
                                pass   
                            logger.debug(f"{kanal} kayıtlardan silindi.")
                    else:
                        postdata.insert_one({"pid": post.message_id, "chat": kan, "mesih": mesjid})
                        count = count + 1
                logger.info("Başarılı!")
            else:
                pass
        basari = "{} kaynağından, {} Kanalda Post Paylaşıldı.".format(kynk.title, count)
        logger.warning(basari)
        bot.send_message(botlog, basari)
    # Bedava Link
    elif chat == kaynaklar[1] and bedava:
        bcount = 0
        bmesaj = message.caption
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
        bmesjid = message.message_id
        """ Dosya tespit """
        if message.content_type == "photo":
            bmedya = message.photo[0].file_id
        if message.content_type == "animation":
            medya = message.animation.file_id
        if message.content_type == "video":
            bmedya = message.video.file_id
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
                    bsablon = f"{baciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {blink}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 @linkgec06"
                elif bsablon == "9":
                    bsablon = f"{baciklama} \n\n𝙇𝙄𝙉𝙆🔗 {blink} \n\n     𝙇𝙄𝙉𝙆🔗 {balink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 @linkk_gecmee"
                elif bsablon.find('{alink}') != -1:
                    bsablon = bsablon.replace("{aciklama}", "{}").replace("{alink}","{}").replace("{link}", "{}").format(baciklama, blink, balink)
                    
                else:
                    bsablon = bsablon.replace("{aciklama}", "{}").replace("{link}", "{}")
                    bsablon = str(bsablon).format(baciklama, blink)
                sleep(1)
                for bkan in bkanal:
                    try:
                        if message.content_type == "photo" and bret:
                            bpost = bot.send_photo(bkan, bmedya, caption=bsablon)
                        if message.content_type == "video" and bret:
                            bpost = bot.send_video(bkan, bmedya, caption=bsablon)
                        if message.content_type == "animation" and bret:
                            bpost = bot.send_animation(bkan, bmedya, caption=bsablon)
                    except Exception as e:
                        logger.debug(f"Hatalı kanal: {bkanal}")
                        e = str(e)
                        if e.find("bot is") != -1:
                            collection.update_one({"_id": buser}, {"$pull": {"kanal": bkan}})
                            try:
                                bot.send_message(buser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                            except: #Hem botu engelleyip hemde kanaldan sildiyse
                                pass   
                            logger.debug(f"{bkanal} kayıtlardan silindi.")
                    else:
                        bpostdata.insert_one({"mesih": bmesjid, "pid": bpost.message_id, "chat": bkan})
                        bcount = bcount + 1
                logger.info("Başarılı!")
        bbasari = "{} kaynağından, {} Kanalda Post Paylaşıldı.".format(bkynk.title, bcount)
        logger.warning(bbasari)
        bot.send_message(botlog, bbasari)
    # Link Evi
    elif chat == kaynaklar[2] and evi:
        ccount = 0
        cmesaj = message.caption
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
        cmesjid = message.message_id
        """ Dosya tespit """
        if message.content_type == "photo":
            cmedya = message.photo[0].file_id
        if message.content_type == "animation":
            cmedya = message.animation.file_id
        if message.content_type == "video":
            cmedya = message.video.file_id
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
                    csablon = f"{caciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {clink}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 @linkgec06"
                elif csablon == "9":
                    csablon = f"{caciklama} \n\n𝙇𝙄𝙉𝙆🔗 {clink} \n\n     𝙇𝙄𝙉𝙆🔗 {calink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 @linkk_gecmee"
                elif csablon.find('{alink}') != -1:
                    csablon = csablon.replace("{link}", "{}").replace("{aciklama}", "{}").replace("{alink}","{}").format(caciklama, clink, calink)
                    
                else:
                    csablon = csablon.replace("{link}", "{}").replace("aciklama", "").format(caciklama, clink)
                sleep(1)
                for ckan in ckanal:
                    try:
                        if message.content_type == "photo" and cret:
                            cpost = bot.send_photo(ckan, cmedya, caption=csablon)
                        if message.content_type == "video" and cret:
                            cpost = bot.send_video(ckan, cmedya, caption=csablon)
                        if message.content_type == "animation" and cret:
                            cpost = bot.send_animation(ckan, cmedya, caption=csablon)
                    except Exception as e:
                        logger.debug(f"Hatalı kanal: {ckanal}")
                        e = str(e)
                        if e.find("bot is") != -1:
                            collection.update_one({"_id": cuser}, {"$pull": {"kanal": ckan}})
                            try:
                                bot.send_message(cuser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                            except: #Hem botu engelleyip hemde kanaldan sildiyse
                                pass   
                            logger.debug(f"{ckanal} kayıtlardan silindi.")
                    else:
                        cpostdata.insert_one({"chat": ckan, "pid": cpost.message_id, "mesih": cmesjid})
                        ccount = ccount + 1
                logger.info("Başarılı!")
        cbasari = "{} kaynağından, {} Kanalda Post Paylaşıldı.".format(ckynk.title, ccount)
        logger.warning(cbasari)
        bot.send_message(botlog, cbasari)
    # BAŞHUB
    elif chat == kaynaklar[3] and bashub:
        dcount = 0
        dmesaj = message.caption
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
        dmesjid = message.message_id
        """ Dosya tespit """
        if message.content_type == "photo":
            dmedya = message.photo[0].file_id
        if message.content_type == "animation":
            dmedya = message.animation.file_id
        if message.content_type == "video":
            dmedya = message.video.file_id
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
                    dsablon = f"{daciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {dlink}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 @linkgec06"
                elif dsablon == "9":
                    dsablon = f"{daciklama} \n\n𝙇𝙄𝙉𝙆🔗 {dlink} \n\n     𝙇𝙄𝙉𝙆🔗 {dalink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 @linkk_gecmee"
                elif dsablon.find('{alink}') != -1:
                    dsablon = dsablon.replace("{link}", "{}").replace("{aciklama}", "{}").replace("{alink}", "{}").format(daciklama, dlink, dalink)
                else:
                    dsablon = dsablon.replace("{link}", "{}").replace("{aciklama}", "{}").format(daciklama, dlink)
                sleep(0.5)
                for dkan in dkanal:
                    try:
                        if message.content_type == "photo" and dret:
                            dpost = bot.send_photo(dkan, dmedya, caption=dsablon)
                        if message.content_type == "video" and dret:
                            dpost = bot.send_video(dkan, dmedya, caption=dsablon)
                        if message.content_type == "animation" and dret:
                            dpost = bot.send_animation(dkan, dmedya, caption=dsablon)
                    except Exception as e:
                        logger.debug(f"Hatalı kanal: {dkanal}")
                        e = str(e)
                        if e.find("bot is") != -1:
                            collection.update_one({"_id": duser}, {"$pull": {"kanal": dkan}})
                            try:
                                bot.send_message(duser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                            except: #Hem botu engelleyip hemde kanaldan sildiyse
                                pass   
                            logger.debug(f"{dkanal} kayıtlardan silindi.")
                    else:
                        dpostdata.insert_one({"chat": dkan, "pid": dpost.message_id, "mesih": dmesjid})
                        dcount = dcount + 1
                logger.info("Başarılı!")
        dbasari = "{} kaynağından, {} Kanalda Post Paylaşıldı.".format(dkynk.title, dcount)
        logger.warning(dbasari)
        bot.send_message(botlog, dbasari)
    # Açık mı link
    elif chat == kaynaklar[4] and acikmi:
        ecount = 0
        emesaj = message.caption
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
        emesjid = message.message_id
        """ Dosya tespit """
        if message.content_type == "photo":
            emedya = message.photo[0].file_id
        if message.content_type == "animation":
            emedya = message.animation.file_id
        if message.content_type == "video":
            emedya = message.video.file_id
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
                    esablon = f"{eaciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {elink}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 @linkgec06"
                elif esablon == "9":
                    esablon = f"{eaciklama} \n\n𝙇𝙄𝙉𝙆🔗 {elink} \n\n     𝙇𝙄𝙉𝙆🔗 {ealink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 @linkk_gecmee"
                elif esablon.find('{alink}') != -1:
                    esablon = esablon.replace("{link}", "{}").replace("{aciklama}", "{}").replace("{alink}", "{}").format(eaciklama, elink, ealink)
                else:
                    esablon = esablon.replace("{link}", "{}").replace("{aciklama}", "{}").format(eaciklama, elink)
                sleep(0.5)
                for ekan in ekanal:
                    try:
                        if message.content_type == "photo" and eret:
                            epost = bot.send_photo(ekan, emedya, caption=esablon)
                        if message.content_type == "video" and eret:
                            epost = bot.send_video(ekan, emedya, caption=esablon)
                        if message.content_type == "animation" and eret:
                            epost = bot.send_animation(ekan, emedya, caption=esablon)
                    except Exception as e:
                        logger.debug(f"Hatalı kanal: {ekanal}")
                        e = str(e)
                        if e.find("bot is") != -1:
                            collection.update_one({"_id": euser}, {"$pull": {"kanal": ekan}})
                            try:
                                bot.send_message(euser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                            except: #Hem botu engelleyip hemde kanaldan sildiyse
                                pass   
                            logger.debug(f"{ekanal} kayıtlardan silindi.")
                    else:
                        epostdata.insert_one({"chat": ekan, "pid": epost.message_id, "mesih": emesjid})
                        ecount = ecount + 1
                logger.info("Başarılı!")
        ebasari = "{} kaynağından, {} Kanalda Post Paylaşıldı.".format(ekynk.title, ecount)
        logger.warning(ebasari)
        bot.send_message(botlog, ebasari)
    # MuhoVip
    elif chat == kaynaklar[5] and muho:
        gcount = 0
        gmesaj = message.caption
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
        gmesjid = message.message_id
        """ Dosya tespit """
        if message.content_type == "photo":
            gmedya = message.photo[0].file_id
        if message.content_type == "animation":
            gmedya = message.animation.file_id
        if message.content_type == "video":
            gmedya = message.video.file_id
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
                    gsablon = f"{gaciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {glink}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 @linkgec06"
                elif gsablon == "9":
                    gsablon = f"{gaciklama} \n\n𝙇𝙄𝙉𝙆🔗 {glink} \n\n     𝙇𝙄𝙉𝙆🔗 {galink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 @linkk_gecmee"
                elif gsablon.find('{alink}') != -1:
                    gsablon = gsablon.replace("{link}", "{}").replace("{aciklama}", "{}").replace("{alink}", "{}").format(gaciklama, glink, galink)
                else:
                    gsablon = gsablon.replace("{link}", "{}").replace("aciklama", "").format(gaciklama, glink)
                sleep(0.5)
                for gkan in gkanal:
                    try:
                        if message.content_type == "photo" and gret:
                            gpost = bot.send_photo(gkan, gmedya, caption=gsablon)
                        if message.content_type == "video" and gret:
                            gpost = bot.send_video(gkan, gmedya, caption=gsablon)
                        if message.content_type == "animation" and gret:
                            gpost = bot.send_animation(gkan, gmedya, caption=gsablon)
                    except Exception as e:
                        logger.debug(f"Hatalı kanal: {gkanal}")
                        e = str(e)
                        if e.find("bot is") != -1:
                            collection.update_one({"_id": guser}, {"$pull": {"kanal": gkan}})
                            try:
                                bot.send_message(guser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                            except: #Hem botu engelleyip hemde kanaldan sildiyse
                                pass   
                            logger.debug(f"{gkanal} kayıtlardan silindi.")
                    else:
                        gpostdata.insert_one({"chat": gkan, "pid": gpost.message_id, "mesih": gmesjid})
                        gcount = gcount + 1

                logger.info("Başarılı!")
        gbasari = "{} kaynağından, {} Kanalda Post Paylaşıldı.".format(gkynk.title, gcount)
        logger.warning(gbasari)
        bot.send_message(botlog, gbasari)
    # Tutan Linkler
    elif chat == kaynaklar[6] and tutan:
        fcount = 0
        fmesaj = message.caption
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
        fmesjid = message.message_id
        """ Dosya tespit """
        if message.content_type == "photo":
            fmedya = message.photo[0].file_id
        if message.content_type == "animation":
            fmedya = message.animation.file_id
        if message.content_type == "video":
            fmedya = message.video.file_id
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
                    fsablon = f"{faciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {flink}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 @linkgec06"
                elif fsablon == "9":
                    fsablon = f"{faciklama} \n\n𝙇𝙄𝙉𝙆🔗 {flink} \n\n     𝙇𝙄𝙉𝙆🔗 {falink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 @linkk_gecmee"
                elif fsablon.find('{alink}') != -1:
                    fsablon = fsablon.replace("{aciklama}", "{}").replace("{alink}", "{}").replace("{link}", "{}").format(faciklama, flink, falink)
                else:
                    fsablon = fsablon.replace("{aciklama}", "{}").replace("{link}", "{}")
                    fsablon = str(fsablon).format(faciklama, flink)
                sleep(1)
                for fkan in fkanal:
                    try:
                        if message.content_type == "photo" and fret:
                            fpost = bot.send_photo(fkan, fmedya, caption=fsablon)
                        if message.content_type == "video" and fret:
                            fpost = bot.send_video(fkan, fmedya, caption=fsablon)
                        if message.content_type == "animation" and fret:
                            fpost = bot.send_animation(fkan, fmedya, caption=fsablon)
                    except Exception as e:
                        logger.debug(f"Hatalı kanal: {fkanal}")
                        e = str(e)
                        if e.find("bot is") != -1:
                            collection.update_one({"_id": fuser}, {"$pull": {"kanal": fkan}})
                            try:
                                bot.send_message(fuser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                            except: #Hem botu engelleyip hemde kanaldan sildiyse
                                pass   
                            logger.debug(f"{fkanal} kayıtlardan silindi.")
                    else:
                        fpostdata.insert_one({"chat": fkan, "pid": fpost.message_id, "mesih": fmesjid})
                        fcount = fcount + 1
                    
                logger.info("Başarılı!")
        fbasari = "{} kaynağından, {} Kanalda Post Paylaşıldı.".format(fkynk.title, fcount)
        bot.send_message(botlog, fbasari)
        logger.warning(fbasari)
    # Özel Kaynaklar
    else:
        okaynak = OzelCol.find_one({"okaynak": chat})
    if okaynak != None:
        ocount = 0
        omesaj = message.caption
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
        if message.content_type == "photo":
            omedya = message.photo[0].file_id
        if message.content_type == "animation":
            omedya = message.animation.file_id
        if message.content_type == "video":
            omedya = message.video.file_id
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
                osablon = f"{oaciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {olink}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 @linkgec06"
            elif osablon == "9":
                osablon = f"{oaciklama} \n\n𝙇𝙄𝙉𝙆🔗 {olink} \n\n     𝙇𝙄𝙉𝙆🔗 {oalink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 @linkk_gecmee"
            elif osablon.find('{alink}') != -1:
                osablon = osablon.replace("{aciklama}", "{}").replace("{alink}", "{}").replace("{link}", "{}").format(oaciklama, olink, oalink)
            else:
                osablon = osablon.replace("{aciklama}", "{}").replace("{link}", "{}").format(oaciklama, olink)
            sleep(1)
            for okan in okanal:
                try:
                    if message.content_type == "photo" and oret:
                        opost = bot.send_photo(okan, omedya, caption=osablon)
                    if message.content_type == "video" and oret:
                        opost = bot.send_video(okan, omedya, caption=osablon)
                    if message.content_type == "animation" and oret:
                        opost = bot.send_animation(okan, omedya, caption=osablon)
                except Exception as e:
                    logger.debug(f"Hatalı kanal: {okanal}")
                    e = str(e)
                    if e.find("bot is") != -1:
                        collection.update_one({"_id": ouser}, {"$pull": {"kanal": okan}})
                        try:
                            bot.send_message(ouser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                        except: #Hem botu engelleyip hemde kanaldan sildiyse
                            pass                        
                        logger.debug(f"{okanal} kayıtlardan silindi.")
            logger.info("Başarılı!")
        obasari = "[ÖZEL] {} kaynağından post Paylaşıldı.".format(okynk.title)
        logger.warning(obasari)

def gunluk():
    while 0 < 1:
        zaman = datetime.datetime.now()
        if zaman.hour == 11 and zaman.minute == 50:
            msg = bot.send_message(botlog, "<code>Günlük veriler hesaplanıyor...</code>")
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
            msg = bot.edit_message_text("👥 Toplam Kullanıcı Sayısı: {}\n📢 Toplam Kayıtlı Kanal Sayısı: {}\n🙋 Toplam Kitle: {}K\n\nHer gün saat 22:00'da otomatik olarak güncel veriler paylaşılacak.".format(users, kanals, toplam), botlog, msg.message_id)
            bot.pin_chat_message(botlog, msg.message_id)
        time.sleep(60)
    
threading.Thread(target=gunluk).start()

logger.info("Bot Çalışıyor...")
bildir('Bot Başladı 🍕')
bot.polling(none_stop=False, interval=0)