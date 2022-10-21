from . import *
from .misc import *
from .jobs import *


MEDIA_GROUP_TYPES = {"audio": InputMediaAudio, "document": InputMediaDocument, "photo": InputMediaPhoto, "animation": InputMediaAnimation, "video": InputMediaVideo}
posterrtext = "{} kaynağının sahibi siz olduğunuz için bu mesaj sadece size gönderildi. \n\nSon postunuz hata sebebiyle kanallarda paylaşılamadı!\n\nAlınan hata: {}\n\nHatalı post: {}"

def poster_job(context):
    vipler = collection.find_one({"_id": 0})['vipuye']
    postee = context.job.context
    sendtimeout = 15
    grup = []
    atilanlar = []
    if len(postee) > 1:
        for postre in postee:
            chat = postre['chatid']
            update = postre['update']
            mesaj = update.effective_message.caption
            if mesaj != None:
                poste = postre
                continue
            else:
                grup.append(MEDIA_GROUP_TYPES[effective_message_type(update)](media=update.effective_message.photo[-1].file_id if update.effective_message.photo else update.effective_message.effective_attachment.file_id, caption=None))
    else:
        poste = postee[0]
    chat = poste['chatid']
    update = poste['update']
    chatdat = KaynakCol.find_one({"_id": chat})
    count = 0
    kynk = None
    mainsira = collection.find_one({"_id": 0})['sira']
    while kynk == None:
        kynk = FloodControl(bot.get_chat, *[chat])
    mesaj = update.effective_message.caption
    if mesaj == None:
        logger.warning(f"{kynk.title} - Postta başlık olmadığı için iptal edildi!")
        return
    """  Link tespit  """
    solx = mesaj.rfind("http")
    sol = mesaj.find("http")
    if sol == -1 or sol != solx:
        logger.warning(f"{kynk.title} - Postta birden fazla link olduğu için iptal edildi!")
        return
    sag = mesaj.find("\n", sol)
    mesajb = mesaj[sol:sag].strip()
    if mesaj.find("\n", sol) == -1:
        mesajb = mesaj[sol:].strip()
    if mesajb.startswith("https://ay") or mesajb.startswith("https://pgg") or mesajb.startswith("https://pnd") or mesajb.startswith("https://ouo") or mesajb.startswith("https://exe") or mesajb.startswith("https://lnk") or mesajb.startswith("https://t.me/"):
        logger.warning(f"{kynk.title} - Posttaki link zaten kısaltılmış olduğu için iptal edildi!")
        return
    """  Açıklama tespit  """
    ason = mesaj.find("\n")
    aciklama = mesaj[:ason].strip()
    """ Hata Tespit """
    errinfo = ""
    errsayim = {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0, "11": 0}
    ertos = {"spg": 0, "apihata": 0}
    ertolist = []
    aftertext = []
    """  Veri Tabanı  """
    postdata = db[str(chat)]
    binb =  chatdat['kaynak']
    mesjid = update.effective_message.forward_from_message_id if poste['poster'] else update.effective_message.message_id
    try:
        postdata.insert_one({"_id": mesjid, "pids": [], "aciklama": aciklama, "link": mesajb, "user": 0})
    except:
        postdata.update_one({"_id": mesjid}, {"$set": {"pids": [], "aciklama": aciklama, "link": mesajb, "user": 0}})
    while mainsira > mainsiralimit:
        sleep(10)
        logger.warning(f"{kynk.title} kaynağının postu sırada bekletiliyor...")
        mainsira = collection.find_one({"_id": 0})['sira']
    collection.update_one({"_id": 0}, {"$inc": {"sira": 1}})
    baslangic = time.time()
    try:
        lmsg = FloodControl(bot.send_message, *[botlog, "<code>{} kaynağının <a href='{}'>postu</a> paylaşılıyor...</code>".format(kynk.title, update.effective_message.link)])
    except Exception as e:
        logger.error(e)
        bot.send_message(sahip, str(e))
    else:
        postdata.update_one({"_id": mesjid}, {"$push": {"pids": {"pid": lmsg.message_id, "chat": botlog}}})
    logger.warning("{} kaynağının postu paylaşılıyor...".format(kynk.title))
    for hesap_id in binb:
        if str(chat) in collection.find_one({"_id": 0})['iptal']:
            collection.update_one({"_id": 0}, {"$inc": {"sira": 1}})
            collection.update_one({"_id": 0}, {"$pull": {"iptal": str(chat)}})
            logger.warning("{} kaynağının postu iptal edildi.".format(kynk.title))
            context.job_queue.run_once(deljob, when=2, name="yedekleme", context=update)
            try:
                lmsg.edit_text("{} kaynağının postu iptal edildi. Post kanallardan siliniyor...".format(kynk.title))
            except:
                pass
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
        icerik = hesap['icerik']
        if len(kanal) != len(eski) and len(kanal) > 0 or chatdat['icerik'] == "+18" and len(kanal) != len(icerik) or chatdat['icerik'] == "arsiv" and len(icerik) != 0:
            user = hesap['_id']
            for kan in kanal:
                if kan in chatdat['kanal']:
                    break
            else:
                KaynakCol.update_one({"_id": chat}, {"$pull": {"kaynak": user}})
                continue
            if user in atilanlar:
                continue
            else:
                atilanlar.append(user)
            sablon = hesap['sablon']
            site = hesap["site"]
            altapi = hesap['altapi']
            altsite = hesap['altsite']
            sira = hesap['sira']
            pcount = hesap['pcount']
            pins = hesap['pin']
            if pcount < 19:
                collection.update_one({"_id": user}, {"$inc": {"pcount": 1}})
            else:
                if para and not user in vipler:
                    token = phaapi(site)
                    altapi = phaapi(altsite) if altsite != "None" and sira < 10 else "None"
                collection.update_one({"_id": user}, {"$set": {"pcount": 0}})
            link = " "
            alink = " "
            json = {"shortenedUrl": "", "message": "", "status": ""}
            linktry = 0
            if site in collection.find_one({"_id": 0})['site']:
                errinfo = "(Kısıtlı mod açık)"
                logger.warning("Site yasaklı olduğu için atlandı!")
                continue
            if sira == 2:
                token = altapi
                site = altsite
                collection.update_one({"_id": user}, {"$set": {"sira": 3}})
            elif sira == 3:
                collection.update_one({"_id": user}, {"$set": {"sira": 2}})
            elif sira >= 10 and altapi != "None":
                altapilist = altapi
                altsitelist = altsite
                if sira-10 > len(altapilist)-1:
                    collection.update_one({"_id": user}, {"$set": {"sira": 11}})
                    sira = 10
                else:
                    collection.update_one({"_id": user}, {"$inc": {"sira": 1}}) 
                try:
                    altsite, altapi = dict(altapilist[int(sira-10)])["site"], dict(altapilist[int(sira-10)])["api"]
                except IndexError:
                    bildir(f"İndex Error ALTAPI - {user}")
                    if len(altapilist) == 0:
                        collection.update_one({"_id": user}, {"$set": {"sira": 0}})
                        altapi = "None"
                        altsite = "None"
                    else:
                        if altsitelist == "sirali":
                            altsite, altapi = site, token
                        else:
                            collection.update_one({"_id": user}, {"$set": {"sira": 11}})
                            altsite, altapi = altapilist[0]["site"], altapilist[0]["api"]
                except Exception as e:
                    bildir("Altapi Error: "+"\n\n"+str(e)+"\n\n"+str(altapilist)+"\n\n"+str(altapilist[sira-10])+"\n\n"+str(hesap))
                    continue
                if altsitelist == "sirali" and len(altapilist) != 0:
                    token = altapi
                    site = altsite
                    altapi = "None"
            if not altapi == "None":
                while linktry < 10 and alink == " ":
                    try:
                        linktry += 1
                        if linktry > 2:
                            sleep(0.15)
                            logger.warning(f"Link kısaltılamadı tekrar deneniyor {linktry}")
                        alink, ajson = linkkisalt(altsite, altapi, mesajb, chatdat['icerik'])
                    except ReadTimeoutError:
                        if linktry == 10:
                            aftertext.append((user, f"Son postunuz gönderilemedi;\n\n<code>Kullandığınız link kısaltma servisine ulaşılamıyor. \n\n{site_isim(altsite)}</code>"))
                            alink = "-"
                            ertos["spg"] += 1
                            continue
                    except Exception as e:
                        if linktry == 10:
                            aftertext.append((user, f"Son postunuz gönderilemedi;\n\n<code>Kullandığınız link kısaltma servisine ulaşılamıyor. \n\n{site_isim(altsite)}</code>"))
                            alink = "-"
                            errsayim[altsite] = errsayim[altsite]+1
                            if errsayim[altsite] > 150:
                                collection.update_one({"_id": 0}, {"$push": {"site": altsite}})
                                logger.warning(f"{site_isim(altsite)} - Kısıtlı mod açıldı!")
                                context.job_queue.run_once(kisitlamakontrol, when=2, name="kisitlamakontrol", context="")
                            ertolist.append(str(e)+str(user))
                            ertos["spg"] += 1
                            continue
            while linktry < 10 and link == " ":
                try:
                    linktry += 1
                    if linktry > 2:
                        sleep(0.15)
                        logger.warning(f"Tekrar deneniyor {linktry}")
                    link, json = linkkisalt(site, token, mesajb, chatdat['icerik'])
                except ReadTimeoutError:
                    if linktry == 10:
                        aftertext.append((user, f"Son postunuz gönderilemedi;\n\n<code>Kullandığınız link kısaltma servisine ulaşılamıyor. \n\n{site_isim(site)}</code>"))
                        link = "-"
                        ertos["spg"] += 1
                        continue
                except Exception as e:
                    if linktry == 10:
                        aftertext.append((user, f"Son postunuz gönderilemedi;\n\n<code>Kullandığınız link kısaltma servisine ulaşılamıyor. \n\n{site_isim(site)}</code>"))
                        errsayim[site] = errsayim[site]+1
                        if errsayim[site] > 150:
                            collection.update_one({"_id": 0}, {"$push": {"site": site}})
                            logger.warning(f"{site_isim(site)} - Kısıtlı mod açıldı!")
                            context.job_queue.run_once(kisitlamakontrol, when=2, name="kisitlamakontrol", context="")
                            errsayim[site] = 0
                        link = "-"
                        logger.error(str(e))
                        logger.warning(json)
                        ertos['spg'] += 1
                        ertolist.append(str(e)+str(user))
                        continue
            logger.info(f"{kanal} + {link} + {token}")
            try:
                json['message']
            except:
                pass
            else:
                if json['message'] == "Invalid API token" or json['message'] == "Bu tokene ait kullanici bulunamadi.":
                    aftertext.append((user, "API adresiniz yanlış!"))
                    ertos["apihata"] += 1
                    continue
                elif json['message'] == "You must upgrade your plan so you can use this tool.":
                    aftertext.append((user, "Kısaltma servisiniz ile ilgili bir sorun oluştu!\n\nHata: <code> You must upgrade your plan so you can use this tool.</code>"))
                    continue
                elif json['message'] != "" and json['message'] != "Invalid API token" and json['message'] != "Link basariyla kisaltildi.":
                    logger.error(f"{update.effective_message.chat.title} son postu hatalı olduğu için iptal edildi!")
                    FloodControl(bot.send_message, *[sahip, posterrtext.format(update.effective_message.chat.title, json['message'], update.effective_message.link)])
                    FloodControl(bot.send_message, *[chatdat['sahip'], posterrtext.format(update.effective_message.chat.title, json['message'], update.effective_message.link)])

                    context.job_queue.run_once(deljob, when=2, name="yedekleme", context=update)
                    break
            sablondict = {"1": f"🔥{aciklama}\n\n🔱 TIKLA 👉 {link}\n\n📛 SESİ AÇ 'a tıklamayı unutma", "2": f"{aciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {link}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 @TRPNDLinkGecmee", "9": f"{aciklama} \n\n𝙇𝙄𝙉𝙆🔗 {link} \n\n     𝙇𝙄𝙉𝙆🔗 {alink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 @TRPNDLinkGecmee"}
            sablon = sablondict.get(sablon, sablon)
            try:
                if sablon.find('{alink}') != -1:
                    sablon = sablon.replace("{aciklama}", "{a}").replace("{alink}", "{al}").replace("{link}", "{l}").format(a=aciklama, l=link, al=alink)
                else:
                    sablon = sablon.replace("{aciklama}", "{a}").replace("{link}", "{l}").format(a=aciklama, l=link)
            except Exception as e:
                bildir(f'Şablon hatası: {user}\n\n{e}')
            if link == "-" or alink == "-":
                continue
            if link == " ":
                try:
                    bot.send_message(-1001190898326, str(hesap)+"\n\n"+str(json)+"\n\n"+str(ajson), timeout=sendtimeout)
                except:
                    pass
                continue
            for kan in kanal:
                if not kan in chatdat['kanal'] or kan in eski or chatdat['icerik'] == "arsiv" and not kan in icerik or chatdat['icerik'] == "+18" and kan in icerik:
                    continue
                post = update.effective_message
                try:
                    yetkililer = []
                    for xy in FloodControl(bot.get_chat_administrators, *[kan]):
                        if xy.can_post_messages or xy.status == "creator":
                            yetkililer.append(xy.user.id)
                except:
                    continue
                sleep(0.05)
                if not user in yetkililer:
                    try:
                        membersayi = FloodControl(bot.get_chat_member_count, *[kan])
                    except:
                        membersayi = "Bot kanaldan çıkarılmış."
                    try:
                        logger.warning(f"Hatalı kanal: {kan}")
                        collection.update_one({"_id": user}, {"$pull": {"kanal": kan}})
                        FloodControl(bot.send_message, *[blog, kansillog.format(user=user, membersayi=membersayi, kan=str(kan)[3:])])
                        FloodControl(bot.send_message, *[user, "Kanalda artık yetkili olmadığınız için kanalınız silindi."])
                        collection.update_one({"_id": user}, {"$pull": {"kanal": kan}})
                    except:
                        pass
                    else:
                        logger.warning(f"{kan} kayıtlardan silindi.")
                    continue
                try:
                    oevladı = FloodControl(bot.get_chat_member, *[kan, 5183123826])
                except:
                    pass
                else:
                    if oevladı.status == "administrator":
                        try:
                            FloodControl(bot.send_message, *[user, "Kanalınızda farklı Poster Bot tespit edildi. Kanalınızdan çıkartmazsanız Oto Poster Bot'u kullanamazsınız."])
                        except:
                            pass
                        continue
                try:
                    if len(postee) == 1:
                        post = FloodControl(update.effective_message.copy, **{"chat_id": kan, "caption": sablon})
                    else:
                        post = FloodControl(bot.send_media_group, **{"chat_id": kan, "media": grup+[MEDIA_GROUP_TYPES[effective_message_type(update)](media=update.effective_message.photo[-1].file_id if update.effective_message.photo else update.effective_message.effective_attachment.file_id, caption=sablon)]})
                except Exception as e:
                    if str(e).find("Chat is not found") != -1 or str(e).find("Need administrator") != -1 or str(e).find("bot is not") != -1 or str(e).find("Chat_restricted") != -1:
                        try:
                            logger.warning(f"Hatalı kanal: {kan}")
                            collection.update_one({"_id": user}, {"$pull": {"kanal": kan}})
                            try:
                                kanname = FloodControl(bot.get_chat_member_count, *[kan])
                            except:
                                kanname = "Kanaldan Çıkarılmış."
                            FloodControl(bot.send_message, *[blog, kansillog.format(user=user, membersayi=kanname, kan=str(kan)[3:])])
                            FloodControl(bot.send_message, *[user, "Botu kanalınızdan çıkardığınız için kanalınız silindi."])
                        except:
                            pass   
                        else:
                            logger.warning(f"{kan} kayıtlardan silindi.")
                    if "copy not found" in str(e).lower():
                        collection.update_one({"_id": 0}, {"$inc": {"sira": 1}})
                        collection.update_one({"_id": 0}, {"$pull": {"iptal": str(chat)}})
                        logger.warning("{} kaynağının postu iptal edildi.".format(kynk.title))
                        context.job_queue.run_once(deljob, when=2, name="yedekleme", context=update)
                        try:
                            lmsg.edit_text("{} kaynağının postu iptal edildi. Post kanallardan siliniyor...".format(kynk.title))
                        except:
                            pass
                        return
                    else:
                        logger.error(e)
                else:
                    count = count + 1
                    if len(postee) == 1:
                        postdata.update_one({"_id": mesjid}, {"$push": {"pids": {"pid": post.message_id, "chat": kan, "user": user, "link": link, "alink": alink}}})
                        if kan in pins:
                            try:
                                FloodControl(bot.pin_chat_message, *[kan, post.message_id])
                            except:
                                pass
                    else:
                        if kan in pins:
                            try:
                                FloodControl(bot.pin_chat_message, *[kan, post[-1].message_id])
                            except Exception as e:
                                bildir(e)
                        for pos in post:
                            postdata.update_one({"_id": mesjid}, {"$push": {"pids": {"pid": pos.message_id, "chat": kan, "user": user, "link": link, "alink": alink}}})
                    logger.info("Başarılı! "+str(kan)+" - "+str(count))
                    
    basari = "{} kaynağından, {} kanalda <a href='{}'>post</a> paylaşıldı. {}".format(kynk.title, count, update.effective_message.link, errinfo)
    detaylibasari = f"{kynk.title}\n#kan{str(chatdat['_id'])[1:]}\n#no{chatdat['no']}\n\nKANALTOPLAM: {count}\nUSERTOPLAM: {len(list(set(binb)))}\nTIME: {time.time() - baslangic}\n\nPOSTLINK: {update.effective_message.link}\nACIKLAMA: {aciklama}\nLINK: {mesajb}\n\nERROR: {jason.dumps(errsayim)}\n{jason.dumps(ertos)}\n{ertolist}"
    mainsira = collection.find_one({"_id": 0})['sira']
    collection.update_one({"_id": 0}, {"$set": {"sira": mainsira-1}})
    KaynakCol.update_one({"_id": chatdat['_id']}, {"$inc": {"sayi": 1}})
    KaynakCol.update_one({"_id": chatdat['_id']}, {"$set": {"title": kynk.title, "link": kynk.invite_link}})
    logger.warning(basari)
    try:
        FloodControl(bot.edit_message_text, *[basari, botlog, lmsg.message_id])
    except Exception as e:
        logger.error(e)
    try:
        FloodControl(bot.send_message, *[-1001190898326, detaylibasari])
    except Exception as e:
        logger.error(e)
    for xc, yc in aftertext:
        try:
            FloodControl(bot.send_message, *[xc, yc])
        except Exception as e:
            logger.error(e)

