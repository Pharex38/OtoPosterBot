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
from requests import get, Session
from .cancel import cancel
from .callback import *
from otoposter import *
from .misc import *

def start(update, context):
    user = update.message.from_user.id
    chat = update.message.chat.id
    bot = context.bot
    if user in kara:
        bot.send_message(chat, "🤓 Üzgünüm senin gibi aptal birisi için çalışmıyorum")
        return
    kat = collection.find_one({"_id": user})
    ref = update.message.text.split()[1] if len(update.message.text.split()) > 1 else None
    kyn = str(ref.split('k')[-1]) if len(update.message.text.split()) > 1 else None
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
    
    mention = "@"+update.message.from_user.username if update.message.from_user.username else update.message.from_user.first_name
    bot.send_message(chat, """
✨ <b>Merhaba {}!</b>

❔<b>Ne İşe Yarıyor? </b>
<i>Bu update.message sizin seçtiğiniz kaynak kanalında paylaşılan postların linklerini otomatik olarak kısaltıp sizin kanalınızda paylaşır.</i>

❔<b>Nasıl Kullanılır?</b>
<i>1. Adım: Botu kanlınıza yönetici olarak ekleyin.
2. Adım: Kaydet butonunu kullanarak bilgilerinizi kaydedin.
3. Adım: <b>KANALINIZDA</b> /onayla yazın.
4. Adım: Keyfini çıkarın.</i>

<b>❤️ Geliştirici & Sahip : @Pharex
👨🏻‍🔧 Fix & Eklentiler : @berce</b>
 
  📔        <b>@OtoPosterBotLog</b>
""".format(mention), disable_web_page_preview=True, reply_markup=dugme(user))

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
        global mahzen, bedava, evi, bashub, acikmi, muho, tutan
        mahzen = bot.get_chat(kaynaklar[0])
        bedava = bot.get_chat(kaynaklar[1])
        evi = bot.get_chat(kaynaklar[2])
        bashub = bot.get_chat(kaynaklar[3])
        acikmi = bot.get_chat(kaynaklar[4])
        muho = bot.get_chat(kaynaklar[5])
        tutan = bot.get_chat(kaynaklar[6])
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
            bot.send_message(chat, """<b>Özel Kaynak Kullandığınız için başka kaynak seçemezsiniz.</b>\n\n      <i>Özel Kaynağınız:</i><b> <a href="{}">{}</a>\n</b>      <i>Bu Kaynağı Toplam </i><code>{}</code> <i>Kişi Kullanıyor.</i>""".format(ozel_kaynak_bilgi.invite_link, ozel_kaynak_bilgi.title, kullanan_sayisi), reply_markup=kaynakmark(user))
            return
        bot.send_message(chat, """<b>Kullanmak istediğiniz kaynak kanalını seçin.</b>""", reply_markup=kaynakmark(user))
        return
    if mesaj == "📏 Şablon":
        link = "https://ay.live/vRpKVx"
        aciklama = "Pharex, lord adminin karısını sikerken lord adminn basıyor."
        alink = "https://pgg.fyi/X0DK3"
        if mj == None:
            bot.send_message(chat, "Lütfen önce bir API kaydedin.", reply_markup=dagme())
            return
        if mj['sablon'] == "1":
            bot.send_message(chat, "<b>Varsayılan Şablon:</b>\n\n🔥{aciklama} \n\n🔱 TIKLA 👉 {link} \n\n📛 SESİ AÇ 'a tıklamayı unutma", reply_markup=sablonmark(user))
        elif mj['sablon'] == "2":
            bot.send_message(chat, "<b>Varsayılan Şablon:</b>\n\n{aciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {link}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 #linkgec06", reply_markup=sablonmark(user))
        elif mj['sablon'] == "9":
            bot.send_message(chat, "<b>Varsayılan Şablon:</b>\n\n{aciklama} \n\n𝙇𝙄𝙉𝙆🔗 {link} \n\n     𝙇𝙄𝙉𝙆🔗 {alink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 #linkk_gecmee", reply_markup=sablonmark(user))
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
        kayitli = 0
        chat = update.message.chat.id
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
            
            return APIDEGISTIR
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
        if user != sahip:
            bot.send_message(chat, "Bu komut bakımda.")
            return
        bot.send_message(chat, "🥰Madem bu kadar çok istiyorsun. \n\n🏧Papara: <code>1666982412</code> \n🏦İninal: <code>4003140030544</code>")
        return
    if mesaj == "⛓️ Elle Post Paylaş":
        if mj == None:
            bot.send_message(chat, "Lütfen önce bir API kaydedin.", reply_markup=dagme())
            return
        if len(mj['kanal']) < 1:
            bot.send_message(chat, "Lütfen önce bir kanal kaydedin.", reply_markup=dagme())
            return
        msg = bot.send_message(chat, "Paylaşmamı istediğin hazır postu ilet.", reply_markup=imark())
        
        return PATPOST
        
    kisi = collection.find_one({"_id": user})
    if kisi == None:
        bot.send_message(chat, "<i>Lütfen alttaki butonları kullan</i>", reply_markup=dagme())
        return
    bot.send_message(chat, "<i>Lütfen alttaki butonları kullan</i>", reply_markup=dugme(user))
    


