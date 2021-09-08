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
    cek_ = bot.send_message(botlog, cekilis_text.format("0"), reply_markup=cekilismark())
    context.bot_data['cekilis_chat'] = botlog
    context.bot_data['cekilis_mid'] = cek_.message_id
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
    bulko = collection.find_one(dict(context.args[0]))
    if bulko:
        update.effective_message.reply_text(jason.dumps(bulko, indent=2, ensure_ascii=False))
    else:
        update.effective_message.reply_text("Kriterlerinize uygun sonuç bulunamadı!")

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
        for kpsd in KaynakCol.find_one({"_id": chat})['kaynak']:
            try:
                kpsd = collection.find_one({"_id": kpsd})
                collection.update_one({"_id": kpsd['_id']}, {"$set": {"pcount": kpsd['pcount']-1}})
            except:
                pass
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
    if type(data) == dict:
        data = data['pids']
    for d in data:
        try:
            bot.delete_message(d['chat'], d['pid'])
        except Exception as e:
            logger.error(e)
        else:
            spcount += 1
    if spcount > 2:
        for kpsd in KaynakCol.find_one({"_id": int(hedef)})['kaynak']:
            try:
                kpsd = collection.find_one({"_id": kpsd})
                collection.update_one({"_id": kpsd['_id']}, {"$set": {"pcount": kpsd['pcount']-1}})
            except:
                pass
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
    msj = update.message.reply_to_message.text if update.message.reply_to_message and "/zaman" in update.effective_message.text else update.message.text.replace("/zaman ", "")
    if update.effective_message.text == "❌ İptal":
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme(user))
        return ConversationHandler.END
    if len(msj) >= 200:
        bot.send_message(chat, "Mesajınız çok uzun.")
        return
    try:
        KaynakCol.update_one({"sahip": user}, {"$set": {"zaman": msj}})
    except:
        bot.send_message(user, "Kaynağınız bulunmuyor.")
        return
    else:
        bot.send_message(chat, "Kaydedildi.")

def yenikaynakkomutu(update, context):
    user = update.effective_user.id
    kaynak_degisken = KaynakCol.find_one({"_id": user})
    kaynak_degisken['kaynak'] = []
    kaynak_degisken['kanal'] = []
    kaynak_degisken['zaman'] = "Henüz ayarlanmamış."
    kaynak_degisken['sahip'] = int(context.args[0])
    kaynak_degisken['_id'] = int(context.args[1])
    kaynak_degisken['icerik'] = str(context.args[2])
    for zorp in range(1, 80):
        if KaynakCol.find_one({"no": zorp['no']}) == None:
            kaynak_degisken['no'] = zorp
            break
    KaynakCol.insert_one(kaynak_degisken)
    bot.send_message(user, str(jason.dumps(kaynak_degisken, indent=2, ensure_ascii=False)))

def SetKomutu(update, context):
    if len(context.args) != 4:
        update.effective_message.reply_text("Eksik parametre!")
        return
    deger = update.effective_message.reply_to_message.text_html_urled
    if context.args[3] == "dict":
        deger = dict(deger)
    elif context.args[3] == "list":
        deger = list(deger)
    elif context.args[3] == "int":
        deger = int(deger)
    elif context.args[3] == "str":
        deger = str(deger)
    collection.update_one({"_id": int(context.args[0])}, {"$"+str(context.args[1]): {str(context.args[2]): deger}})
    update.effective_message.reply_to_message.reply_text("Set!")

