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

def begenicall(call, context):
    user = call.effective_user.id
    chat = call.effective_chat.id
    bot.send_message(chat, "Ayarlamak istediğin buton emojilerini örnekteki gibi gönderin.\n\nÖrnek;\n<code>❤️/⛔️/🥰</code>", reply_markup=imark())
    return BEGENI

def kaynakcall(call, context):
    user = call.effective_user.id
    chat = call.effective_chat.id
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
        durak = context.bot_data['durak']
        if durak and user in collection.find_one({"_id": 0})['cekilis'] and kys == int(context.bot_data['sahip']):
            bot.send_message(chat, "Çekiliş kaynağını kullanmayı bıraktığınız için çekilişten atıldınız!")
            collection.update_one({"_id": 0}, {"$pull": {"cekilis": user}})
        for kop in kkul['kanal']:
            if kop in KaynakCol.find_one({"sahip": kys})['kanal']:
                call.callback_query.answer(text="❌ Kaynak Kaldırıldı")
                return
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
    if context.bot_data['durak']:
        call.callback_query.answer("Çekilişe katılılım süresi dolmuş, geç kaldınız :(")
        return
    if cek_dat == None:
        call.callback_query.answer("Çekilişe katılabilmek için en az bir kanalınız olmalı!")
        return
    if len(cek_dat['kanal']) == 0:
        call.callback_query.answer("Çekilişe katılabilmek için en az bir kanalınız olmalı!")
        return
    cek_k_isim = bot.get_chat(KaynakCol.find_one({'sahip': int(context.bot_data['sahip'])})['_id']).title
    if not user in KaynakCol.find_one({"sahip": int(context.bot_data['sahip'])})['kaynak']:
        call.callback_query.answer(f"Çekilişe katılabilmek için en az bir kanalınız {cek_k_isim} kaynağını kullanıyor olmalı.")
        return
    for cekkan in cek_dat['kanal']:
        if cekkan in KaynakCol.find_one({"sahip": int(context.bot_data['sahip'])})['kanal']:
            if bot.get_chat_members_count(cekkan) > 1001:
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
    call.callback_query.answer(f"En az 1000 abone olan bir kanalınız {cek_k_isim} kaynağını kullanmak zorunda.")

def devampatcall(call, context):
    chat = call.effective_chat.id
    call.effective_message.delete()
    bot.send_message(chat, "Paylaşmamı istediğin hazır postu ilet.", reply_markup=imark())
    return PATPOST

