from . import *
from .markups import *
from .anafonks import *
from .misc import *
from .komutlar import *

def sabloncall(call, context):
    user = call.effective_user.id
    chat = call.effective_chat.id
    mesajid = call.effective_message.message_id
    try:
        bot.delete_message(chat, mesajid)
    except:
        pass
    if collection.find_one({"_id": user}) == None:
        call.callback_query.edit_message_text(text="<b>Önce bir API kaydedin!</b>")
        return
    if collection.find_one({"_id": user})['sira'] == 1 or collection.find_one({"_id": user})['altsite'] == "tpil":
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
    if smesaj == "15":
        bot.send_message(chat, f"Bu site alternatif olarak kullanılamıyor.")
        return
    call.callback_query.answer(call.callback_query.id, "✅ Site Kaydedildi!")
    bot.edit_message_text("✅ Alternatif site kaydedildi.", user, mesajid)
    bot.send_message(chat, "📝 Alternatif API adresinizi gönderin.", reply_markup=imark())
    return ALTAPI

def ayarlarcall(call, context):
    user = call.effective_user.id
    chat = call.effective_chat.id
    
def kaynakkontrolcall(call, context):
    chat = call.effective_chat.id
    user = call.effective_user.id
    query = call.callback_query
    callkd = query.data.split("-")[1]
    query.answer(".")
    if callkd == "evet":
        query.edit_message_text(f"<b>Aşağıdaki kuralları onaylıyor musun?</b>\n\n{collection.find_one({'_id': 0})['kurallar']}\n\nBoşu boşuna istek gönderenleri bottan banlarım!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Okudum, onaylıyorum.", callback_data="kont-devam1")], [InlineKeyboardButton("Vazgeçtim", callback_data="aiptal")]]))
    elif callkd == "devam1":
        query.edit_message_text("İçeriğiniz nedir?", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("+18", callback_data="kont-devam2-+18")], [InlineKeyboardButton("Arşiv", callback_data="kont-devam2-arsiv")], [InlineKeyboardButton("Vazgeçtim", callback_data="aiptal")]]))
    elif callkd == "devam2":
        context.user_data["kont-icerik"] = query.data.split("-")[2]
        if query.data.split("-")[2] == "+18":
            query.edit_message_text("Yerli/Yabanci ?", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🇹🇷", callback_data="kont-devam3-tr")], [InlineKeyboardButton("🇬🇧", callback_data="kont-devam3-yb")], [InlineKeyboardButton("Vazgeçtim", callback_data="aiptal")]]))
        else:
            context.user_data['kont-tur'] = None
            pass
    elif callkd == "devam3":
        context.user_data['kont-tur'] = query.data.split("-")[2]
        query.edit_message_text("Kullanacağınız depolama servisi nedir?", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Yandex, Cloud vs.", callback_data="kont-son-cloud")], [InlineKeyboardButton("Streamtape veya Streamtape benzeri", callback_data="kont-son-tape")]]))
    elif callkd == "son":
        if context.user_data['kont-icerik'] == "+18":
            collection.update_one({"_id": 0}, {"$push": {"kont": {"user": user, "icerik": context.user_data['kont-icerik'], "tur": context.user_data['kont-tur']}}})
        elif context.user_data['kont-icerik'] == "arsiv":
            collection.update_one({"_id": 0}, {"$push": {"kont": {"user": user, "icerik": context.user_data['kont-icerik'], "tur": None}}})
        bot.send_message(chat, "İsteğiniz gönderildi!")

def begenicall(call, context):
    user = call.effective_user.id
    chat = call.effective_chat.id
    if len(collection.find_one({"_id": user})['kanal']) == 0:
        bot.send_message(chat, "Beğeni butonu ayarlayabilmek için önce bir kanal kaydetmelisiniz!")
        return
    bot.send_message(chat, "Ayarlamak istediğin buton emojilerini örnekteki gibi gönderin.\n\nÖrnek;\n<code>❤️/⛔️/🥰</code>", reply_markup=imark())
    return BEGENI

def kaynakcall(call, context):
    user = call.effective_user.id
    call.callback_query.edit_message_text("Menü eski kaldığı için kapatıldı.")
    return

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
    try:
        bot.delete_message(chat, mesajid)
    except:
        pass
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
        call.callback_query.answer(show_alert=True, text="Çekilişe zaten katılmışsınız, geriye kazanmak kaldı!")
        return
    try:
        durak = context.bot_data['durak']
    except KeyError:
        durak = False
    if context.bot_data['durak']:
        call.callback_query.answer(show_alert=True, text="Çekilişe katılılım süresi dolmuş, geç kaldınız :(")
        return
    if cek_dat == None:
        call.callback_query.answer(show_alert=True, text="Çekilişe katılabilmek için en az bir kanalınız olmalı!")
        return
    if len(cek_dat['kanal']) == 0:
        call.callback_query.answer(show_alert=True, text="Çekilişe katılabilmek için en az bir kanalınız olmalı!")
        return
    cek_k_isim = bot.get_chat(KaynakCol.find_one({'sahip': int(context.bot_data['sahip'])})['_id']).title
    if not user in KaynakCol.find_one({"sahip": int(context.bot_data['sahip'])})['kaynak']:
        call.callback_query.answer(show_alert=True, text=f"Çekilişe katılabilmek için en az bir kanalınız {cek_k_isim} kaynağını kullanıyor olmalı.")
        return
    for cekkan in cek_dat['kanal']:
        if cekkan in KaynakCol.find_one({"sahip": int(context.bot_data['sahip'])})['kanal']:
            try:
                cekkanabone = bot.get_chat_member_count(cekkan)
            except:
                continue
            if cekkanabone > 1001:
                try:
                    collection.update_one({"_id": 0}, {"$push": {"cekilis": user}})
                except:
                    call.callback_query.answer(show_alert=True, text="Bir sorun oluştu.")
                    return
                else:
                    call.callback_query.answer("Çekilişe katıldınız.")
                    cekilis_text = context.bot_data['cekilis'].format(len(collection.find_one({"_id": 0})['cekilis']))
                    call.callback_query.edit_message_text(cekilis_text, reply_markup=cekilismark())
                    return
    call.callback_query.answer(show_alert=True, text=f"En az 1000 abone olan bir kanalınız {cek_k_isim} kaynağını kullanmak zorunda.")

def devampatcall(call, context):
    chat = call.effective_chat.id
    try:
        call.effective_message.delete()
    except:
        pass
    bot.send_message(chat, "Paylaşmamı istediğin hazır postu ilet.", reply_markup=imark())
    return PATPOST

def panelcall(call, context):
    query = call.callback_query
    chat = call.effective_chat.id
    user = call.effective_user.id
    query.answer("Lütfen bekleyin...")
    if query.data == "panelzaman":
        bot.send_message(call.effective_chat.id, "Ayarlamak istediğiniz mesajı gönderin.", reply_markup=imark())
        return PANELZAMAN
    elif query.data == "panelkural":
        bot.send_message(chat, str(collection.find_one({"_id": 0})['kurallar']))
    elif query.data.startswith("pau"):
        kaynak_users = KaynakCol.find_one({"sahip": user})['kaynak'].remove(sahip) if sahip in KaynakCol.find_one({"sahip": user})['kaynak'] else KaynakCol.find_one({"sahip": user})['kaynak']
        panel_user_text = f"<b>Kaynağınızı Kullanan Kullanıcılar;</b>\n\n"
        que = int(query.data.split("-")[-1]) if query.data.split("-")[-1] != "bul" else None
        if que == None:
            bot.send_message(chat, "Bulmak istediğiniz kullanıcının ID'sini veya kullanıcıdan herhangi bir mesaj iletin.", reply_markup=imark())
            return PANELBUL
        for paucount in range(que-10,que):
            try:
                if type(kaynak_users) != list:
                    continue
                if kaynak_users[paucount] == sahip:
                    continue
                panel_user_text += str(paucount) + ". " + mention_html(kaynak_users[paucount], bot.get_chat(kaynak_users[paucount]).first_name) + "\n"
            except IndexError:
                paumark = [[InlineKeyboardButton("🔍 Kullanıcı Bul", callback_data="pau-bul")], [InlineKeyboardButton("⏪Önceki Sayfa ", callback_data="pau-{}".format(que-10))]]
                break
        else:
            paumark = [[InlineKeyboardButton("🔍 Kullanıcı Bul", callback_data="pau-bul")], [InlineKeyboardButton("⏪Önceki Sayfa ", callback_data="pau-{}".format(que-10)), InlineKeyboardButton("Sonraki Sayfa ⏩", callback_data="pau-{}".format(que+10))] if len(kaynak_users) > que else []]
        if que == len(kaynak_users):
            paumark = [[InlineKeyboardButton("🔍 Kullanıcı Bul", callback_data="pau-bul")], [InlineKeyboardButton("⏪Önceki Sayfa ", callback_data="pau-{}".format(que-10))]]
        if que == 10:
            paumark = [[InlineKeyboardButton("🔍 Kullanıcı Bul", callback_data="pau-bul")], [InlineKeyboardButton("Sonraki Sayfa ⏩", callback_data="pau-{}".format(que+10))] if len(kaynak_users) > que else []]
        query.edit_message_text(panel_user_text, reply_markup=InlineKeyboardMarkup(paumark))
    elif query.data == "panelkullanici":
        kaynak_users = KaynakCol.find_one({"sahip": user})['kaynak']
        panel_user_text = f"<b>Kaynağınızı Kullanan Kullanıcılar;</b>\n\n"
        for paucount in range(11):
            try:
                panel_user_text += str(paucount) + ". " + mention_html(kaynak_users[paucount], bot.get_chat(kaynak_users[paucount]).first_name) + "\n"
            except IndexError:
                paumark = [[InlineKeyboardButton("🔍 Kullanıcı Bul", callback_data="pau-bul")]]
                break
        else:
            paumark = [[InlineKeyboardButton("🔍 Kullanıcı Bul", callback_data="pau-bul")], [InlineKeyboardButton("Sonraki Sayfa ⏩", callback_data="pau-20")] if len(kaynak_users) > 10 else []]
        bot.send_message(chat, panel_user_text, reply_markup=InlineKeyboardMarkup(paumark))
    elif query.data.startswith("pak-"):
        kaynak_users = KaynakCol.find_one({"sahip": user})['kanal']
        panel_user_text = f"<b>Kaynağınızı Kullanan Kanallar;</b>\n\n"
        que = int(query.data.split("-")[-1]) if query.data.split("-")[-1] != "bul" else None
        if que == None:
            bot.send_message(chat, "Bulmak istediğiniz Kanalın ID'sini veya Kanaldan herhangi bir mesaj iletin.", reply_markup=imark())
            return PANELBUL
        for pakcount in range(que-10,que):
            try:
                panel_user_text += str(pakcount) + ". " + kan_mention_html(kaynak_users[pakcount]) + "\n"
            except IndexError:
                pakmark = [[InlineKeyboardButton("🔍 Kanal Bul", callback_data="pak-bul")], [InlineKeyboardButton("⏪Önceki Sayfa ", callback_data="pak-{}".format(que-10))]]
                break
        else:
            pakmark = [[InlineKeyboardButton("🔍 Kanal Bul", callback_data="pak-bul")], [InlineKeyboardButton("⏪Önceki Sayfa ", callback_data="pak-{}".format(que-10)), InlineKeyboardButton("Sonraki Sayfa ⏩", callback_data="pak-{}".format(que+10))] if len(kaynak_users) > que else []]
        if que == len(kaynak_users):
            pakmark = [[InlineKeyboardButton("🔍 Kanal Bul", callback_data="pak-bul")], [InlineKeyboardButton("⏪Önceki Sayfa ", callback_data="pak-{}".format(que-10))]]
        if que == 10:
            pakmark = [[InlineKeyboardButton("🔍 Kanal Bul", callback_data="pak-bul")], [InlineKeyboardButton("Sonraki Sayfa ⏩", callback_data="pak-{}".format(que+10))] if len(kaynak_users) > que else []]
        query.edit_message_text(panel_user_text, reply_markup=InlineKeyboardMarkup(pakmark))
    elif query.data == "panelkanal":
        kaynak_users = KaynakCol.find_one({"sahip": user})['kanal']
        panel_user_text = f"<b>Kaynağınızı Kullanan Kanallar;</b>\n\n"
        for pakcount in range(11):
            try:
                panel_user_text += str(pakcount) + ". " + kan_mention_html(kaynak_users[pakcount]) + "\n"
            except IndexError:
                pakmark = [[InlineKeyboardButton("🔍 Kanal Bul", callback_data="pak-bul")]]
                break
        else:
            pakmark = [[InlineKeyboardButton("🔍 Kanal Bul", callback_data="pak-bul")], [InlineKeyboardButton("Sonraki Sayfa ⏩", callback_data="pak-20")] if len(kaynak_users) > 10 else []]
        bot.send_message(chat, panel_user_text, reply_markup=InlineKeyboardMarkup(pakmark))
    elif query.data == "panelguncellemeler":
        gunc_text = "<b>Bottaki Son Güncellemeler;</b>\n\n<i>• "
        gunc_text += "\n• ".join(collection.find_one({"_id": 0})['guncelleme'][::-1][:5])
        bot.send_message(chat, gunc_text+"</i>")
    else:
        query.answer("Yanıt bulunamadı!")

def callback_query(call, context):
    user = call.effective_user.id
    chat = call.effective_chat.id
    mesajid = call.callback_query.message.message_id
    """ İstek """
    if call.callback_query.data.startswith("smiktari-"):
        call.callback_query.answer("ㅤ")
        istekkanno = int(call.callback_query.data.split("-")[1])
        istekcount = 0
        try:
            istekkan = bot.get_chat(collection.find_one({"_id": user})['kanal'][istekkanno])
        except:
            call.callback_query.edit_message_text("Butonların kullanım süresi dolmuş lütfen menüden tekrar açın.")
            return
        if istekkan.invite_link == None:
            call.callback_query.edit_message_text("İstek onaylayabilmem için bota kanalınızda <b>Üye Ekleme</b> yetkisi vermelisiniz!")
            return
        bot.send_message(chat, "Aşağıdaki butonlari kullanarak onaylanmasını istediğiniz istek miktarını belirleyin.\n\n>>> {}".format(istekkan.title), reply_markup=miktarliistekmark(istekkanno, istekcount))
        return

    if call.callback_query.data.startswith("miktari-"):
        call.callback_query.answer("ㅤ")
        
        istekkanno = int(call.callback_query.data.split("-")[1])
        try:
            istekcount = int(call.callback_query.data.split("-")[2])
        except ValueError:
            return
        try:
            call.callback_query.edit_message_reply_markup(reply_markup=miktarliistekmark(istekkanno, istekcount))
        except:
            pass
        return
    if call.callback_query.data.startswith("isteklink-"):
        call.callback_query.edit_message_text("<code>Yükleniyor...</code>")
        rpmup = []
        istekkanno = int(call.callback_query.data.split("-")[1])
        istekcount = int(call.callback_query.data.split("-")[2])
        istekkan = collection.find_one({"_id": user})['kanal'][istekkanno]
        if len(IstekCol.find_one({"_id": 0})[istekkan].get("istekler", [])) == 0:
            call.callback_query.edit_message_text("Hiç onaylanmamış istek göremiyorum. 😔")
            return
        xrlist = IstekCol.find_one({"_id": 0})[istekkan]["istekler"]
        shuffle(xrlist)
        for xrp in xrlist[:20]:
            xrp = IstekCol.update_one({"_id": 0}, {"$pull": {f"{istekkan}.istekler": xrp}})
            if type(xrp) != dict:
                continue
            rpbut = [InlineKeyboardButton(xrp['link'], callback_data=f"allistek-{istekkanno}-{istekcount}-{xrp['link']}")]
            if not rpbut in rpmup:
                rpmup.append(rpbut)
        rpmup.append([InlineKeyboardButton("Hepsini Onayla", callback_data=f"allistek-{istekkanno}-99999-all")])
        call.callback_query.edit_message_text("<i>İsteklerin onaylanmasını istediğiniz linki seçin.</i>", reply_markup=InlineKeyboardMarkup(rpmup))
        return
    if call.callback_query.data.startswith("allistek-"):
        call.callback_query.answer("ㅤ")
        try:
            call.effective_message.delete()
        except:
            pass
        istekkanno = int(call.callback_query.data.split("-")[1])
        istekcount = int(call.callback_query.data.split("-")[2])
        pushlink = call.callback_query.data.split("-")[3]
        istekkan = collection.find_one({"_id": user})['kanal'][istekkanno]
        
        try:
            istekkanlink = bot.get_chat(istekkan)
        except:
            call.callback_query.edit_message_text("Butonların kullanım süresi dolmuş lütfen menüden tekrar açın.")
            return
        if istekkanlink.invite_link == None:
            call.callback_query.edit_message_text("İstek onaylayabilmem için bota kanalınızda <b>Üye Ekleme</b> yetkisi vermelisiniz!")
            return
        onaymsg = bot.send_message(chat, "<code>İşlem başlıyor...</code>")
        isteklers = IstekCol.find_one({"_id": 0})[str(istekkan)]['istekler']
        if len(isteklers) < 1:
            onaymsg.edit_text("Hiç onaylanmamış istek göremiyorum. 😔")
            return
        onaycount = 0
        logger.warning(f"İstekler Onaylanıyor - {istekcount}")
        for isteka in isteklers:
            sleep(0.025)
            if type(isteka) != dict:
                IstekCol.update_one({"_id": 0}, {"$pull": {f"{str(istekkan)}.istekler": isteka}})
                continue
            try:
                if isteka['link'] == pushlink or pushlink == "all":
                    bot.approve_chat_join_request(istekkan, isteka['user'])
                else:
                    continue
            except Exception as e:
                logger.error(e)
            else:
                onaycount += 1
            IstekCol.update_one({"_id": 0}, {"$pull": {f"{str(istekkan)}.istekler": isteka}})
            if onaycount >= istekcount:
                break
            if onaycount % 10 == 0:
                logger.info(f"{onaycount} istek onaylandı...")
        logger.warning(f"Onaylama işlemi bitti - {onaycount}")
        bot.send_message(blog, istekonaylog.format(istek=onaycount, kan=istekkan[3:], user=user))
        onaymsg.edit_text(f"{onaycount} istek onaylandı!")
        return
        
    if call.callback_query.data.startswith("istek-"):
        istekno = int(call.callback_query.data.split("-")[-1])
        try:
            pushedistekkan = collection.find_one({"_id": user})['kanal'][istekno]
            istekkanlink = bot.get_chat(pushedistekkan)
        except:
            call.callback_query.edit_message_text("Butonların kullanım süresi dolmuş lütfen menüden tekrar açın.")
            return
        if istekkanlink.invite_link == None:
            call.callback_query.edit_message_text("İstek onaylayabilmem için bota kanalınızda <b>Üye Ekleme</b> yetkisi vermelisiniz!")
            return
        if pushedistekkan in collection.find_one({"_id": 0})['istek']:
            collection.update_one({"_id": 0}, {"$pull": {"istek": pushedistekkan}})
            call.callback_query.answer("Kanalınız için istek modu kapatıldı.")
        else:
            collection.update_one({"_id": 0}, {"$push": {"istek": pushedistekkan}})
            call.callback_query.answer("Kanalınız için istek modu açıldı.")
        try:
            call.callback_query.edit_message_reply_markup(istekmark(user))
        except:
            pass
        return 
    if call.callback_query.data.startswith("ozicerik-"):
        if call.callback_query.data.split("-")[-1] == "arsiv":
            icc = "+18"
        else:
            icc = "arsiv"
        OzelCol.update_one({"_id": user}, {"$set": {"icerik": icc}})
        bot.edit_message_reply_markup(chat_id=chat, message_id=mesajid, reply_markup=ozelkaynakmark(user, 0))
        call.callback_query.answer("Tür değiştirildi")
    """ İptal """
    if call.callback_query.data == "del":
        try:
            call.effective_message.delete()
        except:
            pass
    if call.callback_query.data == "dsil":
        collection.delete_one({"_id": user})
        try:
            call.callback_query.answer("💔")
            call.callback_query.edit_message_text("💔")
        except:
            pass
        bot.send_message(chat, "Tüm bilgileriniz silindi.", reply_markup=dagme())
    if call.callback_query.data == "akaldır":
        collection.update_one({"_id": user}, {"$set": {"altsite": "None", "altapi": "None", "sira": 0, "sablon": "1"}})
        bot.edit_message_text("⛔ Alternatif Kaldırıldı.", user, mesajid)
        call.callback_query.answer("⛔ Alternatif Kaldırıldı.")
    if call.callback_query.data == "aiptal":
        bot.edit_message_text("<i>Menü kapatıldı.</i>", user, mesajid)
        return
    if call.callback_query.data == "iptal":
        bot.edit_message_text("<i>İptal Edildi</i>", user, mesajid)
        return
    """ Site Değiştir """
    if call.callback_query.data.startswith("site"):
        ss = str(call.callback_query.data.split("-")[1])
        collection.update_one({"_id": user}, {"$set": {"site": ss}})
        
        bot.edit_message_text("Site Kaydedildi!\n\nAPI adresinizi seçtiğiniz siteye göre değiştirmeyi unutmayın.", user, mesajid)
        call.callback_query.answer(call.callback_query.id, "Site Kaydedildi!")
    """ Alternatif """
    if call.callback_query.data.startswith("sistem"):
        context.user_data['sss'] = str(call.callback_query.data.split("-")[1])
        call.callback_query.answer(call.callback_query.id, "✅ Site Kaydedildi!")
        bot.edit_message_text("Alternatif olarak kullanmak istediğiniz siteyi seçin.", user, mesajid)
        bot.edit_message_reply_markup(chat_id=chat, message_id=mesajid, reply_markup=altsitemarkup("asite"))
    if call.callback_query.data == "okay":
        bot.edit_message_text("""<b>Özel Kaynak Hakkında Bilmeniz Gerekenler</b>\n\n<i>- Sadece bir tane Özel kaynak kullanabilirsiniz.\n- Başkaları da isterse sizin özel kaynağınızı kullanabilir.\n- Kaynağınız @OtoPosterBotLog'da gözükmeyecek.\n- Postlar, diğer kaynaklara göre daha yavaş atılır.\n- Özel kaynağa kısaltılmamış link atmanız gerekiyor. Kısaltılmış linkli post atarsanız bot linki geçmez direkt olarak kısaltılmış linki tekrar kısaltır.</i>""", chat, mesajid)
        bot.edit_message_reply_markup(chat, mesajid, reply_markup=ozelmark())
        return
    if call.callback_query.data == "okayk":
        use_r = 0
        collection.update_one({"_id": user}, {"$set": {"ozel": False}})
        for u in OzelCol.find({"kanal": {"$in": [user]}}):
            
            OzelCol.update_one({"_id": u['_id']}, {"$pull": {"kanal": user}})
        collection.update_one({"_id": user}, {"$pull": {"kaynak": "32"}})
        bot.edit_message_text("Özel Kaynak Kaldırıldı.", chat, mesajid)
        return
    if call.callback_query.data == "logokaldir":
        OzelCol.update_one({"_id": user}, {"$set": {"log": "yok"}})
        call.callback_query.edit_message_text("Botlog Kaldırıldı.")
        return
    if call.callback_query.data == "okaykanal":
        bot.send_message(chat, "Özel kaynağınızda kullanmak istediğiniz kanalları seçin.", reply_markup=okaykanalmark(user))
        return
    if call.callback_query.data.startswith("okayk-"):
        okid = None if OzelCol.find_one({"kanal": {"$in": [user]}}) == None else OzelCol.find_one({"kanal": {"$in": [user]}})["_id"]
        if okid == None:
            call.callback_query.edit_message_text("Butonların kullanım süresi dolmuş lütfen menüden tekrar açın.")
            return
            
        okaykno = int(call.callback_query.data.split("-")[-1])
        try:
            pushedokaykkan = collection.find_one({"_id": user})['kanal'][okaykno]
        except:
            call.callback_query.edit_message_text("Butonların kullanım süresi dolmuş lütfen menüden tekrar açın.")
            return
        if pushedokaykkan in OzelCol.find_one({"_id": okid})['kaynak']:
            OzelCol.update_one({"_id": okid}, {"$pull": {"kaynak": pushedokaykkan}})
            call.callback_query.answer("Kanalınız için Özel Kaynak kapatıldı.")
        else:
            OzelCol.update_one({"_id": okid}, {"$push": {"kaynak": pushedokaykkan}})
            call.callback_query.answer("Kanalınız için Özel Kaynak açıldı.")
        call.callback_query.edit_message_reply_markup(okaykanalmark(user))
        return
    if call.callback_query.data == "yoket":
        kayna_k = OzelCol.find_one({"_id": user})
        if kayna_k.get('kanal', None) == None:
            return
        for xk in kayna_k['kanal']:
            if user != xk:
                try:
                    FloodControl(bot.send_message, *[xk, "Özel kaynağınız sahibi tarafından <b>yok edildi!</b> Bence başka kaynak aramaya başlamalısın."])
                except:
                    pass
        OzelCol.delete_one({"_id": user})
        collection.update_one({"_id": user}, {"$set": {"ozel": False}})
        call.callback_query.edit_message_text("Kaynak, sen de dahil bütün kullanıcılardan silindi. 💣")
        return
    if call.callback_query.data == "eminmisin":
        call.callback_query.edit_message_text("Alttaki düğmeye basarsan, bu kaynağı kullanan herkesi güzel postlarından mahrum ediceksin.", reply_markup=eminmisin())
        return
    """ PAT """
    if call.callback_query.data.startswith("jop"):
        jc = int(call.callback_query.data.split("-")[-1])
        calljob = context.job_queue.get_jobs_by_name(str(user))
        try:
            calljob[jc].schedule_removal()
        except:
            call.callback_query.edit_message_text("Bu post zaten gönderilmiş veya silinmiş.")
            return ConversationHandler.END
        call.callback_query.edit_message_text("Post silindi.")
        return ConversationHandler.END
    if call.callback_query.data == "pzamanla":
        call.callback_query.edit_message_text("Postun gönderilmesini istediğiniz saati gönderin.\n\n<b>Örnek biçim;</b>\n<code>30/03/21 18:30:00</code>")
        return PATZAMAN
    if call.callback_query.data == "simdi": 
        try:
            bot.delete_message(user, mesajid)
        except:
            pass
        patbegeni = collection.find_one({"_id": user})['begeni']
        if len(patbegeni) == 0 and begstate:
            patmarkup = InlineKeyboardMarkup([[]])
        else:
            pbkeyb = []
            pbkc = 0
            for pbeg in patbegeni:
                pbkeyb.append(InlineKeyboardButton(str(pbeg)+" 0", callback_data="begeni-{}".format(pbkc)))
                pbkc += 1
            patmarkup = InlineKeyboardMarkup([pbkeyb])
        try:
            ptip = context.user_data['ptip']
            fid = context.user_data['fid']
            psablon = context.user_data['psablon']
        except:
            call.callback_query.edit_message_text("Bir hata oluştı! Lütfen tekrar deneyin.")
            return
        pukanallar = collection.find_one({"_id": user})['kanal']
        if len(pukanallar) < 2:
            try:
                ppost = SEND_MEDIA_TYPES[ptip](pukanallar[0], fid, caption=psablon, reply_markup=patmarkup)
            except Exception as e:
                logger.error(e)
                bot.send_message(user, "Postunuz gönderilemedi, botu kanaldan çıkarmış olabilirsiniz.", reply_markup=dugme(user))
                return ConversationHandler.END
            if len(patbegeni) > 0 and begstate:
                if ButonCol.find_one({"_id": pukanallar[0]}) == None:
                    ButonCol.insert_one({"_id": pukanallar[0], str(ppost.message_id): [], "begeni": patbegeni})
                else:
                    ButonCol.update_one({"_id": pukanallar[0]}, {"$set": {str(ppost.message_id): [], "begeni": patbegeni}})
            bot.send_message(user, "Postunuz gönderildi.", reply_markup=dugme(user))
            bot.send_message(chat, "Başka post paylaşacak mısınız?", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Evet", callback_data="devam"), InlineKeyboardButton("Hayır", callback_data="del")]]))
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
            context.user_data['zaman']
        except:
            return
        patbegeni = collection.find_one({"_id": user})['begeni']
        if len(patbegeni) == 0 and begstate:
            patmarkup = InlineKeyboardMarkup([[]])
        else:
            pbkeyb = []
            pbkc = 0
            for pbeg in patbegeni:
                pbkeyb.append(InlineKeyboardButton(str(pbeg)+" 0", callback_data="begeni-{}".format(pbkc)))
                pbkc += 1
            patmarkup = InlineKeyboardMarkup([pbkeyb])        
        kanal = collection.find_one({"_id": user})['kanal']
        if context.user_data['zaman'] == "yok":
            if o == -1:
                for kan in kanal:
                    try:
                        pyetkililer = [pxy.user.id for pxy in bot.get_chat_administrators(kan)]
                    except:
                        continue
                    if not user in pyetkililer:
                        bot.send_message(chat, f"{bot.get_chat(kan).title} Bu kanalda yetkili olmadığınız için post gönderilemedi ve kanal silindi.", reply_markup=dugme(user))
                        bot.delete_message(user, mesajid)
                        collection.update_one({"_id": user}, {"$pull": {"kanal": kan}})
                        continue 
                    try:
                        ppost = SEND_MEDIA_TYPES[ptip](kan, fid, caption=psablon, reply_markup=patmarkup)
                    except Exception as e:
                        logger.exception(e)
                        pass
                    else:
                        if len(patbegeni) > 0 and begstate:
                            if ButonCol.find_one({"_id": kan}) == None:
                                ButonCol.insert_one({"_id": kan, str(ppost.message_id): [], "begeni": patbegeni})
                            else:
                                ButonCol.update_one({"_id": kan}, {"$set": {str(ppost.message_id): [], "begeni": patbegeni}})
                bot.edit_message_text("✅<b>Postunuz Tüm Kanallarınıza Gönderildi!</b>", user, mesajid)
                context.user_data.clear()
                mstd = bot.send_message(chat, "Başka post paylaşacak mısınız?", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Evet", callback_data="devam"), InlineKeyboardButton("Hayır", callback_data="del")]]))
                return ConversationHandler.END
            try:
                pyetkililer = [pxy.user.id for pxy in bot.get_chat_administrators(kanal[o])]
            except:
                pyetkililer = []
            if not user in pyetkililer:
                bot.send_message(chat, f"{bot.get_chat(kanal[o]).title} Bu kanalda yetkili olmadığınız için post gönderilemedi ve kanal silindi.", reply_markup=dugme(user))
                bot.delete_message(user, mesajid)
                collection.update_one({"_id": user}, {"$pull": {"kanal": kanal[o]}})
                return ConversationHandler.END
            try:
                ppost = SEND_MEDIA_TYPES[ptip](kanal[o], fid, caption=psablon, reply_markup=patmarkup)
            except Exception as e:
                bot.edit_message_text(f"Postunuz gönderilemedi \n\n{e}", user, mesajid)
                context.user_data.clear()
                return ConversationHandler.END
            if len(patbegeni) > 0 and begstate:
                if ButonCol.find_one({"_id": kanal[o]}) == None:
                    ButonCol.insert_one({"_id": kanal[o], str(ppost.message_id): [], "begeni": patbegeni})
                else:
                    ButonCol.update_one({"_id": kanal[o]}, {"$set": {str(ppost.message_id): [], "begeni": patbegeni}})
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
        return
    """ Şablon """
    if call.callback_query.data == "vsablon":
        if collection.find_one({"_id": user})['sira'] == 1:
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
    if call.callback_query.data.startswith("tsenough"):
        call.callback_query.edit_message_text("Tekrarli Postunuzun kaç saatte bir gönderilmesini istediğiniz saati seçin", reply_markup=tekrarlisaatmark())
        return
    if call.callback_query.data.startswith("tkan+"):
        try:
            context.user_data['tskan']
        except KeyError:
            context.user_data['tskan'] = []
        
        context.user_data['tskan'].append(call.callback_query.data.split("+")[-1])
        call.callback_query.answer("Kanal belirlendi!")
        try:
            call.callback_query.edit_message_reply_markup(tekrarlipostkan(user, context))
        except:
            pass
        return 
    if call.callback_query.data == "tekrarlisil":
        call.callback_query.edit_message_text("Silmek istediğiniz postu seçin.", reply_markup=tekrarlipostsilmark(user, context))
        return
    if call.callback_query.data == "yenitekrarli":
        if len(collection.find_one({"_id": user})['kanal']) == 0:
            call.callback_query.edit_message_text("Tekrarli Post ayarlayabilmek için önce bir kanal kaydetmelisiniz!")
            return
        elif len(collection.find_one({"_id": user})['kanal']) > 1:
            context.user_data['tskan'] = []
            call.callback_query.edit_message_text("Tekrarli Post ayarlamak istediğiniz kanalları seçin.", reply_markup=tekrarlipostkan(user, context))
        else:
            context.user_data["tskan"] = collection.find_one({"_id": user})['kanal'][0]
            call.callback_query.edit_message_text("Tekrarli Postunuzun kaç saatte bir gönderilmesini istediğiniz saati seçin", reply_markup=tekrarlisaatmark())
        return
    if call.callback_query.data.startswith("tssil-"):
        try:
            context.job_queue.get_jobs_by_name(f"ts{user}")[int(call.callback_query.data.split("-")[-1])].schedule_removal()
        except:
            call.callback_query.edit_message_text("Post iptal edilemedi!")
        else:
            call.callback_query.edit_message_text("Postunuz silindi artık paylaşılmayacak")
        return
    """ Panel """
    """ iOS Kontrol """
    if call.callback_query.data.startswith("iosk-"):
        call.callback_query.edit_message_text("<code>Kontrol ediliyor...</code>")
        ioskanal = collection.find_one({"_id": user})['kanal'][int(call.callback_query.data.split("-")[-1])]
        ioskanlink = bot.get_chat(ioskanal)
        if ioskanlink.invite_link == None:
            call.callback_query.edit_message_text("iOS Ban kontrol edebilmem için bota kanalınızda <b>Üye Ekleme</b> yetkisi vermelisiniz!")
            return
        bot.send_message(eklenti, f'ios*{user}*{ioskanlink.invite_link}')
        context.user_data['iosmsgid'] = mesajid
        return
    call.callback_query.answer(f"Yanıt yok - {call.callback_query.data}")

def tekrarlisaatayarlacall(call, context):
    context.user_data['tsaat'] = int(call.callback_query.data.split("-")[-1])
    try:
        call.effective_message.delete()
    except:
        pass
    bot.send_message(call.effective_chat.id, "Tekrarlı postunuza bir başlık verin.\n\nÖrnek;\nJigolo afiş, IVR afiş", reply_markup=imark())
    call.callback_query.answer("Saat belirlendi!")
    return TSBASLIK

def tsmodcall(call, context):
    user = call.effective_user.id
    chat = call.effective_chat.id
    query = call.callback_query
    try:
        call.effective_message.delete()
    except:
        pass
    mod = query.data.split("-")[1] + "-0"
    context.user_data["tspostdict"]["mod"] = mod
    tetik = datetime.datetime.now(pytz.timezone('Europe/Istanbul')) + datetime.timedelta(hours = int(context.user_data['tsaat']))
    context.user_data["tspostdict"]["tetik"] = tetik.strftime("%Y-%m-%d %H:%M:%S")
    firstmod = 3600*int(context.user_data["tsaat"])-3600 if int(context.user_data["tsaat"]) != 1 else 3600
    context.job_queue.run_repeating(tekrarlipostjob, first=firstmod, interval=3600*int(context.user_data['tsaat']), name=f"ts{user}", context=context.user_data["tspostdict"])
    context.user_data.clear()
    bot.send_message(chat, "Postlarınız başarıyla ayarlandı!", reply_markup=dugme(user))
    return ConversationHandler.END


def advcall(call, context):
    user = call.effective_user.id
    chat = call.effective_chat.id
    advdat = collection.find_one({"_id": user})
    query = call.callback_query
    if query.data == "advsistem":
        if advdat["altsite"] == "sirali":
            collection.update_one({"_id": user}, {"$set": {"altsite": "tpil"}})
            query.answer("Alternatif sisteminiz Tek Post İki Link olarak değiştirldi.")
        else:
            query.answer("Alternatif sisteminiz Sıralı olarak değiştirldi.")
            collection.update_one({"_id": user}, {"$set": {"altsite": "sirali"}})
        query.edit_message_reply_markup(advaltmark(user))
    elif query.data == "advekle":
        query.answer("Site seçin.")
        context.user_data["sss"] = "ekle"
        bot.send_message(chat, "Yeni eklemem istediğiniz siteyi seçin.", reply_markup=altsitemarkup("asite"))
    elif query.data.startswith("advapi-"):
        query.answer(f"API Adresiniz:\n {advdat['altapi'][int(query.data.split('-')[-1])]['api']}", show_alert=True)
    elif query.data.startswith("advsil-"):
        collection.update_one({"_id": user}, {"$pull": {"altapi": advdat['altapi'][int(query.data.split("-")[-1])]}})
        query.answer("API Kaldırıldı!")
        query.edit_message_reply_markup(advaltmark(user))
    elif query.data == "advbilgi":
        query.answer("Sıralı:\nKaydettiğiniz tüm apileri sırayla kullanır.\n\nTek Post İki Link:\nKaydettiğiniz tüm apileri birincil apiniz ile birlikte tek postta iki link olarak sırayla paylaşır.", show_alert=True)
    

def begeniislemcall(call, context):
    user = call.effective_user.id
    chat = call.effective_chat.id
    mesajid = call.effective_message.message_id    
    pushed = int(call.callback_query.data.split("-")[-1])
    if not begstate:
        call.callback_query.answer("Üzgünüm bu özellik geçici olarak devredışı bırakılmıştır.")
        return
    for i in range(10):
        begkeyb = []
        mrkpc = 0
        if not user in ButonCol.find_one({"_id": str(chat)})[str(mesajid)]:
            ButonCol.update_one({"_id": str(chat)}, {"$push": {str(mesajid): user}})
        else:
            try:
                call.callback_query.answer("Butonları bir kez kullanabilirsiniz")
            except:
                pass
            return
        for beg in ButonCol.find_one({"_id": str(chat)})['begeni']:
            try:
                butsayi = int(call.effective_message.reply_markup.inline_keyboard[0][mrkpc].text.split()[-1])
            except:
                butsayi = 0
            if mrkpc == pushed:
                begkeyb.append(InlineKeyboardButton(str(beg)+" "+str(butsayi+1), callback_data="begeni-{}".format(mrkpc)))
            else:
                begkeyb.append(InlineKeyboardButton(str(beg)+" "+str(butsayi), callback_data="begeni-{}".format(mrkpc)))
            mrkpc += 1
        try:
            call.callback_query.answer(str(call.effective_message.reply_markup.inline_keyboard[0][pushed].text.split()[-2]))
        except:
            pass
        try:
            call.callback_query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([begkeyb]))
        except RetryAfter as rtt:
            time.sleep(rtt.retry_after+1)
            try:
                call.callback_query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([begkeyb]))
            except:
                pass
            else:
                break
        except:
            pass
        else:
            pass
