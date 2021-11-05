from . import *
from .misc import *


def jobyedekleme(context):
    global ptimeout
    collection.update_one({"_id": 0}, {"$set": {"jobs": []}})
    ptimeout = collection.find_one({"_id": 0})['timeout']
    yjcount = 0
    for kap in context.job_queue.jobs():
        if not str(kap.name) in ignorejob:
            jobstr = str(kap.job)
            jnam = jobstr.find("date[")
            jname = jobstr[jnam+7:jnam+24]
            if jname[:2].isdigit():
                kapdct = {'msgdict': kap.context, 'name': kap.name, 'when': jname}
                collection.update_one({"_id": 0}, {"$push": {"jobs": kapdct}})
                yjcount += 1
    logger.warning(str(yjcount)+" Adet Job Yedeklendi!")

def tekrarlipostjob(context):
    tsdict = context.job.context
    tspostsira = int(tsdict["mod"].split("-")[1])
    tspostdict = choice(tsdict["tspost"]) if tsdict["mod"].startswith("rastgele") else tsdict["tspost"][tspostsira]
    if tspostsira == len(tsdict["tspost"])-1:
        tspostsira = -1
    for tsgetj in context.job_queue.get_jobs_by_name(f"ts{tsdict['tsuser']}"):
        if tsgetj.context["tspost"][0]['fid'] == tsdict["tspost"][0]['fid'] and tsgetj.context["tspost"][0]['tscaption'] == tsdict["tspost"][0]['tscaption'] and tsgetj.context["tspost"][0]['text'] == tsdict["tspost"][0]['text']:
            tsgetjj = tsgetj
            break
    tsgetjj.context["mod"] = tsdict["mod"].split("-")[0] + "-" + tspostsira + 1
    if tspostdict['text'] != None:
        try:
            bot.send_message(tsdict['tskan'], tspostdict['text'])
        except:
            bot.send_message(tsdict['tsuser'], f"{tsdict['baslik']} Tekrarli Postunuz gönderilemedi!")
        return
    try:
        SEND_MEDIA_TYPES[tspostdict['ptip']](tspostdict['tskan'], tspostdict['fid'], caption=tspostdict['tscaption'])
    except:
        try:
            bot.send_message(tsdict['tsuser'], f"{tsdict['baslik']} Tekrarli Postunuz gönderilemedi!")
        except:
            for tsgetj in context.job_queue.get_jobs_by_name(f"ts{tsdict['tsuser']}"):
                if tsgetj.context["tspost"][0]['fid'] == tsdict["tspost"][0]['fid'] and tsgetj.context["tspost"][0]['tscaption'] == tsdict["tspost"][0]['tscaption'] and tsgetj.context["tspost"][0]['text'] == tsdict["tspost"][0]['text']:
                    tsgetjj = tsgetj
                    break
            try:
                tsdict['try']
            except:
                tsgetjj.context['try'] = 0
            else:
                if tsdict['try'] >= 6:
                    tsgetjj.schedule_removal()
                else:
                    tsgetjj.context['try'] = tsdict['try']+1

def deljob(context):
    delcont = context.job.context
    hedef = str(delcont.effective_chat.id)
    mesid = int(delcont.effective_message.message_id)
    try:
        data = db[str(hedef)].find_one({"_id": mesid})
        data['pids']
    except:
        data = list(db[str(hedef)].find({"mesih": mesid}))
    spcount = 0
    for kpsd in KaynakCol.find_one({"_id": int(hedef)})['kaynak']:
        try:
            kpsd = collection.find_one({"_id": kpsd})
            collection.update_one({"_id": kpsd['_id']}, {"$set": {"pcount": kpsd['pcount']-1}})
        except:
            pass
    if type(data) != list:
        data = data['pids']
    for d in data:
        try:
            bot.delete_message(d['chat'], d['pid'])
        except Exception as e:
            logger.error(e)
        else:
            spcount += 1
    logger.warning(f"{spcount} post silindi.")

