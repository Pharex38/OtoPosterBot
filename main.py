
from requests import get, Session
from os import environ
from time import sleep
from pymongo import MongoClient
import time, datetime
import threading, pytz, os, asyncio, logging
from ssl import CERT_NONE
from typing import Dict, TypedDict, List, Literal, cast
import Colorer
from telegram import *
from telegram.error import *
from telegram.ext import *
from telegram.utils.helpers import *

mpass = os.environ['MONGOPASS']
mongo = f"os.environ["MONGO_URI"]"

pid = ogetpid()
open("pid.txt", "w").write(str(pid))
print(pid)

cluster = MongoClient(mongo, ssl_cert_reqs=CERT_NONE)
db = cluster["OtoPost"]
collection = db["Kanallar"]
OzelCol = db["Özel Kaynaklar"]
maindata = collection.find_one({"_id": 0})
kara = maindata['kara']
apikara = maindata['apikara']
bottoken = maindata['bottoken']
para = maindata['para']
bot = ExtBot(bottoken, defaults=Defaults(parse_mode=ParseMode.HTML, run_async=True, timeout=99))

blog = -1001391561285
botlog = -1001352123979
sahip = 1302980840
fixer = 1687646994
adminlist = [1687646994,1302980840]

def bildir(neyi='Boş Bildirim Testi !'):
    for i in adminlist:
        try:
            bot.send_message(i,neyi)
        except:
            pass

kaynaklar = [-1001368112299, -1001122395785, -1001423365614, -1001240514861, -1001405966343, -1001368008488, -1001379893661, -1001572457634]

SEND_MEDIA_TYPES = {"document": bot.send_document, "photo": bot.send_photo, "video": bot.send_video, "animation": bot.send_animation}

ALTMENU, APIDEGISTIR, KANALKAYDET = range(3)

OZELKAYNAK = range(1)

OZELBOTLOG = range(1)

ALTAPI = range(1)

SABLON = range(1)

PATZAMAN = range(1)

PATPOST = range(1)

markup = ForceReply(selective=False)

def dugme(user):
    first = collection.find_one({'_id': user})
    if first == None:
        return ReplyKeyboardMarkup(keyboard=[['📝 Kaydet']], row_width=2, one_time_keyboard=True, resize_keyboard=True, selective=True)

    dugme = ReplyKeyboardMarkup(keyboard=[['⚙️ Menü'], ['🔧 Kaynak', '📏 Şablon'], ['▶️ SFS Modu', '🥰 Bağış'], ['⛓️ Elle Post Paylaş']], resize_keyboard=True)
    
    return dugme

def markupp():
    markupp = ReplyKeyboardMarkup(keyboard=[['🔶 Yeni Kanal Ekle', '🗑️ Kanal Sil'], ['♻️ API değiştir', '🔗 Site değiştir'], ['🤖 Alternatif Ekle'], ['↩️ Ana Menü']], row_width=2, one_time_keyboard=False, resize_keyboard=True)

    return markupp

def imark():
    imark = ReplyKeyboardMarkup(keyboard=[['❌ İptal']], one_time_keyboard=True, resize_keyboard=True, selective=True)

    return imark

def dagme():
    dagme = ReplyKeyboardMarkup(keyboard=[['📝 Kaydet']], row_width=2, one_time_keyboard=True, resize_keyboard=True, selective=True)

    return dagme

def deep(u_kod, user):
    kat = collection.find_one({"_id": user})
    key = {"_id": user, "kanal": [], "sablon": "1", "kaynak": ["32"], "site": "1", "altapi": "None", "altsite": "None", "sira": "0", "ozel": True}
    if int(u_kod) > 10:
        ref_kanal_ismi = bot.get_chat(OzelCol.find_one({"_id": int(u_kod)})['okaynak']).title
        if kat == None:
            if not user in OzelCol.find_one({"_id": int(u_kod)})['kanal']:
                OzelCol.update_one({"_id": int(u_kod)}, {"$push": {"kanal": user}})
            collection.insert_one(key)
            bot.send_message(user, "🏋🏻 {} referansı ile geldiniz!".format(ref_kanal_ismi))
            bot.send_message(user, "📝 API adresinizi gönderin.", reply_markup=imark())
            return False
        else:
            if user in OzelCol.find_one({"_id": int(u_kod)})['kanal']:
                bot.send_message(user, "Zaten Bu Kaynağı Kullanıyorsunuz!", reply_markup=dugme(user))
                return True
            collection.update_one({"_id": user}, {"$set": {"ozel": True, "kaynak": ["32"]}})
            OzelCol.update_one({"_id": int(u_kod)}, {"$push": {"kanal": user}})
            bot.send_message(user, "🏋🏻 {} referansı ile geldiniz!".format(ref_kanal_ismi), reply_markup=dugme(user))
            return True
    uu_kod = int(u_kod) - 1
    key = {"_id": user, "kanal": [], "sablon": "1", "kaynak": [str(u_kod)], "site": "1", "altapi": "None", "altsite": "None", "sira": "0", "ozel": False, "pcount": 0}
    ref_kanal_ismi = bot.get_chat(kaynaklar[int(uu_kod)]).title
    if kat == None:
        collection.insert_one(key)
        bot.send_message(user, "🏋🏻 {} referansı ile geldiniz!".format(ref_kanal_ismi))
        bot.send_message(user, "📝 API adresinizi gönderin.", reply_markup=imark())
        return False
    else:
        if not kat['ozel']:
            collection.update_one({"_id": user}, {"$push": {"kaynak": str(u_kod)}})
            bot.send_message(user, "Kaynağınız Eklendi!", reply_markup=dugme(user))
        else:
            bot.send_message(user, "Özel kaynağınız olduğu için başka kaynak kullanamazsınız!")
        return True

def phaapi(sit):
    if sit == "1":
        return "***REMOVED-SHORTENER-KEY***"
    if sit == "2":
        return "***REMOVED-SHORTENER-KEY***"
    if sit == "3":
        return "***REMOVED-SHORTENER-KEY***"
    if sit == "4":
        return "***REMOVED-SHORTENER-KEY***"
    if sit == "5":
        return "***REMOVED-SHORTENER-KEY***"
    
def setup_logger():
    global logger
    zaman = datetime.datetime.now()
    logd = "{}.{}.{} - {}.{}".format(zaman.year, zaman.month, zaman.day, zaman.hour, zaman.minute)
    file_handler = logging.FileHandler(f'Loglar/{logd}.txt', 'w', 'utf-8')
    stream_handler = logging.StreamHandler()
    logger = logging.getLogger("main_log")
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger.addHandler(file_handler)
    #logger.addHandler(stream_handler)


############## Komutlar #####################
def start(update, context):
    user = update.message.from_user.id
    chat = update.message.chat.id
    bot = context.bot
    if user in kara:
        bot.send_message(chat, "🤓 Üzgünüm senin gibi aptal birisi için çalışmıyorum")
        return
    
    if len(context.args) > 0:
        ref = context.args[0]
        kyn = str(ref.split('k')[-1]) if len(update.message.text.split()) > 1 else None
        if deep(kyn, user):
            return
        return APIDEGISTIR
    
    mention = "@"+update.message.from_user.username if update.message.from_user.username else update.message.from_user.first_name
    bot.send_message(chat, """
✨ <b>Merhaba {}!</b>

❔<b>Ne İşe Yarıyor? </b>
<i>Bu bot sizin seçtiğiniz kaynak kanalında paylaşılan postların linklerini otomatik olarak kısaltıp sizin kanalınızda paylaşır.</i>

❔<b>Nasıl Kullanılır?</b>
<i>1. Adım: Botu kanlınıza yönetici olarak ekleyin.
2. Adım: Kaydet butonunu kullanarak bilgilerinizi kaydedin.
3. Adım: <b>KANALINIZDA</b> /onayla yazın.
4. Adım: Keyfini çıkarın.</i>

❔<b>Senin kazancın nedir?</b>
<i>kanalınıza atılan <b>yirmi</b> linkten birisi benim API adresim ile kısaltılır.</i>

<b>❤️ Geliştirici & Sahip : @Pharex
👨🏻‍🔧 Fix & Eklentiler : @berce</b>
 
  📔        <b>@OtoPosterBotLog</b>
""".format(mention), disable_web_page_preview=True, reply_markup=dugme(user))
    return ConversationHandler.END

def stats(update, context):
    kanals = 0
    users = 0
    toplam = 0
    chat = update.message.chat.id
    user = update.message.from_user.id
    kum = []
    kulkum = []
    mahzen_kitle, bedava_kitle, hazır_kitle, acikmi_kitle, bashub_kitle, evi_kitle, tutan_kitle = 0, 0, 0, 0, 0, 0, 0
    ozel_kaynak_kullanan_sayisi, mahzen_kullanan_sayisi, hazır_kullanan_sayisi, tutan_kullanan_sayisi, acikmi_kullanan_sayisi, bedava_kullanan_sayisi, evi_kullanan_sayisi, bashub_kullanan_sayisi = 0, 0, 0, 0, 0, 0, 0, 0
    exe_kullanan_sayisi, pubiza_kullanan_sayisi, ouo_kullanan_sayisi, trlink_kullanan_sayisi, pnd_kullanan_sayisi = 0, 0, 0, 0, 0
    if not user in [sahip,fixer]:
        bot.send_message(chat, "Sen benim sahibim değilsin!")
        return
    msg = bot.send_message(chat, "<code> Veriler toplanıyor...</code>")
    kullanicilar = [x for x in collection.find({})]
    for kullanici in kullanicilar:
        if not kullanici in kulkum:
            kulkum.append(kullanici)
            users += 1
            if kullanici['site'] == "1":
                trlink_kullanan_sayisi += 1
            elif kullanici['site'] == "2":
                pnd_kullanan_sayisi += 1
            elif kullanici['site'] == "3":
                exe_kullanan_sayisi += 1
            elif kullanici['site'] == "4":
                ouo_kullanan_sayisi += 1
            elif kullanici['site'] == "5":
                pubiza_kullanan_sayisi += 1
            if "1" in kullanici['kaynak']:
                mahzen_kullanan_sayisi += 1
            if "2" in kullanici['kaynak']:
                bedava_kullanan_sayisi += 1
            if "3" in kullanici['kaynak']:
                evi_kullanan_sayisi += 1
            if "4" in kullanici['kaynak']:
                bashub_kullanan_sayisi += 1
            if "5" in kullanici['kaynak']:
                acikmi_kullanan_sayisi += 1
            if "6" in kullanici['kaynak']:
                hazır_kullanan_sayisi += 1
            if "7" in kullanici['kaynak']:
                tutan_kullanan_sayisi += 1
            if kullanici['ozel']:
                ozel_kaynak_kullanan_sayisi += 1
            for kul in kullanici['kanal']:
                if not kul in kum:
                    kum.append(kul)
                    time.sleep(0.5)
                    kanals += 1
                    try:
                        uye = bot.get_chat_members_count(kul)
                        print(uye)
                    except Exception as e:
                        logger.error(e)
                        time.sleep(20)
                    else:
                        toplam += uye
                        if "1" in kullanici['kaynak']:
                            mahzen_kitle += uye
                        if "2" in kullanici['kaynak']:
                            bedava_kitle += uye
                        if "3" in kullanici['kaynak']:
                            evi_kitle += uye
                        if "4" in kullanici['kaynak']:
                            bashub_kitle += uye
                        if "5" in kullanici['kaynak']:
                            acikmi_kitle += uye
                        if "6" in kullanici['kaynak']:
                            hazır_kitle += uye
                        if "7" in kullanici['kaynak']:
                            tutan_kitle += uye
          
    toplam = toplam / 1000
    toplam = str(round(toplam, 1))+"K" if round(toplam, 1) < 1000 else str(round(toplam / 1000, 2))+"M"
    bot.edit_message_text(f"Toplam Kullanıcı Sayısı: {users}\nToplam Kayıtlı Kanal Sayısı: {kanals}\nToplam Kitle: {toplam}\n\n<b>Toplam Site Kullanan Sayısı;</b>\nTRLink: {trlink_kullanan_sayisi}\nPND.TL: {pnd_kullanan_sayisi}\nExe.io: {exe_kullanan_sayisi}\nOuo.io: {ouo_kullanan_sayisi}\nPubiza: {pubiza_kullanan_sayisi}\n\n<b>Toplam Kaynak Kullanan Sayıları:</b>\n{mahzen.title}: {mahzen_kullanan_sayisi} Kitle: {mahzen_kitle}\n{bedava.title}: {bedava_kullanan_sayisi} Kitle: {bedava_kitle}\n{evi.title}: {evi_kullanan_sayisi} Kitle: {evi_kitle}\n{bashub.title}: {bashub_kullanan_sayisi} Kitle: {bashub_kitle}\n{acikmi.title}: {acikmi_kullanan_sayisi} Kitle: {acikmi_kitle}\n{muho.title}: {hazır_kullanan_sayisi} Kitle: {hazır_kitle}\n{tutan.title}: {tutan_kullanan_sayisi} Kitle: {tutan_kitle}\nÖzel kullanan: {ozel_kaynak_kullanan_sayisi} ", chat, msg.message_id)

def joblist(update, context):
     jobs = context.job_queue.jobs()
     context.job_queue.run_once(jobyedekleme, when=1, name="yedekleme")
     for jok in jobs:
        if str(jok.name) != "yedekleme" or str(jok.name) != "gunluk":
            bot.send_message(update.message.chat.id, str(jok.context)+"\n\n\n"+str(jok.name)+"\n\n\n"+str(jok.job))

def parak(update, context):
    global para
    if collection.find_one({"_id": 0})['para']:
        collection.update_one({"_id": 0}, {"$set": {"para": False}})
    else:
        collection.update_one({"_id": 0}, {"$set": {"para": True}})
    para = collection.find_one({"_id": 0})['para']
    bot.send_message(update.message.chat.id, f"Para: {para}")

def bul(update, context):
    cnt = update.message.text.split()[1] if len(update.message.text.split()) > 1 else int(update.message.from_user.id)
    if not update.message.from_user.id in adminlist:
        bot.send_message(update.message.chat.id, "Sie")
        return
    try:
        cntt = collection.find({"_id": int(cnt)})
        for c in cntt:
            bot.send_message(update.message.chat.id, 'ID: {}\nToken: {} \nKaynak: {} \nSite: {} \nKanal: {} \nAlt Token: {} \n Alt Site: {} \n Özel Kaynak: {}'.format(c['_id'], c['token'], c['kaynak'], c['site'], c['kanal'], c['altapi'], c['altsite'], c['ozel']))
    except:
        pass
    try:
        cntt = collection.find({"token": cnt})
        for c in cntt:
            bot.send_message(update.message.chat.id, 'ID: {}\nToken: {} \nKaynak: {} \nSite: {} \nKanal: {} \nAlt Token: {} \n Alt Site: {} \n Özel Kaynak: {}'.format(c['_id'], c['token'], c['kaynak'], c['site'], c['kanal'], c['altapi'], c['altsite'], c['ozel']))
    except:
        pass
    try:
        cntt = collection.find({"altapi": cnt})
        for c in cntt:
            bot.send_message(update.message.chat.id, 'ID: {}\nToken: {} \nKaynak: {} \nSite: {} \nKanal: {} \nAlt Token: {} \n Alt Site: {} \n Özel Kaynak: {}'.format(c['_id'], c['token'], c['kaynak'], c['site'], c['kanal'], c['altapi'], c['altsite'], c['ozel']))
    except:
        pass
    try:
        cntt = collection.find({})
        for c in cntt:
            if cnt in c['kanal']:
                bot.send_message(update.message.chat.id, 'ID: {}\nToken: {} \nKaynak: {} \nSite: {} \nKanal: {} \nAlt Token: {} \n Alt Site: {} \n Özel Kaynak: {}'.format(c['_id'], c['token'], c['kaynak'], c['site'], c['kanal'], c['altapi'], c['altsite'], c['ozel']))
    except:
        pass
    try:
        cntt = collection.find({"site": cnt})
        for c in cntt:
            bot.send_message(update.message.chat.id, 'ID: {}\nToken: {} \nKaynak: {} \nSite: {} \nKanal: {} \nAlt Token: {} \n Alt Site: {} \n Özel Kaynak: {}'.format(c['_id'], c['token'], c['kaynak'], c['site'], c['kanal'], c['altapi'], c['altsite'], c['ozel']))
    except:
        pass

def ona(m, context):
    cid = m.message.chat.id
    msj = bot.send_message(cid, "Bu komutu kanalınızda kullanmalısınız.")

