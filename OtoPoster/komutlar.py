from . import *
from .misc import *
from .jobs import *
from .markups import *
from .poster import poster_job, ozel_poster_job

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

❔<b>Senin Kazancın Nedir?</b>
<i>Kanalınıza atılan <b>yirmi</b> linkten birisi benim API adresim ile kısaltılır.</i>

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
    exe_kullanan_sayisi, ozel_kaynak_kullanan_sayisi, pubiza_kullanan_sayisi, ouo_kullanan_sayisi, trlink_kullanan_sayisi, pnd_kullanan_sayisi, girist = 0, 0, 0, 0, 0, 0, 0
    if not user in [sahip,fixer]:
        bot.send_message(chat, "Sen benim sahibim değilsin!")
        return
    msg = bot.send_message(chat, "<code> Veriler toplanıyor...</code>")
    kullanicilar = [x for x in collection.find({})]
    for kullanici in kullanicilar:
        try:
            kullanici['site']
        except:
            continue
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
            if kullanici['ozel']:
                ozel_kaynak_kullanan_sayisi += 1
            for kul in kullanici['kanal']:
                if not kul in kum:
                    kum.append(kul)
                    sleep(0.5)
                    kanals += 1
                    try:
                        uye = bot.get_chat_members_count(kul)
                        print(uye)
                    except RetryAfter as after:
                        sleep(after.retry_after)
                    except Exception as e:
                        logger.error(e)
                        if str(e).find("Chat is not found") != -1 or str(e).find("Need administrator") != -1 or str(e).find("bot is not") != -1:
                            sleep(1)
                    else:
                        toplam += uye
    toplam = toplam / 1000
    toplam = str(round(toplam, 1))+"K" if round(toplam, 1) < 1000 else str(round(toplam / 1000, 2))+"M"
    stat_text = f"Toplam Kullanıcı Sayısı: {users}\nToplam Kayıtlı Kanal Sayısı: {kanals}\nToplam Kitle: {toplam}\n\n<b>Sitelerin Toplam Kullanıcı Sayısı;</b>\nTRLink: {trlink_kullanan_sayisi}\nPND.TL: {pnd_kullanan_sayisi}\nExe.io: {exe_kullanan_sayisi}\nOuo.io: {ouo_kullanan_sayisi}\nPubiza: {pubiza_kullanan_sayisi}\n\n<b>Kaynakların toplam Kullanıcı Sayıları:</b>\n"
    statscount = 0
    for kstat in KaynakCol.find({}):
        getskaynak = bot.get_chat(kstat['_id'])
        kkitle = 0
        for sl in kstat["kaynak"]:
            for slb in collection.find_one({"_id": sl})['kanal']:
                try:
                    amc = bot.get_chat_members_count(slb)
                except RetryAfter as after:
                    sleep(after.retry_after)
                except Exception as e:
                    logger.error(e)
                else:
                    kkitle += amc
                    sleep(1)
        stat_text += "{} -> {}\nKitle: {}".format(getskaynak.title, len(kstat['kaynak']), round(kkitle / 1000, 1))
    ozel_text = f"Özel kullanan: {ozel_kaynak_kullanan_sayisi}"
          
    bot.edit_message_text(stat_text+ozel_text, chat, msg.message_id)

def IptalPoster(update, context):
    user = update.effective_user.id
    try:
        ipt = KaynakCol.find_one({"sahip": user})['_id']
    except:
        if user == sahip:
            ipt = context.args[0]
        else:
            return
    collection.update_one({"_id": 0}, {"$push": {"iptal": str(ipt)}})
    update.effective_message.reply_text("Postunuz İptal Edildi!")

def cekilis(update, context):
    user = update.effective_user.id
    try:
        cekilis_text = update.effective_message.reply_to_message.text_html_urled
    except:
        update.effective_message.reply_text("Bir çekiliş mesajı vermelisiniz.")
        return
    collection.update_one({"_id": 0}, {"$set": {"cekilis": []}})
    context.bot_data['cekilis'] = cekilis_text
    bot.send_message(user, "Çekiliş başladı")
    cek_msg = bot.send_message(botlog, cekilis_text.format("0"), reply_markup=cekilismark())
    context.bot_data['cekilis_chat'] = botlog
    context.bot_data['cekilis_mid'] = cek_msg.message_id
    context.bot_data['durak'] = False
    context.bot_data['sahip'] = int(context.args[0])