def zamanjob(context):
    cont = context.job.context
    patbegeni = collection.find_one({"_id": cont[0]['user']})['begeni']
    if len(patbegeni) == 0:
        patmarkup = InlineKeyboardMarkup([[]])
    else:
        pbkeyb = []
        pbkc = 0
        for pbeg in patbegeni:
            pbkeyb.append(InlineKeyboardButton(str(pbeg)+" 0", callback_data="begeni-{}".format(pbkc)))
            pbkc += 1
        patmarkup = InlineKeyboardMarkup([pbkeyb])
    for msgd in cont:
        try:
            ppost = SEND_MEDIA_TYPES[msgd['ptip']](msgd['pkan'], msgd['fid'], caption=msgd['psablon'], reply_markup=patmarkup)
        except Exception as e:
            logger.error(e)
            try:
                bot.send_message(msgd['user'], "Zamanlı Postunuz gönderilemedi.")
            except:
                pass
        else:            
            if len(patbegeni) > 0:
                if ButonCol.find_one({"_id": msgd['pkan']}) == None:
                    ButonCol.insert_one({"_id": msgd['pkan'], str(ppost.message_id): [], "begeni": patbegeni})
                else:
                    ButonCol.update_one({"_id": msgd['pkan']}, {"$set": {str(ppost.message_id): [], "begeni": patbegeni}})

def delonejob(context):
    delh = context.job.context
    bot.delete_message(delh['chat'], delh['mid'])

