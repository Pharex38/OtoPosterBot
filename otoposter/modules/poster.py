import requests
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
from telegram.error import BadRequest, Unauthorized
from requests import get, Session
from otoposter import *
from time import sleep
from .misc import *

def poster(update, context):
    okaynak = None
    chat = update.channel_post.chat.id
    # Link Mahzeni
    if chat == kaynaklar[0] and mahzen:
        count = 0
        mesaj = update.channel_post.caption
        if mesaj == None:
            return
        """  Link tespit  """
        solx = mesaj.rfind("http")
        sol = mesaj.find("http")
        if sol == -1:
            return
        if sol != solx:
            return
        sag = mesaj.find("\n", sol)
        kynk = bot.get_chat(chat)
        mesajb = mesaj[sol:sag].strip()
        if mesaj.find("\n", sol) == -1:
            mesajb = mesaj[sol:].strip()
        if mesajb.startswith("https://t.me/"):
            return
        logger.warning("{} postu atılıyor... ".format(kynk.title))
        """  Açıklama tespit  """
        ason = mesaj.rfind("\n", 0, sol)
        aciklama = mesaj[:ason].strip()
        """  Cookies  """
        s = Session()
        link = s.get("https://ay.live/")
        cookies = dict(link.cookies)
        """  Veri Tabanı  """
        postdata = db[str(chat)]
        binb = collection.find({})
        mesjid = update.channel_post.message_id
        """ Dosya tespit """
        if update.channel_post.photo:
            medya = update.channel_post.photo[0].file_id
        if update.channel_post.animation:
            medya = update.channel_post.animation.file_id
        if update.channel_post.video:
            medya = update.channel_post.video.file_id
        for hesap in binb:
            ret = True
            kaynak = hesap['kaynak']
            try:
                token = hesap['token']
            except:
                ret = False
            kanal = hesap['kanal']
            sablon = hesap['sablon']
            user = hesap['_id']
            site = hesap["site"]
            altapi = hesap['altapi']
            altsite = hesap['altsite']
            sira = hesap['sira']
            if "1" in kaynak and len(kanal) > 0 and ret:
                link = " "
                alink = " "
                json = " "
                try:
                    if sira == "2":
                        token = altapi
                        site = altsite
                        collection.update_one({"_id": user}, {"$set": {"sira": "3"}})
                    if sira == "3":
                        collection.update_one({"_id": user}, {"$set": {"sira": "2"}})
                    if not altapi == "None":
                        if altsite == "1":
                            json = s.get(f"https://ay.live/api/?", params={'api': altapi, 'url': mesajb, 'ct': 1}, cookies=cookies).json()
                            alink = json['shortenedUrl']
                        if altsite == "2":
                            json = s.get(f"https://www.pnd.tl/api?", params={'api': altapi, 'url': mesajb, 'category': 6}).json()
                            alink = json['shortenedUrl']
                        if altsite == "3":
                            json = s.get(f"https://exe.io/api?", params={'api': altapi, 'url': mesajb}).json()
                            alink = json['shortenedUrl']
                        if altsite == "4":
                            alink = s.get(f"http://ouo.io/api/{altapi}?", params={'s': mesajb}).text
                        if altsite == "5":
                            alink = s.get(f"http://pubiza.com/api.php?", params={'token': altapi, 'url': mesajb, 'ads_type': "adult"}).text
                    if site == "1":
                        json = s.get(f"https://ay.live/api/?", params={'api': token, 'url': mesajb, 'ct': 1}, cookies=cookies).json()
                        link = json['shortenedUrl']
                    if site == "2":
                        json = s.get(f"https://www.pnd.tl/api?", params={'api': token, 'url': mesajb, 'category': 6}).json()
                        link = json['shortenedUrl']
                    if site == "3":
                        json = s.get(f"https://exe.io/api?", params={'api': token, 'url': mesajb}).json()
                        link = json['shortenedUrl']
                    if site == "4":
                        link = s.get(f"http://ouo.io/api/{token}?", params={'s': mesajb}).text
                    if site == "5":
                        link = s.get(f"http://pubiza.com/api.php?", params={'token': token, 'url': mesajb, 'ads_type': "adult"}).text
                    logger.info(f"{kanal} + {link} + {token}")
                except Exception as e:
                    bot.send_message(user, "Son postunuz gönderilemedi;\n\n<code>API adresiniz sıkıntılı veya sitenize ulaşılamıyor. API adresinizi kontrol edin, bir sıkıntı yoksa bu mesajı görmezden gelin muhtemelen seçtiğiniz site ile ilgili bir sorun vardır.</code>")
                    logger.error(e)
                    logger.debug(json)
                    ret = False
                if sablon == "1":
                    sablon = f"🔥{aciklama}\n\n🔱 TIKLA 👉 {link}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
                elif sablon == "2" or sablon == "3":
                    sablon = f"{aciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {link}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 #linkgec06"
                elif sablon == "9":
                    sablon = f"{aciklama} \n\n𝙇𝙄𝙉𝙆🔗 {link} \n\n     𝙇𝙄𝙉𝙆🔗 {alink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 #linkk_gecmee"
                elif sablon.find('{alink}') != -1:
                    sablon = sablon.replace("{aciklama}", "{}").replace("{alink}", "{}").replace("{link}", "{}").format(aciklama, link, alink)
                else:
                    sablon = sablon.replace("{aciklama}", "{}").replace("{link}", "{}").format(aciklama, link)
                sleep(1.6)
                for kan in kanal:
                    try:
                        if update.channel_post.photo and ret:
                            post = bot.send_photo(kan, medya, caption=sablon)
                        if update.channel_post.video and ret:
                            post = bot.send_video(kan, medya, caption=sablon)
                        if update.channel_post.animation and ret:
                            post = bot.send_animation(kan, medya, caption=sablon)
                    except BadRequest as bd:
                        if bd.args == "Chat is not found":
                            raise Unauthorized
                        else:
                            logger.error(bd)
                    except Unauthorized:
                        logger.debug(f"Hatalı kanal: {kanal}")
                        collection.update_one({"_id": user}, {"$pull": {"kanal": kan}})
                        try:
                            bot.send_message(user, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                        except:
                            pass   
                        logger.debug(f"{kanal} kayıtlardan silindi.")
                    except Exception as e:
                        logger.error(e)
                    else:
                        count = count + 1
                        postdata.insert_one({"pid": post.message_id, "chat": kan, "mesih": mesjid})
                logger.info("Başarılı!")
            else:
                pass
        basari = "{} kaynağından, {} Kanalda Post Paylaşıldı.".format(kynk.title, count)
        logger.warning(basari)
        bot.send_message(botlog, basari)
    # Bedava Link
    elif chat == kaynaklar[1] and bedava:
        bcount = 0
        bmesaj = update.channel_post.caption
        if bmesaj == None:
            return
        """ Link tespit """
        bsolx = bmesaj.rfind("http")
        bsol = bmesaj.find("http")
        if bsol == -1:
            return
        bsag = bmesaj.find("\n", bsol)
        if bsol != bsolx:
            return
        bmesajb = bmesaj[bsol:bsag].strip()
        if bmesaj.find("\n", bsol) == -1:
            bmesajb = bmesaj[bsol:].strip()
        if bmesajb.startswith("https://t.me/"):
            return
        bkynk = bot.get_chat(chat)
        logger.warning("{} postu atılıyor... ".format(bkynk.title))
        """ Açıklama tespit """
        bason = bmesaj.rfind("\n", 0, bsol)
        baciklama = bmesaj[:bason].strip()
        """    Cookies    """
        s = Session()
        link = s.get("https://ay.live/api")
        cookies = dict(link.cookies)
        """  Veri Tabanı  """
        bpostdata = db[str(chat)]
        bbinb = collection.find({})
        bmesjid = update.channel_post.message_id
        """ Dosya tespit """
        if update.channel_post.photo:
            bmedya = update.channel_post.photo[0].file_id
        if update.channel_post.animation:
            medya = update.channel_post.animation.file_id
        if update.channel_post.video:
            bmedya = update.channel_post.video.file_id
        for bhesap in bbinb:
            bret = True
            bkaynak = bhesap['kaynak']
            bsablon = bhesap['sablon']
            bsablon = str(bsablon)
            try:
                btoken = bhesap['token']
            except:
                bret = False
            bkanal = bhesap['kanal']
            buser = bhesap['_id']
            bsite = bhesap['site']
            baltapi = bhesap['altapi']
            baltsite = bhesap['altsite']
            bsira = bhesap['sira']
            if "2" in bkaynak and len(bkanal) > 0 and bret:
                balink = " "
                blink = " "
                bjson = " "
                if bsira == "2":
                    btoken = baltapi
                    bsite = baltsite
                    collection.update_one({"_id": buser}, {"$set": {"sira": "3"}})
                if bsira == "3":
                    collection.update_one({"_id": buser}, {"$set": {"sira": "2"}})
                try:
                    if not baltapi == "None":
                        if baltsite == "1":
                            bjson = s.get(f"https://ay.live/api/?", params={'api': baltapi, 'url': bmesajb, 'ct': 1}, cookies=cookies).json()
                            balink = bjson['shortenedUrl']
                        if baltsite == "2":
                            bjson = s.get(f"https://www.pnd.tl/api?", params={'api': baltapi, 'url': bmesajb, 'category': 6}).json()
                            balink = bjson['shortenedUrl']
                        if baltsite == "3":
                            bjson = s.get(f"https://exe.io/api?", params={'api': baltapi, 'url': bmesajb}).json()
                            balink = bjson['shortenedUrl']
                        if baltsite == "4":
                            balink = s.get(f"http://ouo.io/api/{baltapi}?", params={'s': bmesajb}).text
                        if baltsite == "5":
                            balink = s.get(f"http://pubiza.com/api.php?", params={'token': baltapi, 'url': bmesajb, 'ads_type': "adult"}).text
                    sleep(1.6)
                    if bsite == "1":
                        bjson = s.get(f"https://ay.live/api/?", params={'api': btoken, 'url': bmesajb, 'ct': 1}, cookies=cookies).json()
                        blink = bjson['shortenedUrl']
                    if bsite == "2":
                        bjson = s.get(f"https://www.pnd.tl/api?", params={'api': btoken, 'url': bmesajb, 'category': 6}).json()
                        blink = bjson['shortenedUrl']
                    if bsite == "3":
                        bjson = s.get(f"https://exe.io/api?", params={'api': btoken, 'url': bmesajb}).json()
                        blink = bjson['shortenedUrl']
                    if bsite == "4":
                        blink = s.get(f"http://ouo.io/api/{btoken}?", params={'s': bmesajb}).text
                    if bsite == "5":
                        blink = s.get(f"http://pubiza.com/api.php?", params={'token': btoken, 'url': bmesajb, 'ads_type': "adult"}).text
                    logger.info(f"{bkanal} + {blink} + {btoken}")
                except Exception as e:
                    bot.send_message(buser, "Son postunuz gönderilemedi;\n\n<code>API adresiniz sıkıntılı veya sitenize ulaşılamıyor. API adresinizi kontrol edin, bir sıkıntı yoksa bu mesajı görmezden gelin muhtemelen seçtiğiniz site ile ilgili bir sorun vardır.</code>")
                    logger.error(e)
                    logger.debug(bjson)
                    bret = False
                if bsablon == "1":
                    bsablon = f"🔥{baciklama}\n\n🔱 TIKLA 👉 {blink}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
                elif bsablon == "2" or bsablon == "3":
                    bsablon = f"{baciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {blink}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 #linkgec06"
                elif bsablon == "9":
                    bsablon = f"{baciklama} \n\n𝙇𝙄𝙉𝙆🔗 {blink} \n\n     𝙇𝙄𝙉𝙆🔗 {balink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 #linkk_gecmee"
                elif bsablon.find('{alink}') != -1:
                    bsablon = bsablon.replace("{aciklama}", "{}").replace("{alink}","{}").replace("{link}", "{}").format(baciklama, blink, balink)
                    
                else:
                    bsablon = bsablon.replace("{aciklama}", "{}").replace("{link}", "{}")
                    bsablon = str(bsablon).format(baciklama, blink)
                sleep(1.6)
                for bkan in bkanal:
                    try:
                        if update.channel_post.photo and bret:
                            bpost = bot.send_photo(bkan, bmedya, caption=bsablon)
                        if update.channel_post.video and bret:
                            bpost = bot.send_video(bkan, bmedya, caption=bsablon)
                        if update.channel_post.animation and bret:
                            bpost = bot.send_animation(bkan, bmedya, caption=bsablon)
                    except BadRequest as bd:
                        if bd.args == "Chat is not found":
                            raise Unauthorized
                        else:
                            logger.error(bd)
                    except Unauthorized:
                        logger.debug(f"Hatalı kanal: {bkanal}")
                        collection.update_one({"_id": buser}, {"$pull": {"kanal": bkan}})
                        try:
                            bot.send_message(buser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                        except:
                            pass   
                        logger.debug(f"{bkanal} kayıtlardan silindi.")
                    except Exception as e:
                        logger.error(e)
                    else:
                        bpostdata.insert_one({"mesih": bmesjid, "pid": bpost.message_id, "chat": bkan})
                        bcount = bcount + 1
                    
                logger.info("Başarılı!")
        bbasari = "{} kaynağından, {} Kanalda Post Paylaşıldı.".format(bkynk.title, bcount)
        logger.warning(bbasari)
        bot.send_message(botlog, bbasari)
    # Link Evi
    elif chat == kaynaklar[2] and evi:
        ccount = 0
        cmesaj = update.channel_post.caption
        if cmesaj == None:
            return
        """ Link tespit """
        csolx = cmesaj.rfind("http")
        csol = cmesaj.find("http")
        if csol == -1:
            return
        if csol != csolx:
            return
        csag = cmesaj.find("\n", csol)
        cmesajb = cmesaj[csol:csag].strip()
        if cmesaj.find("\n", csol) == -1:
            cmesajb = cmesaj[csol:].strip()
        if cmesajb.startswith("https://t.me/"):
            return
        ckynk = bot.get_chat(chat)
        logger.warning("{} postu atılıyor... ".format(ckynk.title))
        """ Açıklama tespit """
        cason = cmesaj.find("\n", 0, csol)
        caciklama = cmesaj[:cason].strip()
        """    Cookies    """
        s = Session()
        link = s.get("https://ay.live/api")
        cookies = dict(link.cookies)
        """  Veri Tabanı  """
        cpostdata = db[str(chat)]
        cbinb = collection.find({})
        cmesjid = update.channel_post.message_id
        """ Dosya tespit """
        if update.channel_post.photo:
            cmedya = update.channel_post.photo[0].file_id
        if update.channel_post.animation:
            cmedya = update.channel_post.animation.file_id
        if update.channel_post.video:
            cmedya = update.channel_post.video.file_id
        for chesap in cbinb:
            cret = True
            ckaynak = chesap['kaynak']
            csablon = chesap['sablon']
            csablon = str(csablon)
            try:
                ctoken = chesap['token']
            except:
                cret = False
            ckanal = chesap['kanal']
            cuser = chesap['_id']
            csite = chesap['site']
            caltapi = chesap['altapi']
            caltsite = chesap['altsite']
            csira = chesap['sira']
            if "3" in ckaynak and len(ckanal) > 0 and cret:
                clink = " "
                calink = " "
                cjson = " "
                if csira == "2":
                    ctoken = caltapi
                    csite = caltsite
                    collection.update_one({"_id": cuser}, {"$set": {"sira": "3"}})
                if csira == "3":
                    collection.update_one({"_id": cuser}, {"$set": {"sira": "2"}})
                try:
                    if not caltapi == "None":
                        if caltsite == "1":
                            cjson = s.get(f"https://ay.live/api/?", params={'api': caltapi, 'url': cmesajb, 'ct': 1}, cookies=cookies).json()
                            calink = cjson['shortenedUrl']
                        if caltsite == "2":
                            cjson = s.get(f"https://www.pnd.tl/api?", params={'api': caltapi, 'url': cmesajb, 'category': 6}).json()
                            calink =     cjson['shortenedUrl']
                        if caltsite == "3":
                            cjson = s.get(f"https://exe.io/api?", params={'api': caltapi, 'url': cmesajb}).json()
                            calink = cjson['shortenedUrl']
                        if caltsite == "4":
                            calink = s.get(f"http://ouo.io/api/{caltapi}?", params={'s': cmesajb}).text
                        if caltsite == "5":
                            calink = s.get(f"http://pubiza.com/api.php?", params={'token': caltapi, 'url': cmesajb, 'ads_type': "adult"}).text
                    sleep(1.6)
                    if csite == "1":
                        cjson = s.get(f"https://ay.live/api/?", params={'api': ctoken, 'url': cmesajb, 'ct': 1},
                                      cookies=cookies).json()
                        clink = cjson['shortenedUrl']
                    if csite == "2":
                        cjson = s.get(f"https://www.pnd.tl/api?", params={'api': ctoken, 'url': cmesajb, 'category': 6}).json()
                        clink = cjson['shortenedUrl']
                    if csite == "3":
                        cjson = s.get(f"https://exe.io/api?", params={'api': ctoken, 'url': cmesajb}).json()
                        clink = cjson['shortenedUrl']
                    if csite == "4":
                        clink = s.get(f"http://ouo.io/api/{ctoken}?", params={'s': cmesajb}).text
                    if csite == "5":
                        clink = s.get(f"http://pubiza.com/api.php?", params={'token': ctoken, 'url': cmesajb, 'ads_type': "adult"}).text
                    logger.info(f"{ckanal} + {clink} + {ctoken}")
                except Exception as e:
                    bot.send_message(cuser, "Son postunuz gönderilemedi;\n\n<code>API adresiniz sıkıntılı veya sitenize ulaşılamıyor. API adresinizi kontrol edin, bir sıkıntı yoksa bu mesajı görmezden gelin muhtemelen seçtiğiniz site ile ilgili bir sorun vardır.</code>")
                    logger.error(e)
                    logger.debug(cjson)
                    cret = False
                    
                if csablon == "1":
                    csablon = f"🔥{caciklama}\n\n🔱 TIKLA 👉 {clink}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
                elif csablon == "2" or csablon == "3":
                    csablon = f"{caciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {clink}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 #linkgec06"
                elif csablon == "9":
                    csablon = f"{caciklama} \n\n𝙇𝙄𝙉𝙆🔗 {clink} \n\n     𝙇𝙄𝙉𝙆🔗 {calink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 #linkk_gecmee"
                elif csablon.find('{alink}') != -1:
                    csablon = csablon.replace("{link}", "{}").replace("{aciklama}", "{}").replace("{alink}","{}").format(caciklama, clink, calink)
                    
                else:
                    csablon = csablon.replace("{link}", "{}").replace("aciklama", "").format(caciklama, clink)
                sleep(1.6)
                for ckan in ckanal:
                    try:
                        if update.channel_post.photo and cret:
                            cpost = bot.send_photo(ckan, cmedya, caption=csablon)
                        if update.channel_post.video and cret:
                            cpost = bot.send_video(ckan, cmedya, caption=csablon)
                    except BadRequest as bd:
                        if bd.args == "Chat is not found":
                            raise Unauthorized
                        else:
                            logger.error(bd)
                    except Unauthorized:
                        logger.debug(f"Hatalı kanal: {ckanal}")
                        collection.update_one({"_id": cuser}, {"$pull": {"kanal": ckan}})
                        try:
                            bot.send_message(cuser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                        except: 
                            pass   
                        logger.debug(f"{ckanal} kayıtlardan silindi.")
                    except Exception as e:
                        logger.error(e)
                    else:
                        cpostdata.insert_one({"chat": ckan, "pid": cpost.message_id, "mesih": cmesjid})
                        ccount = ccount + 1

                logger.info("Başarılı!")
        cbasari = "{} kaynağından, {} Kanalda Post Paylaşıldı.".format(ckynk.title, ccount)
        logger.warning(cbasari)
        bot.send_message(botlog, cbasari)
    # BAŞHUB
    elif chat == kaynaklar[3] and bashub:
        dcount = 0
        dmesaj = update.channel_post.caption
        if dmesaj == None:
            return
        """ Link tespit """
        dsolx = dmesaj.rfind("http")
        dsol = dmesaj.find("http")
        if dsol == -1:
            return
        if dsol != dsolx:
            return
        dsag = dmesaj.find("\n", dsol)
        dmesajb = dmesaj[dsol:dsag].strip()
        if dmesaj.find("\n", dsol) == -1:
            dmesajb = dmesaj[dsol:].strip()
        if dmesajb.startswith("https://t.me/"):
            return
        dkynk = bot.get_chat(chat)
        logger.warning("{} postu atılıyor... ".format(dkynk.title))
        """ Açıklama tespit """
        dason = dmesaj.find("\n", 0, dsol)
        daciklama = dmesaj[:dason].strip()
        """    Cookies    """
        s = Session()
        link = s.get("https://ay.live/api")
        cookies = dict(link.cookies)
        """  Veri Tabanı  """
        dpostdata = db[str(chat)]
        dbinb = collection.find({})
        dmesjid = update.channel_post.message_id
        """ Dosya tespit """
        if update.channel_post.photo:
            dmedya = update.channel_post.photo[0].file_id
        if update.channel_post.animation:
            dmedya = update.channel_post.animation.file_id
        if update.channel_post.video:
            dmedya = update.channel_post.video.file_id
        for dhesap in dbinb:
            dret = True
            dkaynak = dhesap['kaynak']
            dsablon = dhesap['sablon']
            dsablon = str(dsablon)
            try:
                dtoken = dhesap['token']
            except:
                dret = False
            dkanal = dhesap['kanal']
            duser = dhesap['_id']
            dsite = dhesap['site']
            daltapi = dhesap['altapi']
            daltsite = dhesap['altsite']
            dsira = dhesap['sira']
            if "4" in dkaynak and len(dkanal) > 0 and dret:
                dalink = " "
                dlink = " "
                djson = " "
                if dsira == "2":
                    dtoken = daltapi
                    dsite = daltsite
                    collection.update_one({"_id": duser}, {"$set": {"sira": "3"}})
                if dsira == "3":
                    collection.update_one({"_id": duser}, {"$set": {"sira": "2"}})
                try:
                    if not daltapi == "None":
                        if daltsite == "1":
                            djson = s.get(f"https://ay.live/api/?", params={'api': daltapi, 'url': dmesajb, 'ct': 1}, cookies=cookies).json()
                            dalink = djson['shortenedUrl']
                        if daltsite == "2":
                            djson = s.get(f"https://www.pnd.tl/api?", params={'api': daltapi, 'url': dmesajb, 'category': 6}).json()
                            dalink = djson['shortenedUrl']
                        if daltsite == "3":
                            djson = s.get(f"https://exe.io/api?", params={'api': daltapi, 'url': dmesajb}).json()
                            dalink = djson['shortenedUrl']
                        if daltsite == "4":
                            dalink = s.get(f"http://ouo.io/api/{daltapi}?", params={'s': dmesajb}).text
                        if daltsite == "5":
                            dalink = s.get(f"http://pubiza.com/api.php?", params={'token': daltapi, 'url': dmesajb, 'ads_type': "adult"}).text
                    sleep(1.6)
                    if dsite == "1":
                        djson = s.get(f"https://ay.live/api/?", params={'api': dtoken, 'url': dmesajb, 'ct': 1}, cookies=cookies).json()
                        dlink = djson['shortenedUrl']
                    if dsite == "2":
                        djson = s.get(f"https://www.pnd.tl/api?", params={'api': dtoken, 'url': dmesajb, 'category': 6}).json()
                        dlink = djson['shortenedUrl']
                    if dsite == "3":
                        djson = s.get(f"https://exe.io/api?", params={'api': dtoken, 'url': dmesajb}).json()
                        dlink = djson['shortenedUrl']
                    if dsite == "4":
                        dlink = s.get(f"http://ouo.io/api/{dtoken}?", params={'s': dmesajb}).text
                    if dsite == "5":
                        dlink = s.get(f"http://pubiza.com/api.php?", params={'token': dtoken, 'url': dmesajb, 'ads_type': "adult"}).text
                    logger.info(f"{dkanal} + {dlink} + {dtoken}")
                except Exception as e:
                    bot.send_message(duser, "Son postunuz gönderilemedi;\n\n<code>API adresiniz sıkıntılı veya sitenize ulaşılamıyor. API adresinizi kontrol edin, bir sıkıntı yoksa bu mesajı görmezden gelin muhtemelen seçtiğiniz site ile ilgili bir sorun vardır.</code>")
                    logger.error(e)
                    logger.debug(djson)
                    dret = False
                    
                if dsablon == "1":
                    dsablon = f"🔥{daciklama}\n\n🔱 TIKLA 👉 {dlink}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
                elif dsablon == "2" or dsablon == "3":
                    dsablon = f"{daciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {dlink}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 #linkgec06"
                elif dsablon == "9":
                    dsablon = f"{daciklama} \n\n𝙇𝙄𝙉𝙆🔗 {dlink} \n\n     𝙇𝙄𝙉𝙆🔗 {dalink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 #linkk_gecmee"
                elif dsablon.find('{alink}') != -1:
                    dsablon = dsablon.replace("{link}", "{}").replace("{aciklama}", "{}").replace("{alink}", "{}").format(daciklama, dlink, dalink)
                else:
                    dsablon = dsablon.replace("{link}", "{}").replace("{aciklama}", "{}").format(daciklama, dlink)
                sleep(1.6)
                for dkan in dkanal:
                    try: 
                        if update.channel_post.photo and dret:
                            dpost = bot.send_photo(dkan, dmedya, caption=dsablon)
                        if update.channel_post.video and dret:
                            dpost = bot.send_video(dkan, dmedya, caption=dsablon)
                        if update.channel_post.animation and dret:
                            dpost = bot.send_animation(dkan, dmedya, caption=dsablon)
                    except BadRequest as bd:
                        if bd.args == "Chat is not found":
                            raise Unauthorized
                        else:
                            logger.error(bd)
                    except Unauthorized:
                        logger.debug(f"Hatalı kanal: {dkanal}")
                        collection.update_one({"_id": duser}, {"$pull": {"kanal": dkan}})
                        try:
                            bot.send_message(duser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                        except: 
                            pass   
                        logger.debug(f"{dkanal} kayıtlardan silindi.")
                    except Exception as e:
                        logger.error(e)
                    else:
                        dpostdata.insert_one({"chat": dkan, "pid": dpost.message_id, "mesih": dmesjid})
                        dcount = dcount + 1

                logger.info("Başarılı!")
        dbasari = "{} kaynağından, {} Kanalda Post Paylaşıldı.".format(dkynk.title, dcount)
        logger.warning(dbasari)
        bot.send_message(botlog, dbasari)
    # Açık mı link
    elif chat == kaynaklar[4] and acikmi:
        ecount = 0
        emesaj = update.channel_post.caption
        """ Link tespit """
        esolx = emesaj.rfind("http")
        esol = emesaj.find("http")
        if esol == -1:
            return
        if esol != esolx:
            return
        esag = emesaj.find("\n", esol)
        emesajb = emesaj[esol:esag].strip()
        if emesaj.find("\n", esol) == -1:
            emesajb = emesaj[esol:].strip()
        if emesajb.startswith("https://t.me/"):
            return
        ekynk = bot.get_chat(chat)
        logger.warning("{} postu atılıyor... ".format(ekynk.title))
        """ Açıklama tespit """
        eason = emesaj.find("\n", 0, esol)
        eaciklama = emesaj[:eason].strip()
        """    Cookies    """
        s = Session()
        link = s.get("https://ay.live/api")
        cookies = dict(link.cookies)
        """  Veri Tabanı  """
        epostdata = db[str(chat)]
        ebinb = collection.find({})
        emesjid = update.channel_post.message_id
        """ Dosya tespit """
        if update.channel_post.photo:
            emedya = update.channel_post.photo[0].file_id
        if update.channel_post.animation:
            emedya = update.channel_post.animation.file_id
        if update.channel_post.video:
            emedya = update.channel_post.video.file_id
        for ehesap in ebinb:
            eret = True
            ekaynak = ehesap['kaynak']
            esablon = ehesap['sablon']
            esablon = str(esablon)
            try:
                etoken = ehesap['token']
            except:
                eret = False
            ekanal = ehesap['kanal']
            euser = ehesap['_id']
            esite = ehesap['site']
            ealtapi = ehesap['altapi']
            ealtsite = ehesap['altsite']
            esira = ehesap['sira']
            if "5" in ekaynak and len(ekanal) > 0 and eret:
                elink = " "
                ealink = " "
                ejson = " "
                if esira == "2":
                    etoken = ealtapi
                    esite = ealtsite
                    collection.update_one({"_id": euser}, {"$set": {"sira": "3"}})
                if esira == "3":
                    collection.update_one({"_id": euser}, {"$set": {"sira": "2"}})
                try:
                    if not ealtapi == "None":
                        if ealtsite == "1":
                            ejson = s.get(f"https://ay.live/api/?", params={'api': ealtapi, 'url': emesajb, 'ct': 1}, cookies=cookies).json()
                            ealink = ejson['shortenedUrl']
                        if ealtsite == "2":
                            ejson = s.get(f"https://www.pnd.tl/api?", params={'api': ealtapi, 'url': emesajb, 'category': 6}).json()
                            ealink = ejson['shortenedUrl']
                        if ealtsite == "3":
                            ejson = s.get(f"https://exe.io/api?", params={'api': ealtapi, 'url': emesajb}).json()
                            ealink = ejson['shortenedUrl']
                        if ealtsite == "4":
                            ealink = s.get(f"http://ouo.io/api/{ealtapi}?", params={'s': emesajb}).text
                        if ealtsite == "5":
                            ealink = s.get(f"http://pubiza.com/api.php?", params={'token': ealtapi, 'url': emesajb, 'ads_type': "adult"}).text
                    if esite == "1":
                        ejson = s.get(f"https://ay.live/api/?", params={'api': etoken, 'url': emesajb, 'ct': 1}, cookies=cookies).json()
                        elink = ejson['shortenedUrl']
                    if esite == "2":
                        ejson = s.get(f"https://www.pnd.tl/api?", params={'api': etoken, 'url': emesajb, 'category': 6}).json()
                        elink = ejson['shortenedUrl']
                    if esite == "3":
                        ejson = s.get(f"https://exe.io/api?", params={'api': etoken, 'url': emesajb}).json()
                        elink = ejson['shortenedUrl']
                    if esite == "4":
                        elink = s.get(f"http://ouo.io/api/{etoken}?", params={'s': emesajb}).text
                    if esite == "5":
                        elink = s.get(f"http://pubiza.com/api.php?", params={'token': etoken, 'url': emesajb, 'ads_type': "adult"}).text
                    logger.info(f"{ekanal} + {elink} + {etoken}")
                except Exception as e:
                    bot.send_message(euser, "Son postunuz gönderilemedi;\n\n<code>API adresiniz sıkıntılı veya sitenize ulaşılamıyor. API adresinizi kontrol edin, bir sıkıntı yoksa bu mesajı görmezden gelin muhtemelen seçtiğiniz site ile ilgili bir sorun vardır.</code>")
                    logger.error(e)
                    logger.debug(ejson)
                    eret = False
                if esablon == "1":
                    esablon = f"🔥{eaciklama}\n\n🔱 TIKLA 👉 {elink}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
                elif esablon == "2" or esablon == "3":
                    esablon = f"{eaciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {elink}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 #linkgec06"
                elif esablon == "9":
                    esablon = f"{eaciklama} \n\n𝙇𝙄𝙉𝙆🔗 {elink} \n\n     𝙇𝙄𝙉𝙆🔗 {ealink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 #linkk_gecmee"
                elif esablon.find('{alink}') != -1:
                    esablon = esablon.replace("{link}", "{}").replace("{aciklama}", "{}").replace("{alink}", "{}").format(eaciklama, elink, ealink)
                else:
                    esablon = esablon.replace("{link}", "{}").replace("{aciklama}", "{}").format(eaciklama, elink)
                sleep(1.6)
                for ekan in ekanal:
                    try:
                        if update.channel_post.photo and eret:
                            epost = bot.send_photo(ekan, emedya, caption=esablon)
                        if update.channel_post.video and eret:
                            epost = bot.send_video(ekan, emedya, caption=esablon)
                        if update.channel_post.animation and eret:
                            epost = bot.send_animation(ekan, emedya, caption=esablon)
                    except BadRequest as bd:
                        if bd.args == "Chat is not found":
                            raise Unauthorized
                        else:
                            logger.error(bd)
                    except Unauthorized:
                        logger.debug(f"Hatalı kanal: {ekanal}")
                        collection.update_one({"_id": euser}, {"$pull": {"kanal": ekan}})
                        try:
                            bot.send_message(euser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                        except: 
                            pass   
                        logger.debug(f"{ekanal} kayıtlardan silindi.")
                    except Exception as e:
                        logger.error(e)
                    else:
                        epostdata.insert_one({"chat": ekan, "pid": epost.message_id, "mesih": emesjid})
                        ecount = ecount + 1

                logger.info("Başarılı!")
        ebasari = "{} kaynağından, {} Kanalda Post Paylaşıldı.".format(ekynk.title, ecount)
        logger.warning(ebasari)
        bot.send_message(botlog, ebasari)
    # MuhoVip
    elif chat == kaynaklar[5] and muho:
        gcount = 0
        gmesaj = update.channel_post.caption
        if gmesaj == None:
           return
        """ Link tespit """
        gsolx = gmesaj.rfind("http")
        gsol = gmesaj.find("http")
        if gsol == -1:
            return
        if gsol != gsolx:
            return
        gkynk = bot.get_chat(chat)
        gsag = gmesaj.find("\n", gsol)
        gmesajb = gmesaj[gsol:gsag].strip()
        if gmesaj.find("\n", gsol) == -1:
            gmesajb = gmesaj[gsol:].strip()
        if gmesajb.startswith("https://t.me/"):
            return
        logger.warning("{} postu atılıyor... ".format(gkynk.title))
        """ Açıklama tespit """
        gason = gmesaj.find("\n", 0, gsol)
        gaciklama = gmesaj[:gason].strip()
        """    Cookies    """
        s = Session()
        link = s.get("https://ay.live/api")
        cookies = dict(link.cookies)
        """  Veri Tabanı  """
        gpostdata = db[str(chat)]
        gbinb = collection.find({})
        gmesjid = update.channel_post.message_id
        """ Dosya tespit """
        if update.channel_post.photo:
            gmedya = update.channel_post.photo[0].file_id
        if update.channel_post.animation:
            gmedya = update.channel_post.animation.file_id
        if update.channel_post.video:
            gmedya = update.channel_post.video.file_id
        for ghesap in gbinb:
            gret = True
            gkaynak = ghesap['kaynak']
            gsablon = ghesap['sablon']
            gsablon = str(gsablon)
            try:
                gtoken = ghesap['token']
            except:
                gret = False
            gkanal = ghesap['kanal']
            guser = ghesap['_id']
            gsite = ghesap['site']
            galtapi = ghesap['altapi']
            galtsite = ghesap['altsite']
            gsira = ghesap['sira']
            if "6" in gkaynak and len(gkanal) > 0 and gret:
                glink = " "
                galink = " "
                gjson = " "
                if gsira == "2":
                    gtoken = galtapi
                    gsite = galtsite
                    collection.update_one({"_id": guser}, {"$set": {"sira": "3"}})
                if gsira == "3":
                    collection.update_one({"_id": guser}, {"$set": {"sira": "2"}})
                try:
                    if not galtapi == "None":
                        if galtsite == "1":
                            gjson = s.get(f"https://ay.live/api/?", params={'api': galtapi, 'url': gmesajb, 'ct': 1}, cookies=cookies).json()
                            galink = gjson['shortenedUrl']
                        if galtsite == "2":
                            gjson = s.get(f"https://www.pnd.tl/api?", params={'api': galtapi, 'url': gmesajb, 'category': 6}).json()
                            galink = gjson['shortenedUrl']
                        if galtsite == "3":
                            gjson = s.get(f"https://exe.io/api?", params={'api': galtapi, 'url': gmesajb}).json()
                            galink = gjson['shortenedUrl']
                        if galtsite == "4":
                            galink = s.get(f"http://ouo.io/api/{galtapi}?", params={'s': gmesajb}).text
                        if galtsite == "5":
                            galink = s.get(f"http://pubiza.com/api.php?", params={'token': galtapi, 'url': gmesajb, 'ads_type': "adult"}).text
                    if gsite == "1":
                        gjson = s.get(f"https://ay.live/api/?", params={'api': gtoken, 'url': gmesajb, 'ct': 1},
                                      cookies=cookies).json()
                        glink = gjson['shortenedUrl']
                    if gsite == "2":
                        gjson = s.get(f"https://www.pnd.tl/api?", params={'api': gtoken, 'url': gmesajb, 'category': 6}).json()
                        glink = gjson['shortenedUrl']
                    if gsite == "3":
                        gjson = s.get(f"https://exe.io/api?", params={'api': gtoken, 'url': gmesajb}).json()
                        glink = gjson['shortenedUrl']
                    if gsite == "4":
                      glink = s.get(f"http://ouo.io/api/{gtoken}?", params={'s': gmesajb}).text
                    if gsite == "5":
                        glink = s.get(f"http://pubiza.com/api.php?", params={'token': gtoken, 'url': gmesajb, 'ads_type': "adult"}).text
                    logger.info(f"{gkanal} + {glink} + {gtoken}")
                except Exception as e:
                    bot.send_message(guser, "Son postunuz gönderilemedi;\n\n<code>API adresiniz sıkıntılı veya sitenize ulaşılamıyor. API adresinizi kontrol edin, bir sıkıntı yoksa bu mesajı görmezden gelin muhtemelen seçtiğiniz site ile ilgili bir sorun vardır.</code>")
                    logger.error(e)
                    logger.debug(gjson)
                    gret = False
                if gsablon == "1":
                    gsablon = f"🔥{gaciklama}\n\n🔱 TIKLA 👉 {glink}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
                elif gsablon == "2" or gsablon == "3":
                    gsablon = f"{gaciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {glink}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 #linkgec06"
                elif gsablon == "9":
                    gsablon = f"{gaciklama} \n\n𝙇𝙄𝙉𝙆🔗 {glink} \n\n     𝙇𝙄𝙉𝙆🔗 {galink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 #linkk_gecmee"
                elif gsablon.find('{alink}') != -1:
                    gsablon = gsablon.replace("{link}", "{}").replace("{aciklama}", "{}").replace("{alink}", "{}").format(gaciklama, glink, galink)
                else:
                    gsablon = gsablon.replace("{link}", "{}").replace("aciklama", "").format(gaciklama, glink)
                sleep(1.6)
                for gkan in gkanal:
                    try:
                        if update.channel_post.photo and gret:
                            gpost = bot.send_photo(gkan, gmedya, caption=gsablon)
                        if update.channel_post.video and gret:
                            gpost = bot.send_video(gkan, gmedya, caption=gsablon)
                        if update.channel_post.animation and gret:
                            gpost = bot.send_animation(gkan, gmedya, caption=gsablon)
                    except BadRequest as bd:
                        if bd.args == "Chat is not found":
                            raise Unauthorized
                        else:
                            logger.error(bd)
                    except Unauthorized:
                        logger.debug(f"Hatalı kanal: {gkanal}")
                        collection.update_one({"_id": guser}, {"$pull": {"kanal": gkan}})
                        try:
                            bot.send_message(guser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                        except: 
                            pass   
                        logger.debug(f"{gkanal} kayıtlardan silindi.")
                    except Exception as e:
                        logger.error(e)
                    else:
                        gpostdata.insert_one({"chat": gkan, "pid": gpost.message_id, "mesih": gmesjid})
                        gcount = gcount + 1

                logger.info("Başarılı!")
        gbasari = "{} kaynağından, {} Kanalda Post Paylaşıldı.".format(gkynk.title, gcount)
        logger.warning(gbasari)
        bot.send_message(botlog, gbasari)
    # Tutan Linkler
    elif chat == kaynaklar[6] and tutan:
        fcount = 0
        fmesaj = update.channel_post.caption
        if fmesaj == None:
            return
        """ Link tespit """
        fsolx = fmesaj.rfind("http")
        fsol = fmesaj.find("http")
        if fsol == -1:
            return
        if fsol != fsolx:
            return
        fsag = fmesaj.find("\n", fsol)
        fmesajb = fmesaj[fsol:fsag].strip()
        if fmesaj.find("\n", fsol) == -1:
            fmesajb = fmesaj[fsol:].strip()
        if fmesajb.startswith("https://t.me/"):
            return
        fkynk = bot.get_chat(chat)
        logger.warning("{} postu atılıyor... ".format(fkynk.title))
        """ Açıklama tespit """
        fason = fmesaj.find("\n", 0, fsol)
        faciklama = fmesaj[:fason].strip()
        """    Cookies    """
        s = Session()
        link = s.get("https://ay.live/api")
        cookies = dict(link.cookies)
        """  Veri Tabanı  """
        fpostdata = db[str(chat)]
        fbinb = collection.find({})
        fmesjid = update.channel_post.message_id
        """ Dosya tespit """
        if update.channel_post.photo:
            fmedya = update.channel_post.photo[0].file_id
        if update.channel_post.animation:
            fmedya = update.channel_post.animation.file_id
        if update.channel_post.video:
            fmedya = update.channel_post.video.file_id
        for fhesap in fbinb:
            fret = True
            fkaynak = fhesap['kaynak']
            fsablon = fhesap['sablon']
            fsablon = str(fsablon)
            try:
                ftoken = fhesap['token']
            except:
                fret = False
            fkanal = fhesap['kanal']
            fuser = fhesap['_id']
            fsite = fhesap['site']
            faltapi = fhesap['altapi']
            faltsite = fhesap['altsite']
            fsira = fhesap['sira']
            if "7" in fkaynak and len(fkanal) > 0 and fret:
                falink = " "
                flink = " "
                fjson = " "
                if fsira == "2":
                    ftoken = faltapi
                    fsite = faltsite
                    collection.update_one({"_id": fuser}, {"$set": {"sira": "3"}})
                if fsira == "3":
                    collection.update_one({"_id": fuser}, {"$set": {"sira": "2"}})
                try:
                    if not faltapi == "None":
                        if faltsite == "1":
                            fjson = s.get(f"https://ay.live/api/?", params={'api': faltapi, 'url': fmesajb, 'ct': 1}, cookies=cookies).json()
                            falink = fjson['shortenedUrl']
                        if faltsite == "2":
                            fjson = s.get(f"https://www.pnd.tl/api?", params={'api': faltapi, 'url': fmesajb, 'category': 6}).json()
                            falink = fjson['shortenedUrl']
                        if faltsite == "3":
                            fjson = s.get(f"https://exe.io/api?", params={'api': faltapi, 'url': fmesajb}).json()
                            falink = fjson['shortenedUrl']
                        if faltsite == "4":
                            falink = s.get(f"http://ouo.io/api/{faltapi}?", params={'s': fmesajb}).text
                        if faltsite == "5":
                            falink = s.get(f"http://pubiza.com/api.php?", params={'token': faltapi, 'url': fmesajb, 'ads_type': "adult"}).text
                    sleep(1.6)
                    if fsite == "1":
                        fjson = s.get(f"https://ay.live/api/?", params={'api': ftoken, 'url': fmesajb, 'ct': 1}, cookies=cookies).json()
                        flink = fjson['shortenedUrl']
                    if fsite == "2":
                        fjson = s.get(f"https://www.pnd.tl/api?", params={'api': ftoken, 'url': fmesajb, 'category': 6}).json()
                        flink = fjson['shortenedUrl']
                    if fsite == "3":
                        fjson = s.get(f"https://exe.io/api?", params={'api': ftoken, 'url': fmesajb}).json()
                        flink = fjson['shortenedUrl']
                    if fsite == "4":
                        flink = s.get(f"http://ouo.io/api/{ftoken}?", params={'s': fmesajb}).text
                    if fsite == "5":
                        flink = s.get(f"http://pubiza.com/api.php?", params={'token': faltapi, 'url': fmesajb, 'ads_type': "adult"}).text
                    logger.info(f"{fkanal} + {flink} + {ftoken}")
                except Exception as e:
                    bot.send_message(fuser, "Son postunuz gönderilemedi;\n\n<code>API adresiniz sıkıntılı veya sitenize ulaşılamıyor. API adresinizi kontrol edin, bir sıkıntı yoksa bu mesajı görmezden gelin muhtemelen seçtiğiniz site ile ilgili bir sorun vardır.</code>")
                    logger.error(e)
                    logger.debug(fjson)
                    fret = False
                if fsablon == "1":
                    fsablon = f"🔥{faciklama}\n\n🔱 TIKLA 👉 {flink}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
                elif fsablon == "2" or fsablon == "3":
                    fsablon = f"{faciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {flink}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 #linkgec06"
                elif fsablon == "9":
                    fsablon = f"{faciklama} \n\n𝙇𝙄𝙉𝙆🔗 {flink} \n\n     𝙇𝙄𝙉𝙆🔗 {falink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 #linkk_gecmee"
                elif fsablon.find('{alink}') != -1:
                    fsablon = fsablon.replace("{aciklama}", "{}").replace("{alink}", "{}").replace("{link}", "{}").format(faciklama, flink, falink)
                else:
                    fsablon = fsablon.replace("{aciklama}", "{}").replace("{link}", "{}")
                    fsablon = str(fsablon).format(faciklama, flink)
                sleep(1.6)
                for fkan in fkanal:
                    try:
                        if update.channel_post.photo and fret:
                            fpost = bot.send_photo(fkan, fmedya, caption=fsablon)
                        if update.channel_post.video and fret:
                            fpost = bot.send_video(fkan, fmedya, caption=fsablon)
                        if update.channel_post.animation and fret:
                            fpost = bot.send_animation(fkan, fmedya, caption=fsablon)
                    except BadRequest as bd:
                        if bd.args == "Chat is not found":
                            raise Unauthorized
                        else:
                            logger.error(bd)
                    except Unauthorized:
                        logger.debug(f"Hatalı kanal: {fkanal}")
                        collection.update_one({"_id": fuser}, {"$pull": {"kanal": fkan}})
                        try:
                            bot.send_message(fuser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                        except: 
                            pass   
                        logger.debug(f"{fkanal} kayıtlardan silindi.")
                    except Exception as e:
                        logger.error(e)
                    else:
                        fpostdata.insert_one({"chat": fkan, "pid": fpost.message_id, "mesih": fmesjid})
                        fcount = fcount + 1
                    
                logger.info("Başarılı!")
        fbasari = "{} kaynağından, {} Kanalda Post Paylaşıldı.".format(fkynk.title, fcount)
        bot.send_message(botlog, fbasari)
        logger.warning(fbasari)
    # Özel Kaynaklar
    else:
        okaynak = OzelCol.find_one({"okaynak": chat})
    if okaynak != None:
        ocount = 0
        omesaj = update.channel_post.caption
        if omesaj == None:
            return
        """  Link tespit  """
        osolx = omesaj.rfind("http")
        osol = omesaj.find("http")
        if osol == -1:
            return
        if osol != osolx:
            return
        osag = omesaj.find("\n", osol)
        okynk = bot.get_chat(chat)
        omesajb = omesaj[osol:osag].strip()
        if omesaj.find("\n", osol) == -1:
            omesajb = omesaj[osol:].strip()
        if omesajb.startswith("https://t.me/"):
            return
        logger.warning("[ÖZEL] {} postu atılıyor... ".format(okynk.title))
        """  Açıklama tespit  """
        oason = omesaj.rfind("\n", 0, osol)
        oaciklama = omesaj[:oason].strip()
        """  Cookies  """
        s = Session()
        link = s.get("https://ay.live/api")
        cookies = dict(link.cookies)
        """ Dosya tespit """
        if update.channel_post.photo:
            omedya = update.channel_post.photo[0].file_id
        if update.channel_post.animation:
            omedya = update.channel_post.animation.file_id
        if update.channel_post.video:
            omedya = update.channel_post.video.file_id
        oret = True
        for ozelkanal in okaynak['kanal']:
            ohesap = collection.find_one({"_id": ozelkanal})
            try:    
                otoken = ohesap['token']
            except:
                oret = False
            okanal = ohesap['kanal']
            osablon = ohesap['sablon']
            ouser = ohesap['_id']
            osite = ohesap["site"]
            oaltapi = ohesap['altapi']
            oaltsite = ohesap['altsite']
            osira = ohesap['sira']
            if len(okanal) > 0 and oret:
                oalink = " "
                olink = " "
                if osira == "2":
                    otoken = oaltapi
                    osite = oaltsite
                    collection.update_one({"_id": ouser}, {"$set": {"sira": "3"}})
                if osira == "3":
                    collection.update_one({"_id": ouser}, {"$set": {"sira": "2"}})
                try:
                    if not oaltapi == "None":
                        if oaltsite == "1":
                            ojson = s.get(f"https://ay.live/api/?", params={'api': oaltapi, 'url': omesajb, 'ct': 1}, cookies=cookies).json()
                            oalink = ojson['shortenedUrl']
                        if oaltsite == "2":
                            ojson = s.get(f"https://www.pnd.tl/api?", params={'api': oaltapi, 'url': omesajb, 'category': 6}).json()
                            oalink = ojson['shortenedUrl']
                        if oaltsite == "3":
                            ojson = s.get(f"https://exe.io/api?", params={'api': oaltapi, 'url': omesajb}).json()
                            oalink = ojson['shortenedUrl']
                        if oaltsite == "4":
                            oalink = s.get(f"http://ouo.io/api/{oaltapi}?", params={'s': omesajb}).text
                        if oaltsite == "5":
                            oalink = s.get(f"http://pubiza.com/api.php?", params={'token': oaltapi, 'url': omesajb, 'ads_type': "adult"}).text
                    if osite == "1":
                        ojson = s.get(f"https://ay.live/api/?", params={'api': otoken, 'url': omesajb, 'ct': 1}, cookies=cookies).json()
                        olink = ojson['shortenedUrl']
                    if osite == "2":
                        ojson = s.get(f"https://www.pnd.tl/api?", params={'api': otoken, 'url': omesajb, 'category': 6}).json()
                        olink = ojson['shortenedUrl']
                    if osite == "3":
                        ojson = s.get(f"https://exe.io/api?", params={'api': otoken, 'url': omesajb}).json()
                        olink = ojson['shortenedUrl']
                    if osite == "4":
                        olink = s.get(f"http://ouo.io/api/{otoken}?", params={'s': omesajb}).text
                    if osite == "5":
                        olink = s.get(f"http://pubiza.com/api.php?", params={'token': etoken, 'url': omesajb, 'ads_type': "adult"}).text
                    logger.info(f"{okanal} + {olink} + {otoken}")
                except:
                    bot.send_message(ouser, "Son postunuz gönderilemedi;\n\n<code>API adresiniz sıkıntılı veya sitenize ulaşılamıyor. API adresinizi kontrol edin, bir sıkıntı yoksa bu mesajı görmezden gelin muhtemelen seçtiğiniz site ile ilgili bir sorun vardır.</code>")
                    logger.error(e)
                    oret = False
                    
                if osablon == "1":
                    osablon = f"🔥{oaciklama}\n\n🔱 TIKLA 👉 {olink}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
                elif osablon == "2" or osablon == "3":
                    osablon = f"{oaciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {olink}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 #linkgec06"
                elif osablon == "9":
                    osablon = f"{oaciklama} \n\n𝙇𝙄𝙉𝙆🔗 {olink} \n\n     𝙇𝙄𝙉𝙆🔗 {oalink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 #linkk_gecmee"
                elif osablon.find('{alink}') != -1:
                    osablon = osablon.replace("{aciklama}", "{}").replace("{alink}", "{}").replace("{link}", "{}").format(oaciklama, olink, oalink)
                else:
                    osablon = osablon.replace("{aciklama}", "{}").replace("{link}", "{}").format(oaciklama, olink)
                sleep(2.3)
                for okan in okanal:
                    try:
                        if update.channel_post.photo and oret:
                            opost = bot.send_photo(okan, omedya, caption=osablon)
                        if update.channel_post.video and oret:
                            opost = bot.send_video(okan, omedya, caption=osablon)
                        if update.channel_post.animation and oret:
                            opost = bot.send_animation(okan, omedya, caption=osablon)
                    except BadRequest as bd:
                        if bd.args == "Chat is not found":
                            raise Unauthorized
                        else:
                            logger.error(bd)
                    except Unauthorized:
                        logger.debug(f"Hatalı kanal: {okan}")
                        collection.update_one({"_id": ouser}, {"$pull": {"kanal": okan}})
                        try:
                            bot.send_message(ouser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                        except Exception as e: 
                            logger.error(e)
                        else:
                            logger.debug(f"{okan} kayıtlardan silindi.")
                    except Exception as e:
                        logger.error(e)
                    else:
                        ocount += 1                     
                logger.info("Başarılı!")
        obasari = "[ÖZEL] {} kaynağından {} kanalda post paylaşıldı.".format(okynk.title, ocount)
        if okaynak["log"] != "yok":
            bot.send_message(okaynak["log"], obasari)
        logger.warning(obasari)

dispatcher.add_handler(MessageHandler(Filters.photo & Filters.update.channel_post | Filters.video & Filters.update.channel_post | Filters.animation & Filters.update.channel_post, poster))