def durdur(update, context):
    chat = update.message.chat.id
    user = update.message.from_user.id
    kimi = int(update.message.text.split()[1]) if len(update.message.text.split()) > 1 and user in adminlist else update.message.from_user.id
    if collection.find_one({"_id": kimi}) == None:
        bot.send_message(chat, "Henüz bir bilgi kaydetmemişsin.", reply_markup=dagme())
        return
    if collection.find_one({"_id": kimi})['ozel']:
        for oc in OzelCol.find({}):
            if kimi in oc['kanal']:
                OzelCol.update_one({"_id": oc['_id']}, {"$pull": {"kanal": kimi}})
                break
    collection.delete_one({"_id": kimi})
    bot.send_message(chat, "<b>Kanalınız Silindi!</b>", reply_markup=dagme())

def kpostsil(update, context):
    chat = update.channel_post.chat.id
    if not chat in kaynaklar:
        return
    mesid = update.channel_post.reply_to_message.message_id if update.channel_post.reply_to_message else None
    if mesid == None:
        bot.send_message(chat, "Silmek istediğiniz postu yanıtlayın.")
        return
    data = db[str(chat)].find({"mesih": mesid})
    spcount = 0
    for d in data:
        try:
            bot.delete_message(d['chat'], d['pid'])
        except Exception as e:
            logger.error(e)
        else:
            spcount += 1
    bot.send_message(chat, f"{spcount} Post Silindi.")

def cpostsil(update, context):
    chat = update.message.chat.id
    if chat != sahip:
        return

    hedef = "-100"+update.message.text.split("/")[-2] if len(update.message.text.split()) > 1 else None
    mesid = int(update.message.text.split("/")[-1]) if len(update.message.text.split()) > 1 else None
    if hedef == None or mesid == None:
        return
    data = db[str(hedef)].find({"mesih": mesid})
    spcount = 0
    for d in data:
        try:
            bot.delete_message(d['chat'], d['pid'])
        except Exception as e:
            logger.error(e)
        else:
            spcount += 1
    bot.send_message(chat, f"{spcount} Post Silindi.")

def viple(update, context):
    chat = update.message.chat.id
    bot.send_message(context.args[0], "Hesabınız Artık VIP!")
    try:
        collection.update_one({"_id": 0}, {"$push": {"vipuye": int(context.args[0])}})
    except Exception as e:
        bot.send_message(chat, e)
    else:
        bot.send_message(chat, "Kullanıcı artık VIP!")

def apibanla(update, context):
    global apikara
    chat = update.message.chat.id
    try:
        collection.update_one({"_id": 0}, {"$push": {"apikara": str(context.args[0])}})
    except Exception as e:
        bot.send_message(chat, e)
    else:
        bot.send_message(chat, "API yasaklandı!")
    apikara = collection.find_one({"_id": 0})['apikara']

def banla(update, context):
    global kara
    chat = update.message.chat.id
    try:
        collection.update_one({"_id": 0}, {"$push": {"kara": int(context.args[0])}})
    except Exception as e:
        bot.send_message(chat, e)
    else:
        bot.send_message(chat, "Kullanıcı yasaklandı!")
    kara = collection.find_one({"_id": 0})['kara']

def unbanla(update, context):
    global kara
    chat = update.message.chat.id
    try:
        collection.update_one({"_id": 0}, {"$pull": {"kara": int(context.args[0])}})
    except Exception as e:
        bot.send_message(chat, e)
    else:
        bot.send_message(chat, "Kullanıcının yasağı kaldırıldı!")
    kara = collection.find_one({"_id": 0})['kara']

def duy(update, context):
    chat = update.message.chat.id
    if chat != sahip:
        return
    duyurus = 0
    if update.message.reply_to_message:
        duyurumsg = update.message.reply_to_message.text
        kullanicilar = collection.find({})
        for kullanici in kullanicilar:
            if len(kullanici['kanal']) > 0:
                try:
                    dmsg = bot.send_message(kullanici['_id'], duyurumsg, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("😕 Bilgilerimi sil", callback_data="dsil")], [InlineKeyboardButton("✅ Kullanmaya devam etmek istiyorum.", callback_data="devam")]]))
                except Exception as e:
                    logger.error(e)
                else:
                    duyurus += 1
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
            db[str(chat)].delete_one({"_id": t['_id']})
    bot.send_message(chat, "{} Duyuru Mesajı Silindi!".format(sd))
        
def post(update, context):
    chat = update.channel_post.chat.id
    mid = update.channel_post.message_id
    msj = update.channel_post.reply_text("Tamamdır!")
    sleep(1.5)
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

############# Error Handler ##################
import html
import json
import traceback
def error_handler(update: object, context: CallbackContext) -> None:
    logger.error(msg="Bir Hata oluştu:", exc_info=context.error)
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = ''.join(tb_list)
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        f'BİR HATA OLUŞTU!\n'
        f'<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}'
        '</pre>\n\n'
        f'<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n'
        f'<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n'
        f'<pre>{html.escape(tb_string)}</pre>'
    )

    context.bot.send_message(chat_id=1302980840, text=message, parse_mode=ParseMode.HTML)

################ Callback ###################
def sabloncall(call, context):
    user = call.effective_user.id
    chat = call.effective_chat.id
    mesajid = call.effective_message.message_id
    bot.delete_message(chat, mesajid)
    if collection.find_one({"_id": user}) == None:
        call.callback_query.edit_message_text(text="<b>Önce bir API kaydedin!</b>")
        return
    if collection.find_one({"_id": user})['sira'] == "1":
        msz = bot.send_message(chat, "<i>Oluşturduğunuz şablonda</i> <b>{aciklama}, {alink}</b> ve <b>{link}</b> <i>kelimelerinin bulunduğundan emin olun yoksa şablon çalışmaz</i>", reply_markup=imark())
    else:
        msz = bot.send_message(chat, "<i>Oluşturduğunuz şablonda</i> <b>{aciklama}</b> ve <b>{link}</b> <i>kelimelerinin bulunduğundan emin olun yoksa şablon çalışmaz</i>", reply_markup=imark())
    return SABLON

def altcall(call, context):
    user = call.effective_user.id
    chat = call.effective_chat.id
    mesajid = call.effective_message.message_id
    smesaj = str(call.callback_query.data.split("-")[1])
    context.user_data['asite'] = smesaj
    call.callback_query.answer(call.callback_query.id, "✅ Site Kaydedildi!")
    bot.edit_message_text("✅ Alternatif site kaydedildi.", user, mesajid)
    bot.send_message(chat, "📝 Alternatif API adresinizi gönderin.", reply_markup=imark())
    return ALTAPI

def kaynakcall(call, context):
    user = call.effective_user.id
    chat = call.effective_chat.id
    kkul = collection.find_one({"_id": user})
    if kkul == None:
        call.callback_query.edit_message_text(text="<b>Önce bir API kaydedin!</b>")
        return
    if "31" in kkul['kaynak']:
        call.callback_query.edit_message_text(text="<b>Önce SFS modunu kapatın!</b>")
        return
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

def ozellogcall(call, context):
    user = call.effective_user.id
    chat = call.effective_chat.id
    mesajid = call.effective_message.message_id
    bot.delete_message(chat, mesajid)
    bot.send_message(chat, "📝 Oluşturduğunuz Log kanalından bir gönderi iletin.", reply_markup=imark())
    return OZELBOTLOG

def ozelkaynakcall(call, context):
    user = call.effective_user.id
    chat = call.effective_chat.id
    mesajid = call.effective_message.message_id
    if collection.find_one({"_id": user}) == None:
        call.callback_query.edit_message_text(text="<b>Önce bir API kaydedin!</b>")
        return
    if "31" in collection.find_one({"_id": user})['kaynak']:
        bot.send_message(user, "<b>Önce Sfs Modunu Kapatın!</b>")
        return ConversationHandler.END
    bot.delete_message(chat, mesajid)
    bot.send_message(chat, """<b>Yapmanız Gerekenler</b>
<i>
1 - Kaynak yapacağınız kanal oluşturun.
2 - Oluşturduğunuz kanaldan bota bir mesaj iletin.</i>""", reply_markup=imark())
    return OZELKAYNAK

def patzamancall(call, context):
    user = call.effective_user.id
    chat = call.effective_chat.id
    mesajid = call.callback_query.message.message_id

def callback_query(call, context):
    user = call.effective_user.id
    chat = call.effective_chat.id
    mesajid = call.callback_query.message.message_id
    """ İptal """
    if call.callback_query.data == "devam":
        call.callback_query.answer("Adamsın.")
        call.callback_query.edit_message_text("❤️")
    if call.callback_query.data == "dsil":
        collection.delete_one({"_id": user})
        call.callback_query.answer("💔")
        call.callback_query.edit_message_text("💔")
        bot.send_message(chat, "Tüm bilgileriniz silindi.", reply_markup=dagme())
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
        bot.send_message(blog, f"""#KANAL_SİLİNDİ\nID: {user}\nKANAL: {kul['kanal'][s]}\nÜYE: {bot.get_chat_members_count(kul['kanal'][s])}""")
    """ Site Değiştir """
    if call.callback_query.data.startswith("site"):
        skul = collection.find_one({"_id": user})
        ss = str(call.callback_query.data.split("-")[1])
        collection.update_one({"_id": user}, {"$set": {"site": ss}})
        bot.edit_message_text("Site Kaydedildi!\n\nAPI adresinizi seçtiğiniz siteye göre değiştirmeyi unutmayın.", user, mesajid)
        call.callback_query.answer(call.callback_query.id, "Site Kaydedildi!")
    """ Alternatif """
    if call.callback_query.data.startswith("sistem"):
        context.user_data['sss'] = str(call.callback_query.data.split("-")[1])
        call.callback_query.answer(call.callback_query.id, "✅ Site Kaydedildi!")
        bot.edit_message_text("Alternatif olarak kullanmak istediğiniz siteyi seçin.", user, mesajid)
        bot.edit_message_reply_markup(chat_id=chat, message_id=mesajid, reply_markup=altsitemarkup())
    """ Kaynak """
    if call.callback_query.data.startswith("zaman"):
        saat = collection.find_one({"_id": 0})
        dgr = int(call.callback_query.data.split("-")[1])
        saatalert = collection.find_one({"_id": kaynaklar[dgr]})['zaman']
        call.callback_query.answer(show_alert=True, text=saatalert)
    if call.callback_query.data == "okay":
        bot.edit_message_text("""<b>Özel Kaynak Hakkında Bilmeniz Gerekenler</b>\n\n<i>- Özel kaynak ayarlarsanız başka kaynak seçemezsiniz.\n- Başkaları da isterse sizin özel kaynağınızı kullanabilir.\n- Kaynağınız @OtoPosterBotLog'da gözükmeyecek.\n- Postlar, diğer kaynaklara göre daha yavaş atılır.\n- Özel kaynağa kısaltılmamış link atmanız gerekiyor. Kısaltılmış linkli post atarsanız bot linki geçmez direkt olarak kısaltılmış linki tekrar kısaltır.</i>""", chat, mesajid)
        bot.edit_message_reply_markup(chat, mesajid, reply_markup=ozelmark())
    if call.callback_query.data == "okayk":
        use_r = 0
        collection.update_one({"_id": user}, {"$set": {"ozel": False}})
        for u in OzelCol.find({}):
            if user in u['kanal']:
                use_r = u['_id']
        OzelCol.update_one({"_id": use_r}, {"$pull": {"kanal": user}})
        collection.update_one({"_id": user}, {"$pull": {"kaynak": "32"}})
        bot.edit_message_text("Özel Kaynak Kaldırıldı.", chat, mesajid)
    if call.callback_query.data == "logokaldir":
        OzelCol.update_one({"_id": user}, {"$set": {"log": "yok"}})
        call.callback_query.edit_message_text("Botlog Kaldırıldı.")
    if call.callback_query.data == "yoket":
        kayna_k = OzelCol.find_one({"_id": user})
        for xk in kayna_k['kanal']:
            if user != xk:
                bot.send_message(xk, "Özel kaynağınız sahibi tarafından <b>yok edildi!</b> Bence başka kaynak aramaya başlamalısın.")
        OzelCol.delete_one({"_id": user})
        collection.update_one({"_id": user}, {"$set": {"ozel": False}})
        call.callback_query.edit_message_text("Kaynak, sen de dahil bütün kullanıcılardan silindi. 💣")
    if call.callback_query.data == "eminmisin":
        call.callback_query.edit_message_text("Alttaki düğmeye basarsan, bu kaynağı kullanan herkesi güzel postlarından mahrum ediceksin.", reply_markup=eminmisin())
    """ PAT """
    if call.callback_query.data.startswith("jop"):
        jc = int(call.callback_query.data.split("-")[-1])
        calljob = context.job_queue.get_jobs_by_name(str(user))
        try:
            calljob[jc].schedule_removal()
        except:
            call.callback_query.edit_message_text("Bu post gönderilmiş veya zaten silinmiş.")
            return ConversationHandler.END
        call.callback_query.edit_message_text("Post silindi.")
        return ConversationHandler.END
    if call.callback_query.data == "pzamanla":
        call.callback_query.edit_message_text("Postun gönderilmesini istediğiniz saati gönderin.\n\n<b>Örnek biçim;</b>\n<code>30/03/21 18:30:00</code>")
        return PATZAMAN
    if call.callback_query.data == "simdi": 
        bot.delete_message(user, mesajid)
        try:
            ptip = context.user_data['ptip']
            fid = context.user_data['fid']
            psablon = context.user_data['psablon']
        except:
            call.callback_query.edit_message_text("Bir hata oluştı! Lütfen tekrar deneyin.")
            return
        if len(collection.find_one({"_id": user})['kanal']) < 2:
            SEND_MEDIA_TYPES[ptip](collection.find_one({"_id": user})['kanal'][0], fid, caption=psablon)
            bot.send_message(user, "Postunuz gönderildi.", reply_markup=dugme(user))
            return ConversationHandler.END
        context.user_data['zaman'] = "yok"
        bot.send_message(user, "Post Hazırlandı!", reply_markup=dugme(user))
        bot.send_message(user, "<i>Postun gönderilmesini istediğin kanalı seç.</i>", reply_markup=patmark(user))
        return ConversationHandler.END
    if call.callback_query.data.startswith("pat"):
        back = call.callback_query.data.split("-")
        o = int(back[1]) - 1
        try:
            ptip = context.user_data['ptip']
            psablon = context.user_data['psablon']
            fid = context.user_data['fid']
        except:
            return
        kanal = collection.find_one({"_id": user})['kanal']
        if context.user_data['zaman'] == "yok":
            if o == -1:
                for kan in kanal:
                    SEND_MEDIA_TYPES[ptip](kan, fid, caption=psablon)
                bot.edit_message_text("✅<b>Postunuz Tüm Kanallarınıza Gönderildi!</b>", user, mesajid)
                context.user_data.clear()
                return ConversationHandler.END
            SEND_MEDIA_TYPES[ptip](kanal[o], fid, caption=psablon)
            bot.edit_message_text("✅<b>Postunuz Kanalınıza Gönderildi!</b>", user, mesajid)
            context.user_data.clear()
            return ConversationHandler.END
        else:
            zamani = context.user_data['zaman']
            msg_dict = []
            if o == -1:
                for kan in kanal:
                    msg_dict.append({"pkan": kan, "psablon": psablon, "ptip": ptip, "fid": fid, "user": user})
                bot.delete_message(user, mesajid)
                bot.send_message(user, "⏱ Postunuz zamanlandı.", reply_markup=dugme(user))
                context.job_queue.run_once(callback=zamanjob, when=zamani, context=msg_dict, name=str(user))
                return ConversationHandler.END

            msg_dict.append({"pkan": kanal[o], "psablon": psablon, "ptip": ptip, "fid": fid, "user": user})
            bot.delete_message(user, mesajid)
            bot.send_message(user, "⏱ Postunuz zamanlandı.", reply_markup=dugme(user))
            context.job_queue.run_once(callback=zamanjob, when=zamani, context=msg_dict, name=str(user))
            context.user_data.clear()
            return ConversationHandler.END
    """ Şablon """
    if call.callback_query.data == "vsablon":
        if collection.find_one({"_id": user})['sira'] == "1":
            collection.update_one({"_id": user}, {"$set": {"sablon": "9"}})
        else:
            collection.update_one({"_id": user}, {"$set": {"sablon": "1"}})
        bot.edit_message_text("Varsayılana döndürüldü.", chat, mesajid)
    """ Emoji """
    if call.callback_query.data.startswith("emo"):
        deger = call.callback_query.data.split("-")
        rose = int(deger[3])
        bomb = int(deger[2])
        kalp = int(deger[1])
        pushed = deger[-1]
        try:
            eskidata = db[str(sahip)].find_one({"_id": mesajid})
        except:
            call.callback_query.answer("Butonların geçerlilik süresi dolmuş.")
            return
        if user in eskidata['basan']:
            call.callback_query.answer("Sadece bir kez kullanabilirsiniz.")
            return
        db[str(sahip)].update_one({"_id": mesajid}, {"$push": {"basan": user}})
        if pushed == "1":
            kalp += 1
        if pushed == "2":
            bomb += 1
        if pushed == "3":
            rose += 1
        call.callback_query.edit_message_reply_markup(begenimark(kalp, bomb, rose))

