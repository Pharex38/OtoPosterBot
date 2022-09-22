from .misc import *
from . import *
from .jobs import *
from .markups import *
from .callbacks import *


@send_typing_action
def menu(update, context):
    chat = update.effective_message.chat.id
    user = update.effective_message.from_user.id
    mesaj = update.effective_message.text
    bot = context.bot
    mj = collection.find_one({"_id": user})
    if user in kara:
        bot.send_message(chat, "🤓 Üzgünüm senin gibi aptal birisi için çalışmıyorum")
        return
    if mesaj == "❌ İptal":
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme(user))    
        return
    if mesaj == "🥰   Bağış":
        bot.send_message(chat, "🥰Madem bu kadar çok istiyorsun. \n\n🏧Papara: <code>1666982412</code> \n🏦İninal: <code>4003140030544</code>")
        return
    if mesaj == "📝 Kaydet":
        bot.send_message(chat, """📝 <i>Lütfen</i> <a href="https://tr.link/member/tools/quick">burdan</a> <i>aldığınız API adresinizi gönderin</i>""", reply_markup=imark())
        return APIDEGISTIR
    if mesaj == "↩️ Ana Menü":
        bot.send_message(chat, "Ana Menü.", reply_markup=dugme(user))
        return
    if mesaj == "🖥 Kanal Menü":
        try:
            tokenn = mj['token']
        except:
            bot.send_message(chat, """⛔ Bu menüyü görebilmek içim önce bir API kaydetmelisiniz!\n\n📝 <i>Lütfen</i> <a href="https://tr.link/member/tools/quick">burdan</a> <i>aldığınız API adresinizi gönderin</i>""", reply_markup=imark())
            return APIDEGISTIR
        kayitli = 0
        menu_mesaj = "<b>🖥Kayıtlı Kanalınız;</b>\n"
        for chan in mj['kanal']:
            try:
                kbilgi = bot.get_chat(chan)
            except RetryAfter as krt:
                time.sleep(krt.retry_after+1)
                try:
                    kbilgi = bot.get_chat(chan)
                except:
                    pass
            except Exception as e:
                logger.error(e)
                collection.update_one({"_id": user}, {"$pull": {"kanal": chan}})
                logger.warning("Kanal silindi")
            else:    
                kayitli = kayitli + 1
                logger.info(WebAppDBUpdate(user, kbilgi, data_type="kanal_data_ready", kanal_id=str(chan)))
                if kayitli == len(mj['kanal']):
                    menu_mesaj += """└<a href="{}">{}</a>""".format("tg://privatepost?channel={}&post=9999999".format(chan[3:]), kbilgi.title)
                else:
                    menu_mesaj += """├<a href="{}">{}</a>\n""".format("tg://privatepost?channel={}&post=9999999".format(chan[3:]), kbilgi.title)
        menu_mesaj += f"\n\nToplam {kayitli} Kanalınız Bulunuyor."
        if get("https://pharex.dev/otoposterbot/veritabani?user={user}").text != "1":
            logger.info(WebAppDBUpdate(user))
        bot.send_message(chat, menu_mesaj, reply_markup=kanalmenumark(user))
        return KANALMENU
    if mesaj == "🛠 Ekstralar":
        try:
            tokenn = mj['token']
        except:
            bot.send_message(chat, """⛔ Bu menüyü görebilmek içim önce bir API kaydetmelisiniz!\n\n📝 <i>Lütfen</i> <a href="https://tr.link/member/tools/quick">burdan</a> <i>aldığınız API adresinizi gönderin</i>""", reply_markup=imark())
            return APIDEGISTIR
        WebAppDBUpdate(user)
        WebAppDBUpdate(user, mj['kanal'], data_type="kanal_datas", kanal_id=None, kontrol=True)
        bot.send_message(chat, "Ekstralar Menüsü", reply_markup=ekstralarmenumark(user))
        return EKSTRAMENU
    if mesaj == "🎛 Post Menü":
        try:
            tokenn = mj['token']
        except:
            bot.send_message(chat, """⛔ Bu menüyü görebilmek içim önce bir API kaydetmelisiniz!\n\n📝 <i>Lütfen</i> <a href="https://tr.link/member/tools/quick">burdan</a> <i>aldığınız API adresinizi gönderin</i>""", reply_markup=imark())
            return APIDEGISTIR
        bot.send_message(chat, "Post menüsü.", reply_markup=postmenumark(mj['ozel']))
        return POSTMENU
    if mesaj == "🔗 API Menü":
        try:
            tokenn = mj['token']
        except:
            bot.send_message(chat, """⛔ Bu menüyü görebilmek içim önce bir API kaydetmelisiniz!\n\n📝 <i>Lütfen</i> <a href="https://tr.link/member/tools/quick">burdan</a> <i>aldığınız API adresinizi gönderin</i>""", reply_markup=imark())
            return APIDEGISTIR
        if mj['altsite'] == "None" or mj['sira'] not in [2, 3, 1]:
            apimenu_mesaj = "<i>♦️Kayıtlı API: {}\nSite: {}</i>".format(mj['token'], site_isim(mj['site']))
        else:
            apimenu_mesaj = "<i>♦️Birincil API: {}\n  Birincil Site: {}\n  Alternatif API: {}\n  Alternatif Site: {}</i>".format(mj['token'], site_isim(mj['site']), mj['altapi'], site_isim(mj['altsite']))
        bot.send_message(chat, apimenu_mesaj, reply_markup=apimenumark())
        return APIMENU
            
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
        msg = bot.send_message(chat, """⛔ Bu menüyü görebilmek içim önce bir API kaydetmelisiniz!\n\n📝 <i></i> <a href="https://tr.link/member/tools/quick">buraya tıklayarak</a> <i>aldığınız API adresinizi gönderin</i>""", reply_markup=imark())            
        return APIDEGISTIR

    if mesaj == "🗑️ Kanal Sil":
        if len(kudat['kanal']) < 1:
            bot.send_message(chat, "Henüz bir kanal kaydetmemişsiniz!", reply_markup=kanalmenumark(user))
            return 
        bot.send_message(chat, "Silmek istediğiniz kanalı seçin.", reply_markup=gen_markup(user))
        return 
    if mesaj == "💠 Tür Değiştir":
        if len(kudat['kanal']) < 1:
            bot.send_message(chat, "Henüz bir kanal kaydetmemişsiniz!", reply_markup=kanalmenumark(user))
            return 
        bot.send_message(chat, "Türünü değiştirmek istediğiniz kanalı seçin.", reply_markup=icerikmark(user))
        return
    if mesaj == "🔶 Yeni Kanal Ekle":
        vip_uyeler = collection.find_one({"_id": 0})['vipuye']
        if len(kudat['kanal']) > 49 and not user in vip_uyeler:
            bot.send_message(chat, "<i>Üzgünüm en fazla 50 kanal kaydedebilirsiniz.</i>")
            return 
        bot.send_message(chat, """📝 <i>Lütfen kanalınızdan bir gönderi iletin.</i>""", reply_markup=imark())
        return KANALKAYDET
    if mesaj == "▶️ SFS Modu":
        if len(kudat['kanal']) < 1:
            bot.send_message(chat, "SFS moduna alabilmek için henüz bir kanal kaydetmemişsiniz!", reply_markup=kanalmenumark(user))
            return
        bot.send_message(chat, "<i>SFS moduna almak istediğiniz kanalı seçin. SFS moduna aldığınız kanala modu kapatana kadar post atılmaz!</i>\n\n", reply_markup=sfsmark(user))    
        return
    if mesaj == "↩️ Ana Menü" or mesaj == "❌ İptal":
        bot.send_message(chat, "<b>Biliyor muydunuz? -></b> "+"<i>"+choice(tips)+"</i>")
        bot.send_message(chat, "Ana Menü.", reply_markup=dugme(user))
        return ConversationHandler.END

    bot.send_message(chat, "<i>Lütfen alttaki butonları kullan</i>", reply_markup=kanalmenumark(user))

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
        bot.send_message(chat, "⛔ Bu menüyü görebilmek içim önce bir API kaydetmelisiniz!\n\n📝 <i></i> <a href='https://tr.link/member/tools/quick'>buraya tıklayarak</a> <i>aldığınız API adresinizi gönderin</i>", reply_markup=imark())
        return APIDEGISTIR
    if mesaj == "♻️ API değiştir":
        bot.send_message(chat, "Yeni API adresinizi girin.", reply_markup=imark())
        return APIDEGISTIR
    if mesaj == "🔗 Site değiştir":
        bot.send_message(chat, "<i>Kullanmak istediğiniz siteyi seçin</i>", reply_markup=sitemarkup())
        return
    if mesaj == "🤖 Alternatif Link":
        if type(audat["altapi"]) == list:
            bot.send_message(chat, "<b> Gelişmiş Alternatif Menüsü</b>", reply_markup=advaltmark(user))
        else:
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
        bot.send_message(chat, """⛔ Bu menüyü görebilmek içim önce bir API kaydetmelisiniz!\n\n📝 <i></i> <a href="https://tr.link/member/tools/quick">buraya tıklayarak</a> <i>aldığınız API adresinizi gönderin</i>""", reply_markup=imark())            
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
            for vak in poudat['vakit']:
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
        if poudat['site'] == "6":
            link = "https://gir.ist/qcu9xub"
        if poudat['site'] == "7":
            link = "https://urlably.com/qcu9xub"
        if poudat['site'] == "8":
            link = "https://cuty.io/Yil655h"
        if poudat['site'] == "0":
            link = "https://urlcik.com/bTdmM5F6"
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
            if poudat['altsite'] == "6":
                alink = "https://gir.ist/qcu9xub"
            if poudat['altsite'] == "7":
                alink = "https://urlably.com/qcu9xub"
            if poudat['altsite'] == "8":
                alink = "https://cuty.io/Yil655h"
            if poudat['altsite'] == "tpil":
                alink = "https://www.alternatif.link/ifsa"
            if poudat['altsite'] == "0":
                alink = "https://urlcik.com/bTdmM5F6"
        else:
            alink = "https://lnkload.com/2v5vy"
        if poudat['sablon'] == "1":
            bot.send_message(chat, "<b>Varsayılan Şablon:</b>\n\n🔥{aciklama} \n\n🔱 TIKLA 👉 {link} \n\n📛 SESİ AÇ 'a tıklamayı unutma", reply_markup=sablonmark(user))
        elif poudat['sablon'] == "2":
            bot.send_message(chat, "<b>Varsayılan Şablon:</b>\n\n{aciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {link}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 @TRPNDLinkGecmee", reply_markup=sablonmark(user))
        elif poudat['sablon'] == "9":
            bot.send_message(chat, "<b>Varsayılan Şablon:</b>\n\n{aciklama} \n\n𝙇𝙄𝙉𝙆🔗 {link} \n\n     𝙇𝙄𝙉𝙆🔗 {alink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 @TRPNDLinkGecmee", reply_markup=sablonmark(user))
        else:
            try:
                if poudat['sira'] == 1 or poudat['altsite'] == "tpil":
                    pst = poudat['sablon'].replace("{aciklama}", "{a}").replace("{link}", "{l}").replace("{alink}", "{al}").format(a=aciklama, l=link, al=alink)
                else:
                    pst = poudat['sablon'].replace("{aciklama}", "{a}").replace("{link}", "{l}").format(a=aciklama, l=link)
            except Exception as e:
                pst = f"Şablonunuz hatalı olduğun için görüntülenemedi lütfen Varsayılana döndürün veya yeni şablon ayarlayın.\n\n{str(e)}"
            try:
                bot.send_message(chat, f"<b>Şablonunuz böyle gözükecek:</b>\n\n{pst}", reply_markup=sablonmark(user))
            except:
                pst = f"Şablonunuz hatalı olduğun için görüntülenemedi lütfen Varsayılana döndürün veya yeni şablon ayarlayın.\n\n{str(e)}"
                bot.send_message(chat, f"<b>Şablonunuz böyle gözükecek:</b>\n\n{pst}", reply_markup=sablonmark(user))
        return
    if mesaj == "🔧 Kaynak":
        if len(poudat['kanal']) < 1:
            bot.send_message(chat, "Henüz bir kanal kaydetmemişsiniz.", reply_markup=postmenumark(poudat['ozel']))
            return
        kaynakmsg = bot.send_message(chat, "<code>Yükleniyor...</code>")
        bot.send_message(user, "Aşağıdaki menüden bir kanal seçin.", reply_markup=webappmark(user, -1))
        kaynakmsg.delete()
        return

    if mesaj == "♋️ Özel Kaynak Oluştur":
        bot.send_message(user, """<b>Özel Kaynak Hakkında Bilmeniz Gerekenler</b>\n\n<i>- Sadece bir tane Özel kaynak kullanabilirsiniz.\n- Başkaları da isterse sizin özel kaynağınızı kullanabilir.\n- Kaynağınız @OtoPosterBotLog'da gözükmeyecek.\n- Postlar, diğer kaynaklara göre daha yavaş atılır.\n- Özel kaynağa kısaltılmamış link atmanız gerekiyor. Kısaltılmış linkli post atarsanız bot linki geçmez direkt olarak kısaltılmış linki tekrar kısaltır.</i>""", reply_markup=ozelmark())
        return
    if mesaj == "♋️ Özel Kaynak Ayarları":
        kaynakmsg = bot.send_message(user, "<code>Yükleniyor...</code>")
        
        for m in OzelCol.find({}):
            if user in m['kanal']:
                try:
                    ozel_kaynak_bilgi = bot.get_chat(m['okaynak'])
                except:
                    kaynakmsg.edit_text("Bot kaynak kanalından çıkartıldığı için Özel Kaynak kullanılamıyor!", reply_markup=ozelkaynakmark(user, 0))
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
    if mesaj == "⏱ Zamanladıklarım":
        zjobs = context.job_queue.get_jobs_by_name(str(user))
        if len(zjobs) < 1:
            bot.send_message(chat, "Henüz bir post zamanlamamışsınız.", reply_markup=postmenumark(poudat['ozel']))
            return 
        bot.send_message(chat, "Silmek istediğiniz postu seçin.", reply_markup=jobmark(user, context))
        return 
    if mesaj == "⛓️ Elle Post Paylaş":
        if len(poudat['kanal']) < 1:
            bot.send_message(chat, "Lütfen önce bir kanal kaydedin.", reply_markup=postmenumark(poudat['ozel']))
            return
        bot.send_message(chat, "Paylaşmamı istediğin hazır postu ilet.", reply_markup=imark())
        return PATPOST
    if mesaj == "↩️ Ana Menü" or mesaj == "❌ İptal":
        bot.send_message(chat, "<b>Biliyor muydunuz? -></b> "+"<i>"+choice(tips)+"</i>")
        bot.send_message(chat, "Ana Menü.", reply_markup=dugme(user))
        return ConversationHandler.END

    bot.send_message(chat, "<i>Lütfen alttaki butonları kullan</i>", reply_markup=postmenumark(poudat['ozel']))

