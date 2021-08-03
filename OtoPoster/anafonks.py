from .misc import *
from . import *
from .markups import *
from .callbacks import *


@send_typing_action
def menu(update, context):
    chat = update.message.chat.id
    user = update.message.from_user.id
    mesaj = update.message.text
    bot = context.bot
    mj = collection.find_one({"_id": user})
    if user in kara:
        bot.send_message(chat, "🤓 Üzgünüm senin gibi aptal birisi için çalışmıyorum")
        return
    try:
        tokenn = mj['token']
    except:
        bot.send_message(chat, """📝 <i>Lütfen</i> <a href="https://tr.link/member/tools/quick">burdan</a> <i>aldığınız API adresinizi gönderin</i>""", reply_markup=imark())
        return APIDEGISTIR
    if mesaj == "📝 Kaydet":
        try:
            tokenn = mj['token']
        except:
            bot.send_message(chat, """📝 <i>Lütfen</i> <a href="https://tr.link/member/tools/quick">burdan</a> <i>aldığınız API adresinizi gönderin</i>""", reply_markup=imark())
            
            return APIDEGISTIR
    if mesaj == "🖥 Kanal Menü":
        kayitli = 0
        menu_mesaj = "<b>🖥Kayıtlı Kanalınız;</b>\n"
        for chan in mj['kanal']:
            try:
                kbilgi = bot.get_chat(chan)
            except Exception as e:
                logger.error(e)
                collection.update_one({"_id": user}, {"$pull": {"kanal": chan}})
                logger.warning("Kanal silindi")
            else:    
                kayitli = kayitli + 1
                if kayitli == len(mj['kanal']):
                    menu_mesaj += """└<a href="{}">{}</a>""".format("tg://privatepost?channel={}&post=9999999".format(chan[3:]), kbilgi.title)
                else:
                    menu_mesaj += """├<a href="{}">{}</a>\n""".format("tg://privatepost?channel={}&post=9999999".format(chan[3:]), kbilgi.title)
        menu_mesaj += f"\n\nToplam {kayitli} Kanalınız Bulunuyor."
        bot.send_message(chat, menu_mesaj, reply_markup=kanalmenumark())
        return KANALMENU
    if mesaj == "🎛 Post Menü":
        bot.send_message(chat, "Post menüsü.", reply_markup=postmenumark())
        return POSTMENU
    if mesaj == "🔗 API Menü":
        if mj['altsite'] == "None":
            apimenu_mesaj = "<i>♦️Kayıtlı API: {}\nSite: {}</i>".format(mj['token'], site_isim(mj['site']))
        else:
            apimenu_mesaj = "<i>♦️Birincil API: {}\n  Birincil Site: {}\n  Alternatif API: {}\n  Alternatif Site: {}</i>".format(mj['token'], site_isim(mj['site']), mj['altapi'], site_isim(mj['altsite']))
        bot.send_message(chat, apimenu_mesaj, reply_markup=apimenumark())
        return APIMENU
    
    if mesaj == "🥰 Bağış":
        bot.send_message(chat, "🥰Madem bu kadar çok istiyorsun. \n\n🏧Papara: <code>1666982412</code> \n🏦İninal: <code>4003140030544</code>")
        return
    
        
    bot.send_message(chat, "<i>Lütfen alttaki butonları kullan</i>", reply_markup=dugme(user))