def duraklat(update, context):
    try:
        durak = context.bot_data['durak']
    except:
        context.bot_data['durak'] = True
        durak = context.bot_data['durak']
    if durak:
        context.bot_data['durak'] = False
    else:
        context.bot_data['durak'] = True
    update.effective_message.reply_text(f"{context.bot_data['durak']}")

def sonuclandir(update, context):
    katilimcilar = list(collection.find_one({"_id": 0})['cekilis'])
    sonuc_text = update.effective_message.reply_to_message.text_html_urled
    kazcount = 0
    kazananlar = ""
    yedekler = ""
    cek_chat = context.bot_data['cekilis_chat']
    cek_mid = context.bot_data['cekilis_mid']
    cek_k_no = context.bot_data['sahip']
    while kazcount != int(context.args[0]):
        kazananid = choice(katilimcilar)
        cek_dat = collection.find_one({"_id": kazananid})
        if cek_dat == None:
            continue
        if len(cek_dat['kanal']) == 0 or not kazananid in KaynakCol.find_one({"sahip": cek_k_no})['kaynak']:
            continue
        for cekkan in cek_dat['kanal']:
            if cekkan in KaynakCol.find_one({"sahip": cek_k_no})['kanal']:
                if bot.get_chat_members_count(cekkan) > 501:
                    kazadi = bot.get_chat(kazananid)
                    kazananlar += '<a href="tg://user?id={}">{}</a>\n'.format(kazananid, "@"+str(kazadi.username) if kazadi.username else kazadi.first_name)
                    katilimcilar.remove(kazananid)
                    kazcount += 1
                    break
    kazcount = 0
    while kazcount != int(context.args[1]):
        kazananid = choice(katilimcilar)
        cek_dat = collection.find_one({"_id": kazananid})
        if cek_dat == None:
            continue
        if len(cek_dat['kanal']) == 0 or not kazananid in KaynakCol.find_one({"sahip": cek_k_no})['kaynak']:
            continue
        for cekkan in cek_dat['kanal']:
            if cekkan in KaynakCol.find_one({"sahip": cek_k_no})['kanal']:
                if bot.get_chat_members_count(cekkan) > 501:
                    kazadi = bot.get_chat(kazananid)
                    yedekler += '<a href="tg://user?id={}">{}</a>\n'.format(kazananid, "@"+str(kazadi.username) if kazadi.username else kazadi.first_name)
                    katilimcilar.remove(kazananid)
                    kazcount += 1
                    break
    if kazananlar == "":
        update.effective_message.reply_text("Uygun şartlarda kazanan bulunamadı!")
        return
    if yedekler == "":
        update.effective_message.reply_text("Uygun şartlarda yedek bulunamadı!")
        return
    try:
        bot.send_message(sahip, sonuc_text.format(k=kazananlar, y=yedekler))
    except Exception as e:
        update.effective_message.reply_text(str(e))
    else:
        update.effective_message.reply_text("Çekiliş sonuçlandırıldı.")
    