@send_typing_action
def ekstramenu(update, context):
    user = update.effective_user.id
    chat = update.effective_chat.id
    eudat = collection.find_one({"_id": user})
    mesaj = update.effective_message.text
    if user in kara:
        bot.send_message(chat, "🤓 Üzgünüm senin gibi aptal birisi için çalışmıyorum")
        return
    if mesaj == "📌 Post Sabitleme":
        if len(eudat['kanal']) == 0:
            bot.send_message(chat, "Bu modu kullanabilmek için önce bir kanal kaydetmelisin!")
            return
        WebAppDBUpdate(user)
        bot.send_message(chat, "<b>Paylaşılan postların otomatik olarak sabitlenmesini istersen bu modu açabilirsin.</b>", reply_markup=pinmark(user))
        return
    if mesaj == "🔁 Tekrarlı Post Paylaş":
        tekrarlipostlari = context.job_queue.get_jobs_by_name("ts"+str(user))
        if len(tekrarlipostlari) == 0:
            text_tekrarli = f"<b>Henüz hiç tekrarlı post ayarlamamışsınız.</b>"
        else:
            text_tekrarli = "<b>Tekrarlı Postlarınız;</b>\n\n"
        for tpost in tekrarlipostlari:
            tpoststr = str(tpost.job)
            tpp = tpoststr.find("run at: ")
            tapp = tpoststr.find("rval[")
            tskanisim = ""
            tskanerrorcount = 0
            if type(tpost.context['tskan']) == list:
                for tspostk in tpost.context['tskan']:
                    try:
                        tskanisim += bot.get_chat(tspostk).title + ", " if not tpost.context['tskan'].index(tspostk) in [len(tpost.context['tskan'])-1] and len(tpost.context['tskan']) != 1 else bot.get_chat(tspostk).title
                    except:
                        tskanerrorcount += 1
                if tskanerrorcount != 0:
                    if len(tpost.context['tskan']) != 1:
                        tskanisim += " ve {} ulaşılamayan kanal.".format(tskanerrorcount)
                    else:
                        tskanisim += "Kanalınıza ulaşılamadı!"
            else:
                try:
                    tskanisim = bot.get_chat(tpost.context['tskan']).title
                except:
                    tskanisim = "Kanalınıza ulaşılamadı."
            text_tekrarli += "<b>Sonraki tetiklenme tarihi:</b> {}\n<b>Paylaşılma aralığı:</b> {}\n<b>Başlık:</b> {}\n<b>Kanal(lar):</b> {}\n<b>Post Sayısı: {}</b>\n\n".format(tpoststr[tpp+8:tpp+27], tpoststr[tapp+4:tapp+13], tpost.context['baslik'], tskanisim, len(tpost.context["tspost"]))
        bot.send_message(chat, text_tekrarli, reply_markup=tekrarlipostmark(user, context))
        return
    if mesaj == "🍎 iOS Ban Kontrol":
        if len(eudat['kanal']) == 0:
            bot.send_message(chat, "Kontrol edebilmem için önce bir kanal kaydetmelisin!")
            return
        bot.send_message(chat, "Kontrol etmek istediğiniz kanalı seçin.", reply_markup=ioskontrolmark(user))
        return
    if mesaj == "↩️ Ana Menü" or mesaj == "❌ İptal":
        bot.send_message(chat, "<b>Biliyor muydunuz? -></b> "+"<i>"+choice(tips)+"</i>")
        bot.send_message(chat, "Ana Menü.", reply_markup=dugme(user))
        return ConversationHandler.END
    
    bot.send_message(chat, "<i>Lütfen alttaki butonları kullan</i>", reply_markup=ekstralarmenumark(user))

