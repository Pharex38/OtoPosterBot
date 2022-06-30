from . import *
from .markups import *
from .anafonks import *
from .misc import *
from .komutlar import *

async def sabloncall(call, context):
    bot = context.bot
    user = call.effective_user.id
    chat = call.effective_chat.id
    mesajid = call.effective_message.message_id
    try:
        await bot.delete_message(chat, mesajid)
    except:
        pass
    if collection.find_one({"_id": user}) == None:
        await call.callback_query.edit_message_text(text="<b>Önce bir API kaydedin!</b>")
        return
    if collection.find_one({"_id": user})['sira'] == 1 or collection.find_one({"_id": user})['altsite'] == "tpil":
        msz = await bot.send_message(chat, "<i>Oluşturduğunuz şablonda</i> <b>{aciklama}, {alink}</b> ve <b>{link}</b> <i>kelimelerinin bulunduğundan emin olun yoksa şablon çalışmaz</i>", reply_markup=imark())
    else:
        msz = await bot.send_message(chat, "<i>Oluşturduğunuz şablonda</i> <b>{aciklama}</b> ve <b>{link}</b> <i>kelimelerinin bulunduğundan emin olun yoksa şablon çalışmaz</i>", reply_markup=imark())
    return SABLONA

async def altcall(call, context):
    bot = context.bot
    user = call.effective_user.id
    chat = call.effective_chat.id
    mesajid = call.effective_message.message_id
    smesaj = str(call.callback_query.data.split("-")[1])
    context.user_data['asite'] = smesaj
    await call.callback_query.answer(call.callback_query.id, "✅ Site Kaydedildi!")
    await bot.edit_message_text("✅ Alternatif site kaydedildi.", user, mesajid)
    await bot.send_message(chat, "📝 Alternatif API adresinizi gönderin.", reply_markup=imark())
    return ALTAPI

async def ayarlarcall(call, context):
    bot = context.bot
    user = call.effective_user.id
    chat = call.effective_chat.id
    