def sabloniki(update, context):
    mesaj = update.message.text
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
    sss = context.user_data['sistem']
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
    key = {"_id": user, "token": token, "kanal": [], "sablon": "1", "kaynak": ["1"], "site": "1", "altapi": "None", "altsite": "None", "sira": "0", "ozel": False}
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
        bot.send_message(chat, "<i>📝 Lütfen kanalınızdan bir gönderi iletin.</i>", reply_markup=imark())
        bot.send_message(blog, f"#YENİ_KULLANİCİ\nID: {user}\nAPI: {token}\nK.ADI: {update.message.from_user.username}")
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

def kayitapi(update, context):
    chat = update.message.chat.id
    mesaj = update.message.text
    user = update.message.from_user.id
    ka = collection.find_one({"_id": user})
    vip_uyeler = collection.find_one({"_id": 0})['vipuye']
    if mesaj == "🗑️ Kanal Sil":
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
        if len(bol['kanal']) > 2 and not user in vip_uyeler:
            bot.send_message(chat, "<i>Üzgünüm en fazla 3 kanal kaydedebilirsiniz.</i>")
            return 
        bot.send_message(chat, """📝 <i>Lütfen kanalınızdan bir gönderi iletin.</i>""", reply_markup=imark())

        return KANALKAYDET
    bot.send_message(chat, "Lütfen alttaki butonları kullanıns.", reply_markup=markupp())

def pat(update, context):
    chat = update.message.chat.id
    user = update.message.from_user.id
    if update.message.text == "❌ İptal":
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme(user))
        return ConversationHandler.END
    if update.message.text:
        msg = bot.send_message(chat, "Lütfen paylaşmamı istediğin postu at")
        return PATPOST
    if update.message.caption == None:
        msg = bot.send_message(chat, "Lütfen paylaşmamı istediğin postu at")
        return PATPOST
    mesaj = update.message.caption
    if update.message.video:
        fid = update.message.video.file_id
        ptip = "video"
    if update.message.photo:
        fid = update.message.photo[0].file_id
        ptip = "photo"
    if update.message.animation:
        fid = update.message.animation.file_id
        ptip = "animation"
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
            psablon = f"{paciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {plink}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 #linkgec06"
        elif psablon == "9":
            psablon = f"{paciklama} \n\n𝙇𝙄𝙉𝙆🔗 {plink} \n\n     𝙇𝙄𝙉𝙆🔗 {palink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 #linkk_gecmee"
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
        bot.send_message(chat, "Postunuz gönderildi.", reply_markup=dugme(user))
        return ConversationHandler.END
    
    context.user_data['psablon'] = psablon
    context.user_data['ptip'] = ptip
    context.user_data['fid'] = fid
    if pret:
        bot.send_message(chat, "Post Hazırlandı!", reply_markup=dugme(user))
        bot.send_message(chat, "<i>Postun gönderilmesini istediğin kanalı seç.</i>", reply_markup=patmark(user))
        return ConversationHandler.END
    else:
        bot.send_message(chat, "Bir hata oluştu")

def altcall(call, context):
    user = call.effective_user.id
    chat = call.effective_chat.id
    mesajid = call.effective_message.message_id
    smesaj = str(call.callback_query.data.split("-")[1])
    sss = str(call.callback_query.data.split("-")[2])
    context.user_data['asite'] = smesaj
    context.user_data['sistem'] = sss
    call.callback_query.answer(call.callback_query.id, "✅ Site Kaydedildi!")
    bot.edit_message_text("✅ Alternatif site kaydedildi.", user, mesajid)
    bot.send_message(chat, "📝 Alternatif API adresinizi gönderin.", reply_markup=imark())
    return ALTAPI

conv_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.update.message & ~Filters.command, menu)],
    states={ 
        ALTMENU: [MessageHandler(Filters.text & Filters.update.message, kayitapi)], 
        APIDEGISTIR: [MessageHandler(Filters.text & Filters.update.message, apikayit)],
        KANALKAYDET: [MessageHandler(~Filters.command & Filters.update.message, kanalkayit)],
        SABLON: [MessageHandler(Filters.text & Filters.update.message, sabloniki)],
        PATPOST: [MessageHandler(~Filters.command & Filters.update.message, pat)]
        },
    fallbacks=[MessageHandler(Filters.regex('^↩️ Ana Menü$') & Filters.update.message, cancel), CommandHandler('start', start, filters=~Filters.update.edited_message)]
    )

altconver = ConversationHandler(
    entry_points=[CallbackQueryHandler(altcall, pattern="^asite(.*)")],
    states={
        ALTAPI: [MessageHandler(Filters.text & Filters.update.message, altakayit)]
        },
    fallbacks=[MessageHandler(Filters.regex('^↩️ Ana Menü$') & Filters.update.message, cancel), CommandHandler('start', start, filters=~Filters.update.edited_message)],
    per_message=False)

dispatcher.add_handler(conv_handler)
dispatcher.add_handler(altconver)


