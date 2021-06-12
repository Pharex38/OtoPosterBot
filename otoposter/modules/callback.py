from telegram.ext import CallbackQueryHandler
from otoposter import *
from .markup import *

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
        bot.edit_message_text("""<b>Özel Kaynak Hakkında Bilmeniz Gerekenler</b>\n\n<i>- Özel kaynak ayarlarsanız başka kaynak seçemezsiniz.\n- Başkaları da isterse sizin özel kaynağınızı kullanabilir.\n- Kaynağınız @OtoPosterBotLog'da gözükmeyecek.\n- Postlar, diğer kaynaklara göre daha yavaş atılır.\n- Özel kaynağa kısaltılmamış link atmanız gerekiyor. Kısaltılmış linkli post atarsanız bot linki geçmez direkt olarak kısaltılmış linki tekrar kısaltır.</i>""", chat, mesajid)
        bot.edit_message_reply_markup(chat, mesajid, reply_markup=ozelmark())
    if call.callback_query.data == "okayk":
        use_r = 0
        collection.update_one({"_id": user}, {"$set": {"ozel": False}})
        for u in OzelCol.find({}):
            if user in u['kanal']:
                use_r = u['_id']
        OzelCol.update_one({"_id": use_r}, {"$pull": {"kanal": user}})
        bot.edit_message_text("Özel Kaynak Kaldırıldı.", chat, mesajid)
    if call.callback_query.data == "logokaldir":
        OzelCol.update_one({"_id": user}, {"$set": {"log": "yok"}})
        call.callback_query.edit_message_text("Botlog Kaldırıldı.")
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


dispatcher.add_handler(CallbackQueryHandler(kaynakcall, pattern="^kaynak(.*)"))
dispatcher.add_handler(CallbackQueryHandler(callback_query))