def panelbul(update, context):
    chat = update.effective_message.chat.id
    user = update.effective_message.from_user.id
    if update.effective_message.text == "❌ İptal":
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme(user))
        return ConversationHandler.END
    kaynak_user_dat = KaynakCol.find_one({"sahip": user})['kaynak']
    kaynak_kanal_dat = KaynakCol.find_one({"sahip": user})['kanal']
    if update.effective_message.forward_from_chat:
        bul_user = int(update.effective_message.forward_from_chat.id)
    elif update.effective_message.forward_from:
        bul_user = int(update.effective_message.forward_from.id)
    else:
        try:
            bul_user = int(update.effective_message.text)
        except:
            update.effective_message.reply_text("Geçersiz bir ID gönderdiniz!")
            return ConversationHandler.END
    if not str(bul_user) in kaynak_kanal_dat and bul_user < 0:
        update.effective_message.reply_text("Bu kanal sizin kaynağınıza bağlı değil.")
        return ConversationHandler.END
    if not bul_user in kaynak_user_dat and bul_user > 0:
        update.effective_message.reply_text("Bu kullanıcı sizin kaynağınızı kullanmıyor.")
        return ConversationHandler.END
    bulunanuser = collection.find_one({"kanal": {"$in": [str(bul_user)]}}) if bul_user < 0 else collection.find_one({"_id": bul_user})
    
    bultext = "<b>🔢 ID:</b> {}\n🏷 <b>İsim:</b> {}\n🖥 <b>Kaynağınıza Bağlı Kanalları:</b> \n".format(bulunanuser['_id'], bot.get_chat(bulunanuser['_id']).full_name)
    for bulkan in bulunanuser['kanal']:
        if not bulkan in KaynakCol.find_one({"sahip": user})['kanal']:
            continue
        try:
            if bulunanuser['kanal'].index(bulkan) == len(bulunanuser['kanal'])-1:
                bultext += "└" + kan_mention_html(bulkan) + "\n"
                break
            else:
                bultext += "├" + kan_mention_html(bulkan) + "\n"
        except:
            pass
    else:
        bultext += "Kaynığınıza bağlı hiç kanalı bulunmuyor."
    bot.send_message(chat, bultext)
    return ConversationHandler.END

