from . import *
from .markups import *
from .anafonks import *
from .misc import *
from .komutlar import *

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
    return SABLONA

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
    call.callback_query.edit_message_text("<code>Yükleniyor...</code>")
    kys = int(call.callback_query.data.split("-")[1])
    kkanil = int(call.callback_query.data.split("-")[2])
    kkul = collection.find_one({"_id": user})
    if kkul == None:
        call.callback_query.edit_message_text(text="<b>Önce bir API kaydedin!</b>")
        return
    if kkul['ozel']:
        call.callback_query.edit_message_text(text="<b>Özel kaynak kullandığınız için kaynak başka kaynak kullanamazsınız!</b>")
        return
    mesajid = call.effective_message.message_id
    if user in KaynakCol.find_one({"sahip": kys})['kaynak'] and kkul['kanal'][kkanil] in KaynakCol.find_one({"sahip": kys})['kanal']:
        KaynakCol.update_one({"sahip": kys}, {"$pull": {"kanal": kkul['kanal'][kkanil]}})
        kopc = 0
        for kop in kkul['kanal']:
            if kop in KaynakCol.find_one({"sahip": kys})['kanal']:
                kopc += 1
        if kopc < 1:
            KaynakCol.update_one({"sahip": kys}, {"$pull": {"kaynak": user}})
        call.callback_query.answer(text="❌ Kaynak Kaldırıldı")
    else:
        if not kkul['kanal'][kkanil] in KaynakCol.find_one({"sahip": kys})['kanal']:
            KaynakCol.update_one({"sahip": kys}, {"$push": {"kanal": kkul['kanal'][kkanil]}})
        if not user in KaynakCol.find_one({"sahip": kys})['kaynak']:
            KaynakCol.update_one({"sahip": kys}, {"$push": {"kaynak": user}})
        call.callback_query.answer(text="✅ Kaynak Eklendi")
    try:
        kcisim = bot.get_chat(kkul['kanal'][kkanil]).title
    except:
        kcisim = "Kanalınıza ulaşılamadı!"
    try:
        call.callback_query.edit_message_text(text=f"<b> >>>     {kcisim}\n\nKanalınızda kullanmak istediğiniz kaynak kanalını seçin.</b>", reply_markup=kaynakmark(user, kkanil))
    except:
        pass

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

def postzamancall(call, context):
    user = call.effective_user.id
    chat = call.effective_chat.id
    mesajid = call.callback_query.message.message_id
    bot.delete_message(chat, mesajid)
    bot.send_message(chat, "Postlarınız 00:00'dan başlayarak sırasıyla hangi saatlerde gönderilmesini istediğiniz saatleri altalta yazın ve gönderin.\n\nÖrnek;\n00:00\n01:00\n02:00\n03:00\n...", reply_markup=imark())
    return POSTZAMAN

def cekiliscall(call, context):
    user = call.effective_user.id
    chat = call.effective_chat.id
    mesajid = call.callback_query.message.message_id
    cek_dat = collection.find_one({"_id": user})
    if user in collection.find_one({"_id": 0})['cekilis']:
        call.callback_query.answer("Çekilişe zaten katılmışsınız, geriye kazanmak kaldı!")
        return
    if cek_dat == None:
        call.callback_query.answer("Çekilişe katılabilmek için en az bir kanalınız olmalı!")
        return
    if len(cek_dat['kanal']) == 0:
        call.callback_query.answer("Çekilişe katılabilmek için en az bir kanalınız olmalı!")
        return
    if not user in KaynakCol.find_one({"no": 9})['kaynak']:
        call.callback_query.answer("Çekilişe katılabilmek için en az bir kanalınız Yandex Hub kaynağını kullanıyor olmalı.")
        return
    for cekkan in cek_dat['kanal']:
        if cekkan in KaynakCol.find_one({"no": 9})['kanal']:
            if bot.get_chat_members_count(cekkan) > 501:
                try:
                    collection.update_one({"_id": 0}, {"$push": {"cekilis": user}})
                except:
                    call.callback_query.answer("Bir sorun oluştu.")
                    return
                else:
                    call.callback_query.answer("Çekilişe katıldınız.")
                    cekilis_text = context.bot_data['cekilis'].format(len(collection.find_one({"_id": 0})['cekilis']))
                    call.callback_query.edit_message_text(cekilis_text, reply_markup=cekilismark())
                    return
    call.callback_query.answer("En az 500 abone olan bir kanalınız Yandex Hub kaynağını kullanmak zorunda.")