def gunluk(context):
    ozel_kaynak_kullanan_sayisi = 0
    exe_kullanan_sayisi, pubiza_kullanan_sayisi, ouo_kullanan_sayisi, urlably_kullanan_sayisi, trlink_kullanan_sayisi, pnd_kullanan_sayisi, girist = 0, 0, 0, 0, 0, 0, 0
    msg = bot.send_message(botlog, "<code>Günlük veriler hesaplanıyor...</code>")
    toplam = 0
    kum = []
    kanals = 0
    users = 0
    kullanicilar = collection.find({})
    for kullanici in kullanicilar:
        try:
            kullanici['site']
            kullanici['altsite']
        except:
            continue
        if kullanici['site'] == "1":
            trlink_kullanan_sayisi += 1
        if kullanici['altsite'] == "1":
            trlink_kullanan_sayisi += 1
        elif kullanici['site'] == "2":
            pnd_kullanan_sayisi += 1
        elif kullanici['altsite'] == "2":
            pnd_kullanan_sayisi += 1
        elif kullanici['site'] == "3":
            exe_kullanan_sayisi += 1
        elif kullanici['altsite'] == "3":
            exe_kullanan_sayisi += 1
        elif kullanici['site'] == "4":
            ouo_kullanan_sayisi += 1
        elif kullanici['altsite'] == "4":
            ouo_kullanan_sayisi += 1
        elif kullanici['site'] == "5":
            pubiza_kullanan_sayisi += 1
        elif kullanici['altsite'] == "5":
            pubiza_kullanan_sayisi += 1
        elif kullanici['site'] == "6":
            girist += 1
        elif kullanici['altsite'] == "6":
            girist += 1
        elif kullanici['site'] == "7":
            urlably_kullanan_sayisi += 1
        elif kullanici['altsite'] == "7":
            urlably_kullanan_sayisi += 1
        if kullanici['ozel']:
            ozel_kaynak_kullanan_sayisi += 1
        users += 1
        for kul in kullanici['kanal']:
            if not kul in kum:
                kum.append(kul)
                time.sleep(0.5)
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
                        time.sleep(30)
                else:
                    toplam += uye
                    kanals += 1
    
    toplam = toplam / 1000
    toplam = str(round(toplam, 1))+"K" if round(toplam, 1) < 1000 else str(round(toplam / 1000, 2))+"M"
    statscount = 1
    stat_text = "👥 Toplam Kullanıcı Sayısı: {}\n📢 Toplam Kayıtlı Kanal Sayısı: {}\n🙋 Toplam Kitle: {}\n\n<b>Sitelerin Toplam Kullanıcı Sayıları(Alternatifler dahil);</b>\nTRLink -> {}\nPND.TL -> {}\nExe.io -> {}\nOuo.io -> {}\nPubiza -> {}\nGir.ist -> {}\n\n<b>+18 Kaynakların Toplam Kullanıcı Sayıları:</b>\n".format(users, kanals, toplam, trlink_kullanan_sayisi, pnd_kullanan_sayisi, exe_kullanan_sayisi, ouo_kullanan_sayisi, pubiza_kullanan_sayisi, girist)
    gkaynaklar = KaynakCol.find()
    tarih = datetime.datetime.now(pytz.timezone('Europe/Istanbul'))
    for kstat in sorted(gkaynaklar, key = lambda i: len(i['kaynak']), reverse=True):
        if kstat['icerik'] != "+18":
            continue
        try:
            getskaynak = bot.get_chat(kstat['_id'])
        except:
            gktitle = "Kaynağa ulaşılamıyor..."
        else:
            gktitle = getskaynak.title
        stat_text += "{}. {} -> {} \n".format(statscount, gktitle, len(kstat['kaynak']))
        gunkans = []
        for kus in kstat['kaynak']:
            if collection.find_one({"_id": kus}) == None:
                continue
            for gk in collection.find_one({"_id": kus})['kanal']:
                if gk in kstat['kanal'] and not gk in gunkans:
                    gunkans.append(gk)
        KaynakCol.update_one({"_id": kstat['_id']}, {"$set": {f"grafik.{tarih.day}": {"user": len(kstat['kaynak']), "kanal": len(gunkans)}, "kanal": gunkans}})
        statscount += 1
    stat_text += f"Özel Kaynaklar: {ozel_kaynak_kullanan_sayisi}\n\n"
    statscount = 1
    astat_text = "<b>Arşiv Kaynakların Toplam Kullanıcı Sayıları:</b>\n"
    for kstat in sorted(KaynakCol.find(), key = lambda i: len(i['kaynak']), reverse=True):
        if kstat['icerik'] != "arsiv":
            continue
        try:
            getskaynak = bot.get_chat(kstat['_id'])
        except:
            gktitle = "Kaynağa ulaşılamıyor..."
        else:
            gktitle = getskaynak.title
        astat_text += "{}. {} -> {} \n".format(statscount, gktitle, len(kstat['kaynak']))
        gunkans = []
        for kus in kstat['kaynak']:
            if collection.find_one({"_id": kus}) == None:
                continue
            for gk in collection.find_one({"_id": kus})['kanal']:
                if gk in kstat['kanal'] and not gk in gunkans:
                    gunkans.append(gk)
        KaynakCol.update_one({"_id": kstat['_id']}, {"$set": {f"grafik.{tarih.day}": {"user": len(kstat['kaynak']), "kanal": len(gunkans)}, "kanal": gunkans}})
        statscount += 1
    last_text = "\n<b>Her gün saat 22:00'da otomatik olarak güncel veriler paylaşılacak. </b>"
    bot.edit_message_text(stat_text+astat_text+last_text, botlog, msg.message_id)
    bot.pin_chat_message(botlog, msg.message_id)

def panelcleaner(context):
    try:
        context.dispatcher.user_data[context.job.context].pop("panel_text")
    except:
        pass

def siraclean(context):
    if len(context.job_queue.get_jobs_by_name("anaposter")) != 20:
        collection.update_one({"_id": 0}, {"$set": {"sira": 0}})

def resetleme(context):
    try:
        for rest in collection.find({}):
            collection.update_one({"_id": rest['_id']}, {"$set": {"time": 0}})
    except Exception as e:
        bot.send_message(sahip, str(e))
    else:
        bot.send_message(sahip, "Time Sıfırlandı")