@send_typing_action
def kanalmenu(update, context):
    user = update.effective_user.id
    chat = update.effective_chat.id
    kudat = collection.find_one({"_id": user})
    mesaj = update.effective_message.text
    if user in kara:
        bot.send_message(chat, "🤓 Üzgünüm senin gibi aptal birisi için çalışmıyorum")
        return
    try:
        tokenn = kudat['token']
    except:
        msg = bot.send_message(chat, """⛔ Henüz bir API kaydetmemişsiniz!\n\n📝 <i></i> <a href="https://tr.link/member/tools/quick">buraya tıklayarak</a> <i>aldığınız API adresinizi gönderin</i>""", reply_markup=imark())            
        return APIDEGISTIR

    if mesaj == "🗑️ Kanal Sil":
        if len(kudat['kanal']) < 1:
            bot.send_message(chat, "Henüz bir kanal kaydetmemişsiniz!", reply_markup=kanalmenumark())
            return 
        bot.send_message(chat, "Silmek istediğiniz kanalı seçin.", reply_markup=gen_markup(user))
        return 
    if mesaj == "🔶 Yeni Kanal Ekle":
        vip_uyeler = collection.find_one({"_id": 0})['vipuye']
        if len(kudat['kanal']) > 9 and not user in vip_uyeler:
            bot.send_message(chat, "<i>Üzgünüm en fazla 10 kanal kaydedebilirsiniz.</i>")
            return 
        bot.send_message(chat, """📝 <i>Lütfen kanalınızdan bir gönderi iletin.</i>""", reply_markup=imark())
        return KANALKAYDET
    if mesaj == "▶️ SFS Modu":
        bot.send_message(chat, "<i>SFS moduna almak istediğiniz kanalı seçin. SFS moduna aldığınız kanala modu kapatana kadar post atılmaz!</i>\n\n", reply_markup=sfsmark(user))    
        return
    if mesaj == "↩️ Ana Menü" or mesaj == "❌ İptal":
        bot.send_message(chat, "<b>Biliyor muydunuz? -></b> "+"<i>"+choice(tips)+"</i>")
        bot.send_message(chat, "Ana Menü.", reply_markup=dugme(user))
        return ConversationHandler.END

    bot.send_message(chat, "<i>Lütfen alttaki butonları kullan</i>", reply_markup=kanalmenumark())

@send_typing_action
def apimenu(update, context):
    user = update.effective_user.id
    chat = update.effective_chat.id
    audat = collection.find_one({"_id": user})
    mesaj = update.effective_message.text
    if user in kara:
        bot.send_message(chat, "🤓 Üzgünüm senin gibi aptal birisi için çalışmıyorum")
        return
    try:
        tokenn = audat['token']
    except:
        bot.send_message(chat, "⛔ Henüz bir API kaydetmemişsiniz!\n\n📝 <i></i> <a href='https://tr.link/member/tools/quick'>buraya tıklayarak</a> <i>aldığınız API adresinizi gönderin</i>", reply_markup=imark())
        return APIDEGISTIR
    if mesaj == "♻️ API değiştir":
        bot.send_message(chat, "Yeni API adresinizi girin.", reply_markup=imark())
        return APIDEGISTIR
    if mesaj == "🔗 Site değiştir":
        bot.send_message(chat, "<i>Kullanmak istediğiniz siteyi seçin</i>", reply_markup=sitemarkup())
        return
    if mesaj == "🤖 Alternatif Link":
        bot.send_message(chat, "<b>Alternatif Nasıl Kullanılsın.\n\n Tek Post İki Link</b>\n <i>Aynı post iki link</i> \n\n<b>Sıralı</b>\n <i>Bir post birinci servis, bir post alternatif servis.</i>\n\n<b>Kullanmak istediğiniz sistemi seçin.</b>", reply_markup=altmarkup(user))
        return
    if mesaj == "↩️ Ana Menü" or mesaj == "❌ İptal":
        bot.send_message(chat, "<b>Biliyor muydunuz? -></b> "+"<i>"+choice(tips)+"</i>")
        bot.send_message(chat, "Ana Menü.", reply_markup=dugme(user))
        return ConversationHandler.END

    bot.send_message(chat, "<i>Lütfen alttaki butonları kullan</i>", reply_markup=apimenumark())
    