def tekrarlipostbaslikayarla(update, context):
    user = update.effective_user.id
    chat = update.effective_chat.id
    if update.effective_message.text == "❌ İptal":
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme(user))
        return ConversationHandler.END
    context.user_data['tsbaslik'] = update.effective_message.text
    bot.send_message(chat, "Başlık ayarlandı, son olarak paylaşılmasını istediğiniz postu gönderin.", reply_markup=imark())
    return TSPOST

def tekrarlipostayarla(update, context):
    user = update.effective_user.id
    chat = update.effective_chat.id
    if update.effective_message.text == "❌ İptal":
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme(user))
        return ConversationHandler.END
    try:
        bot.delete_message(chat, context.user_data['lastts'])
    except:
        pass
    tfid = None
    if update.effective_message.text == None:
        tfid = update.effective_message.photo[-1].file_id if update.effective_message.photo else update.effective_message.effective_attachment.file_id
    if context.user_data.get("tspostdict", None) == None:
        context.user_data["tspostdict"] = {"baslik": context.user_data['tsbaslik'], "tsaat": context.user_data['tsaat'], "tskan": context.user_data['tskan'], "tspost": [{"tscaption": update.effective_message.caption_html_urled, "fid": tfid, "ptip": effective_message_type(update), "text": update.effective_message.text_html_urled}], "tsuser": user, "mod": None}
    else:
        context.user_data["tspostdict"]["tspost"].append({"tscaption": update.effective_message.caption_html_urled, "fid": tfid, "ptip": effective_message_type(update), "text": update.effective_message.text_html_urled})
    msz = bot.send_message(chat, "Postunuz eklendi!\n\nPost eklemeye devam etmek isterseniz iletmeye devam edin. Bu kadar yeterli ise alttaki butonlardan mod seçin.", reply_markup=tspostmod(user))
    context.user_data["lastts"] = msz.message_id
    return