def callback_query(call, context):
    user = call.effective_user.id
    chat = call.effective_chat.id
    mesajid = call.callback_query.message.message_id    
    """ SFS Modu """
    if call.callback_query.data.startswith("sfs"):
        sfsno = int(call.callback_query.data.split("-")[-1])
        pushedsfskan = collection.find_one({"_id": user})['kanal'][sfsno]
        if pushedsfskan in collection.find_one({"_id": user})['eski']:
            collection.update_one({"_id": user}, {"$pull": {"eski": pushedsfskan}})
            call.callback_query.answer("Kanalınız için SFS modu kapatıldı.")
        else:
            collection.update_one({"_id": user}, {"$push": {"eski": pushedsfskan}})
            call.callback_query.answer("Kanalınız SFS moduna alındı.")
        call.callback_query.edit_message_reply_markup(sfsmark(user))
    """ Eklenti """
    if call.callback_query.data == "pzkaldır":
        collection.update_one({"_id": user}, {"$set": {"vakit": 0}})
        call.callback_query.edit_message_text("Özellik devre dışı bırakıldı!")
        return
    if call.callback_query.data == "ekkur":
        call.callback_query.answer("Yetkilendiriliyor...")
        for ku in collection.find_one({"_id": user})['kanal']:
            bot.send_message(eklenti, bot.get_chat(ku).invite_link)
            sleep(0.5)
            try:
                botdurum = bot.get_chat_member(ku, bot.get_me().id)
            except:
                collection.update_one({"_id": user}, {"$pull": {"kanal": ku}})
                bot.send_message(chat, "Botu kanalınızdan çıkardığınız için eklenti kurulamadı.")
                return
            if botdurum.can_post_messages and botdurum.can_invite_users and botdurum.can_promote_members:
                try:
                    bot.promote_chat_member(ku, eklenti, can_post_messages=True)
                except Exception as e:
                    logger.error(e)
                    try:
                        kurisim = bot.get_chat(ku).title
                    except:
                        bot.send_message(chat, "Botu kanalınızdan çıkardığınız için eklenti kurulamadı.")
                        return
                    bot.send_message(chat, f"Bota {kurisim} kanalınızda yönetici ekleme yetkisi vermediğiniz için eklenti kurulamadı.")
                    return
            
        call.callback_query.edit_message_text("Eklenti tüm Kanallarınıza kuruldu!")
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
        dgr = int(call.callback_query.data.split("-")[1])
        saatalert = KaynakCol.find_one({"sahip": dgr})['zaman']
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
    if call.callback_query.data.startswith("sagyan"):
        try:
            sgynknl = collection.find_one({"_id": user})['kanal'][int(call.callback_query.data.split("-")[-1])+1]
        except Exception as e:
            bot.edit_message_text("<i>İptal Edildi</i>", user, mesajid)
            logger.error(e)
            return
        call.callback_query.answer(bot.get_chat(sgynknl).title)
        call.callback_query.edit_message_text(f"<b> >>>    {bot.get_chat(sgynknl).title}\n\nKanalınızda kullanmak istediğiniz kaynak kanalını seçin.</b>", reply_markup=kaynakmark(user, int(call.callback_query.data.split("-")[-1])+1))
    if call.callback_query.data.startswith("solyan"):
        try:
            sgynknl = collection.find_one({"_id": user})['kanal'][int(call.callback_query.data.split("-")[-1])-1]
        except Exception as e:
            bot.edit_message_text("<i>İptal Edildi</i>", user, mesajid)
            logger.error(e)
            return
        call.callback_query.answer(bot.get_chat(sgynknl).title)
        call.callback_query.edit_message_text(f"<b> >>>    {bot.get_chat(sgynknl).title}\n\nKanalınızda kullanmak istediğiniz kaynak kanalını seçin.</b>", reply_markup=kaynakmark(user, int(call.callback_query.data.split("-")[-1])-1))
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
            try:
                SEND_MEDIA_TYPES[ptip](collection.find_one({"_id": user})['kanal'][0], fid, caption=psablon)
            except Exception as e:
                logger.error(e)
                bot.send_message(user, "Postunuz gönderilemedi, botu kanaldan çıkarmış olabilirsiniz.", reply_markup=dugme(user))
                return ConversationHandler.END
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
                    pyetkililer = [pxy.user.id for pxy in bot.get_chat_administrators(kan)]
                    if not user in pyetkililer:
                        bot.send_message(chat, f"{bot.get_chat(kan).title} Bu kanalda yetkili olmadığınız için post gönderilemedi ve kanal silindi.", reply_markup=dugme(user))
                        bot.delete_message(user, mesajid)
                        collection.update_one({"_id": user}, {"$pull": {"kanal": kan}})
                        continue 
                    SEND_MEDIA_TYPES[ptip](kan, fid, caption=psablon)
                bot.edit_message_text("✅<b>Postunuz Tüm Kanallarınıza Gönderildi!</b>", user, mesajid)
                context.user_data.clear()
                return ConversationHandler.END
            pyetkililer = [pxy.user.id for pxy in bot.get_chat_administrators(kanal[o])]
            if not user in pyetkililer:
                bot.send_message(chat, f"{bot.get_chat(kanal[o]).title} Bu kanalda yetkili olmadığınız için post gönderilemedi ve kanal silindi.", reply_markup=dugme(user))
                bot.delete_message(user, mesajid)
                collection.update_one({"_id": user}, {"$pull": {"kanal": kanal[o]}})
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
                    pyetkililer = [pxy.user.id for pxy in bot.get_chat_administrators(kan)]
                    if not user in pyetkililer:
                        bot.send_message(chat, f"{bot.get_chat(kan).title} Bu kanalda yetkili olmadığınız için post gönderilemedi ve kanal silindi.", reply_markup=dugme(user))
                        bot.delete_message(user, mesajid)
                        collection.update_one({"_id": user}, {"$pull": {"kanal": kan}})
                        continue
                    msg_dict.append({"pkan": kan, "psablon": psablon, "ptip": ptip, "fid": fid, "user": user})
                bot.delete_message(user, mesajid)
                bot.send_message(user, "⏱ Postunuz zamanlandı.", reply_markup=dugme(user))
                context.job_queue.run_once(callback=zamanjob, when=zamani, context=msg_dict, name=str(user))
                return ConversationHandler.END

            pyetkililer = [pxy.user.id for pxy in bot.get_chat_administrators(kanal[o])]
            if not user in pyetkililer:
                bot.send_message(chat, f"{bot.get_chat(kanal[o]).title} Bu kanalda yetkili olmadığınız için post gönderilemedi ve kanal silindi.", reply_markup=dugme(user))
                collection.update_one({"_id": user}, {"$pull": {"kanal": kanal[o]}})
                bot.delete_message(user, mesajid)
                context.user_data.clear()
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