@send_typing_action
def postmenu(update, context):
    user = update.effective_user.id
    chat = update.effective_chat.id
    poudat = collection.find_one({"_id": user})
    mesaj = update.effective_message.text
    if user in kara:
        bot.send_message(chat, "🤓 Üzgünüm senin gibi aptal birisi için çalışmıyorum")
        return
    try:
        tokenn = poudat['token']
    except:
        bot.send_message(chat, """⛔ Henüz bir API kaydetmemişsiniz!\n\n📝 <i></i> <a href="https://tr.link/member/tools/quick">buraya tıklayarak</a> <i>aldığınız API adresinizi gönderin</i>""", reply_markup=imark())            
        return APIDEGISTIR
    if mesaj == "⏱ Post Zamanları":
        if not user == sahip:
            bot.send_message(chat, "<code> Bu özellik henüz test aşamasında.</code> ")
            return
        for kca in poudat['kanal']:
            if not eklenti in [r.user.id for r in bot.get_chat_administrators(kca)]:
                bot.send_message(chat, "Botun post zamanlayabilmesi için eklentiye ihtiyacı var, eklenti kurulsun mu?\n\n<i>Butona basmadan önce bota kanallarınızda resimdeki yetkileri vermeniz gerekiyor</i> <a href='https://telegra.ph/file/d8802d6ca2fe807639a06.png'>ㅤ</a>", reply_markup=ekmark())
                return
        zaman_menu = "<b>Eklenti:</b> ✅\n\n"
        if poudat['vakit'] == 0:
            zaman_menu += "Henüz Post saatleri ayaralamamışsınız"
        else:
            vakcount = 0
            for vak in ka['vakit']:
                zaman_menu += str(vakcount)+ ". " + str(vak) + "\n"
                vakcount += 1
            zaman_menu += f"\n<i>Günlük {vakcount} Post Paylaşıyorsunuz. </i>"
            if poudat['time'] == -1:
                zaman_menu += f"\n\nBugün post sınırınıza ulaştınız"
            else:
                zaman_menu += f"\n\nBir sonraki postunuz günün <code>{poudat['time']}</code>. postu olacak."
        bot.send_message(chat, zaman_menu, reply_markup=zamanmenumark(user))
        return
    if mesaj == "📏 Şablon":
        aciklama = "Pharex, lord adminin karısını sikerken lord adminn basıyor."
        if poudat['site'] == "1":
            link = "https://ay.live/vRpKVx"
        if poudat['site'] == "2":
            link = "https://pgg.fyi/X0DK3"
        if poudat['site'] == "3":
            link = "https://exe.io/o96d4d"
        if poudat['site'] == "4":
            link = "https://ouo.io/RA1K5D"
        if poudat['site'] == "5":
            link = "https://lnkload.com/2v5vy"
        if poudat['altsite'] != "None":
            if poudat['altsite'] == "1":
                alink = "https://ay.live/vRpKVx"
            if poudat['altsite'] == "2":
                alink = "https://pgg.fyi/X0DK3"
            if poudat['altsite'] == "3":
                alink = "https://exe.io/o96d4d"
            if poudat['altsite'] == "4":
                alink = "https://ouo.io/RA1K5D"
            if poudat['altsite'] == "5":
                alink = "https://lnkload.com/2v5vy"
        else:
            alink = "https://lnkload.com/2v5vy"
        if poudat['sablon'] == "1":
            bot.send_message(chat, "<b>Varsayılan Şablon:</b>\n\n🔥{aciklama} \n\n🔱 TIKLA 👉 {link} \n\n📛 SESİ AÇ 'a tıklamayı unutma", reply_markup=sablonmark(user))
        elif poudat['sablon'] == "2":
            bot.send_message(chat, "<b>Varsayılan Şablon:</b>\n\n{aciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {link}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 @linkgec06", reply_markup=sablonmark(user))
        elif poudat['sablon'] == "9":
            bot.send_message(chat, "<b>Varsayılan Şablon:</b>\n\n{aciklama} \n\n𝙇𝙄𝙉𝙆🔗 {link} \n\n     𝙇𝙄𝙉𝙆🔗 {alink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 @linkk_gecmee", reply_markup=sablonmark(user))
        else:
            if poudat['sira'] == "1":
                pst = poudat['sablon'].replace("{aciklama}", "{a}").replace("{link}", "{l}").replace("{alink}", "{al}").format(a=aciklama, l=link, al=alink)
            else:
                pst = poudat['sablon'].replace("{aciklama}", "{a}").replace("{link}", "{l}").replace("{alink}", "{al]").format(a=aciklama, l=link)
            bot.send_message(chat, f"<b>Şablonunuz böyle gözükecek:</b>\n\n{pst}", reply_markup=sablonmark(user))
        return
    if mesaj == "🔧 Kaynak":
        if len(poudat['kanal']) < 1:
            bot.send_message(chat, "Henüz bir kanal kaydetmemişsiniz.", reply_markup=dugme(user))
            return
        kaynakmsg = bot.send_message(chat, "<code>Yükleniyor...</code>")
        kynskm = poudat['kanal'][0]
        if poudat['ozel']:
            for m in OzelCol.find({}):
                if user in m['kanal']:
                    try:
                        ozel_kaynak_bilgi = bot.get_chat(m['okaynak'])
                    except:
                        kaynakmsg.edit_text("Botu kaynak kanalınızdan çıkarttığınız için post atılmayacak.", reply_markup=kaynakmark(user, 0))
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
                try:
                    kcisim = bot.get_chat(kynskm).title
                except:
                    kcisim = "Kanalınıza ulaşılamadı!"
                kaynakmsg.edit_text(f"""<b> >>>    {kcisim}\n\nKanalınızda kullanmak istediğiniz kaynak kanalını seçin.</b>""", reply_markup=kaynakmark(user, 0))
                return
            ref_link = create_deep_linked_url(context.bot.username, str(refsahip))
            kaynakmsg.edit_text("""<b>Özel Kaynak Kullandığınız için başka kaynak seçemezsiniz.</b>\n\n      <i>Özel Kaynağınız:</i><b> <a href="{}">{}</a>\n</b>      <i>Bu Kaynağı Toplam </i><code>{}</code> <i>Kişi Kullanıyor.</i>\n\n<b>Kaynak Referans Linki;</b>\n<code>{}</code>\n<i>Bu link ile botu başlatan herkes otomatik olarak sizin kaynağınıza bağlanacak.</i>""".format(ozel_kaynak_bilgi.invite_link, ozel_kaynak_bilgi.title, kullanan_sayisi, ref_link), reply_markup=kaynakmark(user, 0))
            return
        try:
            kcisim = bot.get_chat(kynskm).title
        except:
            kcisim = "Kanalınıza ulaşılamadı!"
        kaynakmsg.edit_text(f"""<b> >>>    {kcisim}\n\nKanalınızda kullanmak istediğiniz kaynak kanalını seçin.</b>""", reply_markup=kaynakmark(user, 0))
        return
    if mesaj == "⏱ Zamanladıklarım":
        zjobs = context.job_queue.get_jobs_by_name(str(user))
        if len(zjobs) < 1:
            bot.send_message(chat, "Henüz bir post zamanlamamışsınız.", reply_markup=postmenumark())
            return 
        bot.send_message(chat, "Silmek istediğiniz postu seçin.", reply_markup=jobmark(user, context))
        return 
    if mesaj == "⛓️ Elle Post Paylaş":
        if len(poudat['kanal']) < 1:
            bot.send_message(chat, "Lütfen önce bir kanal kaydedin.", reply_markup=postmenumark())
            return
        bot.send_message(chat, "Paylaşmamı istediğin hazır postu ilet.", reply_markup=imark())
        return PATPOST
    if mesaj == "↩️ Ana Menü" or mesaj == "❌ İptal":
        bot.send_message(chat, "<b>Biliyor muydunuz? -></b> "+"<i>"+choice(tips)+"</i>")
        bot.send_message(chat, "Ana Menü.", reply_markup=dugme(user))
        return ConversationHandler.END

    bot.send_message(chat, "<i>Lütfen alttaki butonları kullan</i>", reply_markup=postmenumark())
   
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
    if KaynakCol.find_one({"_id": kanal}):
        mst = bot.send_message(chat, "Kaynak kanalını nasıl kaydedebilirim ki?")
        return OZELKAYNAK
    try:
        yetkiler = bot.get_chat_administrators(kanal)
    except:
        msg = bot.send_message(chat, "Botu kanalınızda yönetici eklememişsiniz.")
        return OZELKAYNAK
    if OzelCol.find_one({"okaynak": kanal}) != None:
        for koy in KaynakCol.find({}):
            if user in koy['kaynak']:
                KaynakCol.update_one({"okaynak": koy['_id']}, {"$pull": {"kaynak": user}})
        collection.update_one({"_id": user}, {"$set": {"ozel": True, "kaynak": ["32"]}})
        if not user in OzelCol.find_one({"okaynak": kanal})['kanal']:
            OzelCol.update_one({"okaynak": kanal}, {"$push": {"kanal": user}})
        if len(OzelCol.find_one({"okaynak": kanal})['kanal']) == 6:
            bot.send_message(OzelCol.find_one({"okaynak": kanal})['_id'], "<i>Özel Kaynağınız 5 kişiyi geçtiği için artık 20 linkte 1 Pharexin olayı sizin için de geçerilidir.</i>")
        bot.send_message(update.message.chat.id, "<b>Özel Kaynak Kaydedildi!</b>", reply_markup=dugme(user))
        return ConversationHandler.END
    else:
        for koy in KaynakCol.find({}):
            if user in koy['kaynak']:
                KaynakCol.update_one({"_id": koy['_id']}, {"$pull": {"kaynak": user}})
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
    if KaynakCol.find_one({"_id": kanal}):
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
    if bnb == None:
        bot.send_message(chat, "Lütfen şablon kaydetmeden önce Kaydet butonu ile bilgilerinizi girin!", reply_markup=dugme(user))
    if update.message.text == None:
        msg = bot.send_message(chat, """ ❌<i> Lütfen mesajınızda "{link}" ve "{aciklama}" bulunduğudan emin olun.</i> """)

        return SABLONA
    if update.message.text == "❌ İptal":
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme(user))
        return ConversationHandler.END
    if bnb['sira'] == "1":
        if mesaj.find("{link}") == -1 or mesaj.find("{aciklama}") == -1 or mesaj.find("{alink}") == -1:
            msg = bot.send_message(chat, """ ❌<i> Lütfen mesajınızda "{link}", "{alink}" ve "{aciklama}" bulunduğudan emin olun.</i> """)
            return SABLONA
    else:
        if mesaj.find("{link}") == -1 or mesaj.find("{aciklama}") == -1:
            msg = bot.send_message(chat, """ ❌<i> Lütfen mesajınızda "{link}" ve "{aciklama}" bulunduğudan emin olun.</i> """)
            return SABLONA
        if mesaj.find("{link}") != mesaj.rfind("{link}"):
            msg = bot.send_message(chat, """ ❌<i> Lütfen mesajınızda bir tane "{link}" bulunduğudan emin olun.</i> """)
            return SABLONA
        if mesaj.find("{aciklama}") != mesaj.rfind("{aciklama}"):
            msg = bot.send_message(chat, """ ❌<i> Lütfen mesajınızda bir tane "{aciklama}" bulunduğudan emin olun.</i> """)
            return SABLONA
    collection.update_one({"_id": user}, {"$set":{"sablon": mesaj}})
    bot.send_message(chat, "Şablon kaydedildi!", reply_markup=dugme(user))
    return ConversationHandler.END