def ozelk(update, context):
    user = update.effective_message.from_user.id
    chat = update.effective_message.chat.id
    if update.effective_message.text == "❌ İptal":
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme(user))
        return ConversationHandler.END
    if not update.effective_message.forward_from_chat:
        msz = bot.send_message(update.effective_message.chat.id, "Lütfen bana oluşturduğun kanaldan bir mesaj ilet.")
        return OZELKAYNAK
    kanal = update.effective_message.forward_from_chat.id
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
            bot.send_message(OzelCol.find_one({"okaynak": kanal})['_id'], "<i>Özel Kaynağınız 5 kişiyi geçtiği için artık postlarınızın 1/20'si benim API adresim ile kısaltılacaktır.</i>")
        bot.send_message(update.effective_message.chat.id, "<b>Özel Kaynak Kaydedildi!</b>", reply_markup=dugme(user))
        return ConversationHandler.END
    else:
        for koy in KaynakCol.find({}):
            if user in koy['kaynak']:
                KaynakCol.update_one({"_id": koy['_id']}, {"$pull": {"kaynak": user}})
        if OzelCol.find_one({"_id": user}) == None:
            OzelCol.insert_one({"_id": user, "okaynak": 546421354, "log": "yok", "kaynak": [], "icerik": "+18"}) 
        OzelCol.update_one({"_id": user}, {"$set": {"okaynak": kanal, "kanal": [user]}})
        collection.update_one({"_id": user}, {"$set": {"ozel": True, "kaynak": ["32"]}})
        bot.send_message(update.effective_message.chat.id, "<b>Özel Kaynak Oluşturuldu!\n\nKaynak butonuna basarak ayarlarını görebilirsin.</b>", reply_markup=dugme(user))
        return ConversationHandler.END