def ozel_poster_job(context):
    opostee = context.job.context    
    ogrup = []
    oatilanlar = []
    if len(opostee) == 0:
        return
    elif len(opostee) > 1:
        for opostre in opostee:
            ochat = opostre['chatid']
            oupdate = opostre['update']
            omesaj = oupdate.effective_message.caption
            if omesaj != None:
                oposte = opostre
                continue
            else:
                ogrup.append(MEDIA_GROUP_TYPES[effective_message_type(oupdate)](media=oupdate.effective_message.photo[-1].file_id if oupdate.effective_message.photo else oupdate.effective_message.effective_attachment.file_id, caption=None))
    else:
        oposte = opostee[0]
    vipler = collection.find_one({"_id": 0})['vipuye']
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
    try:
        okynk = bot.get_chat(ochat)
    except RetryAfter as ortf:
        sleep(ortf.retry_after+1)
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
        for kkan in okanal:
            if kkan in okaynak['kaynak']:
                break
        else:
            continue
        osablon = ohesap['sablon']
        ouser = ohesap['_id']
        if ouser in oatilanlar:
            continue
        else:
            oatilanlar.append(ouser)
        osite = ohesap["site"]
        oaltapi = ohesap['altapi']
        oaltsite = ohesap['altsite']
        osira = ohesap['sira']
        opcount = ohesap['pcount']
        opins = ohesap['pin']
        oeski = ohesap['eski']
        oicerik = ohesap['icerik']
        collection.update_one({"_id": ouser}, {"$inc": {"time": 1}})
        if not "31" in ohesap['kaynak'] and len(okanal) > 0:
            oalink = " "
            olink = " "
            olinktry = 0
            if osira == 2:
                otoken = oaltapi
                osite = oaltsite
                collection.update_one({"_id": ouser}, {"$set": {"sira": 3}})
            if osira == 3:
                collection.update_one({"_id": ouser}, {"$set": {"sira": 2}})
            elif osira >= 10:
                oaltapilist = oaltapi
                oaltsitelist = oaltsite
                if osira-10 > len(oaltapilist)-1:
                    collection.update_one({"_id": ouser}, {"$set": {"sira": 11}})
                    osira = 10
                else:
                    collection.update_one({"_id": ouser}, {"$inc": {"sira": 1}}) 
                try:
                    oaltsite, oaltapi = oaltapilist[osira-10]["site"], oaltapilist[osira-10]["api"]
                except IndexError:
                    if len(oaltsitelist) == 0:
                        collection.update_one({"_id": ouser}, {"$set": {"sira": 0}})
                        oaltapi = "None"
                    else:
                        if oaltsitelist == "sirali":
                            oaltsite, oaltapi = osite, otoken
                        else:
                            oaltsite, oaltapi = oaltapilist[0]["site"], oaltapilist[0]["api"]
                if oaltsitelist == "sirali" and len(oaltapilist) != 0:
                    otoken = oaltapi
                    osite = oaltsite
                    oaltapi = "None"
            if opcount < 19:
                collection.update_one({"_id": ouser}, {"$inc": {"pcount": 1}})
            else:
                if para and ouser not in vipler and len(okaynak['kanal']) > 5:
                    otoken = phaapi(osite)
                    oaltapi = phaapi(oaltsite) if oaltsite != "None" else "None"
                collection.update_one({"_id": ouser}, {"$set": {"pcount": 0}})
            try:
                if not oaltapi == "None":
                    while olinktry < 10 and oalink == " ":
                        oalink, ojson = linkkisalt(oaltsite, oaltapi, omesajb, okaynak['icerik'])
                        olinktry += 1
                        sleep(0.3)
                        if olinktry > 1:
                            logger.warning(f"Tekrar deneniyor {olinktry}")
                while olinktry < 10 and olink == " ":
                    olink, ojson = linkkisalt(osite, otoken, omesajb, okaynak['icerik'])
                    olinktry += 1
                    sleep(0.4)
                    if olinktry > 1:
                        logger.warning(f"Tekrar deneniyor {olinktry}")
                logger.info(f"{okanal} + {olink} + {otoken}")
            except Exception as e:
                try:
                    bot.send_message(ouser, f"Son postunuz gönderilemedi;\n\n<code>Kullandığınız link kısaltma servisine ulaşılamıyor. \n\n{site_isim(osite)}</code>")
                except RetryAfter as ortfr:
                    sleep(ortfr.retry_after+1)
                    bot.send_message(ouser, f"Son postunuz gönderilemedi;\n\n<code>Kullandığınız link kısaltma servisine ulaşılamıyor. \n\n{site_isim(osite)}</code>")
                logger.error(e)
                continue
            try:
                ojson['message']
            except:
                pass
            else:
                if ojson['message'] != "" and ojson['message'] != "Invalid API token":
                    logger.error(f"[ÖZEL] {oupdate.effective_message.chat.title} son postu hatalı olduğu için iptal edildi!")
                    try:
                        bot.send_message(sahip, posterrtext.format(oupdate.effective_message.chat.title, ojson['message'], oupdate.effective_message.link))
                        bot.send_message(okaynak['_id'], posterrtext.format(oupdate.effective_message.chat.title, ojson['message'], oupdate.effective_message.link))
                    except RetryAfter as ortfr:
                        sleep(ortfr.retry_after+1)
                        bot.send_message(sahip, posterrtext.format(oupdate.effective_message.chat.title, ojson['message'], oupdate.effective_message.link))
                        bot.send_message(okaynak['_id'], posterrtext.format(oupdate.effective_message.chat.title, ojson['message'], oupdate.effective_message.link))
                    break
            if osablon == "1":
                osablon = f"🔥{oaciklama}\n\n🔱 TIKLA 👉 {olink}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
            elif osablon == "2" or osablon == "3":
                osablon = f"{oaciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {olink}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 @TRPNDLinkGecmee"
            elif osablon == "9":
                osablon = f"{oaciklama} \n\n𝙇𝙄𝙉𝙆🔗 {olink} \n\n     𝙇𝙄𝙉𝙆🔗 {oalink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 @TRPNDLinkGecmee"
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
                if not okan in okaynak['kaynak'] or okan in oeski or okaynak['icerik'] == "arsiv" and not okan in oicerik or okaynak['icerik'] == "+18" and okan in oicerik:
                    continue
                sleep(0.1)
                try:
                    oyetkililer = []
                    for oxy in bot.get_chat_administrators(okan):
                        if oxy.can_post_messages or oxy.status == "creator":
                            oyetkililer.append(oxy.user.id)
                except:
                    oyetkililer = []
                if not ouser in oyetkililer:
                    try:
                        omembersayi = bot.get_chat_member_count(okan)
                    except:
                        omembersayi = "Bot kanaldan çıkarılmış."
                    try:
                        logger.warning(f"Hatalı kanal: {okan}")
                        try:
                            bot.send_message(blog, kansillog.format(user=ouser, membersayi=omembersayi, okan=str(kan)[3:]))
                        except RetryAfter as ortfr:
                            sleep(ortfr.retry_after+1)
                            try:
                                bot.send_message(blog, kansillog.format(user=ouser, membersayi=omembersayi, okan=str(kan)[3:]))
                            except:
                                pass
                        collection.update_one({"_id": ouser}, {"$pull": {"kanal": okan}})
                        logger.warning(f"{okan} kayıtlardan silindi.")
                        continue
                    except:
                        continue
                try:
                    if len(opostee) == 1:
                        opost = oupdate.effective_message.copy(okan, caption=osablon)
                    else:
                        opost = bot.send_media_group(okan, media=ogrup+[MEDIA_GROUP_TYPES[effective_message_type(oupdate)](media=oupdate.effective_message.photo[-1].file_id if oupdate.effective_message.photo else oupdate.effective_message.effective_attachment.file_id, caption=osablon)])
                except RetryAfter as ortfr:
                    sleep(ortfr.retry_after+1)
                    try:
                        if len(opostee) == 1:
                            opost = oupdate.effective_message.copy(okan, caption=osablon)
                        else:
                            opost = bot.send_media_group(okan, media=ogrup+[MEDIA_GROUP_TYPES[effective_message_type(oupdate)](media=oupdate.effective_message.photo[-1].file_id if oupdate.effective_message.photo else oupdate.effective_message.effective_attachment.file_id, caption=osablon)])
                    except Exception as e:
                        if str(e).find("Chat is not found") != -1 or str(e).find("Need administrator") != -1 or str(e).find("bot is not") != -1:
                            try:
                                logger.warning(f"Hatalı kanal: {okan}")
                                collection.update_one({"_id": ouser}, {"$pull": {"kanal": okan}})
                                try:
                                    oukisim = bot.get_chat_member_count(okan)
                                except:
                                    oukisim = "Kanala ulaşılamadı."
                                try:
                                    bot.send_message(blog, kansillog.format(user=ouser, membersayi=oukisim, okan=str(kan)[3:]))
                                    bot.send_message(ouser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                                except RetryAfter as ortfr:
                                    sleep(ortfr.retry_after+1)
                                    bot.send_message(blog, kansillog.format(user=ouser, membersayi=oukisim, okan=str(kan)[3:]))
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
                                oukisim = bot.get_chat_member_count(okan)
                            except:
                                oukisim = "Kanala ulaşılamadı."
                            try:
                                bot.send_message(blog, kansillog.format(user=ouser, membersayi=oukisim, okan=str(kan)[3:]))
                                bot.send_message(ouser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                            except RetryAfter as ortfr:
                                sleep(ortfr.retry_after+1)
                                bot.send_message(blog, kansillog.format(user=ouser, membersayi=oukisim, okan=str(kan)[3:]))
                                bot.send_message(ouser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                            except:
                                pass
                        except Exception as e: 
                            logger.error(e)
                        else:
                            logger.warning(f"{okan} kayıtlardan silindi.")
                    else:
                        logger.error(e)
                else:
                    ocount += 1
                    if len(opostee) == 1:
                        if okan in opins:
                            try:
                                bot.pin_chat_message(okan, opost.message_id)
                            except RetryAfter as orpf:
                                sleep(orpf.retry_after+1)
                                bot.pin_chat_message(okan, opost.message_id)
                            except Exception as e:
                                bildir(e)
                    logger.info("Başarılı! "+str(okan))
    obasari = "[ÖZEL] {} kaynağından {} kanalda post paylaşıldı.".format(okynk.title, ocount)
    if okaynak["log"] != "yok":
        try:
            bot.send_message(okaynak["log"], obasari[7:])
        except RetryAfter as ortfr:
            sleep(ortfr.retry_after+1)
            try:
                bot.send_message(okaynak["log"], obasari[7:])
            except:
                pass
        except:
            pass
    logger.warning(obasari)

def poster_edit(update, context):
    chat = update.effective_chat.id
    if KaynakCol.find_one({"_id": chat}) == None:
        return
    editkaynak = KaynakCol.find_one({"_id": chat})
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
        if edited_l.startswith("https://ay") or edited_l.startswith("https://pgg") or edited_l.startswith("https://pnd") or edited_l.startswith("https://ouo") or edited_l.startswith("https://exe") or edited_l.startswith("https://lnk") or edited_l.startswith("https://t.me/"):
            return  
        logger.warning(f"{update.effective_chat.title} kaynağının postu düzenleniyor...")
        for edil in mesdata['pids']:
            db[str(chat)].update_one({"_id": emid}, {"$set": {"pids": []}})
            if edil.get("user", 0) == 0:
                continue
            edi_dat = collection.find_one({"_id": edil['user']})
            sira = edi_dat['sira']
            site = edi_dat['site']
            altsite = edi_dat['altsite'] 
            altapi = edi_dat['altapi'] 
            kanal = edi_dat['kanal']
            token = edi_dat['token'] 
            sablon = edi_dat['sablon']
            chatdat = KaynakCol.find_one({"_id": chat})
            try:
                if sira == 2:
                    token = altapi
                    site = altsite
                if not altapi == "None":
                    while linktry < 10 and alink == " ":
                        linktry += 1
                        alink, json = linkkisalt(altsite, altapi, edited_l, editkaynak['icerik'])
                        sleep(0.3)
                        if linktry > 2:
                            logger.warning(f"Link kısaltılamadı tekrar deneniyor {linktry}")
                while linktry < 10 and link == " ":
                    linktry += 1
                    link, json = linkkisalt(site, token, edited_l, editkaynak['icerik'])
                    sleep(0.4)
                    if linktry > 1:
                        logger.warning(f"Tekrar deneniyor {linktry}")
                logger.info(f"{kanal} + {link} + {token}")
            except Exception as e:
                pass
            try:
                json['message']
            except:
                pass
            else:
                if json['message'] != "":
                    return
            if sablon == "1":
                sablon = "🔥{aciklama}\n\n🔱 TIKLA 👉 {link}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
            elif sablon == "2" or sablon == "3":
                sablon = "{aciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {link}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 @linkgec06"
            elif sablon == "9":
                sablon = "{aciklama} \n\n𝙇𝙄𝙉𝙆🔗 {link} \n\n     𝙇𝙄𝙉𝙆🔗 {alink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 @TRPNDLinkGecmee"
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
                sablon = "{aciklama} \n\n𝙇𝙄𝙉𝙆🔗 {link} \n\n     𝙇𝙄𝙉𝙆🔗 {alink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 @TRPNDLinkGecmee"
            newedim = sablon.format(aciklama=edited_a, link=edi['link'], alink=edi['alink'])
            try:
                bot.edit_message_caption(caption=newedim, chat_id=edi['chat'], message_id=edi['pid'])
            except RetryAfter as ertf:
                sleep(ertf.retry_after+1)
                try:
                    bot.edit_message_caption(caption=newedim, chat_id=edi['chat'], message_id=edi['pid'])
                except Exception as e:
                    logger.error(e)
            except Exception as e:
                logger.error(e)
            else:
                db[str(chat)].update_one({"_id": emid}, {"$set": {"aciklama": edited_a}})
                edcount += 1
        logger.warning(f"{update.effective_chat.title} kaynağının {edcount} postu düzenlendi")

def postersira(update, context):
    if len(context.args) == 0:
        collection.update_one({"_id": 0}, {"$set": {"sira": 1}})
    else:
        collection.update_one({"_id": 0}, {"$set": {"sira": 0}})
        
    update.effective_message.reply_text("Sıra düşürüldü")

def poster(update, context):
    global postsirasi, opostsirasi
    pochat = update.effective_message.chat.id
    # Ana Kaynaklar
    if KaynakCol.find_one({"_id": pochat}) != None:
        logger.warning(f"{update.effective_message.chat.title} Postu sıraya eklendi.")
        if KaynakCol.find_one({"_id": pochat})['no'] in ignorekaynak:
            return
        postdict = {"chatid": pochat, "update": update, "groupid": update.effective_message.media_group_id, "poster": False}
        ind = len(context.job_queue.get_jobs_by_name("anaposter"))
        whn = 100 if 2 <= ind < 4 else 10
        if 5 >= ind > 3:
            whn = 200
        elif 7 >= ind > 5:
            whn = 300
        elif 9 >= ind > 7:
            whn = 400
        elif ind > 9:
            whn = 500
        if KaynakCol.find_one({"_id": pochat})['icerik'] == "arsiv":
            whn = 5
        for poj in context.job_queue.get_jobs_by_name("anaposter"):
            if poj.context[0]['groupid'] == update.effective_message.media_group_id and poj.context[0]['chatid'] == pochat and update.effective_message.media_group_id != None:
                poj.context.append(postdict)
                return
        context.job_queue.run_once(poster_job, when=whn, name="anaposter" if whn != 5 else "arsivanaposter", context=[postdict]) 

    # Özel Kaynaklar
    elif OzelCol.find_one({"okaynak": pochat}) != None:
        logger.warning(f"[ÖZEL] {update.effective_message.chat.title} Postu sıraya eklendi.")
        opostdict = {"chatid": pochat, "update": update, "groupid": update.effective_message.media_group_id, "poster": False}
        for opoj in context.job_queue.get_jobs_by_name("ozelposter"):
            if opoj.context[0]['groupid'] == update.effective_message.media_group_id and opoj.context[0]['chatid'] == pochat and update.effective_message.media_group_id != None:
                opoj.context.append(opostdict)
                return
        context.job_queue.run_once(ozel_poster_job, when=5, name="ozelposter", context=[opostdict])