def kaynakpanel(update, context):
    user = update.effective_user.id
    panelkaynak = KaynakCol.find_one({"sahip": user})
    if panelkaynak == None:
        return
    panelmessage = bot.send_animation(user, animation="CgACAgQAAxkBAAEMT_lhLrYhZpgOT6y8AQZRPB-RpHRpaQACNgIAAmbf3VKP6eJ5oebSyiAE",  caption="<code>Yükleniyor</code>")
    try:
        panelkaynakkanal = bot.get_chat(panelkaynak['_id'])
    except:
        panelkaynakkanalisim = "Kaynağa ulaşılamıyor."
    else:
        panelkaynakkanalisim = panelkaynakkanal.title
    try:
        panel_text = context.user_data['panel_text']
    except:
        panco = []
        pankanmember = 0
        for pankan in panelkaynak['kanal']:
            if not pankan in panco:
                try:
                    pankanmember += bot.get_chat_members_count(pankan)
                except RetryAfter as panafter:
                    sleep(panafter.retry_after)
                    try:
                        pankanmember += bot.get_chat_members_count(pankan)
                    except:
                        continue
                except:
                    continue
                else:
                    panco.append(pankan)
        panel_text = "<b>{} Kaynak Paneli;</b>\n\n👥Toplam Kullanıcı: {}\n📢Toplam Kanal: {}\n💿Şimdiye Kadar Paylaştığınız Post Sayısı: {}\n🙋Toplam Kitle: {}\n\n🔗Referans Linkiniz: {}".format(panelkaynakkanalisim, len(panelkaynak['kaynak']), len(panco), db[str(panelkaynak['_id'])].count_documents({}), str(round(pankanmember / 1000, 1))+"K", "https://telegram.me/OtoPosterBot?start=Kaynak"+str(panelkaynak['no']))
        context.user_data['panel_text'] = panel_text
    for cleanjob in context.job_queue.get_jobs_by_name("panelcleaner"):
        if cleanjob.context == user:
            break
    else:
        context.job_queue.run_once(panelcleaner, when=3600, name="panelcleaner", context=user)
        
    tarihnow = datetime.datetime.now(pytz.timezone('Europe/Istanbul')) - datetime.timedelta(days = 6)
    ylab = []
    aykaccekiyo = calendar.monthrange(tarihnow.year, tarihnow.month-1 if tarihnow.month != 1 else 12)[1] + 1
    buaykaccekiyo = calendar.monthrange(tarihnow.year, tarihnow.month if tarihnow.month != 1 else 12)[1]
    xlab = []
    for g in dict(panelkaynak['grafik']).keys():
        if int(g) >= tarihnow.day-1 and tarihnow.day-1 <= buaykaccekiyo:
            ylab.append(str(g.zfill(2))+"/"+str(tarihnow.month).zfill(2))
            if len(ylab) == 7:
                break
    else:
        if len(ylab) != 7:
            for g in dict(panelkaynak['grafik']).keys():
                if int(g) >= 1:
                    ylab.append(str(g.zfill(2))+"/"+str(tarihnow.month).zfill(2))
                    if len(ylab) == 7:
                        break
    vals = list(panelkaynak['grafik'].values())
    for icc in range(7):
        try:
            xlab.append(vals[tarihnow.day-1+icc]['user']) 
        except IndexError:
            xlab.append(vals[tarihnow.day-1+icc-aykaccekiyo]['user'])
            
    pyplot.style.use(['dark_background'])
    fig, plot = pyplot.subplots()
    plot.bar(ylab, xlab, label="Kullanıcı Sayısı", width=0.8)
    xlab = []
    for icc in range(7):
        try:
            xlab.append(vals[tarihnow.day-1+icc]['kanal'])
        except IndexError:
            xlab.append(vals[tarihnow.day-1+icc-aykaccekiyo]['kanal'])
            
    plot.bar(ylab, xlab, label="Kanal Sayısı", align="edge", width=0.4)
    plot.set_title(panelkaynakkanalisim)
    plot.set_xlabel('7 Günlük Grafik')
    plot.legend(loc=3)
    fig.savefig("grafik.png")
    grafikpng = open("grafik.png", "rb")
    panelmessage.edit_media(InputMediaPhoto(media=grafikpng, caption=None))
    grafikpng.close()
    
    panelmessage.edit_caption(panel_text, reply_markup=panelkaynakmark(user))