def ozellog(update, context):
    user = update.effective_message.from_user.id
    chat = update.effective_message.chat.id
    if update.effective_message.text == "❌ İptal":
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme(user))
        return ConversationHandler.END
    if not update.effective_message.forward_from_chat:
        msz = bot.send_message(update.effective_message.chat.id, "Lütfen bana oluşturduğun kanaldan bir mesaj ilet.")
        return OZELBOTLOG
    kanal = update.effective_message.forward_from_chat.id
    if KaynakCol.find_one({"_id": kanal}):
        mst = bot.send_message(chat, "Kaynak kanalını nasıl kaydedebilirim ki?")
        return OZELBOTLOG
    try:
        yetkiler = bot.get_chat_administrators(kanal)
    except:
        msg = bot.send_message(chat, "Botu kanalınızda yönetici eklememişsiniz.")
        return OZELBOTLOG
    OzelCol.update_one({"_id": user}, {"$set": {"log": kanal}})
    bot.send_message(update.effective_message.chat.id, "<b>Özel Botlog Kaydedildi!</b>", reply_markup=dugme(user))
    return ConversationHandler.END

def begenidegistir(update, context):
    mesaj = update.effective_message.text
    chat = update.effective_message.chat.id
    user = update.effective_message.from_user.id
    if mesaj == "❌ İptal":
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme(user))
        return ConversationHandler.END
    if len(mesaj.split("/")) < 1 or " " in mesaj or "//" in mesaj:
        update.effective_message.reply_text("Hatalı biçim! Lütfen örnekteki gibi gönderin.\n\nÖrnek;\n<code>❤️/⛔️/🥰</code>")
        return 
    collection.update_one({"_id": user}, {"$set": {"begeni": update.effective_message.text.split("/")}})
    update.effective_message.reply_text("Butonlarınız kaydedildi!", reply_markup=dugme(user))
    return ConversationHandler.END
    
def sabloniki(update, context):
    mesaj = update.effective_message.text_html_urled
    chat = update.effective_message.chat.id
    user = update.effective_message.from_user.id
    bnb = collection.find_one({"_id": user})
    if bnb == None:
        bot.send_message(chat, "Lütfen şablon kaydetmeden önce Kaydet butonu ile bilgilerinizi girin!", reply_markup=dugme(user))
    if update.effective_message.text == None:
        msg = bot.send_message(chat, """ ❌<i> Lütfen mesajınızda "{link}" ve "{aciklama}" bulunduğudan emin olun.</i> """)

        return SABLONA
    if update.effective_message.text == "❌ İptal":
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme(user))
        return ConversationHandler.END
    if bnb['sira'] == 1:
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
    chat = update.effective_message.chat.id
    bot.send_message(chat, "Ana Menü", reply_markup=dugme(chat))
    return ConversationHandler.END

def altakayit(update, context):
    amesaj = html.escape(update.effective_message.text)
    token = apiscraper(amesaj)
    user = update.effective_message.from_user.id
    chat = update.effective_message.chat.id
    if collection.find_one({"_id": user}) == None:
        bot.send_message(chat, "<b>Önce bir API kaydedin!</b>")
        return
    if update.effective_message.text == "❌ İptal" or update.effective_message.text == None:
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme(user))
        return ConversationHandler.END
    smesaj = context.user_data['asite']
    sss = context.user_data['sss']
    if sss == "gelismis":
        amesaj = [{"api": amesaj, "site": smesaj}]
        if "{alink}" in collection.find_one({"_id": user})["sablon"]:
            smesaj = "tpil"
        else:
            smesaj = "sirali"
        sss = 10
    if sss == "ekle":
        if amesaj in [m["api"] for m in collection.find_one({"_id": user})["altapi"]]:
            bot.send_message(chat, "Bu apiyi zaten kaydetmişsin!", reply_markup=imark())
            return
        amesaj = {"api": amesaj, "site": smesaj}
        collection.update_one({"_id": user}, {"$push": {"altapi": amesaj}})
    else:
        collection.update_one({"_id": user}, {"$set": {"altsite": str(smesaj), "altapi": amesaj, "sira": int(sss)}})
        seskisablon = collection.find_one({"_id": user})['sablon']
        if int(sss) in [2, 3]:
            collection.update_one({"_id": user}, {"$set": {"sablon": seskisablon.replace("{alink}", "∆∆")}})
        else:
            if "{alink}" in seskisablon:
                pass
            elif "∆∆" in seskisablon:
                collection.update_one({"_id": user}, {"$set": {"sablon": seskisablon.replace("∆∆", "{alink}")}})
            else:
                collection.update_one({"_id": user}, {"$set": {"sablon": "9"}})
            
    if sss == 10:
        bot.send_message(chat, "İlk Gelişmiş Alternatifiniz kaydedildi.\n\nAyarlarını görmek için <code>🤖 Alternatif Link</code> butonuna basabilirsin.", reply_markup=apimenumark())
        return APIMENU
    else:
        bot.send_message(chat, "✅ Alternatif API kaydedildi", reply_markup=dugme(user))
    return ConversationHandler.END

