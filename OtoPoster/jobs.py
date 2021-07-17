from . import *
from .anafonks import *
from .callbacks import *
from .poster import *
from .komutlar import *
from .markups import *
from .misc import *


def poster_job(context):
    global postsirasi
    if len(postsirasi) < 1:
        return
    logger.warning(f"{len(postsirasi)} Post tespit edildi")
    vipler = collection.find_one({"_id": 0})['vipuye']
    for poste in postsirasi:
        chat = poste['chatid']
        update = poste['update']
        chatdat = KaynakCol.find_one({"_id": chat})
        count = 0
        mesaj = update.channel_post.caption
        if mesaj == None:
            continue
        """  Link tespit  """
        solx = mesaj.rfind("http")
        sol = mesaj.find("http")
        if sol == -1 or sol != solx:
            continue
        sag = mesaj.find("\n", sol)
        kynk = bot.get_chat(chat)
        mesajb = mesaj[sol:sag].strip()
        if mesaj.find("\n", sol) == -1:
            mesajb = mesaj[sol:].strip()
        if mesajb.startswith("https://t.me/"):
            continue
        """  Veri Tabanı  """
        postdata = db[str(chat)]
        binb =  chatdat['kaynak']
        mesjid = update.channel_post.message_id
        try:
            lmsg = bot.send_message(botlog, "<code>{} kaynağının postu paylaşılıyor...</code>".format(kynk.title))
        except Exception as e:
            logger.error(e)
            bot.send_message(sahip, str(e))
        else:
            postdata.insert_one({"chat": botlog, "pid": lmsg.message_id, "mesih": mesjid})
        logger.warning("{} kaynağının postu paylaşılıyor...".format(kynk.title))
        """  Açıklama tespit  """
        ason = mesaj.find("\n")
        aciklama = mesaj[:ason].strip()
        """ Dosya tespit """
        medya = update.channel_post.photo[0].file_id if update.channel_post.photo else update.channel_post.effective_attachment.file_id
        for hesap_id in binb:
            hesap = collection.find_one({"_id": hesap_id})
            if hesap == None:
                KaynakCol.update_one({"_id": chat}, {"$pull": {"kaynak": hesap_id}})
                continue
            try:
                token = hesap['token']
            except:
                continue
            kaynak = hesap['kaynak']
            kanal = hesap['kanal']
            if not "31" in kaynak and len(kanal) > 0:
                sablon = hesap['sablon']
                user = hesap['_id']
                site = hesap["site"]
                altapi = hesap['altapi']
                altsite = hesap['altsite']
                sira = hesap['sira']
                pcount = hesap['pcount']
                vakitler = hesap['vakit']
                dailycount = hesap['time']
                collection.update_one({"_id": user}, {"$inc": {"time": 1}})
                if pcount < 19:
                    collection.update_one({"_id": user}, {"$inc": {"pcount": 1}})
                else:
                    if para and not user in vipler:
                        token = phaapi(site)
                        altapi = phaapi(altsite) if altsite != "None" else "None"
                    collection.update_one({"_id": user}, {"$set": {"pcount": 0}})
                link = " "
                alink = " "
                json = " "
                linktry = 0
                try:
                    if sira == "2":
                        token = altapi
                        site = altsite
                        collection.update_one({"_id": user}, {"$set": {"sira": "3"}})
                    if sira == "3":
                        collection.update_one({"_id": user}, {"$set": {"sira": "2"}})
                    if not altapi == "None":
                        while linktry < 10 and alink == " ":
                            if altsite == "1":
                                json = get(f"https://ay.live/api/?", params={'api': altapi, 'url': mesajb, 'ct': 1}, headers=headers).json()
                                alink = json['shortenedUrl']
                            if altsite == "2":
                                json = get(f"https://www.pnd.tl/api?", params={'api': altapi, 'url': mesajb, 'category': 6}, headers=headers).json()
                                alink = json['shortenedUrl']
                            if altsite == "3":
                                json = get(f"https://exe.io/api?", params={'api': altapi, 'url': mesajb}, headers=headers).json()
                                alink = json['shortenedUrl']
                            if altsite == "4":
                                alink = get(f"http://ouo.io/api/{altapi}?", params={'s': mesajb}, headers=headers).text
                            if altsite == "5":
                                alink = get(f"http://pubiza.com/api.php?", params={'token': altapi, 'url': mesajb, 'ads_type': "adult"}, headers=headers).text
                            if altsite == "6":
                                json = get("http://gir.ist/api?", params={"api": altapi, "url": mesajb}, headers=headerss).json()
                                alink = json['shortenedUrl']
                            linktry += 1
                            sleep(0.3)
                            if linktry > 1:
                                logger.warning(f"Link kısaltılamadı tekrar deneniyor {linktry}")
                    while linktry < 10 and link == " ":
                        if site == "1":
                            json = get(f"https://ay.live/api/?", params={'api': token, 'url': mesajb, 'ct': 1}, headers=headers).json()
                            link = json['shortenedUrl']
                        if site == "2":
                            json = get(f"https://www.pnd.tl/api?", params={'api': token, 'url': mesajb, 'category': 6}, headers=headers).json()
                            link = json['shortenedUrl']
                        if site == "3":
                            json = get(f"https://exe.io/api?", params={'api': token, 'url': mesajb}, headers=headers).json()
                            link = json['shortenedUrl']
                        if site == "4":
                            link = get(f"http://ouo.io/api/{token}?", params={'s': mesajb}, headers=headers).text
                        if site == "5":
                            link = get(f"http://pubiza.com/api.php?", params={'token': token, 'url': mesajb, 'ads_type': "adult"}, headers=headers).text
                        if site == "6":
                            json = get("http://gir.ist/api?", params={"api": token, "url": mesajb}, headers=headerss).json()
                            link = json['shortenedUrl']
                        linktry += 1
                        sleep(0.3)
                        if linktry > 1:
                            logger.warning(f"Tekrar deneniyor {linktry}")
                    logger.info(f"{kanal} + {link} + {token}")
                except Exception as e:
                    bot.send_message(user, "Son postunuz gönderilemedi;\n\n<code>API adresiniz sıkıntılı veya sitenize ulaşılamıyor. API adresinizi kontrol edin, bir sıkıntı yoksa bu mesajı görmezden gelin muhtemelen seçtiğiniz site ile ilgili bir sorun vardır.</code>")
                    logger.error(e)
                    logger.warning(json)
                    continue
                try:
                    json['message']
                except:
                    pass
                else:
                    if json['message'] == "Invalid URL":
                        logger.error(f"{update.channel_post.chat.title} son postu hatalı olduğu için iptal edildi!")
                        bot.send_message(sahip, f"{update.channel_post.chat.title} kaynağının sahibi siz olduğunuz için bu mesaj sadece size gönderildi. \n\nSon postunuz kanallarda paylaşılamadı muhtemelen postun linki API ile kısaltılamayacak kadar uzun.\n\n{update.channel_post.link}")
                        bot.send_message(chatdat['sahip'], f"{update.channel_post.chat.title} kaynağının sahibi siz olduğunuz için bu mesaj sadece size gönderildi. \n\nSon postunuz kanallarda paylaşılamadı muhtemelen postun linki API ile kısaltılamayacak kadar uzun.\n\n{update.channel_post.link}")
                        context.job_queue.run_once(deljob, when=2, name="yedekleme", context=update.channel_post.link)
                        break
                if sablon == "1":
                    sablon = f"🔥{aciklama}\n\n🔱 TIKLA 👉 {link}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
                elif sablon == "2" or sablon == "3":
                    sablon = f"{aciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {link}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 @linkgec06"
                elif sablon == "9":
                    sablon = f"{aciklama} \n\n𝙇𝙄𝙉𝙆🔗 {link} \n\n     𝙇𝙄𝙉𝙆🔗 {alink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 @linkk_gecmee"
                elif sablon.find('{alink}') != -1:
                    sablon = sablon.replace("{aciklama}", "{}").replace("{alink}", "{}").replace("{link}", "{}").format(aciklama, link, alink)
                else:
                    sablon = sablon.replace("{aciklama}", "{}").replace("{link}", "{}").format(aciklama, link)
                
                if link == " ":
                    print(json)
                    bot.send_message(-1001190898326, str(hesap)+"\n\nX "+str(json))
                    continue
                for kan in kanal:
                    if not kan in chatdat['kanal']:
                        continue
                    post = update.channel_post
                    try:
                        yetkililer = [xy.user.id for xy in bot.get_chat_administrators(kan)]
                    except:
                        yetkililer = []
                    if not user in yetkililer:
                        try:
                            membersayi = bot.get_chat_members_count(kan)
                        except:
                            membersayi = "Bot kanaldan çıkarılmış."
                        try:
                            logger.warning(f"Hatalı kanal: {kan}")
                            bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {user}\nÜYE: {membersayi}\nKANAL: {kan}")
                            collection.update_one({"_id": user}, {"$pull": {"kanal": kan}})
                            continue
                        except:
                            pass
                        else:
                            logger.warning(f"{kan} kayıtlardan silindi.")
                    if vakitler != 0:
                        bot.send_message(eklenti, str(kan) + "+" + str(dailycount) + "+" + str(user))
                        sleep(0.1)
                        kan = eklenti
                    try:
                        if update.channel_post.photo:
                            post = bot.send_photo(kan, medya, caption=sablon)
                        if update.channel_post.video:
                            post = bot.send_video(kan, medya, caption=sablon)
                        if update.channel_post.animation:
                            post = bot.send_animation(kan, medya, caption=sablon)
                    except Exception as e:
                        if str(e).find("Chat is not found") != -1 or str(e).find("Need administrator") != -1 or str(e).find("bot is not") != -1:
                            try:
                                logger.warning(f"Hatalı kanal: {kan}")
                                try:
                                    kanname = bot.get_chat_members_count(kan)
                                except:
                                    kanname = "Kanaldan Çıkarılmış."
                                bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {user}\nÜYE: {kanname}\nKANAL: {kan}")
                                collection.update_one({"_id": user}, {"$pull": {"kanal": kan}})
                                bot.send_message(user, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                            except:
                                pass   
                            else:
                                logger.warning(f"{kan} kayıtlardan silindi.")
                        else:
                            logger.error(e)
                    else:
                        count = count + 1
                        if vakitler == 0:
                            postdata.insert_one({"pid": post.message_id, "chat": kan, "mesih": mesjid})
                logger.info("Başarılı!")
            else:
                pass
        basari = "{} kaynağından, {} kanalda post paylaşıldı.".format(kynk.title, count)
        logger.warning(basari)
        try:
            bot.edit_message_text(basari, botlog, lmsg.message_id)
        except Exception as e:
            logger.error(e)
    postsirasi.clear()
    postsirasi = []

def ozel_poster_job(context):
    global opostsirasi
    if len(opostsirasi) < 1:
        return
    logger.warning(f"{len(opostsirasi)} Özel kaynak postu tespit edildi.")
    vipler = collection.find_one({"_id": 0})['vipuye']
    for oposte in opostsirasi:
        ochat = oposte['chatid']
        oupdate = oposte['update']
        okaynak = OzelCol.find_one({"okaynak": ochat})
        ocount = 0
        omesaj = oupdate.channel_post.caption
        if omesaj == None:
            continue
        """  Link tespit  """
        osolx = omesaj.rfind("http")
        osol = omesaj.find("http")
        if osol == -1 or osol != osolx:
            continue
        osag = omesaj.find("\n", osol)
        okynk = bot.get_chat(ochat)
        omesajb = omesaj[osol:osag].strip()
        if omesaj.find("\n", osol) == -1:
            omesajb = omesaj[osol:].strip()
        if omesajb.startswith("https://t.me/"):
            continue
        logger.warning("[ÖZEL] {} postu atılıyor... ".format(okynk.title))
        """  Açıklama tespit  """
        oason = omesaj.find("\n")
        oaciklama = omesaj[:oason].strip()
        """ Dosya tespit """
        omedya = oupdate.channel_post.photo[0].file_id if oupdate.channel_post.photo else oupdate.channel_post.effective_attachment.file_id
        for ozelkanal in okaynak['kanal']:
            ohesap = collection.find_one({"_id": ozelkanal})
            try:    
                otoken = ohesap['token']
            except:
                continue
            okanal = ohesap['kanal']
            osablon = ohesap['sablon']
            ouser = ohesap['_id']
            osite = ohesap["site"]
            oaltapi = ohesap['altapi']
            oaltsite = ohesap['altsite']
            osira = ohesap['sira']
            opcount = ohesap['pcount']
            ovakitler = ohesap['vakit']
            odailycount = ohesap['time']
            collection.update_one({"_id": ouser}, {"$inc": {"time": 1}})
            if not "31" in ohesap['kaynak'] and len(okanal) > 0:
                oalink = " "
                olink = " "
                olinktry = 0
                if osira == "2":
                    otoken = oaltapi
                    osite = oaltsite
                    collection.update_one({"_id": ouser}, {"$set": {"sira": "3"}})
                if osira == "3":
                    collection.update_one({"_id": ouser}, {"$set": {"sira": "2"}})
                if opcount < 19:
                    collection.update_one({"_id": ouser}, {"$inc": {"pcount": 1}})
                else:
                    if para and ouser not in vipler and len(okaynak) > 5:
                        otoken = phaapi(osite)
                        oaltapi = phaapi(oaltsite) if oaltsite != "None" else "None"
                    collection.update_one({"_id": ouser}, {"$set": {"pcount": 0}})
                try:
                    if not oaltapi == "None":
                        while olinktry < 10 and oalink == " ":
                            if oaltsite == "1":
                                ojson = get(f"https://ay.live/api/?", params={'api': oaltapi, 'url': omesajb, 'ct': 1}, headers=headers).json()
                                oalink = ojson['shortenedUrl']
                            if oaltsite == "2":
                                ojson = get(f"https://www.pnd.tl/api?", params={'api': oaltapi, 'url': omesajb, 'category': 6}, headers=headers).json()
                                oalink = ojson['shortenedUrl']
                            if oaltsite == "3":
                                ojson = get(f"https://exe.io/api?", params={'api': oaltapi, 'url': omesajb}, headers=headers).json()
                                oalink = ojson['shortenedUrl']
                            if oaltsite == "4":
                                oalink = get(f"http://ouo.io/api/{oaltapi}?", params={'s': omesajb}, headers=headers).text
                            if oaltsite == "5":
                                oalink = get(f"http://pubiza.com/api.php?", params={'token': oaltapi, 'url': omesajb, 'ads_type': "adult"}, headers=headers).text
                            if oaltsite == "6":
                                oajson = get("http://gir.ist/api?", params={"api": oaltapi, "url": omesajb}, headers=headerss).json()
                                oalink = oajson['shortenedUrl']
                            olinktry += 1
                            sleep(0.3)
                            if olinktry > 1:
                                logger.warning(f"Tekrar deneniyor {olinktry}")
                    while olinktry < 10 and olink == " ":
                        if osite == "1":
                            ojson = get(f"https://ay.live/api/?", params={'api': otoken, 'url': omesajb, 'ct': 1}, headers=headers).json()
                            olink = ojson['shortenedUrl']
                        if osite == "2":
                            ojson = get(f"https://www.pnd.tl/api?", params={'api': otoken, 'url': omesajb, 'category': 6}, headers=headers).json()
                            olink = ojson['shortenedUrl']
                        if osite == "3":
                            ojson = get(f"https://exe.io/api?", params={'api': otoken, 'url': omesajb}, headers=headers).json()
                            olink = ojson['shortenedUrl']
                        if osite == "4":
                            olink = get(f"http://ouo.io/api/{otoken}?", params={'s': omesajb}, headers=headers).text
                        if osite == "5":
                            olink = get(f"http://pubiza.com/api.php?", params={'token': etoken, 'url': omesajb, 'ads_type': "adult"}, headers=headers).text
                        if osite == "6":
                            ojson = get("https://gir.ist/api?", params={"api": otoken, "url": omesajb}, headers=headerss).json()
                            olink = ojson['shortenedUrl']
                        olinktry += 1
                        sleep(0.3)
                        if olinktry > 1:
                            logger.warning(f"Tekrar deneniyor {olinktry}")
                    logger.info(f"{okanal} + {olink} + {otoken}")
                except Exception as e:
                    bot.send_message(ouser, "Son postunuz gönderilemedi;\n\n<code>API adresiniz sıkıntılı veya sitenize ulaşılamıyor. API adresinizi kontrol edin, bir sıkıntı yoksa bu mesajı görmezden gelin muhtemelen seçtiğiniz site ile ilgili bir sorun vardır.</code>")
                    logger.error(e)
                    continue
                try:
                    ojson['message']
                except:
                    pass
                else:
                    if ojson['message'] == "Invalid URL":
                        logger.error(f"[ÖZEL] {oupdate.channel_post.chat.title} son postu hatalı olduğu için iptal edildi!")
                        bot.send_message(sahip, f"{oupdate.channel_post.chat.title} kaynağının sahibi siz olduğunuz için bu mesaj sadece size gönderildi. \n\nSon postunuz kanallarda paylaşılamadı muhtemelen postun linki API ile kısaltılamayacak kadar uzun.\n\n{oupdate.channel_post.link}")
                        bot.send_message(okaynak['_id'], f"{oupdate.channel_post.chat.title} kaynağının sahibi siz olduğunuz için bu mesaj sadece size gönderildi. \n\nSon postunuz kanallarda paylaşılamadı muhtemelen postun linki API ile kısaltılamayacak kadar uzun.\n\n{oupdate.channel_post.link}")
                        break
                    
                if osablon == "1":
                    osablon = f"🔥{oaciklama}\n\n🔱 TIKLA 👉 {olink}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
                elif osablon == "2" or osablon == "3":
                    osablon = f"{oaciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {olink}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 @linkgec06"
                elif osablon == "9":
                    osablon = f"{oaciklama} \n\n𝙇𝙄𝙉𝙆🔗 {olink} \n\n     𝙇𝙄𝙉𝙆🔗 {oalink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 @linkk_gecmee"
                elif osablon.find('{alink}') != -1:
                    osablon = osablon.replace("{aciklama}", "{}").replace("{alink}", "{}").replace("{link}", "{}").format(oaciklama, olink, oalink)
                else:
                    osablon = osablon.replace("{aciklama}", "{}").replace("{link}", "{}").format(oaciklama, olink)
                if olink == " ":
                    print(ojson)
                    bot.send_message(-1001190898326, str(ohesap)+"   "+str(ojson))
                    continue
                for okan in okanal:
                    try:
                        oyetkililer = [oxy.user.id for oxy in bot.get_chat_administrators(okan)]
                    except:
                        oyetkililer = []
                    if not ouser in oyetkililer:
                        try:
                            omembersayi = bot.get_chat_members_count(okan)
                        except:
                            omembersayi = "Bot kanaldan çıkarılmış."
                        try:
                            logger.warning(f"Hatalı kanal: {okan}")
                            bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {ouser}\nÜYE: {omembersayi}\nKANAL: {okan}")
                            collection.update_one({"_id": ouser}, {"$pull": {"kanal": okan}})
                            continue
                        except:
                            pass
                        else:
                            logger.warning(f"{okan} kayıtlardan silindi.")
                    if ovakitler != 0:
                        if odailycount == len(ovakitler):
                            collection.update_one({"_id": ouser}, {"$set": {"time": -1}})
                        if odailycount != -1:
                            bot.send_message(eklenti, str(okan) + "+" + str(odailycount) + "+" + str(ouser))
                        okan = eklenti
                    try:
                        if oupdate.channel_post.photo:
                            opost = bot.send_photo(okan, omedya, caption=osablon)
                        if oupdate.channel_post.video:
                            opost = bot.send_video(okan, omedya, caption=osablon)
                        if oupdate.channel_post.animation:
                            opost = bot.send_animation(okan, omedya, caption=osablon)
                    except Exception as e:
                        if str(e).find("Chat is not found") != -1 or str(e).find("Need administrator") != -1 or str(e).find("bot is not") != -1:
                            try:
                                logger.warning(f"Hatalı kanal: {okan}")
                                bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {ouser}\nÜYE: {bot.get_chat_members_count(okan)}\nKANAL: {okan}")
                                collection.update_one({"_id": ouser}, {"$pull": {"kanal": okan}})
                                bot.send_message(ouser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                            except Exception as e: 
                                logger.error(e)
                            else:
                                logger.warning(f"{okan} kayıtlardan silindi.")
                        else:
                            logger.error(e)
                    else:
                        ocount += 1                     
                logger.info("Başarılı!")
        obasari = "[ÖZEL] {} kaynağından {} kanalda post paylaşıldı.".format(okynk.title, ocount)
        if okaynak["log"] != "yok":
            bot.send_message(okaynak["log"], obasari[7:])
        logger.warning(obasari)
    opostsirasi.clear()
    opostsirasi = []
    
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