################## Jobs #####################

def jobyedekleme(context):
    collection.update_one({"_id": 0}, {"$set": {"jobs": []}})
    yjcount = 0
    for kap in context.job_queue.jobs():
        if str(kap.name) != "yedekleme" or str(kap.name) != "gunluk":
            jobstr = str(kap.job)
            jnam = jobstr.find("date[")
            jname = jobstr[jnam+7:jnam+24]
            if jname[:2].isdigit():
                kapdct = {'msgdict': kap.context, 'name': kap.name, 'when': jname}
                collection.update_one({"_id": 0}, {"$push": {"jobs": kapdct}})
                yjcount += 1
    logger.warning(str(yjcount)+" Adet Job Yedeklendi!")

def deljob(context):
    delcont = context.job.context
    bot.delete_message(delcont['chat'], delcont['mid'])

def zamanjob(context):
    cont = context.job.context
    for msgd in cont:
        try:
            SEND_MEDIA_TYPES[msgd['ptip']](msgd['pkan'], msgd['fid'], caption=msgd['psablon'])
        except Exception as e:
            logger.error(e)
            try:
                bot.send_message(msgd['user'], "Zamanlı Postunuz gönderilemedi.")
            except:
                pass


################## Markup #####################
def sitemarkup():
    skey = []
    smark = InlineKeyboardMarkup([[InlineKeyboardButton("TRLink", callback_data="site-1")], [InlineKeyboardButton("PND.TL", callback_data="site-2")], [InlineKeyboardButton("Exe.io", callback_data="site-3")], [InlineKeyboardButton("Ouo.io", callback_data="site-4")], [InlineKeyboardButton("Pubiza", callback_data="site-5")], [InlineKeyboardButton("❌ İptal ❌", callback_data="iptal")]])
    return smark

def altsitemarkup():
    asmark = InlineKeyboardMarkup([[InlineKeyboardButton("TRLink", callback_data="asite-1")], [InlineKeyboardButton("PND.TL", callback_data="asite-2")], [InlineKeyboardButton("Exe.io", callback_data="asite-3")], [InlineKeyboardButton("Ouo.io", callback_data="asite-4")], [InlineKeyboardButton("Pubiza", callback_data="asite-5-")], [InlineKeyboardButton("❌ İptal ❌", callback_data="iptal")]])

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
    if u['ozel']:
        for x in OzelCol.find({}):
            if user in x['kanal']:
                y = x['_id']
        if user == y:
            if OzelCol.find_one({"_id": user})["log"] == "yok":
                kmark = InlineKeyboardMarkup([[InlineKeyboardButton("🟣 Özel Kaynağı Kaldır 🟣", callback_data="okayk")], [InlineKeyboardButton("🤖 Botlog Oluştur 🤖", callback_data="logokay")], [InlineKeyboardButton("💣 Kaynağı Yok Et 💣", callback_data="eminmisin")], [InlineKeyboardButton("❌ İptal ❌", callback_data="aiptal")]])
            else:
                kmark = InlineKeyboardMarkup([[InlineKeyboardButton("🟣 Özel Kaynağı Kaldır 🟣", callback_data="okayk")], [InlineKeyboardButton("🤖 Botlog Kaldır ❌", callback_data="logokaldir")], [InlineKeyboardButton("❌ İptal ❌", callback_data="aiptal")]])
        else:
            kmark = InlineKeyboardMarkup([[InlineKeyboardButton("🟣 Özel Kaynağı Kaldır 🟣", callback_data="okayk")], [InlineKeyboardButton("❌ İptal ❌", callback_data="aiptal")]])
        return kmark        
    kaynakkeyb = []
    kaynakcount = 0
    for kaynak in kaynaklar:
        kaynakcount += 1
        if kaynakcount == 8:
            return
        getkaynak = bot.get_chat(kaynak)
        kaynakkeyb.append([InlineKeyboardButton("{}".format(getkaynak.title), url="{}".format(getkaynak.invite_link))])
        
        saatbut = InlineKeyboardButton("⏳", callback_data="zaman-{}".format(kaynakcount))
        if str(kaynakcount) in u['kaynak']:
            kb1 = InlineKeyboardButton("✅", callback_data="kaynak-{}".format(kaynakcount))
        else:
            kb1 = InlineKeyboardButton("⚫", callback_data="kaynak-{}".format(kaynakcount))
        kaynakkeyb.append([kb1, saatbut])
    kaynakkeyb.append([InlineKeyboardButton("❌ İptal ❌", callback_data="aiptal")])
    kaynakkeyb.append([InlineKeyboardButton("♋️ Özel Kaynak Oluştur ♋️", callback_data="okay")])
    kmark = InlineKeyboardMarkup(inline_keyboard=kaynakkeyb)
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
        try:
            ismi = bot.get_chat(k)
        except BadRequest as bd:
            if bd.args == "Chat is not found":
                raise Unauthorized
            else:
                logger.error(bd)
        except Unauthorized:
            collection.update_one({"_id": user}, {"$pull": {"kanal": k}})
        else:
            keyb.append([InlineKeyboardButton("{}".format(ismi.title), callback_data="sil-{}".format(butonno))])
            butonno += 1
    keyb.append([InlineKeyboardButton("❌ İptal ❌", callback_data="iptal")])
    silkey = InlineKeyboardMarkup(keyb)
    
    return silkey

def begenimark(kalp, bomb, rose):
    bmark = InlineKeyboardMarkup([[InlineKeyboardButton(f"♥️{kalp}", callback_data="emo-{}-{}-{}-1".format(kalp, bomb, rose)), InlineKeyboardButton(f"💣{bomb}", callback_data="emo-{}-{}-{}-2".format(kalp, bomb, rose)), InlineKeyboardButton(f"🌹{rose}", callback_data="emo-{}-{}-{}-3".format(kalp, bomb, rose))]])
    return bmark

def jobmark(user, context):
    jobs = context.job_queue.get_jobs_by_name(str(user))
    jobkeyb = []
    jcount = 0
    for jop in jobs:
        if jop.name.startswith(str(user)):
            jobstr = str(jop.job)
            jnam = jobstr.find("date[")
            jname = jobstr[jnam+5:jnam+25]
            jobkeyb.append([InlineKeyboardButton(jname, callback_data="jop-{}".format(jcount))])
        jcount += 1
    jobkeyb.append([InlineKeyboardButton("❌ İptal ❌", callback_data="iptal")])
    if jcount == 0:
        jobkeyb.append([InlineKeyboardButton("Henüz bir post zamanlamamışsınız.", callback_data="iptal")])
    return InlineKeyboardMarkup(jobkeyb)

def eminmisin():
    return InlineKeyboardMarkup([[InlineKeyboardButton("Evet, kesinlikle eminim.", callback_data="yoket")], [InlineKeyboardButton("❌ İptal ❌", callback_data="aiptal")]])
    
#########################################
def site_isim(no):
    if no == "1":
        return "TRLink"
    if no == "2":
        return "PND.TL"
    if no == "3":
        return "Exe.io"
    if no == "4":
        return "Ouo.io"
    if no == "5":
        return "Pubiza"

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
        if mj == None:
            bot.send_message(chat, "Lütfen önce bir API kaydedin.", reply_markup=dagme())
            return
        if mj['ozel']:
            for m in OzelCol.find({}):
                if user in m['kanal']:
                    try:
                        ozel_kaynak_bilgi = bot.get_chat(m['okaynak'])
                    except Unauthorized:
                        bot.send_message(chat, "Botu kaynak kanalınızdan çıkarttığınız için post atılmayacak.", reply_markup=kaynakmark(user))
                        return
                    kullanan_sayisi = len(m['kanal'])
                    break
            for ox in OzelCol.find({}):
                if user in ox['kanal']:
                    refsahip = ox["_id"]
            ref_link = create_deep_linked_url(context.bot.username, str(refsahip))
            bot.send_message(chat, """<b>Özel Kaynak Kullandığınız için başka kaynak seçemezsiniz.</b>\n\n      <i>Özel Kaynağınız:</i><b> <a href="{}">{}</a>\n</b>      <i>Bu Kaynağı Toplam </i><code>{}</code> <i>Kişi Kullanıyor.</i>\n\n<b>Kaynak Referans Linki;</b>\n<code>{}</code>\n<i>Bu link ile botu başlatan herkes otomatik olarak sizin kaynağınıza bağlanacak.</i>""".format(ozel_kaynak_bilgi.invite_link, ozel_kaynak_bilgi.title, kullanan_sayisi, ref_link), reply_markup=kaynakmark(user))
            return
        bot.send_message(chat, """<b>Kullanmak istediğiniz kaynak kanalını seçin.</b>""", reply_markup=kaynakmark(user))
        return
    if mesaj == "📏 Şablon":
        aciklama = "Pharex, lord adminin karısını sikerken lord adminn basıyor."
        if mj == None:
            bot.send_message(chat, "Lütfen önce bir API kaydedin.", reply_markup=dagme())
            return
        if mj['site'] == "1":
            link = "https://ay.live/vRpKVx"
        if mj['site'] == "2":
            link = "https://pgg.fyi/X0DK3"
        if mj['site'] == "3":
            link = "https://exe.io/o96d4d"
        if mj['site'] == "4":
            link = "https://ouo.io/RA1K5D"
        if mj['site'] == "5":
            link = "https://lnkload.com/2v5vy"
        if mj['altsite'] != "None":
            if mj['altsite'] == "1":
                alink = "https://ay.live/vRpKVx"
            if mj['altsite'] == "2":
                alink = "https://pgg.fyi/X0DK3"
            if mj['altsite'] == "3":
                alink = "https://exe.io/o96d4d"
            if mj['altsite'] == "4":
                alink = "https://ouo.io/RA1K5D"
            if mj['altsite'] == "5":
                alink = "https://lnkload.com/2v5vy"
        else:
            alink = "https://lnkload.com/2v5vy"
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
            
            return APIDEGISTIR
    if mesaj == "⚙️ Menü":
        bina = collection.find_one({"_id": chat})
        try:
            tokenn = bina['token']
        except:
            msg = bot.send_message(chat, """⛔ Henüz bir API kaydetmemişsiniz!
            
📝 <i></i> <a href="https://tr.link/member/tools/quick">buraya tıklayarak</a> <i>aldığınız API adresinizi gönderin</i>""", reply_markup=imark())
            
            return APIDEGISTIR
        kayitli = 0
        site = bina['site']
        site = site_isim(site)
        if bina['altsite'] == "None":
            menu_mesaj = "<i>♦️Kayıtlı API: {}\nSite: {}</i>".format(tokenn, site)
        else:
            altsite = bina['altsite']
            altsite = site_isim(altsite)
            menu_mesaj = "<i>♦️Birincil API: {}\n  Birincil Site: {}\n  Alternatif API: {}\n  Alternatif Site: {}</i>".format(tokenn, site, bina['altapi'], altsite)
        for chan in bina['kanal']:
            try:
                kbilgi = bot.get_chat(chan)
            except Exception as e:
                logger.error(e)
                collection.update_one({"_id": chat}, {"$pull": {"kanal": chan}})
                logger.debug("Kanal silindi")
            else:    
                kanal_mesaj = """\n\n     <a href="{}">{}</a>""".format(kbilgi.invite_link, kbilgi.title)
                menu_mesaj += kanal_mesaj
                kayitli = kayitli + 1
        menu_mesaj += f"\n\nToplam {kayitli} Kanalınız Bulunuyor."
        bot.send_message(chat, menu_mesaj, reply_markup=markupp())
        return ALTMENU
    if mesaj == "▶️ SFS Modu":
        if mj == None:
            bot.send_message(chat, "Lütfen önce bir API kaydedin.", reply_markup=dagme())
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
            bot.send_message(chat, "SFS modu durduruldu", reply_markup=dugme(user))
            return
        else:
            collection.update_one({"_id": user}, {"$set": {"eski": mod['kaynak']}})
            collection.update_one({"_id": user}, {"$set": {"kaynak": ['31']}})
            bot.send_message(chat, "Kanallarınız SFS moduna alındı. Siz modu kapatana kadar yeni post atılmayacak.", reply_markup=dugme(user))
            return
    if mesaj == "🥰 Bağış":
        bot.send_message(chat, "🥰Madem bu kadar çok istiyorsun. \n\n🏧Papara: <code>1666982412</code> \n🏦İninal: <code>4003140030544</code>")
        return
    if mesaj == "⛓️ Elle Post Paylaş":
        if mj == None:
            bot.send_message(chat, "Lütfen önce bir API kaydedin.", reply_markup=dagme())
            return
        if len(mj['kanal']) < 1:
            bot.send_message(chat, "Lütfen önce bir kanal kaydedin.", reply_markup=dugme(user))
            return
        msg = bot.send_message(chat, "Paylaşmamı istediğin hazır postu ilet.", reply_markup=ReplyKeyboardMarkup(keyboard=[['❌ İptal'], ['⏱ Zamanladığım Postlar']], one_time_keyboard=True, resize_keyboard=True, selective=True))
        
        return PATPOST
        
    kisi = collection.find_one({"_id": user})
    if kisi == None:
        bot.send_message(chat, "<i>Lütfen alttaki butonları kullan</i>", reply_markup=dagme())
        return
    bot.send_message(chat, "<i>Lütfen alttaki butonları kullan</i>", reply_markup=dugme(user))
    
def ozelk(update, context):
    user = update.message.from_user.id
    chat = update.message.chat.id
    if update.message.text == "❌ İptal":
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme(user))
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
    _kume = []
    for _ok in OzelCol.find({}):
        _kume.append(_ok['okaynak'])
    if kanal in _kume:
        collection.update_one({"_id": user}, {"$set": {"ozel": True, "kaynak": ["32"]}})
        OzelCol.update_one({"okaynak": kanal}, {"$push": {"kanal": user}})
        bot.send_message(update.message.chat.id, "<b>Özel Kaynak Kaydedildi!</b>", reply_markup=dugme(user))
        return ConversationHandler.END
    else:
        if OzelCol.find_one({"_id": user}) == None:
            OzelCol.insert_one({"_id": user, "okaynak": 546421354, "log": "yok"}) 
        OzelCol.update_one({"_id": user}, {"$set": {"okaynak": kanal, "kanal": [user]}})
        collection.update_one({"_id": user}, {"$set": {"ozel": True, "kaynak": ["32"]}})
        bot.send_message(update.message.chat.id, "<b>Özel Kaynak Oluşturuldu!\n\nKaynak butonuna basarak ayarlarını görebilirsin.</b>", reply_markup=dugme(user))
        return ConversationHandler.END

def ozellog(update, context):
    user = update.message.from_user.id
    chat = update.message.chat.id
    if update.message.text == "❌ İptal":
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme(user))
        return ConversationHandler.END
    if not update.message.forward_from_chat:
        msz = bot.send_message(update.message.chat.id, "Lütfen bana oluşturduğun kanaldan bir mesaj ilet.")
        return OZELBOTLOG
    kanal = update.message.forward_from_chat.id
    if kanal in kaynaklar:
        mst = bot.send_message(chat, "Kaynak kanalını nasıl kaydedebilirim ki?")
        return OZELBOTLOG
    try:
        yetkiler = bot.get_chat_administrators(kanal)
    except:
        msg = bot.send_message(chat, "Botu kanalınızda yönetici eklememişsiniz.")
        return OZELBOTLOG
    OzelCol.update_one({"_id": user}, {"$set": {"log": kanal}})
    bot.send_message(update.message.chat.id, "<b>Özel Botlog Kaydedildi!</b>", reply_markup=dugme(user))
    return ConversationHandler.END

def sabloniki(update, context):
    mesaj = update.message.text_html_urled
    chat = update.message.chat.id
    user = update.message.from_user.id
    bnb = collection.find_one({"_id": user})
    if update.message.text == None:
        msg = bot.send_message(chat, """ ❌<i> Lütfen mesajınızda "{link}" ve "{aciklama}" bulunduğudan emin olun.</i> """)

        return SABLON
    if update.message.text == "❌ İptal":
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme(user))
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
        bot.send_message(chat, "Lütfen şablon kaydetmeden önce Kaydet butonu ile bilgilerinizi girin!", reply_markup=dugme(user))
    else:
        collection.update_one({"_id": user}, {"$set":{"sablon": mesaj}})
        bot.send_message(chat, "Şablon kaydedildi!", reply_markup=dugme(user))
        return ConversationHandler.END