def postzaman(update, context):
    chat = update.effective_message.chat.id
    user = update.effective_message.from_user.id
    post_zaman_text = update.effective_message.text
    if post_zaman_text == None:
        bot.send_message(chat, "Gönderdiğiniz saatlerden biri veya birden fazlası yanlış.\n\nÖrnek;\n00:00\n01:00\n02:00\n03:00\n...", reply_markup=imark()) 
        return    
    if update.effective_message.text == "❌ İptal":
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
    try:
        token = html.escape(update.effective_message.text)
    except:
        return
    token = apiscraper(token)

    user = update.effective_message.from_user.id
    chat = update.effective_message.chat.id
    

    if user in kara:
        bot.send_message(chat, "🤓 Üzgünüm senin gibi aptal birisi için çalışmıyorum")
        return
    bnb = collection.find_one({"_id": user})
    if update.effective_message.text == None:
        msg = bot.send_message(chat, "Lütfen geçerli bir API verin.")
        return
    if update.effective_message.text == "❌ İptal":
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme(user))
        return ConversationHandler.END
    if "url=trlink" in token or "script" in token:
        mso = bot.send_message(chat, "❌ Geçersiz bir API verdiniz! Lütfen doğru bir API adresi verin.")
        return APIDEGISTIR
    key = {"_id": user, "token": token, "kanal": [], "sablon": "1", "kaynak": [], "site": "1", "altapi": "None", "altsite": "None", "sira": 0, "ozel": False, "pcount": 0, "time": 0, "vakit": 0, "eski": [], "begeni": [], "pin": [], "icerik": []}
    if token in apikara:
            blmsg = bot.send_message(blog, f"_ID: <a href='tg://user?id={user}'>{user}</a>\nYasaklı API tespit edildi -> {token}\n#id{user}\n#api{token}")
            bot.pin_chat_message(blog, blmsg.message_id)
    if bnb == None:
        kontrol = get("https://ay.live/api/?api={}&url=www.zort.com&format=text&alias=&ct=2".format(token)).text
        if kontrol == "":
            kontrol = get("https://www.pnd.tl/api?api={}&url=www.zort.com&format=text".format(token)).text
            key['site'] = "2"
        if kontrol == "":
            bot.send_message(chat, "❌ Geçersiz bir API verdiniz! Lütfen doğru bir API adresi verin.")
            return APIDEGISTIR
        collection.insert_one(key)
        bot.send_message(chat, "<b>🟢 API kaydedildi!</b>")
        bot.send_message(chat, "<i>📝 Lütfen kanalınızdan bir gönderi iletin.</i>", reply_markup=imark())
        bot.send_message(blog, yeniuserlog.format(user=user, token=token))
        return KANALKAYDET
    collection.update_one({"_id": user}, {"$set": {"token": token}})
    bot.send_message(chat, "<b>🟢 API kaydedildi!</b>", reply_markup=dugme(user))
    return ConversationHandler.END