def cancel(update, context):
    chat = update.message.chat.id
    bot.send_message(chat, "Ana Menü", reply_markup=dugme(chat))
    return ConversationHandler.END

def altakayit(update, context):
    amesaj = update.message.text
    user = update.message.from_user.id
    chat = update.message.chat.id
    if collection.find_one({"_id": user}) == None:
        bot.send_message(chat, "<b>Önce bir API kaydedin!</b>")
        return
    if update.message.text == "❌ İptal" or update.message.text == None:
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme(user))
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

def postzaman(update, context):
    chat = update.message.chat.id
    user = update.message.from_user.id
    post_zaman_text = update.message.text
    if post_zaman_text == None:
        bot.send_message(chat, "Gönderdiğiniz saatlerden biri veya birden fazlası yanlış.\n\nÖrnek;\n00:00\n01:00\n02:00\n03:00\n...", reply_markup=imark()) 
        return    
    if update.message.text == "❌ İptal":
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme(user))
        return ConversationHandler.END
    for px in post_zaman_text.split("\n"):
        if not len(px) == 5 or px.find(":") == -1:
            bot.send_message(chat, "Gönderdiğiniz saatlerden biri veya birden fazlası yanlış.\n\nÖrnek;\n00:00\n01:00\n02:00\n03:00\n...", reply_markup=imark()) 
            return
    collection.update_one({"_id": user}, {"$set": {"vakit": post_zaman_text.split("\n")}})
    bot.send_message(chat, "Post Saatleriniz Değiştirildi!", reply_markup=dugme(user))
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
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme(user))
        return ConversationHandler.END
    if token.startswith('http') or "url=trlink" in token:
        mso = bot.send_message(chat, "❌ Geçersiz bir API verdiniz! Lütfen doğru bir API adresi verin.")
        return APIDEGISTIR
    key = {"_id": user, "token": token, "kanal": [], "sablon": "1", "kaynak": ["1"], "site": "1", "altapi": "None", "altsite": "None", "sira": "0", "ozel": False, "pcount": 0, "time": 0, "vakit": 0, "eski": []}
    if token in apikara:
            ment = "@"+str(update.message.from_user.username) if update.message.from_user.username else update.message.from_user.id
            blmsg = bot.send_message(blog, f"Yasaklı API tespit edildi -> {token}\nK.ADI: {ment}")
            bot.pin_chat_message(blog, blmsg.message_id)
    if bnb == None:
        kontrol = get("https://ay.live/api/?api={}&url=www.zort.com&format=text&alias=&ct=2".format(token)).text
        if kontrol == "":
            bot.send_message(chat, "❌ Geçersiz bir API verdiniz! Lütfen doğru bir API adresi verin.")
            return APIDEGISTIR
        collection.insert_one(key)
        bot.send_message(chat, "<b>🟢 API kaydedildi!</b>")
        bot.send_message(chat, "<i>📝 Lütfen kanalınızdan bir gönderi iletin.</i>", reply_markup=imark())
        bot.send_message(blog, f"#YENİ_KULLANİCİ\nID: {user}\nAPI: {token}\nK.ADI: @{update.message.from_user.username}")
        return KANALKAYDET
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
        return 
    kanal = update.message.forward_from_chat.id
    if KaynakCol.find_one({"_id": kanal}):
        mst = bot.send_message(chat, "Kaynak kanalını nasıl kaydedebilirim ki?", reply_markup=imark())
        return 
    if str(kanal) in y['kanal']:
        msl = bot.send_message(chat, "Bu kanalı zaten kaydetmişsiniz")
        return 
    try:
        kanalbilgi = bot.get_chat(kanal)
    except:
        msg = bot.send_message(chat, "Botu kanalınızda yönetici eklememişsiniz.")
        return 
    try:
        yetkiler = bot.get_chat_administrators(kanal)
    except:
        msg = bot.send_message(chat, "Botu kanalınızda yönetici eklememişsiniz.")        
        return 
    ytliler = [y.user.id for y in yetkiler]
    if not user in ytliler:
        bot.send_message(chat, "Bu kanal sizin değil 😠")
        return
    if y['vakit'] != 0:
        kbotdurum = bot.get_chat_member(ku, bot.get_me().id)
        if botdurum.can_invite_users and botdurum.can_promote_members and botdurum.can_post_messages:
            bot.send_message(eklenti, kanalbilgi.invite_link)
            sleep(0.5)
            try:
                bot.promote_chat_member(ku, eklenti, can_post_messages=True)
            except:
                bot.send_message(chat, "Post zamanlama özelliğiniz açık olduğu için resimdeki yetkileri vermeniz gerekiyor. <a href='https://telegra.ph/file/d8802d6ca2fe807639a06.png'>ㅤ</a>")
                return
        else:
            bot.send_message(chat, "Post zamanlama özelliğiniz açık olduğu için resimdeki yetkileri vermeniz gerekiyor. <a href='https://telegra.ph/file/d8802d6ca2fe807639a06.png'>ㅤ</a>")
            return
    collection.update_one({"_id": user}, {"$push":{"kanal": str(kanal)}})
    update.message.reply_text("<b>🟢Kanalınız Kaydedildi.</b>", reply_markup=dugme(user))
    bot.send_message(blog, f"#YENİ_KANAL\nID: {kanal}\nÜYE: {bot.get_chat_members_count(kanal)}\nSAHİP: {user}")
    for kyt in KaynakCol.find({}):
        if user in kyt['kaynak']:
            if not str(kanal) in KaynakCol.find_one({"_id": kyt['_id']})['kanal']:
                KaynakCol.update_one({"_id": kyt['_id']}, {"$push": {"kanal": str(kanal)}})
    return ConversationHandler.END

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
        pyetkililer = [pxy.user.id for pxy in bot.get_chat_administrators(satkat['kanal'][0])]
        if not user in pyetkililer:
            bot.send_message(chat, f"{bot.get_chat(satkat['kanal'][0]).title} Bu kanalda yetkili olmadığınız için kanal silindi", reply_markup=dugme(user))
            collection.update_one({"_id": user}, {"$pull": {"kanal": satkat['kanal'][0]}})
            return ConversationHandler.END
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
    kplink = mesaj[psol:psag].strip()
    if kplink.startswith("https://ay") or kplink.startswith("https://pgg") or kplink.startswith("https://pnd") or kplink.startswith("https://ouo") or kplink.startswith("https://exe") or kplink.startswith("https://lnk"):
        bot.send_message(chat, "Oops sanırım zaten kısaltılmış bir linki kısaltmaya çalışıyorsun. Üzgünüm bu bot linkleri kendisi geçemez.", reply_markup=imark())
        return 
    if mesaj.find("\n", psol) == -1:
        kplink = mesaj[psol:].strip()
    pathesap = collection.find_one({"_id": user})
    try:
        ptoken = pathesap['token']
    except:
        bot.send_message(chat, "API adresinizi yeniden kaydedin.")
        return
    psablon = pathesap['sablon']
    psite = pathesap['site']
    paltapi = pathesap['altapi']
    paltsite = pathesap['altsite']
    psira = pathesap['sira']
    palink = " "
    plink = " "
    ptry = 0
    if psira == "2":
        ptoken = paltapi
        psite = paltsite
        collection.update_one({"_id": user}, {"$set": {"sira": "3"}})
    if psira == "3":
        collection.update_one({"_id": user}, {"$set": {"sira": "2"}})
    try:
        if not paltapi == "None":
            while ptry < 10 and palink == " ":
                if paltsite == "1":
                    pjson = get(f"https://ay.live/api/?", params={"api": paltapi, "url": kplink, "ct": 1}).json()
                    palink = pjson['shortenedUrl']
                if paltsite == "2":
                    pjson = get(f"https://www.pnd.tl/api?", params={'api': paltapi, 'url': kplink, 'category': 6}).json()
                    palink = pjson['shortenedUrl']
                if paltsite == "3":
                    pjson = get(f"https://exe.io/api?", params={"api": paltapi, "url": kplink}).json()
                    palink = pjson['shortenedUrl']
                if paltsite == "4":
                    palink = get(f"http://ouo.io/api/{paltapi}", params={"s": kplink}).text
                if paltsite == "5":
                    palink = get(f"http://pubiza.com/api.php?", params={"token": paltapi, "url": kplink, "ads_type": "adult"}).text
                if paltsite == "6":
                    pjson = get("https://gir.ist/api?", params={"api": paltapi, "url": kplink}, headers=headerss).json()
                    print(pjson)
                    palink = pjson['shortenedUrl']
                time.sleep(1)
                ptry += 1
        while ptry < 10 and plink == " ":
            if psite == "1":
                pjson = get(f"https://ay.live/api/?", params={"api": ptoken, "url": kplink, "ct": 1}).json()
                plink = pjson['shortenedUrl']
            if psite == "2":
                pjson = get(f"https://www.pnd.tl/api?", params={'api': ptoken, 'url': kplink, 'category': 6}).json()
                plink = pjson['shortenedUrl']
            if psite == "3":
                pjson = get(f"https://exe.io/api?", params={"api": ptoken, "url": kplink}).json()
                plink = pjson['shortenedUrl']
            if psite == "4":
                plink = get(f"http://ouo.io/api/{ptoken}?", params={"s": kplink}).text
            if psite == "5":
                plink = get(f"http://pubiza.com/api.php?", params={"token": ptoken, "url": kplink, "ads_type": "adult"}).text
            if psite == "6":
                plink = get("http://gir.ist/api?", params={"api": ptoken, "url": kplink, "format": "text"}, headers=headerss).text
                print(plink)
            time.sleep(1)
            ptry += 1
        if plink == " ":
            bot.send_message(chat, "İşlem başarısız oldu lütfen tekrar deneyin.")
            return
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
        return
    context.user_data['psablon'] = psablon
    context.user_data['msg'] = update
    update.reply_text("Zamanlamak ister misiniz?", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Şimdi Gönder", callback_data="simdi")], [InlineKeyboardButton("Zamanla", callback_data="pzamanla")]]))
    return ConversationHandler.END