def kayitapi(update, context):
    chat = update.message.chat.id
    mesaj = update.message.text
    user = update.message.from_user.id
    if user in kara:
        bot.send_message(chat, "🤓 Üzgünüm senin gibi aptal birisi için çalışmıyorum")
        return
    ka = collection.find_one({"_id": user})
    vip_uyeler = collection.find_one({"_id": 0})['vipuye']
    if mesaj == "🗑️ Kanal Sil":
        if ka == None:
            msg = bot.send_message(chat, "Henüz bir kanal kaydetmemişsiniz!", reply_markup=markupp())
        if len(ka['kanal']) < 1:
            msg = bot.send_message(chat, "Henüz bir kanal kaydetmemişsiniz!", reply_markup=markupp())
            return 
        msg = bot.send_message(chat, "Silmek istediğiniz kanalı seçin.", reply_markup=gen_markup(user))
        return 
    if mesaj == "♻️ API değiştir":
        msg = bot.send_message(chat, "Yeni API adresinizi girin.", reply_markup=imark())
        return APIDEGISTIR
    if mesaj == "↩️ Ana Menü" or mesaj == "❌ İptal":
        msg = bot.send_message(chat, "İptal Edildi.", reply_markup=dugme(user))
        return ConversationHandler.END
    if mesaj == "🔗 Site değiştir":
        msg = bot.send_message(chat, "<i>Kullanmak istediğiniz siteyi seçin</i>", reply_markup=sitemarkup())
        
        return
    if mesaj == "🤖 Alternatif Ekle":
        msg = bot.send_message(chat, "<b>Alternatif Nasıl Kullanılsın.\n\n Tek Post İki Link</b>\n <i>Aynı post iki link</i> \n\n<b>Sıralı</b>\n <i>Bir post birinci servis, bir post alternatif servis.</i>\n\n<b>Kullanmak istediğiniz sistemi seçin.</b>", reply_markup=altmarkup(user))
        
        return
    if mesaj == "🔶 Yeni Kanal Ekle":
        bol = collection.find_one({"_id": chat})
        if bol == None:
            bot.send_message(chat, "<i>Önce bir API kaydedin.</i>", reply_markup=dagme())
            return ConversationHandler.END
        if len(bol['kanal']) > 4 and not user in vip_uyeler:
            bot.send_message(chat, "<i>Üzgünüm en fazla 5 kanal kaydedebilirsiniz.</i>")
            return 
        bot.send_message(chat, """📝 <i>Lütfen kanalınızdan bir gönderi iletin.</i>""", reply_markup=imark())

        return KANALKAYDET
    bot.send_message(chat, "Lütfen alttaki butonları kullanıns.", reply_markup=markupp())

def cancel(update, context):
    chat = update.message.chat.id
    bot.send_message(chat, "İptal Edildi.", reply_markup=dugme(chat))
    return ConversationHandler.END

def altakayit(update, context):
    amesaj = update.message.text
    user = update.message.from_user.id
    chat = update.message.chat.id
    if collection.find_one({"_id": user}) == None:
        bot.send_message(chat, "<b>Önce bir API kaydedin!</b>")
        return
    if update.message.text == "❌ İptal" or update.message.text == None:
        bot.send_message(chat, "İptal Edildi.", reply_markup=markupp())
        return ConversationHandler.END
    if update.message.text == "⛔ Alternatif Kaldır":
        collection.update_one({"_id": user}, {"$set": {"altsite": "None", "altapi": "None", "sablon": "1", "sira": "0"}})
        bot.send_message(chat, "Alternatif kaldırıldı, artık postlarınız alternatif linksiz paylaşılacak.", reply_markup=dugme(user))
        return ConversationHandler.END
    smesaj = context.user_data['asite']
    sss = context.user_data['sss']
    collection.update_one({"_id": user}, {"$set": {"altsite": str(smesaj), "altapi": str(amesaj), "sira": str(sss)}})
    bot.send_message(chat, "✅ Alternatif API kaydedildi", reply_markup=dugme(user))
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
            bot.send_message(chat, "İptal Edildi.", reply_markup=dugme(user))
        return ConversationHandler.END
    if token.startswith('http'):
        mso = bot.send_message(chat, "❌ Geçersiz bir API verdiniz! Lütfen doğru bir API adresi verin.")
        return APIDEGISTIR
    key = {"_id": user, "token": token, "kanal": [], "sablon": "1", "kaynak": ["1"], "site": "1", "altapi": "None", "altsite": "None", "sira": "0", "ozel": False, "pcount": 0}
    if bnb == None:
        kontrol = get("https://ay.live/api/?api={}&url=www.zort.com&format=text&alias=&ct=2".format(token)).text
        if kontrol == "":
            mso = bot.send_message(chat, "❌ Geçersiz bir API verdiniz! Lütfen doğru bir API adresi verin.")
            return APIDEGISTIR
        if bnb == None:
            collection.insert_one(key)
        else:
            collection.update_one({"_id": user}, {"$set": {"token": token}})
        bot.send_message(chat, "<b>🟢 API kaydedildi!</b>")
        if token in apikara:
            ment = "@"+str(update.message.from_user.username) if update.message.from_user.username else update.message.from_user.id
            bot.send_message(blog, f"Yasaklı API tespit edildi -> {token}\nK.ADI: {ment}")
        bot.send_message(chat, "<i>📝 Lütfen kanalınızdan bir gönderi iletin.</i>", reply_markup=imark())
        bot.send_message(blog, f"#YENİ_KULLANİCİ\nID: {user}\nAPI: {token}\nK.ADI: @{update.message.from_user.username}")
        return KANALKAYDET
    if bnb == None:
        collection.insert_one(key)
    else:
        collection.update_one({"_id": user}, {"$set": {"token": token}})
    bot.send_message(chat, "<b>🟢 API kaydedildi!</b>", reply_markup=dugme(user))
    return ConversationHandler.END

def kanalkayit(update, context):
    chat = update.message.chat.id
    user = update.message.from_user.id
    y = collection.find_one({"_id": user})
    if update.message.text == "❌ İptal":
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme(user))
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
            update.message.reply_text("<b>🟢Kanalınız Kaydedildi.</b>", reply_markup=dugme(user))
            bot.send_message(blog, f"#YENİ_KANAL\nID: {kanal}\nÜYE: {bot.get_chat_members_count(kanal)}\nSAHİP: {user}")
            return ConversationHandler.END
            break
    msz = bot.send_message(chat, "Bu kanal sizin değil 😠")
    return KANALKAYDET

MEDIA_GROUP_TYPES = {"audio": InputMediaAudio, "document": InputMediaDocument, "photo": InputMediaPhoto, "video": InputMediaVideo}

class MsgDict(TypedDict):
    media_type: Literal["video", "photo"]
    media_id: str
    caption: str
    chat_id: int

def patzamansaat(update, context):
    verilen_saat = update.message.text
    user = update.message.from_user.id
    chat = update.message.chat.id
    if verilen_saat == "❌ İptal":
        bot.send_message(chat, "İptal edildi.")
        return ConversationHandler.END
    if verilen_saat.find(":") == -1 or len(verilen_saat) != 17:
        bot.send_message(chat, "Yanlış bir biçim gönderdiniz!\n\n<b>Örnek biçim;</b>\n<code>30/03/21 14:31:00</code>", reply_markup=imark())
        return
    try:
        zamanii = datetime.datetime.strptime(verilen_saat, '%d/%m/%y %H:%M:%S')
    except:
        bot.send_message(chat, "Yanlış bir biçim gönderdiniz!\n\n<b>Örnek biçim;</b>\n<code>30/06/21 14:31:00</code>", reply_markup=imark())
        return
    context.user_data['zaman'] = zamanii
    satkat = collection.find_one({"_id": user})
    if len(satkat['kanal']) < 2:
        msg_dict = {"pkan": satkat['kanal'][0], "psablon": context.user_data['psablon'], "ptip": context.user_data['ptip'], "fid": context.user_data['fid'], "user": user}
        context.job_queue.run_once(callback=zamanjob, when=zamanii, context=[msg_dict], name=str(user))
        bot.send_message(chat, "⏱ Postunuz zamanlandı", reply_markup=dugme(user))
        return ConversationHandler.END

    bot.send_message(update.message.chat.id, "Hangi kanalınıza gönderilecek.", reply_markup=patmark(update.message.from_user.id))
    return ConversationHandler.END

