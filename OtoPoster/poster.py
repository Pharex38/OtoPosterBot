from . import *
from .misc import *
from .jobs import *


MEDIA_GROUP_TYPES = {"audio": InputMediaAudio, "document": InputMediaDocument, "photo": InputMediaPhoto, "animation": InputMediaAnimation, "video": InputMediaVideo}

def poster_job(context):
    vipler = collection.find_one({"_id": 0})['vipuye']
    postee = context.job.context
    grup = []
    for poste in postee:
        chat = poste['chatid']
        update = poste['update']
        chatdat = KaynakCol.find_one({"_id": chat})
        count = 0
        mesaj = update.effective_message.caption
        if len(postee) > 1 and mesaj == None:
            grup.append(MEDIA_GROUP_TYPES[effective_message_type(poste)](media=message.photo[-1].file_id if message.photo else message.effective_attachment.file_id, caption=poste.effective_message.caption))
            continue
        if mesaj == None:
            return
        """  Link tespit  """
        solx = mesaj.rfind("http")
        sol = mesaj.find("http")
        if sol == -1 or sol != solx:
            return
        sag = mesaj.find("\n", sol)
        kynk = bot.get_chat(chat)
        mesajb = mesaj[sol:sag].strip()
        if mesaj.find("\n", sol) == -1:
            mesajb = mesaj[sol:].strip()
        if mesajb.startswith("https://ay") or mesajb.startswith("https://pgg") or mesajb.startswith("https://pnd") or mesajb.startswith("https://ouo") or mesajb.startswith("https://exe") or mesajb.startswith("https://lnk") or mesajb.startswith("https://t.me/"):
            return
        """  Açıklama tespit  """
        ason = mesaj.find("\n\n")
        aciklama = mesaj[:ason].strip()
        """  Veri Tabanı  """
        postdata = db[str(chat)]
        binb =  chatdat['kaynak']
        mesjid = update.effective_message.message_id
        postdata.insert_one({"_id": mesjid, "pids": [], "aciklama": aciklama, "link": mesajb})
        try:
            lmsg = bot.send_message(botlog, "<code>{} kaynağının postu paylaşılıyor...</code>".format(kynk.title))
        except RetryAfter as rtfr:
            sleep(rftr.retry_after+1)
            lmsg = bot.send_message(botlog, "<code>{} kaynağının postu paylaşılıyor...</code>".format(kynk.title))
        except Exception as e:
            logger.error(e)
            bot.send_message(sahip, str(e))
        else:
            postdata.update_one({"_id": mesjid}, {"$push": {"pids": {"pid": lmsg.message_id, "chat": botlog}}})
        logger.warning("{} kaynağının postu paylaşılıyor...".format(kynk.title))
        for hesap_id in binb:
            if str(chat) in collection.find_one({"_id": 0})['iptal']:
                collection.update_one({"_id": 0}, {"$pull": {"iptal": str(chat)}})
                logger.warning("{} kaynağının postu iptal edildi.".format(kynk.title))
                context.job_queue.run_once(deljob, when=2, name="yedekleme", context=update.effective_message.link)
                lmsg.edit_text("{} kaynağının postu iptal edildi. Post kanallardan siliniyor...".format(kynk.title))
                return
            hesap = collection.find_one({"_id": hesap_id})
            if hesap == None:
                KaynakCol.update_one({"_id": chat}, {"$pull": {"kaynak": hesap_id}})
                continue
            try:
                token = hesap['token']
            except:
                continue
            kanal = hesap['kanal']
            eski = hesap['eski']
            if len(kanal) != len(eski) and len(kanal) > 0:
                sablon = hesap['sablon']
                user = hesap['_id']
                site = hesap["site"]
                altapi = hesap['altapi']
                kaynak = hesap['kaynak']
                altsite = hesap['altsite']
                sira = hesap['sira']
                pcount = hesap['pcount']
                vakitler = hesap['vakit']
                dailycount = hesap['time']
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
                if sira == "2":
                    token = altapi
                    site = altsite
                    collection.update_one({"_id": user}, {"$set": {"sira": "3"}})
                if sira == "3":
                    collection.update_one({"_id": user}, {"$set": {"sira": "2"}})
                if not altapi == "None":
                    while linktry < 15 and alink == " ":
                        try:
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
                        except Exception as e:
                            if linktry == 15:
                                try:
                                    bot.send_message(user, "Son postunuz gönderilemedi;\n\n<code>API adresiniz sıkıntılı veya sitenize ulaşılamıyor. API adresinizi kontrol edin, bir sıkıntı yoksa bu mesajı görmezden gelin muhtemelen seçtiğiniz site ile ilgili bir sorun vardır.</code>")
                                    bildir(e)
                                except RetryAfter as rtfr:
                                    sleep(rtfr.retry_after+1)
                                    try:
                                        bot.send_message(user, "Son postunuz gönderilemedi;\n\n<code>API adresiniz sıkıntılı veya sitenize ulaşılamıyor. API adresinizi kontrol edin, bir sıkıntı yoksa bu mesajı görmezden gelin muhtemelen seçtiğiniz site ile ilgili bir sorun vardır.</code>")
                                    except:
                                        pass
                                except:
                                    pass
                                alink = "-"
                                logger.error(e)
                                logger.warning(json)
                                continue
                while linktry < 15 and link == " ":
                    try:
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
                        sleep(0.4)
                        if linktry > 1:
                            logger.warning(f"Tekrar deneniyor {linktry}")
                    except Exception as e:
                        if linktry == 15:
                            try:
                                bot.send_message(user, "Son postunuz gönderilemedi;\n\n<code>API adresiniz sıkıntılı veya sitenize ulaşılamıyor. API adresinizi kontrol edin, bir sıkıntı yoksa bu mesajı görmezden gelin muhtemelen seçtiğiniz site ile ilgili bir sorun vardır.</code>")
                                bildir(e)
                            except RetryAfter as rtfr:
                                sleep(rtfr.retry_after+1)
                                try:
                                    bot.send_message(user, "Son postunuz gönderilemedi;\n\n<code>API adresiniz sıkıntılı veya sitenize ulaşılamıyor. API adresinizi kontrol edin, bir sıkıntı yoksa bu mesajı görmezden gelin muhtemelen seçtiğiniz site ile ilgili bir sorun vardır.</code>")
                                except:
                                    pass
                            except:
                                pass
                            link = "-"
                            logger.error(e)
                            logger.warning(json)
                            continue
                logger.info(f"{kanal} + {link} + {token}")
                try:
                    json['message']
                except:
                    pass
                else:
                    if json['message'] == "Invalid URL":
                        logger.error(f"{update.effective_message.chat.title} son postu hatalı olduğu için iptal edildi!")
                        try:
                            bot.send_message(sahip, f"{update.effective_message.chat.title} kaynağının sahibi siz olduğunuz için bu mesaj sadece size gönderildi. \n\nSon postunuz kanallarda paylaşılamadı muhtemelen postun linki API ile kısaltılamayacak kadar uzun.\n\n{json['message']}\n\n{update.effective_message.link}")
                            bot.send_message(chatdat['sahip'], f"{update.effective_message.chat.title} kaynağının sahibi siz olduğunuz için bu mesaj sadece size gönderildi. \n\nSon postunuz kanallarda paylaşılamadı muhtemelen postun linki API ile kısaltılamayacak kadar uzun.\n\n{json['message']}\n\n{update.effective_message.link}")
                        except RetryAfter as rtfr:
                            sleep(rtfr.retry_after+1)
                        context.job_queue.run_once(deljob, when=2, name="yedekleme", context=update.effective_message.link)
                        break
                if sablon == "1":
                    sablon = f"🔥{aciklama}\n\n🔱 TIKLA 👉 {link}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
                elif sablon == "2" or sablon == "3":
                    sablon = f"{aciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {link}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 @linkgec06"
                elif sablon == "9":
                    sablon = f"{aciklama} \n\n𝙇𝙄𝙉𝙆🔗 {link} \n\n     𝙇𝙄𝙉𝙆🔗 {alink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 @linkk_gecmee"
                elif sablon.find('{alink}') != -1:
                    sablon = sablon.replace("{aciklama}", "{a}").replace("{alink}", "{al}").replace("{link}", "{l}").format(a=aciklama, l=link, al=alink)
                else:
                    sablon = sablon.replace("{aciklama}", "{a}").replace("{link}", "{l}").format(a=aciklama, l=link)
                if link == "-" or alink == "-":
                    continue
                if link == " ":
                    print(json)
                    try:
                        bot.send_message(-1001190898326, str(hesap)+"\n\nX "+str(json))
                    except:
                        pass
                    continue
                if vakitler != 0:
                    trysch = 0
                    while True:
                        if dailycount >= len(user_dat['vakit']):
                            dailycount = 0
                        raw_vakit = user_dat['vakit'][dailycount]
                        bugün = datetime.datetime.now()
                        raw_vakit = str(bugün.day).zfill(2) + "/" + str(bugün.month).zfill(2) + "/" + str(bugün.year) + " " + str(raw_vakit) + ":59"
                        tvakit = datetime.timedelta(hours = 3)
                        vakit = datetime.datetime.strptime(raw_vakit, '%d/%m/%Y %H:%M:%S') - tvakit
                        kontrol = vakit - datetime.datetime.utcnow()
                        if not kontrol.days < 0:
                            break
                        if trysch > len(user_dat['vakit']):
                            return
                        dailycount += 1
                        trysch += 1
                    try:
                        bot.send_message(eklenti, str(kan) + "+" + str(dailycount) + "+" + str(user))
                    except RetryAfter as rtfr:
                        sleep(rftr.retry_after+1)                            
                        bot.send_message(eklenti, str(kan) + "+" + str(dailycount) + "+" + str(user))
                    collection.update_one({"_id": user}, {"$set": {"time": dailycount}})
                    sleep(0.1)
                for kan in kanal:
                    sleep(0.1)
                    if not kan in chatdat['kanal'] or kan in eski:
                        continue
                    post = update.effective_message
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
                            collection.update_one({"_id": user}, {"$pull": {"kanal": kan}})
                            try:
                                bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {user}\nÜYE: {membersayi}\nKANAL: {kan}")
                            except RetryAfter as rtfr:
                                sleep(rftr.retry_after+1)
                                bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {user}\nÜYE: {membersayi}\nKANAL: {kan}")
                            collection.update_one({"_id": user}, {"$pull": {"kanal": kan}})
                            continue
                        except:
                            pass
                        else:
                            logger.warning(f"{kan} kayıtlardan silindi.")
                    try:
                        if len(postee) == 1:
                            post = update.effective_message.copy(kan, caption=sablon)
                        else:
                            grup.append(MEDIA_GROUP_TYPES[effective_message_type(update)](media=message.photo[-1].file_id if message.photo else message.effective_attachment.file_id, caption=sablon))
                            post = bot.send_media_group(kan, media=grup)
                    except RetryAfter as rtfr:
                        sleep(rtfr.retry_after+1)
                        try:
                            if len(postee) == 1:
                                post = update.effective_message.copy(kan, caption=sablon)
                            else:
                                grup.append(MEDIA_GROUP_TYPES[effective_message_type(update)](media=message.photo[-1].file_id if message.photo else message.effective_attachment.file_id, caption=sablon))
                                post = bot.send_media_group(kan, media=grup)
                        except Exception as e:
                            if str(e).find("Chat is not found") != -1 or str(e).find("Need administrator") != -1 or str(e).find("bot is not") != -1:
                                try:
                                    logger.warning(f"Hatalı kanal: {kan}")
                                    try:
                                        kanname = bot.get_chat_members_count(kan)
                                    except:
                                        kanname = "Kanaldan Çıkarılmış."
                                    collection.update_one({"_id": user}, {"$pull": {"kanal": kan}})
                                    try:
                                        bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {user}\nÜYE: {kanname}\nKANAL: {kan}")
                                        bot.send_message(user, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                                    except RetryAfter as rtfr:
                                        sleep(rftr.retry_after+1)
                                        bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {user}\nÜYE: {kanname}\nKANAL: {kan}")
                                        bot.send_message(user, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                                except:
                                    pass   
                                else:
                                    logger.warning(f"{kan} kayıtlardan silindi.")
                            else:
                                logger.error(e)
                        else:
                            count = count + 1
                            if len(postee) == 1:
                                postdata.update_one({"_id": mesjid}, {"$push": {"pids": {"pid": post.message_id, "chat": kan, "user": user, "link": link, "alink": alink}}})
                            else:
                                for pos in post:
                                    postdata.update_one({"_id": mesjid}, {"$push": {"pids": {"pid": pos.message_id, "chat": kan, "user": user, "link": link, "alink": alink}}})
                            logger.info("Başarılı! "+str(kan))
                    except Exception as e:
                        if str(e).find("Chat is not found") != -1 or str(e).find("Need administrator") != -1 or str(e).find("bot is not") != -1:
                            try:
                                logger.warning(f"Hatalı kanal: {kan}")
                                try:
                                    kanname = bot.get_chat_members_count(kan)
                                except:
                                    kanname = "Kanaldan Çıkarılmış."
                                collection.update_one({"_id": user}, {"$pull": {"kanal": kan}})
                                try:
                                    bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {user}\nÜYE: {kanname}\nKANAL: {kan}")
                                    bot.send_message(user, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                                except RetryAfter as rtfr:
                                    sleep(rftr.retry_after+1)
                                    bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {user}\nÜYE: {kanname}\nKANAL: {kan}")
                                    bot.send_message(user, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                            except:
                                pass   
                            else:
                                logger.warning(f"{kan} kayıtlardan silindi.")
                        else:
                            logger.error(e)
                    else:
                        count = count + 1
                        if len(postee) == 1:
                            postdata.update_one({"_id": mesjid}, {"$push": {"pids": {"pid": post.message_id, "chat": kan, "user": user, "link": link, "alink": alink}}})
                        else:
                            for pos in post:
                                postdata.update_one({"_id": mesjid}, {"$push": {"pids": {"pid": pos.message_id, "chat": kan, "user": user, "link": link, "alink": alink}}})
                        logger.info("Başarılı! "+str(kan))
                        
        basari = "{} kaynağından, {} kanalda post paylaşıldı.".format(kynk.title, count)
        logger.warning(basari)
        try:
            bot.edit_message_text(basari, botlog, lmsg.message_id)
        except Exception as e:
            logger.error(e)

def ozel_poster_job(context):
    oposte = context.job.context
    vipler = collection.find_one({"_id": 0})['vipuye']
    if True:
        ochat = oposte['chatid']
        oupdate = oposte['update']
        okaynak = OzelCol.find_one({"okaynak": ochat})
        ocount = 0
        omesaj = oupdate.effective_message.caption
        if omesaj == None:
            return
        """  Link tespit  """
        osolx = omesaj.rfind("http")
        osol = omesaj.find("http")
        if osol == -1 or osol != osolx:
            return
        osag = omesaj.find("\n", osol)
        okynk = bot.get_chat(ochat)
        omesajb = omesaj[osol:osag].strip()
        if omesaj.find("\n", osol) == -1:
            omesajb = omesaj[osol:].strip()
        if omesajb.startswith("https://t.me/"):
            return
        logger.warning("[ÖZEL] {} postu atılıyor... ".format(okynk.title))
        """  Açıklama tespit  """
        oason = omesaj.find("\n")
        oaciklama = omesaj[:oason].strip()
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
                        sleep(0.4)
                        if olinktry > 1:
                            logger.warning(f"Tekrar deneniyor {olinktry}")
                    logger.info(f"{okanal} + {olink} + {otoken}")
                except Exception as e:
                    try:
                        bot.send_message(ouser, "Son postunuz gönderilemedi;\n\n<code>API adresiniz sıkıntılı veya sitenize ulaşılamıyor. API adresinizi kontrol edin, bir sıkıntı yoksa bu mesajı görmezden gelin muhtemelen seçtiğiniz site ile ilgili bir sorun vardır.</code>")
                    except RetryAfter as ortfr:
                        sleep(orftr.retry_after+1)
                        bot.send_message(ouser, "Son postunuz gönderilemedi;\n\n<code>API adresiniz sıkıntılı veya sitenize ulaşılamıyor. API adresinizi kontrol edin, bir sıkıntı yoksa bu mesajı görmezden gelin muhtemelen seçtiğiniz site ile ilgili bir sorun vardır.</code>")
                    logger.error(e)
                    continue
                try:
                    ojson['message']
                except:
                    pass
                else:
                    if ojson['message'] == "Invalid URL":
                        logger.error(f"[ÖZEL] {oupdate.effective_message.chat.title} son postu hatalı olduğu için iptal edildi!")
                        try:
                            bot.send_message(sahip, f"{oupdate.effective_message.chat.title} kaynağının sahibi siz olduğunuz için bu mesaj sadece size gönderildi. \n\nSon postunuz kanallarda paylaşılamadı muhtemelen postun linki API ile kısaltılamayacak kadar uzun.\n\n{oupdate.effective_message.link}")
                            bot.send_message(okaynak['_id'], f"{oupdate.effective_message.chat.title} kaynağının sahibi siz olduğunuz için bu mesaj sadece size gönderildi. \n\nSon postunuz kanallarda paylaşılamadı muhtemelen postun linki API ile kısaltılamayacak kadar uzun.\n\n{oupdate.effective_message.link}")
                        except RetryAfter as ortfr:
                            sleep(orftr.retry_after+1)
                            bot.send_message(sahip, f"{oupdate.effective_message.chat.title} kaynağının sahibi siz olduğunuz için bu mesaj sadece size gönderildi. \n\nSon postunuz kanallarda paylaşılamadı muhtemelen postun linki API ile kısaltılamayacak kadar uzun.\n\n{oupdate.effective_message.link}")
                            bot.send_message(okaynak['_id'], f"{oupdate.effective_message.chat.title} kaynağının sahibi siz olduğunuz için bu mesaj sadece size gönderildi. \n\nSon postunuz kanallarda paylaşılamadı muhtemelen postun linki API ile kısaltılamayacak kadar uzun.\n\n{oupdate.effective_message.link}")
                        break
                    
                if osablon == "1":
                    osablon = f"🔥{oaciklama}\n\n🔱 TIKLA 👉 {olink}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
                elif osablon == "2" or osablon == "3":
                    osablon = f"{oaciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {olink}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 @linkgec06"
                elif osablon == "9":
                    osablon = f"{oaciklama} \n\n𝙇𝙄𝙉𝙆🔗 {olink} \n\n     𝙇𝙄𝙉𝙆🔗 {oalink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 @linkk_gecmee"
                elif osablon.find('{alink}') != -1:
                    osablon = osablon.replace("{aciklama}", "{a}").replace("{alink}", "{al}").replace("{link}", "{l}").format(a=oaciklama, l=olink, al=oalink)
                else:
                    osablon = osablon.replace("{aciklama}", "{a}").replace("{link}", "{l}").format(a=oaciklama, l=olink)
                if olink == " ":
                    print(ojson)
                    try:
                        bot.send_message(-1001190898326, str(ohesap)+"   "+str(ojson))
                    except:
                        pass
                    continue
                for okan in okanal:
                    sleep(0.1)
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
                            try:
                                bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {ouser}\nÜYE: {omembersayi}\nKANAL: {okan}")
                            except RetryAfter as ortfr:
                                sleep(orftr.retry_after+1)
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
                            try:
                                bot.send_message(eklenti, str(okan) + "+" + str(odailycount) + "+" + str(ouser))
                            except RetryAfter as ortfr:
                                sleep(orftr.retry_after+1)
                                bot.send_message(eklenti, str(okan) + "+" + str(odailycount) + "+" + str(ouser))
                        okan = eklenti
                    try:
                        oupdate.effective_message.copy(okan, caption=osablon)
                    except RetryAfter as ortfr:
                        sleep(orftr.retry_after+1)
                        try:
                            oupdate.effective_message.copy(okan, caption=osablon)
                        except Exception as e:
                            if str(e).find("Chat is not found") != -1 or str(e).find("Need administrator") != -1 or str(e).find("bot is not") != -1:
                                try:
                                    logger.warning(f"Hatalı kanal: {okan}")
                                    collection.update_one({"_id": ouser}, {"$pull": {"kanal": okan}})
                                    try:
                                        bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {ouser}\nÜYE: {bot.get_chat_members_count(okan)}\nKANAL: {okan}")
                                        bot.send_message(ouser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                                    except RetryAfter as ortfr:
                                        sleep(orftr.retry_after+1)
                                        bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {ouser}\nÜYE: {bot.get_chat_members_count(okan)}\nKANAL: {okan}")
                                        bot.send_message(ouser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                                except Exception as e: 
                                    logger.error(e)
                                else:
                                    logger.warning(f"{okan} kayıtlardan silindi.")
                            else:
                                logger.error(e)
                        else:
                            ocount += 1                     
                            logger.info("Başarılı! "+str(okan))
                    except Exception as e:
                        if str(e).find("Chat is not found") != -1 or str(e).find("Need administrator") != -1 or str(e).find("bot is not") != -1:
                            try:
                                logger.warning(f"Hatalı kanal: {okan}")
                                collection.update_one({"_id": ouser}, {"$pull": {"kanal": okan}})
                                try:
                                    bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {ouser}\nÜYE: {bot.get_chat_members_count(okan)}\nKANAL: {okan}")
                                    bot.send_message(ouser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                                except RetryAfter as ortfr:
                                    sleep(orftr.retry_after+1)
                                    bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {ouser}\nÜYE: {bot.get_chat_members_count(okan)}\nKANAL: {okan}")
                                    bot.send_message(ouser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                            except Exception as e: 
                                logger.error(e)
                            else:
                                logger.warning(f"{okan} kayıtlardan silindi.")
                        else:
                            logger.error(e)
                    else:
                        ocount += 1                     
                        logger.info("Başarılı! "+str(okan))
        obasari = "[ÖZEL] {} kaynağından {} kanalda post paylaşıldı.".format(okynk.title, ocount)
        if okaynak["log"] != "yok":
            try:
                bot.send_message(okaynak["log"], obasari[7:])
            except RetryAfter as ortfr:
                sleep(orftr.retry_after+1)
                try:
                    bot.send_message(okaynak["log"], obasari[7:])
                except:
                    pass
        logger.warning(obasari)

def poster_edit(update, context):
    chat = update.effective_chat.id
    if KaynakCol.find_one({"_id": chat}) == None:
        return
    indt = context.job_queue.get_jobs_by_name("anaposter")
    while len(indt) != 0:
        sleep(1)
        indt = context.job_queue.get_jobs_by_name("anaposter")
    emid = update.effective_message.message_id
    edited_m = update.effective_message.caption
    bas = edited_m.find("http")
    son = edited_m.find("\n", bas)
    edited_l = edited_m[bas:son].strip()
    edited_a = edited_m[:edited_m.find("\n")]
    if son == -1:
        edited_l = edited_m[bas:].strip()
    try:
        mesdata = db[str(chat)].find_one({"_id": emid})
        eski_a = mesdata['aciklama']
        eski_l = mesdata['link']
    except:
        return
    edcount = 0
    if eski_l != edited_l:
        logger.warning(f"{update.effective_chat.title} kaynağının postu düzenleniyor...")
        for edil in mesdata['pids']:
            db[str(chat)].update_one({"_id": emid}, {"$set": {"pids": []}})
            edi_dat = collection.find_one({"_id": edil['user']})
            sira = edi_dat['sira']
            site = edi_dat['site'] 
            altsite = edi_dat['altsite'] 
            altapi = edi_dat['altapi'] 
            token = edi_dat['token'] 
            chatdat = KaynakCol.find_one({"_id": chat})
            try:
                if sira == "2":
                    token = altapi
                    site = altsite
                    collection.update_one({"_id": edil['user']}, {"$set": {"sira": "3"}})
                if sira == "3":
                    collection.update_one({"_id": edil['user']}, {"$set": {"sira": "2"}})
                if not altapi == "None":
                    while linktry < 15 and alink == " ":
                        if altsite == "1":
                            json = get(f"https://ay.live/api/?", params={'api': altapi, 'url': edited_l, 'ct': 1}, headers=headers).json()
                            alink = json['shortenedUrl']
                        if altsite == "2":
                            json = get(f"https://www.pnd.tl/api?", params={'api': altapi, 'url': edited_l, 'category': 6}, headers=headers).json()
                            alink = json['shortenedUrl']
                        if altsite == "3":
                            json = get(f"https://exe.io/api?", params={'api': altapi, 'url': edited_l}, headers=headers).json()
                            alink = json['shortenedUrl']
                        if altsite == "4":
                            alink = get(f"http://ouo.io/api/{altapi}?", params={'s': edited_l}, headers=headers).text
                        if altsite == "5":
                            alink = get(f"http://pubiza.com/api.php?", params={'token': altapi, 'url': mesajb, 'ads_type': "adult"}, headers=headers).text
                        if altsite == "6":
                            json = get("http://gir.ist/api?", params={"api": altapi, "url": edited_l}, headers=headerss).json()
                            alink = json['shortenedUrl']
                        linktry += 1
                        sleep(0.3)
                        if linktry > 1:
                            logger.warning(f"Link kısaltılamadı tekrar deneniyor {linktry}")
                while linktry < 15 and link == " ":
                    if site == "1":
                        json = get(f"https://ay.live/api/?", params={'api': token, 'url': edited_l, 'ct': 1}, headers=headers).json()
                        link = json['shortenedUrl']
                    if site == "2":
                        json = get(f"https://www.pnd.tl/api?", params={'api': token, 'url': edited_l, 'category': 6}, headers=headers).json()
                        link = json['shortenedUrl']
                    if site == "3":
                        json = get(f"https://exe.io/api?", params={'api': token, 'url': edited_l}, headers=headers).json()
                        link = json['shortenedUrl']
                    if site == "4":
                        link = get(f"http://ouo.io/api/{token}?", params={'s': edited_l}, headers=headers).text
                    if site == "5":
                        link = get(f"http://pubiza.com/api.php?", params={'token': token, 'url': mesajb, 'ads_type': "adult"}, headers=headers).text
                    if site == "6":
                        json = get("http://gir.ist/api?", params={"api": token, "url": edited_l}, headers=headerss).json()
                        link = json['shortenedUrl']
                    linktry += 1
                    sleep(0.4)
                    if linktry > 1:
                        logger.warning(f"Tekrar deneniyor {linktry}")
                logger.info(f"{kanal} + {link} + {token}")
            except Exception as e:
                try:
                    bot.send_message(edil['user'], "Son postunuz gönderilemedi;\n\n<code>API adresiniz sıkıntılı veya sitenize ulaşılamıyor. API adresinizi kontrol edin, bir sıkıntı yoksa bu mesajı görmezden gelin muhtemelen seçtiğiniz site ile ilgili bir sorun vardır.</code>")
                    bildir(e)
                except RetryAfter as rtfr:
                    sleep(rtfr.retry_after+1)
                    try:
                        bot.send_message(edil['user'], "Son postunuz gönderilemedi;\n\n<code>API adresiniz sıkıntılı veya sitenize ulaşılamıyor. API adresinizi kontrol edin, bir sıkıntı yoksa bu mesajı görmezden gelin muhtemelen seçtiğiniz site ile ilgili bir sorun vardır.</code>")
                    except:
                        pass
                except:
                    pass
                logger.error(e)
                logger.warning(json)
                continue
            try:
                json['message']
            except:
                pass
            else:
                if json['message'] == "Invalid URL":
                    logger.error(f"{update.effective_message.chat.title} son postu hatalı olduğu için iptal edildi!")
                    try:
                        bot.send_message(sahip, f"{update.effective_message.chat.title} kaynağının sahibi siz olduğunuz için bu mesaj sadece size gönderildi. \n\nSon postunuz kanallarda paylaşılamadı muhtemelen postun linki API ile kısaltılamayacak kadar uzun.\n\n{json['message']}\n\n{update.effective_message.link}")
                        bot.send_message(chatdat['sahip'], f"{update.effective_message.chat.title} kaynağının sahibi siz olduğunuz için bu mesaj sadece size gönderildi. \n\nSon postunuz kanallarda paylaşılamadı muhtemelen postun linki API ile kısaltılamayacak kadar uzun.\n\n{json['message']}\n\n{update.effective_message.link}")
                    except RetryAfter as rtfr:
                        sleep(rtfr.retry_after+1)
                        bot.send_message(sahip, f"{update.effective_message.chat.title} kaynağının sahibi siz olduğunuz için bu mesaj sadece size gönderildi. \n\nSon postunuz kanallarda paylaşılamadı muhtemelen postun linki API ile kısaltılamayacak kadar uzun.\n\n{json['message']}\n\n{update.effective_message.link}")
                        bot.send_message(chatdat['sahip'], f"{update.effective_message.chat.title} kaynağının sahibi siz olduğunuz için bu mesaj sadece size gönderildi. \n\nSon postunuz kanallarda paylaşılamadı muhtemelen postun linki API ile kısaltılamayacak kadar uzun.\n\n{json['message']}\n\n{update.effective_message.link}")
                    context.job_queue.run_once(deljob, when=2, name="yedekleme", context=update.effective_message.link)
                    break
            newedim_l = sablon.format(aciklama=edited_a, link=link, alink=alink)
            try:
                bot.edit_message_caption(caption=newedim_l, chat_id=edil['chat'], message_id=edil['pid'])
            except Exception as e:
                logger.error(e)
                pass
            else:
                db[str(chat)].update_one({"_id": emid}, {"$set": {"link": edited_l}})
                db[str(chat)].update_one({"_id": emid}, {"$push": {"pids": {"chat": edil['chat'], "pid": edil["pid"], "link": link, "alink": alink, "user": edil["user"]}}})
                edcount += 1
        logger.warning(f"{update.effective_chat.title} kaynağının {edcount} postu düzenlendi.")
        return
    if eski_a != edited_a:
        logger.warning(f"{update.effective_chat.title} kaynağının postu düzenleniyor...")
        for edi in mesdata['pids']:
            if edi['chat'] == botlog:
                continue
            sablon = collection.find_one({"_id": edi['user']})['sablon']
            if sablon == "1":
                sablon = "🔥{aciklama}\n\n🔱 TIKLA 👉 {link}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
            elif sablon == "2" or sablon == "3":
                sablon = "{aciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {link}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 @linkgec06"
            elif sablon == "9":
                sablon = "{aciklama} \n\n𝙇𝙄𝙉𝙆🔗 {link} \n\n     𝙇𝙄𝙉𝙆🔗 {alink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 @linkk_gecmee"
            newedim = sablon.format(aciklama=edited_a, link=edi['link'], alink=edi['alink'])
            try:
                bot.edit_message_caption(caption=newedim, chat_id=edi['chat'], message_id=edi['pid'])
            except Exception as e:
                logger.error(e)
                pass
            else:
                db[str(chat)].update_one({"_id": emid}, {"$set": {"aciklama": edited_a}})
                edcount += 1
        logger.warning(f"{update.effective_chat.title} kaynağının {edcount} postu düzenlendi")

def postsiralandirici(context):
    global postsirasi
    if len(postsirasi) == 0:
        return
    joblananpostlar = context.job_queue.get_jobs_by_name("anaposter")
    for postes in postsirasi:
        ind = postsirasi.index(postes)
        whn = 100 if 3 <= ind < 5 else 10
        if 6 >= ind > 4:
            whn = 200
        if 8 >= ind > 6:
            whn = 300
        if 10 >= ind > 8:
            whn = 400
        if ind > 10:
            whn = 500
        context.job_queue.run_once(poster_job, when=whn, name="anaposter", context=postes) 
    postsirasi = []

def opostsiralandirici(context):
    global opostsirasi
    if len(opostsirasi) == 0:
        return
    ojoblananpostlar = context.job_queue.get_jobs_by_name("ozelposter")
    while len(ojoblananpostlar) > 1:
        ojoblananpostlar = context.job_queue.get_jobs_by_name("ozelposter")
        sleep(1)
    for opostes in opostsirasi:
        context.job_queue.run_once(ozel_poster_job, when=2, name="ozelposter", context=opostes)
    opostsirasi = []

def poster(update, context):
    global postsirasi, opostsirasi
    pochat = update.effective_message.chat.id
    # Ana Kaynaklar
    if KaynakCol.find_one({"_id": pochat}) != None:
        logger.warning(f"{update.effective_message.chat.title} Postu sıraya eklendi.")
        postdict = {"chatid": pochat, "update": update, "groupid": update.effective_message.media_group_id}
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
            if poj.context[0]['groupid'] == update.effective_message.media_group_id:
                poj.context.append(postdict)
                return
        context.job_queue.run_once(poster_job, when=whn, name="anaposter", context=[postdict]) 

    # Özel Kaynaklar
    elif OzelCol.find_one({"okaynak": pochat}) != None:
        logger.warning(f"[ÖZEL] {update.effective_message.chat.title} Postu sıraya eklendi.")
        opostdict = {"chatid": pochat, "update": update}
        opostsirasi.append(opostdict)