def callback_query(call, context):
    user = call.effective_user.id
    chat = call.effective_chat.id
    mesajid = call.callback_query.message.message_id   
    """ PIN """
    if call.callback_query.data.startswith("pin-"):
        pinno = int(call.callback_query.data.split("-")[-1])
        pushedpinkan = collection.find_one({"_id": user})['kanal'][pinno]
        if pushedpinkan in collection.find_one({"_id": user})['pin']:
            collection.update_one({"_id": user}, {"$pull": {"pin": pushedpinkan}})
            call.callback_query.answer("Kanalınız için Pin modu kapatıldı.")
        else:
            collection.update_one({"_id": user}, {"$push": {"pin": pushedpinkan}})
            call.callback_query.answer("Kanalınız için Pin modu açıldı.")
        call.callback_query.edit_message_reply_markup(pinmark(user))
        return 
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
    if call.callback_query.data == "del":
        call.effective_message.delete()
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
        collection.update_one({"_id": user}, {"$pull": {"kanal": kul['kanal'][s], "eski": kul['kanal'][s]}})
        bot.edit_message_text("Kanalınız Silindi!", user, mesajid)
        call.callback_query.answer(call.callback_query.id, "Kanalınız Silindi!")
        bot.send_message(blog, f"""#KANAL_SİLİNDİ\n_ID: <a href='tg://user?id={user}'>{user}</a>\nKANAL: <a href='tg://privatepost?channel={kul['kanal'][s][3:]}&post=9999999'>{kul['kanal'][s][3:]}</a>\nÜYE: {bot.get_chat_members_count(kul['kanal'][s])}\n#id{user}\n#kan{kul['kanal'][s][1:]}""")
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
            mstd = bot.send_message(chat, "Başka post paylaşacak mısınız?", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Evet", callback_data="devam"), InlineKeyboardButton("Hayır", callback_data="del")]]))
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
                    try:
                        SEND_MEDIA_TYPES[ptip](kan, fid, caption=psablon)
                    except Exception as e:
                        logger.error(e)
                        pass
                bot.edit_message_text("✅<b>Postunuz Tüm Kanallarınıza Gönderildi!</b>", user, mesajid)
                context.user_data.clear()
                mstd = bot.send_message(chat, "Başka post paylaşacak mısınız?", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Evet", callback_data="devam"), InlineKeyboardButton("Hayır", callback_data="del")]]))
                return ConversationHandler.END
            pyetkililer = [pxy.user.id for pxy in bot.get_chat_administrators(kanal[o])]
            if not user in pyetkililer:
                bot.send_message(chat, f"{bot.get_chat(kanal[o]).title} Bu kanalda yetkili olmadığınız için post gönderilemedi ve kanal silindi.", reply_markup=dugme(user))
                bot.delete_message(user, mesajid)
                collection.update_one({"_id": user}, {"$pull": {"kanal": kanal[o]}})
                return ConversationHandler.END
            try:
                SEND_MEDIA_TYPES[ptip](kanal[o], fid, caption=psablon)
            except Exception as e:
                bot.edit_message_text(f"Postunuz gönderilemedi \n\n{e}", user, mesajid)
                context.user_data.clear()
                return ConversationHandler.END
            bot.edit_message_text("✅<b>Postunuz Kanalınıza Gönderildi!</b>", user, mesajid)
            context.user_data.clear()
            mstd = bot.send_message(chat, "Başka post paylaşacak mısınız?", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Evet", callback_data="devam"), InlineKeyboardButton("Hayır", callback_data="del")]]))
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
                mstd = bot.send_message(chat, "Başka post paylaşacak mısınız?", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Evet", callback_data="devam"), InlineKeyboardButton("Hayır", callback_data="del")]]))
                context.job_queue.run_once(callback=zamanjob, when=zamani, context=msg_dict, name=str(user))
                context.user_data.clear()
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
            mstd = bot.send_message(chat, "Başka post paylaşacak mısınız?", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Evet", callback_data="devam"), InlineKeyboardButton("Hayır", callback_data="del")]]))
            return ConversationHandler.END
    """ Şablon """
    if call.callback_query.data == "vsablon":
        if collection.find_one({"_id": user})['sira'] == "1":
            collection.update_one({"_id": user}, {"$set": {"sablon": "9"}})
        else:
            collection.update_one({"_id": user}, {"$set": {"sablon": "1"}})
        bot.edit_message_text("Varsayılana döndürüldü.", chat, mesajid)
        return
    """ Emoji """
    if call.callback_query.data == "begenikaldir":
        collection.update_one({"_id": user}, {"$set": {"begeni": []}})
        call.callback_query.edit_message_text("Beğeni butonları kaldırıldı!")
        call.callback_query.answer("Kaldırıldı")
        return
    """ Tekrarli Post """
    if call.callback_query.data.startswith("tkan+"):
        context.user_data['tskan'] = call.callback_query.data.split("+")[-1]
        call.callback_query.answer("Kanal belirlendi!")
        call.callback_query.edit_message_text("Tekrarli Postunuzun kaç saatte bir gönderilmesini istediğiniz saati seçin", reply_markup=tekrarlisaatmark())
        return 
    if call.callback_query.data == "tekrarlisil":
        call.callback_query.edit_message_text("Silmek istediğiniz postu seçin.", reply_markup=tekrarlipostsilmark(user, context))
        return
    if call.callback_query.data == "yenitekrarli":
        call.callback_query.edit_message_text("Tekrarli Post ayarlamak istediğiniz kanalı seçin.", reply_markup=tekrarlipostkan(user))
        return
    if call.callback_query.data.startswith("tssil-"):
        try:
            context.job_queue.get_jobs_by_name(f"ts{user}")[call.callback_query.data.split("-")[-1]].schedule_removal()
        except:
            call.callback_query.edit_message_text("Post iptal edilemedi!")
        else:
            call.callback_query.edit_message_text("Postunuz silindi artık paylaşılmayacak")
        return

def tekrarlisaatayarlacall(call, context):
    context.user_data['tsaat'] = int(call.callback_query.data.split("-")[-1])
    bot.send_message(call.effective_chat.id, "Tekrarlı postunuza bir başlık verin.\n\nÖrnek;\nJigolo afiş, Data afiş", reply_markup=imark())
    call.callback_query.answer("Saat belirlendi!")
    return TSBASLIK

def begeniislemcall(call, context):
    user = call.effective_user.id
    chat = call.effective_chat.id
    mesajid = call.callback_query.message.message_id    
    pushed = int(call.callback_query.data.split("-")[-1])
    begkeyb = []
    mrkpc = 0
    if not user in ButonCol.find_one({"_id": str(chat)})[str(mesajid)]:
        ButonCol.update_one({"_id": str(chat)}, {"$push": {str(mesajid): user}})
    else:
        call.callback_query.answer("Butonları bir kez kullanabilirsiniz")
        return
    for beg in ButonCol.find_one({"_id": str(chat)})['begeni']:
        try:
            butsayi = int(call.effective_message.reply_markup.inline_keyboard[0][mrkpc].text.split()[-1])
        except IndexError:
            butsayi = 0
        if mrkpc == pushed:
            begkeyb.append(InlineKeyboardButton(str(beg)+" "+str(butsayi+1), callback_data="begeni-{}".format(mrkpc)))
        else:
            begkeyb.append(InlineKeyboardButton(str(beg)+" "+str(butsayi), callback_data="begeni-{}".format(mrkpc)))
        mrkpc += 1
    call.callback_query.answer(str(call.effective_message.reply_markup.inline_keyboard[0][pushed].text.split()[-2]))
    try:
        call.callback_query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([begkeyb]))
    except RetryAfter as rtt:
        time.sleep(rtt.retry_after+1)
        call.callback_query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([begkeyb]))
        