async def kaynakkontrolcall(call, context):
    bot = context.bot
    chat = call.effective_chat.id
    user = call.effective_user.id
    query = call.callback_query
    callkd = query.data.split("-")[1]
    query.answer(".")
    if callkd == "evet":
        await query.edit_message_text(f"<b>Aşağıdaki kurallaru onaylıyor musun?</b>\n\n{collection.find_one({'_id': 0})['kurallar']}\n\nBoşu boşuna istek gönderenleri bottan banlarım!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Okudum, onaylıyorum.", callback_data="kont-devam1")], [InlineKeyboardButton("Vazgeçtim", callback_data="aiptal")]]))
    elif callkd == "devam1":
        await query.edit_message_text("İçeriğiniz nedir?", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("+18", callback_data="kont-devam2-+18")], [InlineKeyboardButton("Arşiv", callback_data="kont-devam2-arsiv")], [InlineKeyboardButton("Vazgeçtim", callback_data="aiptal")]]))
    elif callkd == "devam2":
        context.user_data["kont-icerik"] = query.data.split("-")[2]
        if query.data.split("-")[2] == "+18":
            await query.edit_message_text("Yerli/Yabanci ?", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🇹🇷", callback_data="kont-devam3-tr")], [InlineKeyboardButton("🇬🇧", callback_data="kont-devam3-yb")], [InlineKeyboardButton("Vazgeçtim", callback_data="aiptal")]]))
        else:
            context.user_data['kont-tur'] = None
            pass
    elif callkd == "devam3":
        context.user_data['kont-tur'] = query.data.split("-")[2]
        await query.edit_message_text("Kullanacağınız depolama servisi nedir?", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Yandex, Cloud vs.", callback_data="kont-son-cloud")], [InlineKeyboardButton("Streamtape veya Streamtape benzeri", callback_data="kont-son-tape")]]))
    elif callkd == "son":
        if context.user_data['kont-icerik'] == "+18":
            collection.update_one({"_id": 0}, {"$push": {"kont": {"user": user, "icerik": context.user_data['kont-icerik'], "tur": context.user_data['kont-tur']}}})
        elif context.user_data['kont-icerik'] == "arsiv":
            collection.update_one({"_id": 0}, {"$push": {"kont": {"user": user, "icerik": context.user_data['kont-icerik'], "tur": None}}})
        await bot.send_message(chat, "İsteğiniz gönderildi!")

async def begenicall(call, context):
    bot = context.bot
    user = call.effective_user.id
    chat = call.effective_chat.id
    if len(collection.find_one({"_id": user})['kanal']) == 0:
        await bot.send_message(chat, "Beğeni butonu ayarlayabilmek için önce bir kanal kaydetmelisiniz!")
        return
    await bot.send_message(chat, "Ayarlamak istediğin buton emojilerini örnekteki gibi gönderin.\n\nÖrnek;\n<code>❤️/⛔️/🥰</code>", reply_markup=imark())
    return BEGENI

async def kaynakcall(call, context):
    bot = context.bot
    user = call.effective_user.id
    chat = call.effective_chat.id
    kys = int(call.callback_query.data.split("-")[1])
    kkanil = int(call.callback_query.data.split("-")[2])
    kkul = collection.find_one({"_id": user})
    if kkul == None:
        await call.callback_query.edit_message_text(text="<b>Önce bir API kaydedin!</b>")
        return
    callkaynak = KaynakCol.find_one({"sahip": kys})
    try:
        kkul['kanal'][kkanil]
    except:
        await call.callback_query.edit_message_text("Menü eski kaldığı için kapatıldı.")
        return
    if callkaynak == None:
        await call.callback_query.edit_message_text("Menü eski kaldığı için kapatıldı.")
        return
    if user in callkaynak['kaynak'] and kkul['kanal'][kkanil] in callkaynak['kanal']:
        KaynakCol.update_one({"sahip": kys}, {"$pull": {"kanal": kkul['kanal'][kkanil]}})
        try:
            durak = context.bot_data['durak']
        except KeyError:
            durak = False
        if durak and user in collection.find_one({"_id": 0})['cekilis'] and kys == int(context.bot_data['sahip']):
            await bot.send_message(chat, "Çekiliş kaynağını kullanmayı bıraktığınız için çekilişten atıldınız!")
            collection.update_one({"_id": 0}, {"$pull": {"cekilis": user}})
        for kop in kkul['kanal']:
            if kop in callkaynak['kanal']:
                await call.callback_query.answer(text="❌ Kaynak Kaldırıldı")
                return
        KaynakCol.update_one({"sahip": kys}, {"$pull": {"kaynak": user}})
        await call.callback_query.answer(text="❌ Kaynak Kaldırıldı")
    else:
        if not kkul['kanal'][kkanil] in callkaynak['kanal']:
            KaynakCol.update_one({"sahip": kys}, {"$push": {"kanal": kkul['kanal'][kkanil]}})
        if not user in callkaynak['kaynak']:
            KaynakCol.update_one({"sahip": kys}, {"$push": {"kaynak": user}})
        await call.callback_query.answer(text="✅ Kaynak Eklendi")
    try:
        await call.callback_query.edit_message_reply_markup((await kaynakmark(user, kkanil)))
    except:
        pass

async def ozellogcall(call, context):
    bot = context.bot
    user = call.effective_user.id
    chat = call.effective_chat.id
    mesajid = call.effective_message.message_id
    await bot.delete_message(chat, mesajid)
    await bot.send_message(chat, "📝 Oluşturduğunuz Log kanalından bir gönderi iletin.", reply_markup=imark())
    return OZELBOTLOG

async def ozelkaynakcall(call, context):
    bot = context.bot
    user = call.effective_user.id
    chat = call.effective_chat.id
    mesajid = call.effective_message.message_id
    if collection.find_one({"_id": user}) == None:
        await call.callback_query.edit_message_text(text="<b>Önce bir API kaydedin!</b>")
        return
    if "31" in collection.find_one({"_id": user})['kaynak']:
        await bot.send_message(user, "<b>Önce Sfs Modunu Kapatın!</b>")
        return ConversationHandler.END
    try:
        await bot.delete_message(chat, mesajid)
    except:
        pass
    await bot.send_message(chat, """<b>Yapmanız Gerekenler</b>
<i>
1 - Kaynak yapacağınız kanal oluşturun.
2 - Oluşturduğunuz kanaldan bota bir mesaj iletin.</i>""", reply_markup=imark())
    return OZELKAYNAK

async def patzamancall(call, context):
    bot = context.bot
    user = call.effective_user.id
    chat = call.effective_chat.id
    mesajid = call.callback_query.message.message_id

async def postzamancall(call, context):
    bot = context.bot
    user = call.effective_user.id
    chat = call.effective_chat.id
    mesajid = call.callback_query.message.message_id
    await bot.delete_message(chat, mesajid)
    await bot.send_message(chat, "Postlarınız 00:00'dan başlayarak sırasıyla hangi saatlerde gönderilmesini istediğiniz saatleri altalta yazın ve gönderin.\n\nÖrnek;\n00:00\n01:00\n02:00\n03:00\n...", reply_markup=imark())
    return POSTZAMAN

async def cekiliscall(call, context):
    bot = context.bot
    user = call.effective_user.id
    chat = call.effective_chat.id
    mesajid = call.callback_query.message.message_id
    cek_dat = collection.find_one({"_id": user})
    if user in collection.find_one({"_id": 0})['cekilis']:
        await call.callback_query.answer(show_alert=True, text="Çekilişe zaten katılmışsınız, geriye kazanmak kaldı!")
        return
    try:
        durak = context.bot_data['durak']
    except KeyError:
        durak = False
    if context.bot_data['durak']:
        await call.callback_query.answer(show_alert=True, text="Çekilişe katılılım süresi dolmuş, geç kaldınız :(")
        return
    if cek_dat == None:
        await call.callback_query.answer(show_alert=True, text="Çekilişe katılabilmek için en az bir kanalınız olmalı!")
        return
    if len(cek_dat['kanal']) == 0:
        await call.callback_query.answer(show_alert=True, text="Çekilişe katılabilmek için en az bir kanalınız olmalı!")
        return
    cek_k_isim = await bot.get_chat(KaynakCol.find_one({'sahip': int(context.bot_data['sahip'])})['_id']).title
    if not user in KaynakCol.find_one({"sahip": int(context.bot_data['sahip'])})['kaynak']:
        await call.callback_query.answer(show_alert=True, text=f"Çekilişe katılabilmek için en az bir kanalınız {cek_k_isim} kaynağını kullanıyor olmalı.")
        return
    for cekkan in cek_dat['kanal']:
        if cekkan in KaynakCol.find_one({"sahip": int(context.bot_data['sahip'])})['kanal']:
            try:
                cekkanabone = await bot.get_chat_member_count(cekkan)
            except:
                continue
            if cekkanabone > 1001:
                try:
                    collection.update_one({"_id": 0}, {"$push": {"cekilis": user}})
                except:
                    await call.callback_query.answer(show_alert=True, text="Bir sorun oluştu.")
                    return
                else:
                    await call.callback_query.answer("Çekilişe katıldınız.")
                    cekilis_text = context.bot_data['cekilis'].format(len(collection.find_one({"_id": 0})['cekilis']))
                    await call.callback_query.edit_message_text(cekilis_text, reply_markup=cekilismark())
                    return
    await call.callback_query.answer(show_alert=True, text=f"En az 1000 abone olan bir kanalınız {cek_k_isim} kaynağını kullanmak zorunda.")

async def devampatcall(call, context):
    bot = context.bot
    chat = call.effective_chat.id
    try:
        await call.effective_message.delete()
    except:
        pass
    await bot.send_message(chat, "Paylaşmamı istediğin hazır postu ilet.", reply_markup=imark())
    return PATPOST

async def panelcall(call, context):
    bot = context.bot
    query = call.callback_query
    chat = call.effective_chat.id
    user = call.effective_user.id
    query.answer("Lütfen bekleyin...")
    if query.data == "panelzaman":
        await bot.send_message(call.effective_chat.id, "Ayarlamak istediğiniz mesajı gönderin.", reply_markup=imark())
        return PANELZAMAN
    elif query.data == "panelkural":
        await bot.send_message(chat, str(collection.find_one({"_id": 0})['kurallar']))
    elif query.data.startswith("pau"):
        kaynak_users = KaynakCol.find_one({"sahip": user})['kaynak'].remove(sahip) if sahip in KaynakCol.find_one({"sahip": user})['kaynak'] else KaynakCol.find_one({"sahip": user})['kaynak']
        panel_user_text = f"<b>Kaynağınızı Kullanan Kullanıcılar;</b>\n\n"
        que = int(query.data.split("-")[-1]) if query.data.split("-")[-1] != "bul" else None
        if que == None:
            await bot.send_message(chat, "Bulmak istediğiniz kullanıcının ID'sini veya kullanıcıdan herhangi bir mesaj iletin.", reply_markup=imark())
            return PANELBUL
        for paucount in range(que-10,que):
            try:
                if kaynak_users[paucount] == sahip:
                    continue
                panel_user_text += str(paucount) + ". " + mention_html(kaynak_users[paucount], await bot.get_chat(kaynak_users[paucount]).first_name) + "\n"
            except IndexError:
                paumark = [[InlineKeyboardButton("🔍 Kullanıcı Bul", callback_data="pau-bul")], [InlineKeyboardButton("⏪Önceki Sayfa ", callback_data="pau-{}".format(que-10))]]
                break
        else:
            paumark = [[InlineKeyboardButton("🔍 Kullanıcı Bul", callback_data="pau-bul")], [InlineKeyboardButton("⏪Önceki Sayfa ", callback_data="pau-{}".format(que-10)), InlineKeyboardButton("Sonraki Sayfa ⏩", callback_data="pau-{}".format(que+10))] if len(kaynak_users) > que else []]
        if que == len(kaynak_users):
            paumark = [[InlineKeyboardButton("🔍 Kullanıcı Bul", callback_data="pau-bul")], [InlineKeyboardButton("⏪Önceki Sayfa ", callback_data="pau-{}".format(que-10))]]
        if que == 10:
            paumark = [[InlineKeyboardButton("🔍 Kullanıcı Bul", callback_data="pau-bul")], [InlineKeyboardButton("Sonraki Sayfa ⏩", callback_data="pau-{}".format(que+10))] if len(kaynak_users) > que else []]
        await query.edit_message_text(panel_user_text, reply_markup=InlineKeyboardMarkup(paumark))
    elif query.data == "panelkullanici":
        kaynak_users = KaynakCol.find_one({"sahip": user})['kaynak']
        panel_user_text = f"<b>Kaynağınızı Kullanan Kullanıcılar;</b>\n\n"
        for paucount in range(11):
            try:
                panel_user_text += str(paucount) + ". " + mention_html(kaynak_users[paucount], await bot.get_chat(kaynak_users[paucount]).first_name) + "\n"
            except IndexError:
                paumark = [[InlineKeyboardButton("🔍 Kullanıcı Bul", callback_data="pau-bul")]]
                break
        else:
            paumark = [[InlineKeyboardButton("🔍 Kullanıcı Bul", callback_data="pau-bul")], [InlineKeyboardButton("Sonraki Sayfa ⏩", callback_data="pau-20")] if len(kaynak_users) > 10 else []]
        await bot.send_message(chat, panel_user_text, reply_markup=InlineKeyboardMarkup(paumark))
    elif query.data.startswith("pak-"):
        kaynak_users = KaynakCol.find_one({"sahip": user})['kanal']
        panel_user_text = f"<b>Kaynağınızı Kullanan Kanallar;</b>\n\n"
        que = int(query.data.split("-")[-1]) if query.data.split("-")[-1] != "bul" else None
        if que == None:
            await bot.send_message(chat, "Bulmak istediğiniz Kanalın ID'sini veya Kanaldan herhangi bir mesaj iletin.", reply_markup=imark())
            return PANELBUL
        for pakcount in range(que-10,que):
            try:
                panel_user_text += str(pakcount) + ". " + (await kan_mention_html(kaynak_users[pakcount])) + "\n"
            except IndexError:
                pakmark = [[InlineKeyboardButton("🔍 Kanal Bul", callback_data="pak-bul")], [InlineKeyboardButton("⏪Önceki Sayfa ", callback_data="pak-{}".format(que-10))]]
                break
        else:
            pakmark = [[InlineKeyboardButton("🔍 Kanal Bul", callback_data="pak-bul")], [InlineKeyboardButton("⏪Önceki Sayfa ", callback_data="pak-{}".format(que-10)), InlineKeyboardButton("Sonraki Sayfa ⏩", callback_data="pak-{}".format(que+10))] if len(kaynak_users) > que else []]
        if que == len(kaynak_users):
            pakmark = [[InlineKeyboardButton("🔍 Kanal Bul", callback_data="pak-bul")], [InlineKeyboardButton("⏪Önceki Sayfa ", callback_data="pak-{}".format(que-10))]]
        if que == 10:
            pakmark = [[InlineKeyboardButton("🔍 Kanal Bul", callback_data="pak-bul")], [InlineKeyboardButton("Sonraki Sayfa ⏩", callback_data="pak-{}".format(que+10))] if len(kaynak_users) > que else []]
        await query.edit_message_text(panel_user_text, reply_markup=InlineKeyboardMarkup(pakmark))
    elif query.data == "panelkanal":
        kaynak_users = KaynakCol.find_one({"sahip": user})['kanal']
        panel_user_text = f"<b>Kaynağınızı Kullanan Kanallar;</b>\n\n"
        for pakcount in range(11):
            try:
                panel_user_text += str(pakcount) + ". " + (await kan_mention_html(kaynak_users[pakcount])) + "\n"
            except IndexError:
                pakmark = [[InlineKeyboardButton("🔍 Kanal Bul", callback_data="pak-bul")]]
                break
        else:
            pakmark = [[InlineKeyboardButton("🔍 Kanal Bul", callback_data="pak-bul")], [InlineKeyboardButton("Sonraki Sayfa ⏩", callback_data="pak-20")] if len(kaynak_users) > 10 else []]
        await bot.send_message(chat, panel_user_text, reply_markup=InlineKeyboardMarkup(pakmark))
    elif query.data == "panelguncellemeler":
        gunc_text = "<b>Bottaki Son Güncellemeler;</b>\n\n<i>• "
        gunc_text += "\n• ".join(collection.find_one({"_id": 0})['guncelleme'][::-1][:5])
        await bot.send_message(chat, gunc_text+"</i>")
    else:
        query.answer("Yanıt bulunamadı!")

async def callback_query(call, context):
    bot = context.bot
    user = call.effective_user.id
    chat = call.effective_chat.id
    mesajid = call.callback_query.message.message_id
    """ PIN """
    if call.callback_query.data.startswith("pin-"):
        pinno = int(call.callback_query.data.split("-")[-1])
        try:
            pushedpinkan = collection.find_one({"_id": user})['kanal'][pinno]
        except:
            await call.callback_query.edit_message_text("Butonların kullanım süresi dolmuş lütfen menüden tekrar açın.")
            return
        if pushedpinkan in collection.find_one({"_id": user})['pin']:
            collection.update_one({"_id": user}, {"$pull": {"pin": pushedpinkan}})
            await call.callback_query.answer("Kanalınız için Pin modu kapatıldı.")
        else:
            collection.update_one({"_id": user}, {"$push": {"pin": pushedpinkan}})
            await call.callback_query.answer("Kanalınız için Pin modu açıldı.")
        try:
            await call.callback_query.edit_message_reply_markup((await pinmark(user)))
        except:
            pass
        return 
    """ SFS Modu """
    if call.callback_query.data.startswith("sfs"):
        sfsno = int(call.callback_query.data.split("-")[-1])
        try:
            pushedsfskan = collection.find_one({"_id": user})['kanal'][sfsno]
        except:
            await call.callback_query.edit_message_text("Butonların kullanım süresi dolmuş lütfen menüden tekrar açın.")
            return
        if pushedsfskan in collection.find_one({"_id": user})['eski']:
            collection.update_one({"_id": user}, {"$pull": {"eski": pushedsfskan}})
            await call.callback_query.answer("Kanalınız için SFS modu kapatıldı.")
        else:
            collection.update_one({"_id": user}, {"$push": {"eski": pushedsfskan}})
            await call.callback_query.answer("Kanalınız SFS moduna alındı.")
        try:
            await call.callback_query.edit_message_reply_markup((await sfsmark(user)))
        except:
            pass
    """ İcerik """
    if call.callback_query.data.startswith("icerik"):
        icerikno = int(call.callback_query.data.split("-")[-2])
        pushedicerikkan = collection.find_one({"_id": user})['kanal'][icerikno]
        if pushedicerikkan in collection.find_one({"_id": user})['icerik']:
            collection.update_one({"_id": user}, {"$pull": {"icerik": pushedicerikkan}})
        else:
            collection.update_one({"_id": user}, {"$push": {"icerik": pushedicerikkan}})
        await call.callback_query.answer("Kanalınızın içeriği değiştirildi.")
        try:
            if call.callback_query.data.split("-")[-1] == "k":
                await call.callback_query.edit_message_reply_markup((await kaynakmark(user, icerikno)))
            else:
                await call.callback_query.edit_message_reply_markup((await icerikmark(user)))
        except:
            pass
    if call.callback_query.data.startswith("ozicerik-"):
        if call.callback_query.data.split("-")[-1] == "arsiv":
            icc = "+18"
        else:
            icc = "arsiv"
        OzelCol.update_one({"_id": user}, {"$set": {"icerik": icc}})
        await bot.edit_message_reply_markup(chat_id=chat, message_id=mesajid, reply_markup=ozelkaynakmark(user, 0))
        await call.callback_query.answer("Tür değiştirildi")
    """ İptal """
    if call.callback_query.data == "del":
        try:
            await call.effective_message.delete()
        except:
            pass
    if call.callback_query.data == "dsil":
        collection.delete_one({"_id": user})
        try:
            await call.callback_query.answer("💔")
            await call.callback_query.edit_message_text("💔")
        except:
            pass
        await bot.send_message(chat, "Tüm bilgileriniz silindi.", reply_markup=dagme())
    if call.callback_query.data == "akaldır":
        collection.update_one({"_id": user}, {"$set": {"altsite": "None", "altapi": "None", "sira": 0, "sablon": "1"}})
        await bot.edit_message_text("⛔ Alternatif Kaldırıldı.", user, mesajid)
        await call.callback_query.answer("⛔ Alternatif Kaldırıldı.")
    if call.callback_query.data == "aiptal":
        await bot.edit_message_text("<i>Menü kapatıldı.</i>", user, mesajid)
        return
    if call.callback_query.data == "iptal":
        await bot.edit_message_text("<i>İptal Edildi</i>", user, mesajid)
        return
    """ Kanal Sil """
    if call.callback_query.data.startswith("sil"):
        kul = collection.find_one({"_id": user})
        s = int(call.callback_query.data.split("-")[1])
        collection.update_one({"_id": user}, {"$pull": {"kanal": kul['kanal'][s], "eski": kul['kanal'][s], "icerik": kul['kanal'][s]}})
        await bot.edit_message_text("Kanalınız Silindi!", user, mesajid)
        await call.callback_query.answer(call.callback_query.id, "Kanalınız Silindi!")
        await bot.send_message(blog, kansillog.format(user=user, kan=kul['kanal'][s][3:], membersayi=(await bot.get_chat_member_count(int(kul['kanal'][s])))))
    """ Site Değiştir """
    if call.callback_query.data.startswith("site"):
        ss = str(call.callback_query.data.split("-")[1])
        collection.update_one({"_id": user}, {"$set": {"site": ss}})
        await bot.edit_message_text("Site Kaydedildi!\n\nAPI adresinizi seçtiğiniz siteye göre değiştirmeyi unutmayın.", user, mesajid)
        await call.callback_query.answer(call.callback_query.id, "Site Kaydedildi!")
    """ Alternatif """
    if call.callback_query.data.startswith("sistem"):
        context.user_data['sss'] = str(call.callback_query.data.split("-")[1])
        await call.callback_query.answer(call.callback_query.id, "✅ Site Kaydedildi!")
        await bot.edit_message_text("Alternatif olarak kullanmak istediğiniz siteyi seçin.", user, mesajid)
        await bot.edit_message_reply_markup(chat_id=chat, message_id=mesajid, reply_markup=altsitemarkup("asite"))
    """ Kaynak """
    if call.callback_query.data == "ozayar":
        kaynakmsg = call.effective_message
        kynskm = collection.find_one({"_id": user})['kanal'][0]
        
        for m in OzelCol.find({}):
            if user in m['kanal']:
                try:
                    ozel_kaynak_bilgi = await bot.get_chat(m['okaynak'])
                except:
                    kaynakmsg.edit_text("Botu kaynak kanalınızdan çıkarttığınız için post atılmayacak.", reply_markup=ozelkaynakmark(user, 0))
                    return
                kullanan_sayisi = len(m['kanal'])
                break
        refsahip = "yok"
        for ox in OzelCol.find({}):
            if user in ox['kanal']:
                refsahip = ox["_id"]
                break
        if refsahip == "yok":
            collection.update_one({"_id": user}, {"$set": {"ozel": False}})
            collection.update_one({"_id": user}, {"$pull": {"kaynak": "32"}})
            kaynakmsg.edit_text("Özel kaynağınız silinmiş!")
            return
        ref_link = create_deep_linked_url(context.bot.username, str(refsahip))
        try:
            kaynakmsg.edit_text("""<b>Sadece bir tane Özel Kaynak kullanabilirsiniz.</b>\n\n      <i>Özel Kaynağınız:</i><b> <a href="{}">{}</a>\n</b>      <i>Bu Kaynağı Toplam </i><code>{}</code> <i>Kişi Kullanıyor.</i>\n\n<b>Kaynak Referans Linki;</b>\n<code>{}</code>\n<i>Bu link ile botu başlatan herkes otomatik olarak sizin kaynağınıza bağlanacak.</i>""".format(ozel_kaynak_bilgi.invite_link, ozel_kaynak_bilgi.title, kullanan_sayisi, ref_link), reply_markup=ozelkaynakmark(user, 0))
        except:
            pass
        return
    if call.callback_query.data == "anakay":
        kaynakmsg = call.effective_message
        kynskm = collection.find_one({"_id": user})['kanal'][0]
        try:
            kcisim = (await bot.get_chat(kynskm)).title
        except:
            kcisim = "Kanalınıza ulaşılamadı!"
        kaynakmsg.edit_text(f"""<b> >>>    {kcisim}\n\nKanalınızda kullanmak istediğiniz kaynak kanalını seçin.</b>""", reply_markup=kaynakmark(user, 0))
        return
    if call.callback_query.data.startswith("zaman"):
        dgr = int(call.callback_query.data.split("-")[1])
        try:
            saatalert = KaynakCol.find_one({"sahip": dgr})['zaman']
        except:
            saatalert = "Kaynak silinmiş."
        await call.callback_query.answer(show_alert=True, text=saatalert)
        return
    if call.callback_query.data == "okay":
        await bot.edit_message_text("""<b>Özel Kaynak Hakkında Bilmeniz Gerekenler</b>\n\n<i>- Sadece bir tane Özel kaynak kullanabilirsiniz.\n- Başkaları da isterse sizin özel kaynağınızı kullanabilir.\n- Kaynağınız @OtoPosterBotLog'da gözükmeyecek.\n- Postlar, diğer kaynaklara göre daha yavaş atılır.\n- Özel kaynağa kısaltılmamış link atmanız gerekiyor. Kısaltılmış linkli post atarsanız bot linki geçmez direkt olarak kısaltılmış linki tekrar kısaltır.</i>""", chat, mesajid)
        await bot.edit_message_reply_markup(chat, mesajid, reply_markup=ozelmark())
        return
    if call.callback_query.data == "okayk":
        use_r = 0
        collection.update_one({"_id": user}, {"$set": {"ozel": False}})
        for u in OzelCol.find({"kanal": {"$in": [user]}}):
            
            OzelCol.update_one({"_id": u['_id']}, {"$pull": {"kanal": user}})
        collection.update_one({"_id": user}, {"$pull": {"kaynak": "32"}})
        await bot.edit_message_text("Özel Kaynak Kaldırıldı.", chat, mesajid)
        return
    if call.callback_query.data == "logokaldir":
        OzelCol.update_one({"_id": user}, {"$set": {"log": "yok"}})
        await call.callback_query.edit_message_text("Botlog Kaldırıldı.")
        return
    if call.callback_query.data == "okaykanal":
        await bot.send_message(chat, "Özel kaynağınızda kullanmak istediğiniz kanalları seçin.", reply_markup=(await okaykanalmark(user)))
        return
    if call.callback_query.data.startswith("okayk-"):
        okid = None if OzelCol.find_one({"kanal": {"$in": [user]}}) == None else OzelCol.find_one({"kanal": {"$in": [user]}})["_id"]
        if okid == None:
            await call.callback_query.edit_message_text("Butonların kullanım süresi dolmuş lütfen menüden tekrar açın.")
            return
            
        okaykno = int(call.callback_query.data.split("-")[-1])
        try:
            pushedokaykkan = collection.find_one({"_id": user})['kanal'][okaykno]
        except:
            await call.callback_query.edit_message_text("Butonların kullanım süresi dolmuş lütfen menüden tekrar açın.")
            return
        if pushedokaykkan in OzelCol.find_one({"_id": okid})['kaynak']:
            OzelCol.update_one({"_id": okid}, {"$pull": {"kaynak": pushedokaykkan}})
            await call.callback_query.answer("Kanalınız için Özel Kaynak kapatıldı.")
        else:
            OzelCol.update_one({"_id": okid}, {"$push": {"kaynak": pushedokaykkan}})
            await call.callback_query.answer("Kanalınız için Özel Kaynak açıldı.")
        await call.callback_query.edit_message_reply_markup((await okaykanalmark(user)))
        return
    if call.callback_query.data == "yoket":
        kayna_k = OzelCol.find_one({"_id": user})
        for xk in kayna_k['kanal']:
            if user != xk:
                try:
                    FloodControl(await bot.send_message, *[xk, "Özel kaynağınız sahibi tarafından <b>yok edildi!</b> Bence başka kaynak aramaya başlamalısın."])
                except:
                    pass
        OzelCol.delete_one({"_id": user})
        collection.update_one({"_id": user}, {"$set": {"ozel": False}})
        await call.callback_query.edit_message_text("Kaynak, sen de dahil bütün kullanıcılardan silindi. 💣")
        return
    if call.callback_query.data == "eminmisin":
        await call.callback_query.edit_message_text("Alttaki düğmeye basarsan, bu kaynağı kullanan herkesi güzel postlarından mahrum ediceksin.", reply_markup=eminmisin())
        return
    if call.callback_query.data.startswith("sagyan"):
        try:
            sgynknl = collection.find_one({"_id": user})['kanal'][int(call.callback_query.data.split("-")[-1])+1]
        except Exception as e:
            await bot.edit_message_text("<i>İptal Edildi</i>", user, mesajid)
            logger.error(e)
            return
        try:
            sgyisim = await bot.get_chat(sgynknl).title
        except:
            sgyisim = "Kanalınıza ulaşılamadı!"
        await call.callback_query.answer(sgyisim)
        try:
            await call.callback_query.edit_message_text(f"<b> >>>    {sgyisim}\n\nKanalınızda kullanmak istediğiniz kaynak kanalını seçin.</b>", reply_markup=kaynakmark(user, int(call.callback_query.data.split("-")[-1])+1))
        except Exception as e:
            logger.error(e)
            pass
        return
    if call.callback_query.data.startswith("solyan"):
        try:
            sgynknl = collection.find_one({"_id": user})['kanal'][int(call.callback_query.data.split("-")[-1])-1]
        except Exception as e:
            await bot.edit_message_text("<i>İptal Edildi</i>", user, mesajid)
            logger.error(e)
            return
        try:
            sgyisim = await bot.get_chat(sgynknl).title
        except:
            sgyisim = "Kanalınıza ulaşılamadı!"
        await call.callback_query.answer(sgyisim)
        try:
            await call.callback_query.edit_message_text(f"<b> >>>    {sgyisim}\n\nKanalınızda kullanmak istediğiniz kaynak kanalını seçin.</b>", reply_markup=kaynakmark(user, int(call.callback_query.data.split("-")[-1])-1))
        except Exception as e:
            logger.error(e)
            pass
        return
    """ PAT """
    if call.callback_query.data.startswith("jop"):
        jc = int(call.callback_query.data.split("-")[-1])
        calljob = context.job_queue.get_jobs_by_name(str(user))
        try:
            calljob[jc].schedule_removal()
        except:
            await call.callback_query.edit_message_text("Bu post zaten gönderilmiş veya silinmiş.")
            return ConversationHandler.END
        await call.callback_query.edit_message_text("Post silindi.")
        return ConversationHandler.END
    if call.callback_query.data == "pzamanla":
        await call.callback_query.edit_message_text("Postun gönderilmesini istediğiniz saati gönderin.\n\n<b>Örnek biçim;</b>\n<code>30/03/21 18:30:00</code>")
        return PATZAMAN
    if call.callback_query.data == "simdi": 
        try:
            await bot.delete_message(user, mesajid)
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
            await call.callback_query.edit_message_text("Bir hata oluştı! Lütfen tekrar deneyin.")
            return
        pukanallar = collection.find_one({"_id": user})['kanal']
        if len(pukanallar) < 2:
            try:
                ppost = await SEND_MEDIA_TYPES[ptip](pukanallar[0], fid, caption=psablon, reply_markup=patmarkup)
            except Exception as e:
                logger.error(e)
                await bot.send_message(user, "Postunuz gönderilemedi, botu kanaldan çıkarmış olabilirsiniz.", reply_markup=dugme(user))
                return ConversationHandler.END
            if len(patbegeni) > 0 and begstate:
                if ButonCol.find_one({"_id": pukanallar[0]}) == None:
                    ButonCol.insert_one({"_id": pukanallar[0], str(ppost.message_id): [], "begeni": patbegeni})
                else:
                    ButonCol.update_one({"_id": pukanallar[0]}, {"$set": {str(ppost.message_id): [], "begeni": patbegeni}})
            await bot.send_message(user, "Postunuz gönderildi.", reply_markup=dugme(user))
            await bot.send_message(chat, "Başka post paylaşacak mısınız?", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Evet", callback_data="devam"), InlineKeyboardButton("Hayır", callback_data="del")]]))
            return ConversationHandler.END
        context.user_data['zaman'] = "yok"
        await bot.send_message(user, "Post Hazırlandı!", reply_markup=dugme(user))
        await bot.send_message(user, "<i>Postun gönderilmesini istediğin kanalı seç.</i>", reply_markup=(await patmark(user)))
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
                        pyetkililer = [pxy.user.id for pxy in await bot.get_chat_administrators(kan)]
                    except:
                        continue
                    if not user in pyetkililer:
                        await bot.send_message(chat, f"{await bot.get_chat(kan).title} Bu kanalda yetkili olmadığınız için post gönderilemedi ve kanal silindi.", reply_markup=dugme(user))
                        await bot.delete_message(user, mesajid)
                        collection.update_one({"_id": user}, {"$pull": {"kanal": kan}})
                        continue 
                    try:
                        ppost = await SEND_MEDIA_TYPES[ptip](kan, fid, caption=psablon, reply_markup=patmarkup)
                    except Exception as e:
                        logger.exception(e)
                        pass
                    else:
                        if len(patbegeni) > 0 and begstate:
                            if ButonCol.find_one({"_id": kan}) == None:
                                ButonCol.insert_one({"_id": kan, str(ppost.message_id): [], "begeni": patbegeni})
                            else:
                                ButonCol.update_one({"_id": kan}, {"$set": {str(ppost.message_id): [], "begeni": patbegeni}})
                await bot.edit_message_text("✅<b>Postunuz Tüm Kanallarınıza Gönderildi!</b>", user, mesajid)
                context.user_data.clear()
                mstd = await bot.send_message(chat, "Başka post paylaşacak mısınız?", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Evet", callback_data="devam"), InlineKeyboardButton("Hayır", callback_data="del")]]))
                return ConversationHandler.END
            try:
                pyetkililer = [pxy.user.id for pxy in await bot.get_chat_administrators(kanal[o])]
            except:
                pyetkililer = []
            if not user in pyetkililer:
                await bot.send_message(chat, f"{await bot.get_chat(kanal[o]).title} Bu kanalda yetkili olmadığınız için post gönderilemedi ve kanal silindi.", reply_markup=dugme(user))
                await bot.delete_message(user, mesajid)
                collection.update_one({"_id": user}, {"$pull": {"kanal": kanal[o]}})
                return ConversationHandler.END
            try:
                ppost = await SEND_MEDIA_TYPES[ptip](kanal[o], fid, caption=psablon, reply_markup=patmarkup)
            except Exception as e:
                await bot.edit_message_text(f"Postunuz gönderilemedi \n\n{e}", user, mesajid)
                context.user_data.clear()
                return ConversationHandler.END
            if len(patbegeni) > 0 and begstate:
                if ButonCol.find_one({"_id": kanal[o]}) == None:
                    ButonCol.insert_one({"_id": kanal[o], str(ppost.message_id): [], "begeni": patbegeni})
                else:
                    ButonCol.update_one({"_id": kanal[o]}, {"$set": {str(ppost.message_id): [], "begeni": patbegeni}})
            await bot.edit_message_text("✅<b>Postunuz Kanalınıza Gönderildi!</b>", user, mesajid)
            context.user_data.clear()
            mstd = await bot.send_message(chat, "Başka post paylaşacak mısınız?", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Evet", callback_data="devam"), InlineKeyboardButton("Hayır", callback_data="del")]]))
            return ConversationHandler.END
        else:
            zamani = context.user_data['zaman']
            msg_dict = []
            if o == -1:
                for kan in kanal:
                    pyetkililer = [pxy.user.id for pxy in await bot.get_chat_administrators(kan)]
                    if not user in pyetkililer:
                        await bot.send_message(chat, f"{await bot.get_chat(kan).title} Bu kanalda yetkili olmadığınız için post gönderilemedi ve kanal silindi.", reply_markup=dugme(user))
                        await bot.delete_message(user, mesajid)
                        collection.update_one({"_id": user}, {"$pull": {"kanal": kan}})
                        continue
                    msg_dict.append({"pkan": kan, "psablon": psablon, "ptip": ptip, "fid": fid, "user": user})
                await bot.delete_message(user, mesajid)
                await bot.send_message(user, "⏱ Postunuz zamanlandı.", reply_markup=dugme(user))
                mstd = await bot.send_message(chat, "Başka post paylaşacak mısınız?", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Evet", callback_data="devam"), InlineKeyboardButton("Hayır", callback_data="del")]]))
                context.job_queue.run_once(callback=zamanjob, when=zamani, context=msg_dict, name=str(user))
                context.user_data.clear()
                return ConversationHandler.END

            pyetkililer = [pxy.user.id for pxy in await bot.get_chat_administrators(kanal[o])]
            if not user in pyetkililer:
                await bot.send_message(chat, f"{await bot.get_chat(kanal[o]).title} Bu kanalda yetkili olmadığınız için post gönderilemedi ve kanal silindi.", reply_markup=dugme(user))
                collection.update_one({"_id": user}, {"$pull": {"kanal": kanal[o]}})
                await bot.delete_message(user, mesajid)
                context.user_data.clear()
                return ConversationHandler.END
            msg_dict.append({"pkan": kanal[o], "psablon": psablon, "ptip": ptip, "fid": fid, "user": user})
            await bot.delete_message(user, mesajid)
            await bot.send_message(user, "⏱ Postunuz zamanlandı.", reply_markup=dugme(user))
            context.job_queue.run_once(callback=zamanjob, when=zamani, context=msg_dict, name=str(user))
            context.user_data.clear()
            mstd = await bot.send_message(chat, "Başka post paylaşacak mısınız?", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Evet", callback_data="devam"), InlineKeyboardButton("Hayır", callback_data="del")]]))
            return ConversationHandler.END
        return
    """ Şablon """
    if call.callback_query.data == "vsablon":
        if collection.find_one({"_id": user})['sira'] == 1:
            collection.update_one({"_id": user}, {"$set": {"sablon": "9"}})
        else:
            collection.update_one({"_id": user}, {"$set": {"sablon": "1"}})
        await bot.edit_message_text("Varsayılana döndürüldü.", chat, mesajid)
        return
    """ Emoji """
    if call.callback_query.data == "begenikaldir":
        collection.update_one({"_id": user}, {"$set": {"begeni": []}})
        await call.callback_query.edit_message_text("Beğeni butonları kaldırıldı!")
        await call.callback_query.answer("Kaldırıldı")
        return
    """ Tekrarli Post """
    if call.callback_query.data.startswith("tsenough"):
        await call.callback_query.edit_message_text("Tekrarli Postunuzun kaç saatte bir gönderilmesini istediğiniz saati seçin", reply_markup=tekrarlisaatmark())
        return
    if call.callback_query.data.startswith("tkan+"):
        try:
            context.user_data['tskan']
        except KeyError:
            context.user_data['tskan'] = []
        
        context.user_data['tskan'].append(call.callback_query.data.split("+")[-1])
        await call.callback_query.answer("Kanal belirlendi!")
        try:
            await call.callback_query.edit_message_reply_markup((await tekrarlipostkan(user, context)))
        except:
            pass
        return 
    if call.callback_query.data == "tekrarlisil":
        await call.callback_query.edit_message_text("Silmek istediğiniz postu seçin.", reply_markup=tekrarlipostsilmark(user, context))
        return
    if call.callback_query.data == "yenitekrarli":
        if len(collection.find_one({"_id": user})['kanal']) == 0:
            await call.callback_query.edit_message_text("Tekrarli Post ayarlayabilmek için önce bir kanal kaydetmelisiniz!")
            return
        elif len(collection.find_one({"_id": user})['kanal']) > 1:
            context.user_data['tskan'] = []
            await call.callback_query.edit_message_text("Tekrarli Post ayarlamak istediğiniz kanalları seçin.", reply_markup=(await tekrarlipostkan(user, context)))
        else:
            context.user_data["tskan"] = collection.find_one({"_id": user})['kanal'][0]
            await call.callback_query.edit_message_text("Tekrarli Postunuzun kaç saatte bir gönderilmesini istediğiniz saati seçin", reply_markup=tekrarlisaatmark())
        return
    if call.callback_query.data.startswith("tssil-"):
        try:
            context.job_queue.get_jobs_by_name(f"ts{user}")[int(call.callback_query.data.split("-")[-1])].schedule_removal()
        except:
            await call.callback_query.edit_message_text("Post iptal edilemedi!")
        else:
            await call.callback_query.edit_message_text("Postunuz silindi artık paylaşılmayacak")
        return
    """ Panel """
    """ iOS Kontrol """
    if call.callback_query.data.startswith("iosk-"):
        await call.callback_query.edit_message_text("<code>Kontrol ediliyor...</code>")
        ioskanal = collection.find_one({"_id": user})['kanal'][int(call.callback_query.data.split("-")[-1])]
        ioskanlink = await bot.get_chat(ioskanal)
        if ioskanlink.invite_link == None:
            await call.callback_query.edit_message_text("iOS Ban kontrol edebilmem için bota kanalınızda <b>Üye Ekleme</b> yetkisi vermelisiniz!")
            return
        await bot.send_message(eklenti, f'ios*{user}*{ioskanlink.invite_link}')
        context.user_data['iosmsgid'] = mesajid
        return
    await call.callback_query.answer(f"Yanıt yok - {call.callback_query.data}")

async def tekrarlisaatayarlacall(call, context):
    bot = context.bot
    context.user_data['tsaat'] = int(call.callback_query.data.split("-")[-1])
    try:
        await call.effective_message.delete()
    except:
        pass
    await bot.send_message(call.effective_chat.id, "Tekrarlı postunuza bir başlık verin.\n\nÖrnek;\nJigolo afiş, IVR afiş", reply_markup=imark())
    await call.callback_query.answer("Saat belirlendi!")
    return TSBASLIK

async def tsmodcall(call, context):
    bot = context.bot
    user = call.effective_user.id
    chat = call.effective_chat.id
    query = call.callback_query
    try:
        await call.effective_message.delete()
    except:
        pass
    mod = query.data.split("-")[1] + "-0"
    context.user_data["tspostdict"]["mod"] = mod
    tetik = datetime.datetime.now(pytz.timezone('Europe/Istanbul')) + datetime.timedelta(hours = int(context.user_data['tsaat']))
    context.user_data["tspostdict"]["tetik"] = tetik.strftime("%Y-%m-%d %H:%M:%S")
    firstmod = 3600*int(context.user_data["tsaat"])-3600 if int(context.user_data["tsaat"]) != 1 else 3600
    context.job_queue.run_repeating(tekrarlipostjob, first=firstmod, interval=3600*int(context.user_data['tsaat']), name=f"ts{user}", context=context.user_data["tspostdict"])
    context.user_data.clear()
    await bot.send_message(chat, "Postlarınız başarıyla ayarlandı!", reply_markup=dugme(user))
    return ConversationHandler.END


async def advcall(call, context):
    bot = context.bot
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
        await bot.send_message(chat, "Yeni eklemem istediğiniz siteyi seçin.", reply_markup=altsitemarkup("asite"))
    elif query.data.startswith("advapi-"):
        query.answer(f"API Adresiniz:\n {advdat['altapi'][int(query.data.split('-')[-1])]['api']}", show_alert=True)
    elif query.data.startswith("advsil-"):
        collection.update_one({"_id": user}, {"$pull": {"altapi": advdat['altapi'][int(query.data.split("-")[-1])]}})
        query.answer("API Kaldırıldı!")
        query.edit_message_reply_markup(advaltmark(user))
    elif query.data == "advbilgi":
        query.answer("Sıralı:\nKaydettiğiniz tüm apileri sırayla kullanır.\n\nTek Post İki Link:\nKaydettiğiniz tüm apileri birincil apiniz ile birlikte tek postta iki link olarak sırayla paylaşır.", show_alert=True)
    

async def begeniislemcall(call, context):
    bot = context.bot
    user = call.effective_user.id
    chat = call.effective_chat.id
    mesajid = call.effective_message.message_id    
    pushed = int(call.callback_query.data.split("-")[-1])
    if not begstate:
        await call.callback_query.answer("Üzgünüm bu özellik geçici olarak devredışı bırakılmıştır.")
        return
    for i in range(10):
        begkeyb = []
        mrkpc = 0
        if not user in ButonCol.find_one({"_id": str(chat)})[str(mesajid)]:
            ButonCol.update_one({"_id": str(chat)}, {"$push": {str(mesajid): user}})
        else:
            try:
                await call.callback_query.answer("Butonları bir kez kullanabilirsiniz")
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
            await call.callback_query.answer(str(call.effective_message.reply_markup.inline_keyboard[0][pushed].text.split()[-2]))
        except:
            pass
        try:
            await call.callback_query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([begkeyb]))
        except RetryAfter as rtt:
            time.sleep(rtt.retry_after+1)
            try:
                await call.callback_query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([begkeyb]))
            except:
                pass
            else:
                break
        except:
            pass
        else:
            break
