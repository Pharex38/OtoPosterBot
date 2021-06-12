from os import environ
import asyncio
import os, signal
from typing import Dict
import Colorer
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



def stats(update, context):
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
                time.sleep(1.6)
                kanals += 1
                try:
                    uye = bot.get_chat_members_count(kul)
                    print(uye)
                except Exception as e:
                    logger.error(e)
                    time.sleep(20)
                toplam += uye
          
    toplam = toplam / 1000
    toplam = str(round(toplam, 1))+"K" if round(toplam, 1) < 1000 else str(round(toplam / 1000, 1))+"M"
    bot.edit_message_text("Toplam Kullanıcı Sayısı: {}\nToplam Kayıtlı Kanal Sayısı: {}\nToplam Kitle: {}".format(users, kanals, toplam), chat, msg.message_id)

def bul(update, context):
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
    kimi = int(update.message.text.split()[1]) if len(update.message.text.split()) > 1 and user in adminlist else message.from_user.id
    if user in kara:
        bot.send_message(chat, "🤓 Üzgünüm senin gibi aptal birisi için çalışmıyorum")
        return
    try:
        collection.delete_one({"_id": kimi})
    except:
        update.message.reply_text("<b>Henüz bir kanal kaydetmemişsiniz.</b>")
    else:
        update.message.reply_text("<b>Kanalınız Silindi!</b>")

def kpostsil(update, context):
    chat = update.channel_post.chat.id
    if not chat in kaynaklar:
        return
    mesid = update.channel_post.reply_to_message.message_id if update.message.reply_to_message else None
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
    hedef = update.message.text.split()[1] if len(update.message.text.split()) > 1 else None
    mesid = int(update.message.text.split()[2]) if len(update.message.text.split()) > 2 else None
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
    
def duy(m, context):
    chat = m.message.chat.id
    if chat != sahip:
        return
    duyurus = 0
    if m.message.reply_to_message:
        duyurumsg = m.update.reply_to_message.message.text
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
    sleep(1.6)
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
        bot.send_message(update.message.chat.id, "<b>Özel Kaynak Oluşturuldu!</b>", reply_markup=dugme(user))
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






logger.info("Bot Çalışıyor...")
bildir('Bot Başladı 🍕')

def main() -> None:
    updater = Updater(token=bottoken, defaults=Defaults(parse_mode=ParseMode.HTML, run_async=True, timeout=90), request_kwargs={'con_pool_size': 999, 'read_timeout': 150, 'connect_timeout': 150})

    dispatcher = updater.dispatcher

    updater.job_queue
    
    conver = ConversationHandler(
        entry_points=[CallbackQueryHandler(sabloncall, pattern="^(sablon)$")],
        states={
            SABLON: [MessageHandler(Filters.text & Filters.update.message, sabloniki)]
            },
        fallbacks=[MessageHandler(Filters.regex('^(↩️ Ana Menü)$') & Filters.update.message, cancel), CommandHandler('start', start, filters=~Filters.update.edited_message)],
        per_message=False)
    logconver = ConversationHandler(
        entry_points=[CallbackQueryHandler(ozellogcall, pattern="^logokay(.*)")],
        states={
            OZELBOTLOG: [MessageHandler(Filters.all & Filters.update.message, ozellog)]
            },
        fallbacks=[MessageHandler(Filters.regex('^(↩️ Ana Menü)$') & Filters.update.message, cancel), CommandHandler('start', start, filters=~Filters.update.edited_message)],
        per_message=False)
    ozelkconver = ConversationHandler(
        entry_points=[CallbackQueryHandler(ozelkaynakcall, pattern="^okayt(.*)")],
        states={
            OZELKAYNAK: [MessageHandler(~Filters.command & Filters.update.message, ozelk)]
            },
        fallbacks=[MessageHandler(Filters.regex('^(↩️ Ana Menü)$') & Filters.update.message, cancel), CommandHandler('start', start, filters=~Filters.update.edited_message)],
        per_message=False)
    
    dispatcher.add_handler(conver)
    dispatcher.add_handler(ozelkconver)
    dispatcher.add_handler(logconver)


    dispatcher.add_handler(CommandHandler('start', start, Filters.update.message & Filters.chat_type.private))
    dispatcher.add_handler(MessageHandler(Filters.command('onayla') & Filters.update.channel_post, post))
    dispatcher.add_handler(MessageHandler(Filters.command('postsil') & Filters.update.channel_post, kpostsil))
    dispatcher.add_handler(CommandHandler('bul', bul, Filters.update.message & Filters.chat_type.private))
    dispatcher.add_handler(CommandHandler('onayla', ona, Filters.update.message))
    dispatcher.add_handler(CommandHandler('sil', durdur, Filters.update.message & Filters.chat_type.private))
    dispatcher.add_handler(CommandHandler('duyuru', duy, Filters.update.message & Filters.chat_type.private))
    dispatcher.add_handler(CommandHandler('postsil', cpostsil, Filters.update.message & Filters.chat_type.private))
    dispatcher.add_handler(CommandHandler('dsil', dsil, Filters.update.message & Filters.chat_type.private))
    dispatcher.add_handler(CommandHandler('stats', stats, Filters.update.message & Filters.chat_type.private))
    dispatcher.add_handler(CommandHandler('zaman', zaman, Filters.update.message & Filters.chat_type.private))



if __name__ == '__main__':
    main()
