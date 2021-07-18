from . import *
from .misc import *

def jobyedekleme(context):
    collection.update_one({"_id": 0}, {"$set": {"jobs": []}})
    yjcount = 0
    for kap in context.job_queue.jobs():
        if str(kap.name) != "yedekleme" or str(kap.name) != "gunluk" or str(kap.name) != "resetleme" or str(kap.name) != "ozelposter" or str(kap.name) != "anaposter":
            jobstr = str(kap.job)
            jnam = jobstr.find("date[")
            jname = jobstr[jnam+7:jnam+24]
            if jname[:2].isdigit():
                kapdct = {'msgdict': kap.context, 'name': kap.name, 'when': jname}
                collection.update_one({"_id": 0}, {"$push": {"jobs": kapdct}})
                yjcount += 1
    logger.warning(str(yjcount)+" Adet Job Yedeklendi!")

def deljob(context):
    delcont = context.job.context
    hedef = "-100"+delcont.split("/")[-2]
    mesid = int(delcont.split("/")[-1])
    data = db[str(hedef)].find({"mesih": mesid})
    spcount = 0
    for kpsd in collection.find({}):
        try:
            collection.update_one({"_id": kpsd['_id']}, {"$set": {"pcount": kpsd['pcount']-1}})
        except:
            pass
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
    for msgd in cont:
        try:
            SEND_MEDIA_TYPES[msgd['ptip']](msgd['pkan'], msgd['fid'], caption=msgd['psablon'])
        except Exception as e:
            logger.error(e)
            try:
                bot.send_message(msgd['user'], "Zamanlı Postunuz gönderilemedi.")
            except:
                pass


def gunluk(context):
    ozel_kaynak_kullanan_sayisi = 0
    exe_kullanan_sayisi, pubiza_kullanan_sayisi, ouo_kullanan_sayisi, trlink_kullanan_sayisi, pnd_kullanan_sayisi, girist = 0, 0, 0, 0, 0, 0
    msg = bot.send_message(botlog, "<code>Günlük veriler hesaplanıyor...</code>")
    db[str(sahip)].insert_one({"_id": msg.message_id, "basan": []})
    toplam = 0
    kum = []
    kanals = 0
    users = 0
    kullanicilar = collection.find({})
    for kullanici in kullanicilar:
        try:
            kullanici['site']
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
    statscount = 0
    stat_text = "👥 Toplam Kullanıcı Sayısı: {}\n📢 Toplam Kayıtlı Kanal Sayısı: {}\n🙋 Toplam Kitle: {}\n\n<b>Sitelerin Toplam Kullanıcı Sayıları(Alternatifler dahil);</b>\nTRLink -> {}\nPND.TL -> {}\nExe.io -> {}\nOuo.io -> {}\nPubiza -> {}\nGir.ist -> {}\n\n<b>Kaynakların Toplam Kullanıcı Sayıları:</b>\n".format(users, kanals, toplam, trlink_kullanan_sayisi, pnd_kullanan_sayisi, exe_kullanan_sayisi, ouo_kullanan_sayisi, pubiza_kullanan_sayisi, girist)
    for kstat in KaynakCol.find({}):
        getskaynak = bot.get_chat(kstat['_id'])
        stat_text += "{} -> {} \n".format(getskaynak.title, len(kstat['kaynak']))
    ozel_text = f"Özel Kaynaklar: {ozel_kaynak_kullanan_sayisi}\n\n<b>Her gün saat 22:00'da otomatik olarak güncel veriler paylaşılacak. </b>"
    bot.edit_message_text(stat_text+ozel_text, botlog, msg.message_id)
    bot.pin_chat_message(botlog, msg.message_id)

def resetleme(context):
    try:
        for rest in collection.find({}):
            collection.update_one({"_id": rest['_id']}, {"$set": {"time": 0}})
    except Exception as e:
        bot.send_message(sahip, str(e))
    else:
        bot.send_message(sahip, "Time Sıfırlandı")