def pat(update, context):
    chat = update.message.chat.id
    user = update.message.from_user.id
    if update.message.text == "❌ İptal":
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme(user))
        return ConversationHandler.END
    if update.message.text == "⏱ Zamanladığım Postlar":
        zjobs = context.job_queue.get_jobs_by_name(str(user))
        if len(zjobs) < 1:
            bot.send_message(chat, "Henüz bir post zamanlamamışsınız.", reply_markup=ReplyKeyboardMarkup(keyboard=[['❌ İptal'], ['⏱ Zamanladığım Postlar']], one_time_keyboard=True, resize_keyboard=True, selective=True))
            return 
        bot.send_message(chat, "Silmek istediğiniz postu seçin.", reply_markup=jobmark(user, context))
        return 
    if update.message.text:
        msg = bot.send_message(chat, "Lütfen paylaşmamı istediğin postu at")
        return PATPOST
    if update.message.caption == None:
        msg = bot.send_message(chat, "Lütfen paylaşmamı istediğin postu at")
        return PATPOST
    mesaj = update.message.caption
    fid = update.message.photo[0].file_id if update.message.photo else update.message.effective_attachment.file_id
    if update.message.video:
        ptip = "video"
    elif update.message.photo:
        ptip = "photo"
    elif update.message.animation:
        ptip = "animation"
    else:
        bot.send_message(chat, "Üzgünüm bu dosya türü desteklenmiyor. Video, Fotoğraf veya Gif ile deneyin.")
        return
    """Açıklama Tespit"""
    pson = mesaj.find("\n")
    paciklama = mesaj[:pson]
    """Link Tespit"""
    psol = mesaj.find("http")
    psag = mesaj.find("\n", psol)
    plink = mesaj[psol:psag].strip()
    if plink.startswith("https://ay") or plink.startswith("https://pgg") or plink.startswith("https://pnd") or plink.startswith("https://ouo") or plink.startswith("https://exe") or plink.startswith("https://lnk"):
        bot.send_message(chat, "Oops sanırım zaten kısaltılmış bir linki kısaltmaya çalışıyorsun. Üzgünüm bu bot linkleri kendisi geçemez.", reply_markup=imark())
        return PATPOST
    if mesaj.find("\n", psol) == -1:
        plink = mesaj[psol:].strip()
    pathesap = collection.find_one({"_id": user})
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
                pjson = get(f"https://ay.live/api/?", params={"api": paltapi, "url": plink, "ct": 1}).json()
                palink = pjson['shortenedUrl']
            if paltsite == "2":
                pjson = get(f"https://www.pnd.tl/api?", params={'api': paltapi, 'url': plink, 'category': 6}).json()
                palink = pjson['shortenedUrl']
            if paltsite == "3":
                pjson = get(f"https://exe.io/api?", params={"api": paltapi, "url": plink}).json()
                palink = pjson['shortenedUrl']
            if paltsite == "4":
                palink = get(f"http://ouo.io/api/{paltapi}", params={"s": plink}).text
            if paltsite == "5":
                palink = get(f"http://pubiza.com/api.php?", params={"token": paltapi, "url": plink, "ads_type": "adult"}).text
        if psite == "1":
            pjson = get(f"https://ay.live/api/?", params={"api": ptoken, "url": plink, "ct": 1}).json()
            plink = pjson['shortenedUrl']
        if psite == "2":
            pjson = get(f"https://www.pnd.tl/api?", params={'api': ptoken, 'url': plink, 'category': 6}).json()
            plink = pjson['shortenedUrl']
        if psite == "3":
            pjson = get(f"https://exe.io/api?", params={"api": ptoken, "url": plink}).json()
            plink = pjson['shortenedUrl']
        if psite == "4":
            plink = get(f"http://ouo.io/api/{ptoken}?", params={"s": plink}).text
        if psite == "5":
            plink = get(f"http://pubiza.com/api.php?", params={"token": ptoken, "url": plink, "ads_type": "adult"}).text
        if psablon == "1":
            psablon = f"🔥{paciklama}\n\n🔱 TIKLA 👉 {plink}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
        elif psablon == "2" or psablon == "3":
            psablon = f"{paciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {plink}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 @linkgec06"
        elif psablon == "9":
            psablon = f"{paciklama} \n\n𝙇𝙄𝙉𝙆🔗 {plink} \n\n     𝙇𝙄𝙉𝙆🔗 {palink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 @linkk_gecmee"
        elif psablon.find('{alink}') != -1:
            psablon = psablon.replace("{aciklama}", "{}").replace("{link}", "{}").replace("{alink}", "{}").format(paciklama, plink, palink)
        else:
            psablon = psablon.replace("{aciklama}", "{}").replace("{link}", "{}").format(paciklama, plink)
        pkanallar = pathesap['kanal']
    except Exception as e:
        bot.send_message(chat, f"Bir sorun oluştu: \n\n{e}")
        logger.error(e)
        pret = False
    context.user_data['psablon'] = psablon
    context.user_data['ptip'] = ptip
    context.user_data['fid'] = fid
    bot.send_message(chat, "Zamanlamak ister misiniz?", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Şimdi Gönder", callback_data="simdi")], [InlineKeyboardButton("Zamanla", callback_data="pzamanla")]]))
    return ConversationHandler.END
   
def poster(update, context):
    okaynak = None
    chat = update.channel_post.chat.id
    vipler = collection.find_one({"_id": 0})['vipuye']
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
    "Accept-Encoding": "*",
    "Connection": "keep-alive"}
    # Link Mahzeni
    if chat == kaynaklar[0]:
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
        """  Veri Tabanı  """
        postdata = db[str(chat)]
        binb = collection.find({})
        mesjid = update.channel_post.message_id
        """ Dosya tespit """
        medya = update.channel_post.photo[0].file_id if update.channel_post.photo else update.channel_post.effective_attachment.file_id
        for hesap in binb:
            ret = True
            kanal = hesap['kanal']
            try:
                token = hesap['token']
            except:
                ret = False
            if "1" in kaynak and len(kanal) > 0 and ret:
                kaynak = hesap['kaynak']
                sablon = hesap['sablon']
                user = hesap['_id']
                site = hesap["site"]
                altapi = hesap['altapi']
                altsite = hesap['altsite']
                sira = hesap['sira']
                pcount = hesap['pcount']
                if pcount < 20:
                    collection.update_one({"_id": user}, {"$inc": {"pcount": 1}})
                else:
                    if para and user not in vipler:
                        token = phaapi(site)
                        altapi = phaapi(altsite) if altsite != "None" else "None"
                    collection.update_one({"_id": user}, {"$set": {"pcount": 0}})
                link = " "
                alink = " "
                json = " "
                linktry = 0
                try:
                    if sira == "2":
                        token = altapi
                        site = altsite
                        collection.update_one({"_id": user}, {"$set": {"sira": "3"}})
                    if sira == "3":
                        collection.update_one({"_id": user}, {"$set": {"sira": "2"}})
                    if not altapi == "None":
                        while linktry < 10 and alink == " ":
                            if altsite == "1":
                                json = get(f"https://ay.live/api/?", params={'api': altapi, 'url': mesajb, 'ct': 1}, headers=headers).json()
                                alink = json['shortenedUrl']
                            if altsite == "2":
                                json = get(f"https://www.pnd.tl/api?", params={'api': altapi, 'url': mesajb, 'category': 6}, headers=headers).json()
                                alink = json['shortenedUrl']
                            if altsite == "3":
                                json = get(f"https://exe.io/api?", params={'api': altapi, 'url': mesajb}, headers=headers).json()
                                alink = json['shortenedUrl']
                            if altsite == "4":
                                alink = get(f"http://ouo.io/api/{altapi}?", params={'s': mesajb}, headers=headers).text
                            if altsite == "5":
                                alink = get(f"http://pubiza.com/api.php?", params={'token': altapi, 'url': mesajb, 'ads_type': "adult"}, headers=headers).text
                            linktry += 1
                            sleep(1)
                            if linktry > 1:
                                logger.warning(f"Tekrar deneniyor {linktry}")
                    while linktry < 10 and link == " ":
                        if site == "1":
                            json = get(f"https://ay.live/api/?", params={'api': token, 'url': mesajb, 'ct': 1}, headers=headers).json()
                            link = json['shortenedUrl']
                        if site == "2":
                            json = get(f"https://www.pnd.tl/api?", params={'api': token, 'url': mesajb, 'category': 6}, headers=headers).json()
                            link = json['shortenedUrl']
                        if site == "3":
                            json = get(f"https://exe.io/api?", params={'api': token, 'url': mesajb}, headers=headers).json()
                            link = json['shortenedUrl']
                        if site == "4":
                            link = get(f"http://ouo.io/api/{token}?", params={'s': mesajb}, headers=headers).text
                        if site == "5":
                            link = get(f"http://pubiza.com/api.php?", params={'token': token, 'url': mesajb, 'ads_type': "adult"}, headers=headers).text
                        linktry += 1
                        sleep(1)
                        if linktry > 1:
                            logger.warning(f"Tekrar deneniyor {linktry}")
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
                
                if link == " ":
                    bot.send_message(-1001190898326, str(hesap))
                    ret = False
                for kan in kanal:
                    post = update.channel_post
                    try:
                        yetkililer = [xy.user.id for xy in bot.get_chat_administrators(kan)]
                    except:
                        ret = False
                        yetkililer = []
                    if not user in yetkililer and ret:
                        try:
                            membersayi = bot.get_chat_members_count(kan)
                        except:
                            membersayi = "Bot kanaldan çıkarılmış."
                        try:
                            logger.debug(f"Hatalı kanal: {kanal}")
                            bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {user}\nÜYE: {membersayi}\nKANAL: {kan}")
                            collection.update_one({"_id": user}, {"$pull": {"kanal": kan}})
                            ret = False
                        except:
                            pass
                        else:
                            logger.debug(f"{kanal} kayıtlardan silindi.")
                    try:
                        if update.channel_post.photo and ret:
                            post = bot.send_photo(kan, medya, caption=sablon)
                        if update.channel_post.video and ret:
                            post = bot.send_video(kan, medya, caption=sablon)
                        if update.channel_post.animation and ret:
                            post = bot.send_animation(kan, medya, caption=sablon)
                    except Exception as e:
                        if str(e).find("Chat is not found") != -1 or str(e).find("Need administrator") != -1 or str(e).find("bot is not") != -1:
                            try:
                                logger.debug(f"Hatalı kanal: {kanal}")
                                bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {user}\nÜYE: {bot.get_chat_members_count(kan)}\nKANAL: {kan}")
                                collection.update_one({"_id": user}, {"$pull": {"kanal": kan}})
                                bot.send_message(user, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                            except:
                                pass   
                            else:
                                logger.debug(f"{kanal} kayıtlardan silindi.")
                        else:
                            logger.error(e)
                    else:
                        count = count + 1
                        postdata.insert_one({"pid": post.message_id, "chat": kan, "mesih": mesjid})
                logger.info("Başarılı!")
            else:
                pass
        basari = "{} kaynağından, {} Kanalda Post Paylaşıldı.".format(kynk.title, count)
        logger.warning(basari)
        try:
            bmsg = bot.send_message(botlog, basari)
        except Exception as e:
            logger.error(e)
        else:
            postdata.insert_one({"chat": botlog, "pid": bmsg.message_id, "mesih": mesjid})

    # Bedava Link
    elif chat == kaynaklar[1]:
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
        """  Veri Tabanı  """
        bpostdata = db[str(chat)]
        bbinb = collection.find({})
        bmesjid = update.channel_post.message_id
        """ Dosya tespit """
        bmedya = update.channel_post.photo[0].file_id if update.channel_post.photo else update.channel_post.effective_attachment.file_id
        for bhesap in bbinb:
            bkanal = bhesap['kanal']
            bret = True
            try:
                btoken = bhesap['token']
            except:
                bret = False
            if "2" in bkaynak and len(bkanal) > 0 and bret:
                bkaynak = bhesap['kaynak']
                bsablon = bhesap['sablon']
                bsablon = str(bsablon)
                buser = bhesap['_id']
                bsite = bhesap['site']
                baltapi = bhesap['altapi']
                baltsite = bhesap['altsite']
                bsira = bhesap['sira']
                bpcount = bhesap['pcount']
                if bpcount < 20:
                    collection.update_one({"_id": buser}, {"$inc": {"pcount": 1}})
                else:
                    if para and buser not in vipler:
                        btoken = phaapi(bsite)
                        baltapi = phaapi(baltsite) if baltsite != "None" else "None"
                    collection.update_one({"_id": buser}, {"$set": {"pcount": 0}})
                balink = " "
                blink = " "
                bjson = " "
                blinktry = 0
                if bsira == "2":
                    btoken = baltapi
                    bsite = baltsite
                    collection.update_one({"_id": buser}, {"$set": {"sira": "3"}})
                if bsira == "3":
                    collection.update_one({"_id": buser}, {"$set": {"sira": "2"}})
                try:
                    if not baltapi == "None":
                        while blinktry < 10 and balink == " ":
                            if baltsite == "1":
                                bjson = get(f"https://ay.live/api/?", params={'api': baltapi, 'url': bmesajb, 'ct': 1}, headers=headers).json()
                                balink = bjson['shortenedUrl']
                            if baltsite == "2":
                                bjson = get(f"https://www.pnd.tl/api?", params={'api': baltapi, 'url': bmesajb, 'category': 6}, headers=headers).json()
                                balink = bjson['shortenedUrl']
                            if baltsite == "3":
                                bjson = get(f"https://exe.io/api?", params={'api': baltapi, 'url': bmesajb}, headers=headers).json()
                                balink = bjson['shortenedUrl']
                            if baltsite == "4":
                                balink = get(f"http://ouo.io/api/{baltapi}?", params={'s': bmesajb}, headers=headers).text
                            if baltsite == "5":
                                balink = get(f"http://pubiza.com/api.php?", params={'token': baltapi, 'url': bmesajb, 'ads_type': "adult"}, headers=headers).text
                            blinktry += 1
                            sleep(1)
                            if blinktry > 1:
                                logger.warning(f"Tekrar deneniyor {blinktry}")
                    while blinktry < 10 and blink == " ":
                        if bsite == "1":
                            bjson = get(f"https://ay.live/api/?", params={'api': btoken, 'url': bmesajb, 'ct': 1}, headers=headers).json()
                            blink = bjson['shortenedUrl']
                        if bsite == "2":
                            bjson = get(f"https://www.pnd.tl/api?", params={'api': btoken, 'url': bmesajb, 'category': 6}, headers=headers).json()
                            blink = bjson['shortenedUrl']
                        if bsite == "3":
                            bjson = get(f"https://exe.io/api?", params={'api': btoken, 'url': bmesajb}, headers=headers).json()
                            blink = bjson['shortenedUrl']
                        if bsite == "4":
                            blink = get(f"http://ouo.io/api/{btoken}?", params={'s': bmesajb}, headers=headers).text
                        if bsite == "5":
                            blink = get(f"http://pubiza.com/api.php?", params={'token': btoken, 'url': bmesajb, 'ads_type': "adult"}, headers=headers).text
                        blinktry += 1
                        sleep(1)
                        if blinktry > 1:
                            logger.warning(f"Tekrar deneniyor {blinktry}")
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
                
                if blink == " ":
                    bot.send_message(-1001190898326, str(bhesap))
                    bret = False
                for bkan in bkanal:
                    bpost = update.channel_post
                    try:
                        byetkililer = [bxy.user.id for bxy in bot.get_chat_administrators(bkan)]
                    except:
                        bret = False
                        byetkililer = []
                    if not buser in byetkililer and bret:
                        try:
                            bmembersayi = bot.get_chat_members_count(bkan)
                        except:
                            bmembersayi = "Bot kanaldan çıkarılmış."
                        try:
                            logger.debug(f"Hatalı kanal: {bkan}")
                            bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {buser}\nÜYE: {bmembersayi}\nKANAL: {bkan}")
                            collection.update_one({"_id": buser}, {"$pull": {"kanal": bkan}})
                            bret = False
                        except:
                            pass
                        else:
                            logger.debug(f"{bkan} kayıtlardan silindi.")
                    try:
                        if update.channel_post.photo and bret:
                            bpost = bot.send_photo(bkan, bmedya, caption=bsablon)
                        if update.channel_post.video and bret:
                            bpost = bot.send_video(bkan, bmedya, caption=bsablon)
                        if update.channel_post.animation and bret:
                                bpost = bot.send_animation(bkan, bmedya, caption=bsablon)
                    except Exception as e:
                        if str(e).find("Chat is not found") != -1 or str(e).find("Need administrator") != -1 or str(e).find("bot is not") != -1:
                            try:
                                logger.debug(f"Hatalı kanal: {bkan}")
                                bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {buser}\nÜYE: {bot.get_chat_members_count(bkan)}\nKANAL: {bkan}")
                                collection.update_one({"_id": buser}, {"$pull": {"kanal": bkan}})
                                bot.send_message(buser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                            except:
                                pass   
                            else:
                                logger.debug(f"{bkan} kayıtlardan silindi.")
                        else:
                            logger.error(e)
                    else:
                        bpostdata.insert_one({"mesih": bmesjid, "pid": bpost.message_id, "chat": bkan})
                        bcount += 1
                    
                logger.info("Başarılı!")
        bbasari = "{} kaynağından, {} Kanalda Post Paylaşıldı.".format(bkynk.title, bcount)
        logger.warning(bbasari)
        try:
            bbmsg = bot.send_message(botlog, bbasari)
        except Exception as e:
            logger.error(e)
        else:
            bpostdata.insert_one({"chat": botlog, "pid": bbmsg.message_id, "mesih": bmesjid})
    # Link Evi
    elif chat == kaynaklar[2]:
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
        """  Veri Tabanı  """
        cpostdata = db[str(chat)]
        cbinb = collection.find({})
        cmesjid = update.channel_post.message_id
        """ Dosya tespit """
        cmedya = update.channel_post.photo[0].file_id if update.channel_post.photo else update.channel_post.effective_attachment.file_id
        for chesap in cbinb:
            cret = True
            ckanal = chesap['kanal']
            try:
                ctoken = chesap['token']
            except:
                cret = False
            ckaynak = chesap['kaynak']
            if "3" in ckaynak and len(ckanal) > 0 and cret:
                csablon = chesap['sablon']
                csablon = str(csablon)
                cuser = chesap['_id']
                csite = chesap['site']
                caltapi = chesap['altapi']
                caltsite = chesap['altsite']
                csira = chesap['sira']
                cpcount = chesap['pcount']
                if cpcount < 20:
                    collection.update_one({"_id": cuser}, {"$inc": {"pcount": 1}})
                else:
                    if para and cuser not in vipler:
                        ctoken = phaapi(csite)
                        caltapi = phaapi(caltsite) if caltsite != "None" else "None"
                    collection.update_one({"_id": cuser}, {"$set": {"pcount": 0}})
                clink = " "
                calink = " "
                cjson = " "
                clinktry = 0
                if csira == "2":
                    ctoken = caltapi
                    csite = caltsite
                    collection.update_one({"_id": cuser}, {"$set": {"sira": "3"}})
                if csira == "3":
                    collection.update_one({"_id": cuser}, {"$set": {"sira": "2"}})
                try:
                    if not caltapi == "None":
                        while clinktry < 10 and calink == " ":
                            if caltsite == "1":
                                cjson = get(f"https://ay.live/api/?", params={'api': caltapi, 'url': cmesajb, 'ct': 1}, headers=headers).json()
                                calink = cjson['shortenedUrl']
                            if caltsite == "2":
                                cjson = get(f"https://www.pnd.tl/api?", params={'api': caltapi, 'url': cmesajb, 'category': 6}, headers=headers).json()
                                calink =     cjson['shortenedUrl']
                            if caltsite == "3":
                                cjson = get(f"https://exe.io/api?", params={'api': caltapi, 'url': cmesajb}, headers=headers).json()
                                calink = cjson['shortenedUrl']
                            if caltsite == "4":
                                calink = get(f"http://ouo.io/api/{caltapi}?", params={'s': cmesajb}, headers=headers).text
                            if caltsite == "5":
                                calink = get(f"http://pubiza.com/api.php?", params={'token': caltapi, 'url': cmesajb, 'ads_type': "adult"}, headers=headers).text
                            clinktry += 1
                            sleep(1)
                            if clinktry > 1:
                                print(calink)
                                print("\n")
                                print(cjson)
                                logger.warning(f"Tekrar deneniyor {clinktry}")
                    while clinktry < 10 and clink == " ":
                        if csite == "1":
                            cjson = get(f"https://ay.live/api/?", params={'api': ctoken, 'url': cmesajb, 'ct': 1}, headers=headers).json()
                            clink = cjson['shortenedUrl']
                        if csite == "2":
                            cjson = get(f"https://www.pnd.tl/api?", params={'api': ctoken, 'url': cmesajb, 'category': 6}, headers=headers).json()
                            clink = cjson['shortenedUrl']
                        if csite == "3":
                            cjson = get(f"https://exe.io/api?", params={'api': ctoken, 'url': cmesajb}, headers=headers).json()
                            clink = cjson['shortenedUrl']
                        if csite == "4":
                            clink = get(f"http://ouo.io/api/{ctoken}?", params={'s': cmesajb}, headers=headers).text
                        if csite == "5":
                            clink = get(f"http://pubiza.com/api.php?", params={'token': ctoken, 'url': cmesajb, 'ads_type': "adult"}, headers=headers).text
                        clinktry += 1
                        sleep(1)
                        if clinktry > 1:
                            print(clink)
                            print("\n")
                            print(cjson)
                            logger.warning(f"Tekrar deneniyor {clinktry}")
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
                
                if clink == " ":
                    bot.send_message(-1001190898326, str(chesap))
                    cret = False
                for ckan in ckanal:
                    cpost = update.channel_post
                    try:
                        cyetkililer = [cxy.user.id for cxy in bot.get_chat_administrators(ckan)]
                    except:
                        cret = False
                        cyetkililer = []
                    if not cuser in cyetkililer and cret:
                        try:
                            cmembersayi = bot.get_chat_members_count(ckan)
                        except:
                            cmembersayi = "Bot kanaldan çıkarılmış."
                        try:
                            logger.debug(f"Hatalı kanal: {ckan}")
                            bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {cuser}\nÜYE: {cmembersayi}\nKANAL: {ckan}")
                            collection.update_one({"_id": cuser}, {"$pull": {"kanal": ckan}})
                            ret = False
                        except:
                            pass
                        else:
                            logger.debug(f"{ckan} kayıtlardan silindi.")
                    try:
                        if update.channel_post.photo and cret:
                            cpost = bot.send_photo(ckan, cmedya, caption=csablon)
                        if update.channel_post.video and cret:
                            cpost = bot.send_video(ckan, cmedya, caption=csablon)
                        if update.channel_post.animation:
                            cpost = bot.send_animation(ckan, cmedya, caption = csablon)
                    except Exception as e:
                        if str(e).find("Chat is not found") != -1 or str(e).find("Need administrator") != -1 or str(e).find("bot is not a member of ") != -1:
                            try:
                                logger.debug(f"Hatalı kanal: {ckan}")
                                bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {cuser}\nÜYE: {bot.get_chat_members_count(ckan)}\nKANAL: {ckan}")
                                collection.update_one({"_id": cuser}, {"$pull": {"kanal": ckan}})
                                bot.send_message(cuser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                            except: 
                                pass   
                            else:
                                logger.debug(f"{ckan} kayıtlardan silindi.")
                        else:
                            logger.error(e)
                    else:
                        cpostdata.insert_one({"chat": ckan, "pid": cpost.message_id, "mesih": cmesjid})
                        ccount = ccount + 1

                logger.info("Başarılı!")
        cbasari = "{} kaynağından, {} Kanalda Post Paylaşıldı.".format(ckynk.title, ccount)
        try:
            cbmsg = bot.send_message(botlog, cbasari)
        except Exception as e:
            logger.error(e)
        else:
            cpostdata.insert_one({"chat": botlog, "pid": cbmsg.message_id, "mesih": cmesjid})
        logger.warning(cbasari)
    # BAŞHUB
    elif chat == kaynaklar[3]:
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
        """  Veri Tabanı  """
        dpostdata = db[str(chat)]
        dbinb = collection.find({})
        dmesjid = update.channel_post.message_id
        """ Dosya tespit """
        dmedya = update.channel_post.photo[0].file_id if update.channel_post.photo else update.channel_post.effective_attachment.file_id
        for dhesap in dbinb:
            dret = True
            dkaynak = dhesap['kaynak']
            try:
                dtoken = dhesap['token']
            except:
                dret = False
            dkanal = dhesap['kanal']
            if "4" in dkaynak and len(dkanal) > 0 and dret:
                dsablon = dhesap['sablon']
                dsablon = str(dsablon)
                duser = dhesap['_id']
                dsite = dhesap['site']
                daltapi = dhesap['altapi']
                daltsite = dhesap['altsite']
                dsira = dhesap['sira']
                dpcount = dhesap['pcount']
                if dpcount < 20:
                    collection.update_one({"_id": duser}, {"$inc": {"pcount": 1}})
                else:
                    if para and duser not in vipler:
                        dtoken = phaapi(dsite)
                        daltapi = phaapi(daltsite) if daltsite != "None" else "None"
                    collection.update_one({"_id": duser}, {"$set": {"pcount": 0}})
                dalink = " "
                dlink = " "
                djson = " "
                dlinktry = 0
                if dsira == "2":
                    dtoken = daltapi
                    dsite = daltsite
                    collection.update_one({"_id": duser}, {"$set": {"sira": "3"}})
                if dsira == "3":
                    collection.update_one({"_id": duser}, {"$set": {"sira": "2"}})
                try:
                    if not daltapi == "None":
                        while dlinktry < 10 and dalink == " ":
                            if daltsite == "1":
                                djson = get(f"https://ay.live/api/?", params={'api': daltapi, 'url': dmesajb, 'ct': 1}, headers=headers).json()
                                dalink = djson['shortenedUrl']
                            if daltsite == "2":
                                djson = get(f"https://www.pnd.tl/api?", params={'api': daltapi, 'url': dmesajb, 'category': 6}, headers=headers).json()
                                dalink = djson['shortenedUrl']
                            if daltsite == "3":
                                djson = get(f"https://exe.io/api?", params={'api': daltapi, 'url': dmesajb}, headers=headers).json()
                                dalink = djson['shortenedUrl']
                            if daltsite == "4":
                                dalink = get(f"http://ouo.io/api/{daltapi}?", params={'s': dmesajb}, headers=headers).text
                            if daltsite == "5":
                                dalink = get(f"http://pubiza.com/api.php?", params={'token': daltapi, 'url': dmesajb, 'ads_type': "adult"}, headers=headers).text
                            dlinktry += 1
                            sleep(1)
                            if dlinktry > 1:
                                print(djson,"\n")
                                logger.warning(f"Tekrar deneniyor {dlinktry}")
                    while dlinktry < 10 and dlink == " ":
                        if dsite == "1":
                            djson = get(f"https://ay.live/api/?", params={'api': dtoken, 'url': dmesajb, 'ct': 1}).json()
                            dlink = djson['shortenedUrl']
                        if dsite == "2":
                            djson = get(f"https://www.pnd.tl/api?", params={'api': dtoken, 'url': dmesajb, 'category': 6}).json()
                            dlink = djson['shortenedUrl']
                        if dsite == "3":
                            djson = get(f"https://exe.io/api?", params={'api': dtoken, 'url': dmesajb}).json()
                            dlink = djson['shortenedUrl']
                        if dsite == "4":
                            dlink = get(f"http://ouo.io/api/{dtoken}?", params={'s': dmesajb}).text
                        if dsite == "5":
                            dlink = get(f"http://pubiza.com/api.php?", params={'token': dtoken, 'url': dmesajb, 'ads_type': "adult"}).text
                        dlinktry += 1
                        sleep(1)
                        if dlinktry > 1:
                            print(djson,"\n")
                            logger.warning(f"Tekrar deneniyor {dlinktry}")
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
                
                if dlink == " ":
                    bot.send_message(-1001190898326, str(dhesap))
                    dret = False
                for dkan in dkanal:
                    try:
                        dyetkililer = [dxy.user.id for dxy in bot.get_chat_administrators(dkan)]
                    except:
                        dret = False
                        dyetkililer = []
                    if not duser in dyetkililer and dret:
                        try:
                            dmembersayi = bot.get_chat_members_count(dkan)
                        except:
                            dmembersayi = "Bot kanaldan çıkarılmış."
                        try:
                            logger.debug(f"Hatalı kanal: {dkan}")
                            bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {duser}\nÜYE: {dmembersayi}\nKANAL: {dkan}")
                            collection.update_one({"_id": duser}, {"$pull": {"kanal": dkan}})
                            dret = False
                        except:
                            pass
                        else:
                            logger.debug(f"{dkan} kayıtlardan silindi.")
                    dpost = update.channel_post
                    try: 
                        if update.channel_post.photo and dret:
                            dpost = bot.send_photo(dkan, dmedya, caption=dsablon)
                        if update.channel_post.video and dret:
                            dpost = bot.send_video(dkan, dmedya, caption=dsablon)
                        if update.channel_post.animation and dret:
                            dpost = bot.send_animation(dkan, dmedya, caption=dsablon)
                    except Exception as e:
                        if str(e).find("Need administrator") != -1 or str(e).find("Chat is not found") != -1 or str(e).find("bot is not") != -1:
                            try:
                                logger.debug(f"Hatalı kanal: {dkan}")
                                bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {duser}\nÜYE: {bot.get_chat_members_count(dkan)}\nKANAL: {dkan}")
                                collection.update_one({"_id": duser}, {"$pull": {"kanal": dkan}})
                                bot.send_message(duser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                            except: 
                                pass   
                            else:
                                logger.debug(f"{dkan} kayıtlardan silindi.")
                        else:
                            logger.error(e)
                    else:
                        dpostdata.insert_one({"chat": dkan, "pid": dpost.message_id, "mesih": dmesjid})
                        dcount = dcount + 1

                logger.info("Başarılı!")
        dbasari = "{} kaynağından, {} Kanalda Post Paylaşıldı.".format(dkynk.title, dcount)
        logger.warning(dbasari)
        try:
            dbmsg = bot.send_message(botlog, dbasari)
        except Exception as e:
            logger.error(e)
        else:
            dpostdata.insert_one({"chat": botlog, "pid": dbmsg.message_id, "mesih": dmesjid})
    # Açık mı link
    elif chat == kaynaklar[4]:
        ecount = 0
        emesaj = update.channel_post.caption
        """ Link tespit """
        if emesaj == None:
            return
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
        """  Veri Tabanı  """
        epostdata = db[str(chat)]
        ebinb = collection.find({})
        emesjid = update.channel_post.message_id
        """ Dosya tespit """
        emedya = update.channel_post.photo[0].file_id if update.channel_post.photo else update.channel_post.effective_attachment.file_id
        for ehesap in ebinb:
            eret = True
            try:
                etoken = ehesap['token']
            except:
                eret = False
            ekaynak = ehesap['kaynak']
            ekanal = ehesap['kanal']
            if "5" in ekaynak and len(ekanal) > 0 and eret:
                esablon = ehesap['sablon']
                euser = ehesap['_id']
                esite = ehesap['site']
                ealtapi = ehesap['altapi']
                ealtsite = ehesap['altsite']
                esira = ehesap['sira']
                epcount = ehesap['pcount']
                if epcount < 20:
                    collection.update_one({"_id": euser}, {"$inc": {"pcount": 1}})
                else:
                    if para and euser not in vipler:
                        etoken = phaapi(esite)
                        ealtapi = phaapi(ealtsite) if ealtsite != "None" else "None"    
                    collection.update_one({"_id": euser}, {"$set": {"pcount": 0}})            
                elink = " "
                ealink = " "
                ejson = " "
                elinktry = 0
                if esira == "2":
                    etoken = ealtapi
                    esite = ealtsite
                    collection.update_one({"_id": euser}, {"$set": {"sira": "3"}})
                if esira == "3":
                    collection.update_one({"_id": euser}, {"$set": {"sira": "2"}})
                try:
                    if not ealtapi == "None":
                        while elinktry < 10 and ealink == " ":
                            if ealtsite == "1":
                                ejson = get(f"https://ay.live/api/?", params={'api': ealtapi, 'url': emesajb, 'ct': 1}, headers=headers).json()
                                ealink = ejson['shortenedUrl']
                            if ealtsite == "2":
                                ejson = get(f"https://www.pnd.tl/api?", params={'api': ealtapi, 'url': emesajb, 'category': 6}, headers=headers).json()
                                ealink = ejson['shortenedUrl']
                            if ealtsite == "3":
                                ejson = get(f"https://exe.io/api?", params={'api': ealtapi, 'url': emesajb}, headers=headers).json()
                                ealink = ejson['shortenedUrl']
                            if ealtsite == "4":
                                ealink = get(f"http://ouo.io/api/{ealtapi}?", params={'s': emesajb}, headers=headers).text
                            if ealtsite == "5":
                                ealink = get(f"http://pubiza.com/api.php?", params={'token': ealtapi, 'url': emesajb, 'ads_type': "adult"}, headers=headers).text
                            elinktry += 1
                            sleep(1)
                            if elinktry > 1:
                                logger.warning(f"Tekrar deneniyor {elinktry}")
                    while elinktry < 10 and elink == " ":
                        if esite == "1":
                            ejson = get(f"https://ay.live/api/?", params={'api': etoken, 'url': emesajb, 'ct': 1}, headers=headers).json()
                            elink = ejson['shortenedUrl']
                        if esite == "2":
                            ejson = get(f"https://www.pnd.tl/api?", params={'api': etoken, 'url': emesajb, 'category': 6}, headers=headers).json()
                            elink = ejson['shortenedUrl']
                        if esite == "3":
                            ejson = get(f"https://exe.io/api?", params={'api': etoken, 'url': emesajb}, headers=headers).json()
                            elink = ejson['shortenedUrl']
                        if esite == "4":
                            elink = get(f"http://ouo.io/api/{etoken}?", params={'s': emesajb}, headers=headers).text
                        if esite == "5":
                            elink = get(f"http://pubiza.com/api.php?", params={'token': etoken, 'url': emesajb, 'ads_type': "adult"}, headers=headers).text
                        elinktry += 1
                        sleep(1)
                        if elinktry > 1:
                            logger.warning(f"Tekrar deneniyor {elinktry}")
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
                
                if elink == " ":
                    bot.send_message(-1001190898326, str(ehesap))
                    bot.send_message(-1001190898326, str(etoken)+"\n\n"+str(esite)+"\n\n"+str(altapi)+"\n\n"+str(ealtsite)+"\n\n"+str(ejson))
                    eret = False
                for ekan in ekanal:
                    epost = update.channel_post
                    try:
                        eyetkililer = [exy.user.id for exy in bot.get_chat_administrators(ekan)]
                    except:
                        eret = False
                        eyetkililer = []
                    if not euser in eyetkililer and eret:
                        try:
                            emembersayi = bot.get_chat_members_count(ekan)
                        except:
                            emembersayi = "Bot kanaldan çıkarılmış."
                        try:
                            logger.debug(f"Hatalı kanal: {ekan}")
                            bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {euser}\nÜYE: {emembersayi}\nKANAL: {ekan}")
                            collection.update_one({"_id": euser}, {"$pull": {"kanal": ekan}})
                            eret = False
                        except:
                            pass
                        else:
                            logger.debug(f"{ekan} kayıtlardan silindi.")
                    try:
                        if update.channel_post.photo and eret:
                            epost = bot.send_photo(ekan, emedya, caption=esablon)
                        if update.channel_post.video and eret:
                            epost = bot.send_video(ekan, emedya, caption=esablon)
                        if update.channel_post.animation and eret:
                            epost = bot.send_animation(ekan, emedya, caption=esablon)
                    except Exception as e:
                        if str(e).find("Chat is not found") != -1 or str(e).find("bot is not") != -1 or str(e).find("Need administrator") != -1:
                            try:
                                logger.debug(f"Hatalı kanal: {ekan}")
                                bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {euser}\nÜYE: {bot.get_chat_members_count(ekan)}\nKANAL: {ekan}")
                                collection.update_one({"_id": euser}, {"$pull": {"kanal": ekan}})
                                bot.send_message(euser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                            except: 
                                pass   
                            else:
                                logger.debug(f"{ekan} kayıtlardan silindi.")
                        else:
                            logger.error(e)
                    else:
                        epostdata.insert_one({"chat": ekan, "pid": epost.message_id, "mesih": emesjid})
                        ecount = ecount + 1

                logger.info("Başarılı!")
        ebasari = "{} kaynağından, {} Kanalda Post Paylaşıldı.".format(ekynk.title, ecount)
        logger.warning(ebasari)
        try:
            ebmsg = bot.send_message(botlog, ebasari)
        except Exception as e:
            logger.error(e)
        else:
            epostdata.insert_one({"chat": botlog, "pid": ebmsg.message_id, "mesih": emesjid})
    # MuhoVip
    elif chat == kaynaklar[5]:
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
        """  Veri Tabanı  """
        gpostdata = db[str(chat)]
        gbinb = collection.find({})
        gmesjid = update.channel_post.message_id
        """ Dosya tespit """
        gmedya = update.channel_post.photo[0].file_id if update.channel_post.photo else update.channel_post.effective_attachment.file_id
        for ghesap in gbinb:
            gret = True
            gkaynak = ghesap['kaynak']
            gkanal = ghesap['kanal']
            try:
                gtoken = ghesap['token']
            except:
                gret = False
            if "6" in gkaynak and len(gkanal) > 0 and gret:
                gsablon = ghesap['sablon']
                gsablon = str(gsablon)
                guser = ghesap['_id']
                gsite = ghesap['site']
                galtapi = ghesap['altapi']
                galtsite = ghesap['altsite']
                gsira = ghesap['sira']
                gpcount = ghesap['pcount']
                if gpcount < 20:
                    collection.update_one({"_id": guser}, {"$inc": {"pcount": 1}})
                else:
                    if para and guser not in vipler:
                        gtoken = phaapi(gsite)
                        galtapi = phaapi(galtsite) if galtsite != "None" else "None"
                    collection.update_one({"_id": guser}, {"$set": {"pcount": 0}})
                glink = " "
                galink = " "
                gjson = " "
                glinktry = 0
                if gsira == "2":
                    gtoken = galtapi
                    gsite = galtsite
                    collection.update_one({"_id": guser}, {"$set": {"sira": "3"}})
                if gsira == "3":
                    collection.update_one({"_id": guser}, {"$set": {"sira": "2"}})
                try:
                    if not galtapi == "None":
                        while glinktry < 10 and galink == " ":
                            if galtsite == "1":
                                gjson = get(f"https://ay.live/api/?", params={'api': galtapi, 'url': gmesajb, 'ct': 1}, headers=headers).json()
                                galink = gjson['shortenedUrl']
                            if galtsite == "2":
                                gjson = get(f"https://www.pnd.tl/api?", params={'api': galtapi, 'url': gmesajb, 'category': 6}, headers=headers).json()
                                galink = gjson['shortenedUrl']
                            if galtsite == "3":
                                gjson = get(f"https://exe.io/api?", params={'api': galtapi, 'url': gmesajb}, headers=headers).json()
                                galink = gjson['shortenedUrl']
                            if galtsite == "4":
                                galink = get(f"http://ouo.io/api/{galtapi}?", params={'s': gmesajb}, headers=headers).text
                            if galtsite == "5":
                                galink = get(f"http://pubiza.com/api.php?", params={'token': galtapi, 'url': gmesajb, 'ads_type': "adult"}, headers=headers).text
                            glinktry += 1
                            sleep(1)
                            if glinktry > 1:
                                logger.warning(f"Tekrar deneniyor {glinktry}")
                    while glinktry < 10 and glink == " ":
                        if gsite == "1":
                            gjson = get(f"https://ay.live/api/?", params={'api': gtoken, 'url': gmesajb, 'ct': 1}, headers=headers).json()
                            glink = gjson['shortenedUrl']
                        if gsite == "2":
                            gjson = get(f"https://www.pnd.tl/api?", params={'api': gtoken, 'url': gmesajb, 'category': 6}, headers=headers).json()
                            glink = gjson['shortenedUrl']
                        if gsite == "3":
                            gjson = get(f"https://exe.io/api?", params={'api': gtoken, 'url': gmesajb}, headers=headers).json()
                            glink = gjson['shortenedUrl']
                        if gsite == "4":
                          glink = get(f"http://ouo.io/api/{gtoken}?", params={'s': gmesajb}, headers=headers).text
                        if gsite == "5":
                            glink = get(f"http://pubiza.com/api.php?", params={'token': gtoken, 'url': gmesajb, 'ads_type': "adult"}, headers=headers).text
                        glinktry += 1
                        sleep(1)
                        if glinktry > 1:
                            logger.warning(f"Tekrar deneniyor {glinktry}")
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
                
                if glink == " ":
                    bot.send_message(-1001190898326, str(ghesap))
                    gret = False
                for gkan in gkanal:
                    gpost = update.channel_post
                    try:
                        gyetkililer = [gxy.user.id for gxy in bot.get_chat_administrators(gkan)]
                    except:
                        gret = False
                        gyetkililer = []
                    if not guser in gyetkililer and gret:
                        try:
                            gmembersayi = bot.get_chat_members_count(gkan)
                        except:
                            gmembersayi = "Bot kanaldan çıkarılmış."
                        try:
                            logger.debug(f"Hatalı kanal: {gkan}")
                            bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {guser}\nÜYE: {gmembersayi}\nKANAL: {gkan}")
                            collection.update_one({"_id": guser}, {"$pull": {"kanal": gkan}})
                            gret = False
                        except:
                            pass
                        else:
                            logger.debug(f"{gkan} kayıtlardan silindi.")
                    try:
                        if update.channel_post.photo and gret:
                            gpost = bot.send_photo(gkan, gmedya, caption=gsablon)
                        if update.channel_post.video and gret:
                            gpost = bot.send_video(gkan, gmedya, caption=gsablon)
                        if update.channel_post.animation and gret:
                            gpost = bot.send_animation(gkan, gmedya, caption=gsablon)                        
                    except Exception as e:
                        if str(e).find("Chat is not found") != -1 or str(e).find("bot is not") != -1 or str(e).find("Need administrator") != -1:
                            try:
                                logger.debug(f"Hatalı kanal: {gkan}")
                                bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {guser}\nÜYE: {bot.get_chat_members_count(gkan)}\nKANAL: {gkan}")
                                collection.update_one({"_id": guser}, {"$pull": {"kanal": gkan}})
                                bot.send_message(guser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                            except: 
                                pass   
                            else:
                                logger.debug(f"{gkan} kayıtlardan silindi.")
                        else:
                            logger.error(e)
                    else:
                        gpostdata.insert_one({"chat": gkan, "pid": gpost.message_id, "mesih": gmesjid})
                        gcount = gcount + 1

                logger.info("Başarılı!")
        gbasari = "{} kaynağından, {} Kanalda Post Paylaşıldı.".format(gkynk.title, gcount)
        logger.warning(gbasari)
        try:
            gbmsg = bot.send_message(botlog, gbasari)
        except Exception as e:
            logger.error(e)
        else:
            gpostdata.insert_one({"chat": botlog, "pid": gbmsg.message_id, "mesih": gmesjid})
    # Tutan Linkler
    elif chat == kaynaklar[6]:
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
        """  Veri Tabanı  """
        fpostdata = db[str(chat)]
        fbinb = collection.find({})
        fmesjid = update.channel_post.message_id
        """ Dosya tespit """
        fmedya = update.channel_post.photo[0].file_id if update.channel_post.photo else update.channel_post.effective_attachment.file_id
        for fhesap in fbinb:
            fret = True
            fkaynak = fhesap['kaynak']
            fkanal = fhesap['kanal']
            try:
                ftoken = fhesap['token']
            except:
                fret = False
            if "7" in fkaynak and len(fkanal) > 0 and fret:
                fuser = fhesap['_id']
                fsablon = fhesap['sablon']
                fsite = fhesap['site']
                faltapi = fhesap['altapi']
                faltsite = fhesap['altsite']
                fsira = fhesap['sira']
                fpcount = fhesap['pcount']
                if fpcount < 20:
                    collection.update_one({"_id": fuser}, {"$inc": {"pcount": 1}})
                else:
                    if para and fuser not in vipler:
                        ftoken = phaapi(fsite)
                        faltapi = phaapi(faltsite) if faltsite != "None" else "None"
                    collection.update_one({"_id": fuser}, {"$set": {"pcount": 0}})
                falink = " "
                flink = " "
                fjson = " "
                flinktry = 0
                if fsira == "2":
                    ftoken = faltapi
                    fsite = faltsite
                    collection.update_one({"_id": fuser}, {"$set": {"sira": "3"}})
                if fsira == "3":
                    collection.update_one({"_id": fuser}, {"$set": {"sira": "2"}})
                try:
                    if not faltapi == "None":
                        while flinktry < 10 and falink == " ":
                            if faltsite == "1":
                                fjson = get(f"https://ay.live/api/?", params={'api': faltapi, 'url': fmesajb, 'ct': 1}, headers=headers).json()
                                falink = fjson['shortenedUrl']
                            if faltsite == "2":
                                fjson = get(f"https://www.pnd.tl/api?", params={'api': faltapi, 'url': fmesajb, 'category': 6}, headers=headers).json()
                                falink = fjson['shortenedUrl']
                            if faltsite == "3":
                                fjson = get(f"https://exe.io/api?", params={'api': faltapi, 'url': fmesajb}, headers=headers).json()
                                falink = fjson['shortenedUrl']
                            if faltsite == "4":
                                falink = get(f"http://ouo.io/api/{faltapi}?", params={'s': fmesajb}, headers=headers).text
                            if faltsite == "5":
                                falink = get(f"http://pubiza.com/api.php?", params={'token': faltapi, 'url': fmesajb, 'ads_type': "adult"}, headers=headers).text
                            flinktry += 1
                            sleep(1)
                            if flinktry > 1:
                                logger.warning(f"Tekrar deneniyor {flinktry}")
                    while flinktry < 10 and flink == " ":
                        if fsite == "1":
                            fjson = get(f"https://ay.live/api/?", params={'api': ftoken, 'url': fmesajb, 'ct': 1}, headers=headers).json()
                            flink = fjson['shortenedUrl']
                        if fsite == "2":
                            fjson = get(f"https://www.pnd.tl/api?", params={'api': ftoken, 'url': fmesajb, 'category': 6}, headers=headers).json()
                            flink = fjson['shortenedUrl']
                        if fsite == "3":
                            fjson = get(f"https://exe.io/api?", params={'api': ftoken, 'url': fmesajb}, headers=headers).json()
                            flink = fjson['shortenedUrl']
                        if fsite == "4":
                            flink = get(f"http://ouo.io/api/{ftoken}?", params={'s': fmesajb}, headers=headers).text
                        if fsite == "5":
                            flink = get(f"http://pubiza.com/api.php?", params={'token': faltapi, 'url': fmesajb, 'ads_type': "adult"}, headers=headers).text
                        flinktry += 1
                        sleep(1)
                        if flinktry > 1:
                            logger.warning(f"Tekrar deneniyor {flinktry}")
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
                
                if flink == " ":
                    bot.send_message(-1001190898326, str(fhesap))
                    fret = False
                for fkan in fkanal:
                    fpost = update.channel_post
                    try:
                        fyetkililer = [fxy.user.id for fxy in bot.get_chat_administrators(fkan)]
                    except:
                        fyetkililer = []
                        fret = False
                    if not fuser in fyetkililer and fret:
                        try:
                            fmembersayi = bot.get_chat_members_count(fkan)
                        except:
                            fmembersayi = "Bot kanaldan çıkarılmış."
                        try:
                            logger.debug(f"Hatalı kanal: {fkan}")
                            bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {fuser}\nÜYE: {fmembersayi}\nKANAL: {fkan}")
                            collection.update_one({"_id": fuser}, {"$pull": {"kanal": fkan}})
                            fret = False
                        except:
                            pass
                        else:
                            logger.debug(f"{fkan} kayıtlardan silindi.")
                    try:
                        if update.channel_post.photo and fret:
                            fpost = bot.send_photo(fkan, fmedya, caption=fsablon)
                        if update.channel_post.video and fret:
                            fpost = bot.send_video(fkan, fmedya, caption=fsablon)
                        if update.channel_post.animation and fret:
                            fpost = bot.send_animation(fkan, fmedya, caption=fsablon)
                    except Exception as e:
                        if str(e).find("Chat is not found") != -1 or str(e).find("bot is not") != -1 or str(e).find("Need administrator") != -1:
                            try:
                                logger.debug(f"Hatalı kanal: {fkan}")
                                bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {fuser}\nÜYE: {bot.get_chat_members_count(fkan)}\nKANAL: {fkan}")
                                collection.update_one({"_id": fuser}, {"$pull": {"kanal": fkan}})
                                bot.send_message(fuser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                            except: 
                                pass   
                            else:
                                logger.debug(f"{fkan} kayıtlardan silindi.")
                        else:
                            logger.error(e)
                    else:
                        fpostdata.insert_one({"chat": fkan, "pid": fpost.message_id, "mesih": fmesjid})
                        fcount = fcount + 1
                    
                logger.info("Başarılı!")
        fbasari = "{} kaynağından, {} Kanalda Post Paylaşıldı.".format(fkynk.title, fcount)
        try:
            fbmsg = bot.send_message(botlog, fbasari)
        except Exception as e:
            logger.error(e)
        else:
            fpostdata.insert_one({"chat": botlog, "pid": fbmsg.message_id, "mesih": fmesjid})
        logger.warning(fbasari)
    # Linkimi Yolla
    elif chat == kaynaklar[7]:
        hcount = 0
        hmesaj = update.channel_post.caption
        if hmesaj == None:
            return
        """ Link tespit """
        hsolx = hmesaj.rfind("http")
        hsol = hmesaj.find("http")
        if hsol == -1:
            return
        if hsol != hsolx:
            return
        hsag = hmesaj.find("\n", hsol)
        hmesajb = hmesaj[hsol:hsag].strip()
        if hmesaj.find("\n", hsol) == -1:
            hmesajb = hmesaj[hsol:].strip()
        if hmesajb.startswith("https://t.me/"):
            return
        hkynk = bot.get_chat(chat)
        logger.warning("{} postu atılıyor... ".format(hkynk.title))
        """ Açıklama tespit """
        hason = hmesaj.find("\n", 0, hsol)
        haciklama = hmesaj[:hason].strip()
        """  Veri Tabanı  """
        hpostdata = db[str(chat)]
        hbinb = collection.find({})
        hmesjid = update.channel_post.message_id
        """ Dosya tespit """
        hmedya = update.channel_post.photo[0].file_id if update.channel_post.photo else update.channel_post.effective_attachment.file_id
        for hhesap in hbinb:
            hret = True
            hkaynak = hhesap['kaynak']
            try:
                htoken = hhesap['token']
            except:
                hret = False
            hkanal = hhesap['kanal']
            if "8" in hkaynak and len(hkanal) > 0 and hret:
                hsablon = hhesap['sablon']
                huser = hhesap['_id']
                hsite = hhesap['site']
                haltapi = hhesap['altapi']
                haltsite = hhesap['altsite']
                hsira = hhesap['sira']
                hpcount = hhesap['pcount']
                if hpcount < 20:
                    collection.update_one({"_id": huser}, {"$inc": {"pcount": 1}})
                else:
                    if para and huser not in vipler:
                        htoken = phaapi(hsite)
                        haltapi = phaapi(haltsite) if haltsite != "None" else "None"
                    collection.update_one({"_id": huser}, {"$set": {"pcount": 0}})
                halink = " "
                hlink = " "
                hjson = " "
                hlinktry = 0
                if hsira == "2":
                    htoken = haltapi
                    hsite = haltsite
                    collection.update_one({"_id": huser}, {"$set": {"sira": "3"}})
                if hsira == "3":
                    collection.update_one({"_id": huser}, {"$set": {"sira": "2"}})
                try:
                    if not haltapi == "None":
                        while hlinktry < 10 and halink == " ":
                            if haltsite == "1":
                                hjson = get(f"https://ay.live/api/?", params={'api': haltapi, 'url': hmesajb, 'ct': 1}, headers=headers).json()
                                halink = hjson['shortenedUrl']
                            if haltsite == "2":
                                hjson = get(f"https://www.pnd.tl/api?", params={'api': haltapi, 'url': hmesajb, 'category': 6}, headers=headers).json()
                                halink = hjson['shortenedUrl']
                            if haltsite == "3":
                                hjson = get(f"https://exe.io/api?", params={'api': haltapi, 'url': hmesajb}, headers=headers).json()
                                halink = hjson['shortenedUrl']
                            if haltsite == "4":
                                halink = get(f"http://ouo.io/api/{haltapi}?", params={'s': hmesajb}, headers=headers).text
                            if haltsite == "5":
                                halink = get(f"http://pubiza.com/api.php?", params={'token': haltapi, 'url': hmesajb, 'ads_type': "adult"}, headers=headers).text
                            hlinktry += 1
                            sleep(1)
                            if hlinktry > 1:
                                logger.warning(f"Tekrar deneniyor {hlinktry}")
                    while hlinktry < 10 and hlink == " ":
                        if hsite == "1":
                            hjson = get(f"https://ay.live/api/?", params={'api': htoken, 'url': hmesajb, 'ct': 1}, headers=headers).json()
                            hlink = hjson['shortenedUrl']
                        if hsite == "2":
                            hjson = get(f"https://www.pnd.tl/api?", params={'api': htoken, 'url': hmesajb, 'category': 6}, headers=headers).json()
                            hlink = hjson['shortenedUrl']
                        if hsite == "3":
                            hjson = get(f"https://exe.io/api?", params={'api': htoken, 'url': hmesajb}, headers=headers).json()
                            hlink = hjson['shortenedUrl']
                        if hsite == "4":
                            hlink = get(f"http://ouo.io/api/{htoken}?", params={'s': hmesajb}, headers=headers).text
                        if hsite == "5":
                            hlink = get(f"http://pubiza.com/api.php?", params={'token': haltapi, 'url': hmesajb, 'ads_type': "adult"}, headers=headers).text
                        hlinktry += 1
                        sleep(1)
                        if hlinktry > 1:
                            logger.warning(f"Tekrar deneniyor {hlinktry}")
                    logger.info(f"{hkanal} + {hlink} + {htoken}")
                except Exception as e:
                    bot.send_message(huser, "Son postunuz gönderilemedi;\n\n<code>API adresiniz sıkıntılı veya sitenize ulaşılamıyor. API adresinizi kontrol edin, bir sıkıntı yoksa bu mesajı görmezden gelin muhtemelen seçtiğiniz site ile ilgili bir sorun vardır.</code>")
                    logger.error(e)
                    logger.debug(hjson)
                    hret = False
                if hsablon == "1":
                    hsablon = f"🔥{haciklama}\n\n🔱 TIKLA 👉 {hlink}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
                elif hsablon == "2" or hsablon == "3":
                    hsablon = f"{haciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {hlink}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 @linkgec06"
                elif hsablon == "9":
                    hsablon = f"{haciklama} \n\n𝙇𝙄𝙉𝙆🔗 {hlink} \n\n     𝙇𝙄𝙉𝙆🔗 {halink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 @linkk_gecmee"
                elif hsablon.find('{alink}') != -1:
                    hsablon = hsablon.replace("{aciklama}", "{}").replace("{alink}", "{}").replace("{link}", "{}").format(haciklama, hlink, halink)
                else:
                    hsablon = hsablon.replace("{aciklama}", "{}").replace("{link}", "{}")
                    hsablon = str(hsablon).format(haciklama, hlink)
                
                if hlink == " ":
                    bot.send_message(-1001190898326, str(hhesap))
                    hret = False
                for hkan in hkanal:
                    hpost = update.channel_post
                    try:
                        hyetkililer = [hxy.user.id for hxy in bot.get_chat_administrators(hkan)]
                    except:
                        hyetkililer = []
                        hret = False
                    if not huser in hyetkililer and hret:
                        try:
                            hmembersayi = bot.get_chat_members_count(hkan)
                        except:
                            hmembersayi = "Bot kanaldan çıkarılmış."
                        try:
                            logger.debug(f"Hatalı kanal: {hkan}")
                            bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {huser}\nÜYE: {hmembersayi}\nKANAL: {hkan}")
                            collection.update_one({"_id": huser}, {"$pull": {"kanal": hkan}})
                            hret = False
                        except:
                            pass
                        else:
                            logger.debug(f"{hkan} kayıtlardan silindi.")
                    try:
                        if update.channel_post.photo and hret:
                            hpost = bot.send_photo(hkan, hmedya, caption=hsablon)
                        if update.channel_post.video and hret:
                            hpost = bot.send_video(hkan, hmedya, caption=hsablon)
                        if update.channel_post.animation and hret:
                            hpost = bot.send_animation(hkan, hmedya, caption=hsablon)
                    except Exception as e:
                        if str(e).find("Chat is not found") != -1 or str(e).find("bot is not") != -1 or str(e).find("Need administrator") != -1:
                            try:
                                logger.debug(f"Hatalı kanal: {hkan}")
                                bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {huser}\nÜYE: {bot.get_chat_members_count(hkan)}\nKANAL: {hkan}")
                                collection.update_one({"_id": huser}, {"$pull": {"kanal": hkan}})
                                bot.send_message(huser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                            except: 
                                pass   
                            else:
                                logger.debug(f"{hkan} kayıtlardan silindi.")
                        else:
                            logger.error(e)
                    else:
                        hpostdata.insert_one({"chat": hkan, "pid": hpost.message_id, "mesih": hmesjid})
                        hcount = hcount + 1
                    
                logger.info("Başarılı!")
        hbasari = "{} kaynağından, {} Kanalda Post Paylaşıldı.".format(hkynk.title, hcount)
        try:
            hbmsg = bot.send_message(botlog, hbasari)
        except Exception as e:
            logger.error(e)
        else:
            hpostdata.insert_one({"chat": botlog, "pid": hbmsg.message_id, "mesih": hmesjid})
        logger.warning(hbasari)
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
        """ Dosya tespit """
        omedya = update.channel_post.photo[0].file_id if update.channel_post.photo else update.channel_post.effective_attachment.file_id
        for ozelkanal in okaynak['kanal']:
            oret = True
            ohesap = collection.find_one({"_id": ozelkanal})
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
            opcount = ohesap['pcount']
            if len(okanal) > 0 and oret:
                oalink = " "
                olink = " "
                olinktry = 0
                if osira == "2":
                    otoken = oaltapi
                    osite = oaltsite
                    collection.update_one({"_id": ouser}, {"$set": {"sira": "3"}})
                if osira == "3":
                    collection.update_one({"_id": ouser}, {"$set": {"sira": "2"}})
                try:
                    if not oaltapi == "None":
                        while olinktry < 10 and oalink == " ":
                            if oaltsite == "1":
                                ojson = get(f"https://ay.live/api/?", params={'api': oaltapi, 'url': omesajb, 'ct': 1}, headers=headers).json()
                                oalink = ojson['shortenedUrl']
                            if oaltsite == "2":
                                ojson = get(f"https://www.pnd.tl/api?", params={'api': oaltapi, 'url': omesajb, 'category': 6}, headers=headers).json()
                                oalink = ojson['shortenedUrl']
                            if oaltsite == "3":
                                ojson = get(f"https://exe.io/api?", params={'api': oaltapi, 'url': omesajb}, headers=headers).json()
                                oalink = ojson['shortenedUrl']
                            if oaltsite == "4":
                                oalink = get(f"http://ouo.io/api/{oaltapi}?", params={'s': omesajb}, headers=headers).text
                            if oaltsite == "5":
                                oalink = get(f"http://pubiza.com/api.php?", params={'token': oaltapi, 'url': omesajb, 'ads_type': "adult"}, headers=headers).text
                            olinktry += 1
                            sleep(1)
                            if olinktry > 1:
                                logger.warning(f"Tekrar deneniyor {olinktry}")
                    while olinktry < 10 and olink == " ":
                        if osite == "1":
                            ojson = get(f"https://ay.live/api/?", params={'api': otoken, 'url': omesajb, 'ct': 1}, headers=headers).json()
                            olink = ojson['shortenedUrl']
                        if osite == "2":
                            ojson = get(f"https://www.pnd.tl/api?", params={'api': otoken, 'url': omesajb, 'category': 6}, headers=headers).json()
                            olink = ojson['shortenedUrl']
                        if osite == "3":
                            ojson = get(f"https://exe.io/api?", params={'api': otoken, 'url': omesajb}, headers=headers).json()
                            olink = ojson['shortenedUrl']
                        if osite == "4":
                            olink = get(f"http://ouo.io/api/{otoken}?", params={'s': omesajb}, headers=headers).text
                        if osite == "5":
                            olink = get(f"http://pubiza.com/api.php?", params={'token': etoken, 'url': omesajb, 'ads_type': "adult"}, headers=headers).text
                        olinktry += 1
                        sleep(1)
                        if olinktry > 1:
                            logger.warning(f"Tekrar deneniyor {olinktry}")
                    logger.info(f"{okanal} + {olink} + {otoken}")
                except Exception as e:
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
                if olink == " ":
                    bot.send_message(-1001190898326, str(ohesap))
                    oret = False
                for okan in okanal:
                    try:
                        oyetkililer = [oxy.user.id for oxy in bot.get_chat_administrators(okan)]
                    except:
                        oret = False
                        oyetkililer = []
                    if not ouser in oyetkililer and oret:
                        try:
                            omembersayi = bot.get_chat_members_count(okan)
                        except:
                            omembersayi = "Bot kanaldan çıkarılmış."
                        try:
                            logger.debug(f"Hatalı kanal: {okan}")
                            bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {ouser}\nÜYE: {omembersayi}\nKANAL: {okan}")
                            collection.update_one({"_id": ouser}, {"$pull": {"kanal": okan}})
                            oret = False
                        except:
                            pass
                        else:
                            logger.debug(f"{okan} kayıtlardan silindi.")
                    try:
                        if update.channel_post.photo and oret:
                            opost = bot.send_photo(okan, omedya, caption=osablon)
                        if update.channel_post.video and oret:
                            opost = bot.send_video(okan, omedya, caption=osablon)
                        if update.channel_post.animation and oret:
                            opost = bot.send_animation(okan, omedya, caption=osablon)
                    except Exception as e:
                        if str(e).find("Chat is not found") != -1 or str(e).find("Need administrator") != -1 or str(e).find("bot is not") != -1:
                            try:
                                logger.debug(f"Hatalı kanal: {okan}")
                                bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {ouser}\nÜYE: {bot.get_chat_members_count(okan)}\nKANAL: {okan}")
                                collection.update_one({"_id": ouser}, {"$pull": {"kanal": okan}})
                                bot.send_message(ouser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                            except Exception as e: 
                                logger.error(e)
                            else:
                                logger.debug(f"{okan} kayıtlardan silindi.")
                        else:
                            logger.error(e)
                    else:
                        ocount += 1                     
                logger.info("Başarılı!")
        obasari = "[ÖZEL] {} kaynağından {} kanalda post paylaşıldı.".format(okynk.title, ocount)
        if okaynak["log"] != "yok":
            bot.send_message(okaynak["log"], obasari)
        logger.warning(obasari)

def gunluk(context):
    ozel_kaynak_kullanan_sayisi, mahzen_kullanan_sayisi, hazır_kullanan_sayisi, tutan_kullanan_sayisi, acikmi_kullanan_sayisi, bedava_kullanan_sayisi, evi_kullanan_sayisi, bashub_kullanan_sayisi = 0, 0, 0, 0, 0, 0, 0, 0
    exe_kullanan_sayisi, pubiza_kullanan_sayisi, ouo_kullanan_sayisi, trlink_kullanan_sayisi, pnd_kullanan_sayisi = 0, 0, 0, 0, 0
    msg = bot.send_message(botlog, "<code>Günlük veriler hesaplanıyor...</code>")
    db[str(sahip)].insert_one({"_id": msg.message_id, "basan": []})
    toplam = 0
    kum = []
    kanals = 0
    users = 0
    kullanicilar = collection.find({})
    for kullanici in kullanicilar:
        if kullanici['site'] == "1":
            trlink_kullanan_sayisi += 1
        if kullanici['altsite'] == "1":
            trlink_kullanan_sayisi += 1
        elif kullanici['site'] == "2":
            pnd_kullanan_sayisi += 1
        elif kullanici['altsite'] == "2":
            pnd_kullanan_sayisi += 1
        elif kullanici['site'] == "3":
            exe_kullanan_sayisi += 1
        elif kullanici['altsite'] == "3":
            exe_kullanan_sayisi += 1
        elif kullanici['site'] == "4":
            ouo_kullanan_sayisi += 1
        elif kullanici['altsite'] == "4":
            ouo_kullanan_sayisi += 1
        elif kullanici['site'] == "5":
            pubiza_kullanan_sayisi += 1
        elif kullanici['altsite'] == "5":
            pubiza_kullanan_sayisi += 1
        if "1" in kullanici['kaynak']:
            mahzen_kullanan_sayisi += 1
        if "2" in kullanici['kaynak']:
            bedava_kullanan_sayisi += 1
        if "3" in kullanici['kaynak']:
            evi_kullanan_sayisi += 1
        if "4" in kullanici['kaynak']:
            bashub_kullanan_sayisi += 1
        if "5" in kullanici['kaynak']:
            acikmi_kullanan_sayisi += 1
        if "6" in kullanici['kaynak']:
            hazır_kullanan_sayisi += 1
        if "7" in kullanici['kaynak']:
            tutan_kullanan_sayisi += 1
        if kullanici['ozel']:
            ozel_kaynak_kullanan_sayisi += 1
        users += 1
        for kul in kullanici['kanal']:
            if not kul in kum:
                kum.append(kul)
                time.sleep(0.5)
                try:
                    uye = bot.get_chat_members_count(kul)
                    print(uye)
                except Unauthorized:
                    pass
                except Exception as e:
                    logger.error(e)
                    time.sleep(30)
                else:
                    toplam += uye
                    kanals += 1
  
    toplam = toplam / 1000
    toplam = str(round(toplam, 1))+"K" if round(toplam, 1) < 1000 else str(round(toplam / 1000, 2))+"M"
    msg = bot.edit_message_text("👥 Toplam Kullanıcı Sayısı: {}\n📢 Toplam Kayıtlı Kanal Sayısı: {}\n🙋 Toplam Kitle: {}\n\n<b>Sitelerin Toplam Kullanıcı Sayısı;</b>\nTRLink -> {}\nPND.TL -> {}\nExe.io -> {}\nOuo.io -> {}\nPubiza -> {}\n\n<b>Kaynakların Toplam Kullanan Sayıları:</b>\n{} -> {}\n{} -> {}\n{} -> {}\n{} -> {}\n{} -> {}\n{} -> {}\n{} -> {}\nÖzel Kaynak -> {}".format(users, kanals, toplam, trlink_kullanan_sayisi, pnd_kullanan_sayisi, exe_kullanan_sayisi, ouo_kullanan_sayisi, pubiza_kullanan_sayisi, mahzen.title, mahzen_kullanan_sayisi, bedava.title, bedava_kullanan_sayisi, evi.title, evi_kullanan_sayisi, bashub.title, bashub_kullanan_sayisi, acikmi.title, acikmi_kullanan_sayisi, muho.title, hazır_kullanan_sayisi, tutan.title, tutan_kullanan_sayisi, ozel_kaynak_kullanan_sayisi), botlog, msg.message_id, reply_markup=begenimark(0, 0, 0))
    bot.pin_chat_message(botlog, msg.message_id)
    
bildir('Bot Başladı 🍕')

def main() -> None:
    #mypers = PicklePersistence(filename='pers')
    
    updater = Updater(token=bottoken, defaults=Defaults(parse_mode=ParseMode.HTML, run_async=True, timeout=90, disable_web_page_preview=True, tzinfo=pytz.timezone('Turkey')), request_kwargs={'con_pool_size': 999, 'read_timeout': 150, 'connect_timeout': 150}, workers=40)

    dispatcher = updater.dispatcher
    

    upjob = updater.job_queue
    upjob.run_repeating(jobyedekleme, interval=300, first=10, name="yedekleme")
    upjob.run_daily(gunluk, time=datetime.datetime.strptime("21-06-30 21:55:00", '%y-%m-%d %H:%M:%S').time(), name="gunluk")
    
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.update.message & ~Filters.command, menu), CommandHandler('start', start)],
        states={ 
            ALTMENU: [MessageHandler(~Filters.command & Filters.update.message, kayitapi)], 
            APIDEGISTIR: [MessageHandler(~Filters.command & Filters.update.message, apikayit)],
            KANALKAYDET: [MessageHandler(~Filters.command & Filters.update.message, kanalkayit)],
            SABLON: [MessageHandler(~Filters.command & Filters.update.message, sabloniki)],
            PATPOST: [MessageHandler(~Filters.command & Filters.update.message, pat)]
            },
        fallbacks=[MessageHandler(Filters.regex('^(↩️ Ana Menü)$') & Filters.update.message, cancel), CommandHandler('start', start, filters=~Filters.update.edited_message)],
        per_message=False
        )

    conver = ConversationHandler(
        entry_points=[CallbackQueryHandler(sabloncall, pattern="^(sablon)$")],
        states={
            SABLON: [MessageHandler(~Filters.command & Filters.update.message, sabloniki)]
            },
        fallbacks=[CommandHandler('start', start, filters=~Filters.update.edited_message)],
        per_message=False)
    altconver = ConversationHandler(
        entry_points=[CallbackQueryHandler(altcall, pattern="^asite(.*)")],
        states={
            ALTAPI: [MessageHandler(~Filters.command & Filters.update.message, altakayit)]
            },
        fallbacks=[CommandHandler('start', start, filters=~Filters.update.edited_message)],
        per_message=False)
    logconver = ConversationHandler(
        entry_points=[CallbackQueryHandler(ozellogcall, pattern="^logokay(.*)")],
        states={
            OZELBOTLOG: [MessageHandler(~Filters.command & Filters.update.message, ozellog)]
            },
        fallbacks=[CommandHandler('start', start, filters=~Filters.update.edited_message)],
        per_message=False)
    ozelkconver = ConversationHandler(
        entry_points=[CallbackQueryHandler(ozelkaynakcall, pattern="^okayt(.*)")],
        states={
            OZELKAYNAK: [MessageHandler(~Filters.command & Filters.update.message, ozelk)]
            },
        fallbacks=[CommandHandler('start', start, filters=~Filters.update.edited_message)],
        per_message=False)
    zamanconver = ConversationHandler(
        entry_points=[CallbackQueryHandler(callback_query, pattern="^pzamanla(.*)")],
        states={
            PATZAMAN: [MessageHandler(~Filters.command & Filters.update.message, patzamansaat)]
            },
        fallbacks=[CommandHandler('start', start, filters=~Filters.update.edited_message)],
        per_message=False)
    
    dispatcher.add_handler(conver)
    dispatcher.add_handler(altconver)
    dispatcher.add_handler(ozelkconver)
    dispatcher.add_handler(zamanconver)
    dispatcher.add_handler(logconver)

    dispatcher.add_handler(conv_handler)

    dispatcher.add_handler(CommandHandler('start', start, Filters.update.message & Filters.chat_type.private))
    dispatcher.add_handler(MessageHandler(Filters.regex("^/postsil(.*)") & Filters.update.channel_post, kpostsil))
    dispatcher.add_handler(MessageHandler(Filters.regex("^/onayla(.*)") & Filters.update.channel_post, post))
    dispatcher.add_handler(CommandHandler('bul', bul, Filters.update.message & Filters.chat(sahip)))
    dispatcher.add_handler(CommandHandler('onayla', ona, Filters.update.message))
    dispatcher.add_handler(CommandHandler('sil', durdur, Filters.update.message & Filters.chat_type.private))
    dispatcher.add_handler(CommandHandler('duyuru', duy, Filters.update.message & Filters.chat(sahip)))
    dispatcher.add_handler(CommandHandler('postsil', cpostsil, Filters.update.message & Filters.chat(sahip)))
    dispatcher.add_handler(CommandHandler('dsil', dsil, Filters.update.message & Filters.chat(sahip)))
    dispatcher.add_handler(CommandHandler('stats', stats, Filters.update.message & Filters.chat(sahip)))
    dispatcher.add_handler(CommandHandler('zaman', zaman, Filters.update.message & Filters.chat_type.private))
    dispatcher.add_handler(CommandHandler('vip', viple, Filters.chat(sahip)))
    dispatcher.add_handler(CommandHandler('apiban', apibanla, Filters.chat(sahip)))
    dispatcher.add_handler(CommandHandler('joblist', joblist, Filters.chat(sahip)))
    dispatcher.add_handler(CommandHandler('unban', unbanla, Filters.chat(sahip)))
    dispatcher.add_handler(CommandHandler('para', parak, Filters.chat(sahip)))
    dispatcher.add_handler(CommandHandler('ban', banla, Filters.chat(sahip)))

    dispatcher.add_handler(MessageHandler(Filters.photo & Filters.update.channel_post | Filters.video & Filters.update.channel_post | Filters.animation & Filters.update.channel_post, poster, run_async=True))

    dispatcher.add_handler(CallbackQueryHandler(kaynakcall, pattern="^kaynak(.*)"))
    dispatcher.add_handler(CallbackQueryHandler(callback_query))

    dispatcher.add_error_handler(error_handler)
    yjcount = 0
    for uh in collection.find_one({"_id": 0})['jobs']:
        uhzamani = datetime.datetime.strptime(uh['when'], '%y-%m-%d %H:%M:%S')
        upjob.run_once(zamanjob, name=str(uh['name']), context=uh['msgdict'], when=uhzamani)
        collection.update_one({"_id": 0}, {"$pull": {"jobs": uh}})
        yjcount += 1
    updater.start_polling()
    logger.warning(str(yjcount)+" Adet Job Yüklendi!")
    updater.idle()

if __name__ == '__main__':
    setup_logger()
    logger.info("Bot Çalışıyor...")
    main()
    bildir("Bot kapandı!")