def kanalkayit(update, context):
    chat = update.effective_message.chat.id
    user = update.effective_message.from_user.id
    y = collection.find_one({"_id": user})
    if update.effective_message.text == "❌ İptal":
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme(user))
        return ConversationHandler.END
    if not update.effective_message.forward_from_chat:
        bot.send_message(chat, "↪️ Bunun ne olduğu hakkında bir fikrim yok! Lütfen kanaldan herhangi bir gönderi iletin.", reply_markup=imark())
        return 
    kanal = update.effective_message.forward_from_chat.id
    if KaynakCol.find_one({"_id": kanal}):
        bot.send_message(chat, "Kaynak kanalını nasıl kaydedebilirim ki?", reply_markup=imark())
        return 
    if str(kanal) in y['kanal']:
        bot.send_message(chat, "Bu kanalı zaten kaydetmişsiniz")
        return 
    try:
        kanalbilgi = bot.get_chat(kanal)
        yetkiler = bot.get_chat_administrators(kanal)
    except:
        bot.send_message(chat, "Botu kanalınızda yönetici eklememişsiniz.")
        return 
    ytliler = []
    for y in yetkiler:
        if y.can_post_messages or y.status == "creator":
            ytliler.append(y.user.id)
    if not user in ytliler:
        bot.send_message(chat, "Bu kanal sizin değil 😠. Bu kanalı kaydedebilmeniz için kanalda Post Paylaşabilme yetkiniz olması gerekli.")
        return
    collection.update_one({"_id": user}, {"$push":{"kanal": str(kanal)}})
    IstekCol.update_one({"_id": 0}, {"$set": {str(kanal): {"user": user, "count": 0, "istekler": []}}})
    update.effective_message.reply_text("<b>🟢Kanalınız Kaydedildi.</b>", reply_markup=dugme(user))
    
    bot.send_message(blog, yenikanlog.format(user=user, kan=str(kanal)[3:], membersayi=bot.get_chat_member_count(kanal)))
    WebAppDBUpdate(user, str(kanal), data_type="kanal_data", kanal_id=str(kanal))
    WebAppDBUpdate(user)
    for kyt in KaynakCol.find({}):
        if user in kyt['kaynak']:
            if not str(kanal) in KaynakCol.find_one({"_id": kyt['_id']})['kanal']:
                KaynakCol.update_one({"_id": kyt['_id']}, {"$push": {"kanal": str(kanal)}})
    return ConversationHandler.END

def patzamansaat(update, context):
    verilen_saat = update.effective_message.text
    user = update.effective_message.from_user.id
    chat = update.effective_message.chat.id
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
        mstd = bot.send_message(chat, "Başka post paylaşacak mısınız?", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Evet", callback_data="devam"), InlineKeyboardButton("Hayır", callback_data="del")]]))
        return ConversationHandler.END

    bot.send_message(update.effective_message.chat.id, "Hangi kanalınıza gönderilecek.", reply_markup=patmark(update.effective_message.from_user.id))
    return ConversationHandler.END

def pat(update, context):
    chat = update.effective_message.chat.id
    user = update.effective_message.from_user.id
    if update.effective_message.text == "❌ İptal":
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme(user))
        return ConversationHandler.END
    if update.effective_message.text == "⏱ Zamanladığım Postlar":
        zjobs = context.job_queue.get_jobs_by_name(str(user))
        if len(zjobs) < 1:
            bot.send_message(chat, "Henüz bir post zamanlamamışsınız.", reply_markup=ReplyKeyboardMarkup(keyboard=[['❌ İptal'], ['⏱ Zamanladığım Postlar']], one_time_keyboard=True, resize_keyboard=True, selective=True))
            return 
        bot.send_message(chat, "Silmek istediğiniz postu seçin.", reply_markup=jobmark(user, context))
        return 
    if update.effective_message.text:
        msg = bot.send_message(chat, "Lütfen paylaşmamı istediğin postu at")
        return PATPOST
    if update.effective_message.caption == None:
        msg = bot.send_message(chat, "Lütfen paylaşmamı istediğin postu at")
        return PATPOST
    mesaj = update.effective_message.caption
    fid = update.effective_message.photo[0].file_id if update.effective_message.photo else update.effective_message.effective_attachment.file_id
    if update.effective_message.video:
        ptip = "video"
    elif update.effective_message.photo:
        ptip = "photo"
    elif update.effective_message.animation:
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
    if psira == 2:
        ptoken = paltapi
        psite = paltsite
        collection.update_one({"_id": user}, {"$set": {"sira": 3}})
    if psira == 3:
        collection.update_one({"_id": user}, {"$set": {"sira": 2}})
    try:
        if not paltapi == "None":
            while ptry < 10 and palink == " ":
                ptry += 1
                palink, pjson = linkkisalt(paltsite, paltapi, kplink, "+18")
                time.sleep(0.2)
        while ptry < 10 and plink == " ":
            ptry += 1
            plink, pjson = linkkisalt(psite, ptoken, kplink, "+18")
            time.sleep(0.2)
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
    except Timeout:
        bot.send_message(chat, "Kullandığınız link kısaltma servisine ulaşılamıyor.", reply_markup=dugme(user))
        return ConversationHandler.END
    except Exception as e:
        bot.send_message(chat, f"Bir sorun oluştu: \n\n{html.escape(str(e))}")
        logger.error(e)
        return
    context.user_data['psablon'] = psablon
    context.user_data['ptip'] = ptip
    context.user_data['fid'] = fid
    bot.send_message(chat, "Zamanlamak ister misiniz?", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Şimdi Gönder", callback_data="simdi")], [InlineKeyboardButton("Zamanla", callback_data="pzamanla")]]))
    return ConversationHandler.END