def joblist(update, context):
    jobs = context.job_queue.jobs()
    context.job_queue.run_once(jobyedekleme, when=1, name="yedekleme")
    for jok in jobs:
        if True:
        #if not str(jok.name) in ignorejob:
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
            bot.send_message(update.message.chat.id, jason.dumps(c, indent=2, ensure_ascii=False))
            for kkkkk in KaynakCol.find({}):
                if c['_id'] in kkkkk['kaynak']:
                    bot.send_message(update.message.chat.id, str(kkkkk['no']))
    except Exception as e:
        print(e)
    try:
        cntt = collection.find({"token": cnt})
        for c in cntt:
            bot.send_message(update.message.chat.id, jason.dumps(c, indent=2, ensure_ascii=False))
    except:
        pass
    try:
        cntt = collection.find({"altapi": cnt})
        for c in cntt:
            bot.send_message(update.message.chat.id, jason.dumps(c, indent=2, ensure_ascii=False))
    except:
        pass
    try:
        cntt = collection.find({})
        for c in cntt:
            if cnt in c['kanal']:
                bot.send_message(update.message.chat.id, jason.dumps(c, indent=2, ensure_ascii=False))
    except:
        pass
    try:
        cntt = collection.find({"site": cnt})
        for c in cntt:
            bot.send_message(update.message.chat.id, jason.dumps(c, indent=2, ensure_ascii=False))
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
    for kkkkk in KaynakCol.find({}):
        if user in kkkkk['kaynak']:
            KaynakCol.update_one({"_id": kkkkk['_id']}, {"$pull": {"kaynak": user}})
    collection.delete_one({"_id": kimi})
    bot.send_message(chat, "<b>Bilgileriniz Silindi!</b>", reply_markup=dugme(user))

def kpostsil(update, context):
    chat = update.effective_chat.id
    if KaynakCol.find_one({"_id": chat}) == None:
        return
    mesid = update.effective_message.reply_to_message.message_id if update.effective_message.reply_to_message else None
    if mesid == None:
        bot.send_message(chat, "Silmek istediğiniz postu yanıtlayın.")
        return
    collection.update_one({"_id": 0}, {"$push": {"iptal": str(chat)}})
    psmg = bot.send_message(chat, "<code>Siliniyor...</code>")
    try:
        data = dict(db[str(chat)].find_one({"_id": mesid}))
        data['pids']
    except:
        data = db[str(chat)].find({"mesih": mesid})
    spcount = 0
    for kpsd in KaynakCol.find_one({"_id": chat})['kaynak']:
        try:
            kpsd = collection.find_one({"_id": kpsd})
            collection.update_one({"_id": kpsd['_id']}, {"$set": {"pcount": kpsd['pcount']-1}})
        except:
            pass
    if type(data) == dict:
        data = data['pids']
    for d in data:
        try:
            bot.delete_message(d['chat'], d['pid'])
        except Exception as e:
            logger.error(e)
        else:
            spcount += 1
    if spcount == 0:
        psmg.edit_text(f"Post silinimedi!")
    else:
        psmg.edit_text(f"{spcount} Post Silindi.")
    collection.update_one({"_id": 0}, {"$pull": {"iptal": str(chat)}})

def cpostsil(update, context):
    chat = update.message.chat.id
    if chat != sahip:
        return

    hedef = "-100"+update.message.text.split("/")[-2] if len(update.message.text.split()) > 1 else None
    mesid = int(update.message.text.split("/")[-1]) if len(update.message.text.split()) > 1 else None
    if hedef == None or mesid == None:
        return
    try:
        data = dict(db[str(hedef)].find_one({"_id": mesid}))
        data['pids']
    except:
        data = db[str(hedef)].find({"mesih": mesid})
    psmg = bot.send_message(chat, "<code>Siliniyor...</code>")
    spcount = 0
    for kpsd in KaynakCol.find_one({"_id": int(hedef)})['kaynak']:
        try:
            kpsd = collection.find_one({"_id": kpsd})
            collection.update_one({"_id": kpsd['_id']}, {"$set": {"pcount": kpsd['pcount']-1}})
        except:
            pass
    if type(data) == dict:
        data = data['pids']
    for d in data:
        try:
            bot.delete_message(d['chat'], d['pid'])
        except Exception as e:
            logger.error(e)
        else:
            spcount += 1
    psmg.edit_text(f"{spcount} Post Silindi.")

def viple(update, context):
    global postsirasi
    chat = update.message.chat.id
    if len(context.args) < 1:
        context.job_queue.run_once(gunluk, name="gunluk", when=3)
        return
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

def posterkomut(update, context):
    context.bot_data['pochat'] = int(context.args[0])
    update.effective_message.reply_text("Ayarlandı")

def posterkomut2(update, context):
    global postsirasi, opostsirasi
    pochat = update.effective_message.forward_from_chat.id if update.effective_message.forward_from_chat else context.bot_data['pochat']
    # Ana Kaynaklar
    if KaynakCol.find_one({"_id": pochat}) != None:
        logger.warning(f"{update.effective_message.chat.title} Postu sıraya eklendi.")
        postdict = {"chatid": pochat, "update": update, "groupid": update.effective_message.media_group_id, "poster": True}
        ind = len(context.job_queue.get_jobs_by_name("anaposter"))
        whn = 130 if 2 <= ind < 4 else 10
        if 5 >= ind > 3:
            whn = 230
        if 7 >= ind > 5:
            whn = 330
        if 9 >= ind > 7:
            whn = 430
        if ind > 9:
            whn = 530
        for poj in context.job_queue.get_jobs_by_name("anaposter"):
            if poj.context[0]['groupid'] == update.effective_message.media_group_id and poj.context[0]['chatid'] == pochat:
                poj.context.append(postdict)
                return
        context.job_queue.run_once(poster_job, when=whn, name="anaposter", context=[postdict]) 
    # Özel Kaynaklar
    elif OzelCol.find_one({"okaynak": pochat}) != None:
        logger.warning(f"[ÖZEL] {update.effective_message.chat.title} Postu sıraya eklendi.")
        opostdict = {"chatid": pochat, "update": update, "groupid": update.effective_message.media_group_id, "poster": True}
        oind = len(context.job_queue.get_jobs_by_name("ozelposter"))
        owhn = 20 if 2 <= oind < 4 else 10
        if 5 >= oind > 3:
            owhn = 30
        if 7 >= oind > 5:
            owhn = 40
        if 9 >= oind > 7:
            owhn = 50
        if oind > 9:
            owhn = 60
        for opoj in context.job_queue.get_jobs_by_name("ozelposter"):
            if opoj.context[0]['groupid'] == update.effective_message.media_group_id and opoj.context[0]['chatid'] == pochat:
                opoj.context.append(opostdict)
                return
        context.job_queue.run_once(ozel_poster_job, when=owhn, name="ozelposter", context=[opostdict])

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
                    dmsg = update.effective_message.reply_to_message.copy(kullanici['_id'])
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
    for ts in tumks:
        try:
            bot.delete_message(ts['_id'], ts['mid'])
        except Exception as e:
            logger.error(e)
        else:
            sd += 1
            db[str(chat)].delete_one({"_id": ts['_id']})
    bot.send_message(chat, "{} Duyuru Mesajı Silindi!".format(sd))
        
def post(update, context):
    chat = update.effective_message.chat.id
    mid = update.effective_message.message_id
    msj = update.effective_message.reply_text("Tamamdır!")
    sleep(1.5)
    mids = msj.message_id
    try:
        bot.delete_message(chat, mid)
        bot.delete_message(chat, mids)
    except:
        pass

def zaman(update, context):
    chat = update.message.chat.id
    user = update.message.from_user.id
    msj = update.message.reply_to_message.text if update.message.reply_to_message else update.message.text.replace("/zaman ", "")
    if len(msj) >= 200:
        bot.send_message(chat, "Mesajınız çok uzun.")
        return
    if msj == None:
        bot.send_message(chat, "Bu komut bir mesajı yanıtlayarak kullanılmalıdır.")
        return
    try:
        KaynakCol.update_one({"sahip": user}, {"$set": {"zaman": msj}})
    except:
        bot.send_message(user, "Kaynağınız bulunmuyor.")
        return
    else:
        bot.send_message(chat, "Kaydedildi.")

def kaynakpanel(update, context):
    user = update.effective_user.id
    panelkaynak = KaynakCol.find_one({"sahip": user})
    if panelkaynak == None:
        return
    try:
        panelkaynakkanal = bot.get_chat(panelkaynak['_id'])
    except:
        panelkaynakkanalisim = "Kaynağa ulaşılamıyor."
    else:
        panelkaynakkanalisim = panelkaynakkanal.title
    bot.send_message(user, "<b>{} Kaynak Paneli;</b>\n\nToplam Kullanıcı: {}\nToplam Kanal: {}".format(panelkaynakkanalisim, len(panelkaynak['kaynak'], len(panelkaynak['kanal']))) ,reply_markup=panelkaynakmark(user))