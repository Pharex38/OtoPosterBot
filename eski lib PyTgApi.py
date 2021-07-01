def poster(update, context):
    okaynak = None
    chat = update.channel_post.chat.id
    vipler = collection.find_one({"_id": 0})['vipuye']
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
    "Accept-Encoding": "*",
    "Connection": "keep-alive"}
    # Link Mahzeni
    if chat == kaynaklar[0]:
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
        """  Veri Tabanı  """
        postdata = db[str(chat)]
        binb = collection.find({})
        mesjid = update.channel_post.message_id
        """ Dosya tespit """
        medya = update.channel_post.photo[0].file_id if update.channel_post.photo else update.channel_post.effective_attachment.file_id
        for hesap in binb:
            ret = True
            kaynak = hesap['kaynak']
            kanal = hesap['kanal']
            try:
                token = hesap['token']
            except:
                continue
            if "1" in kaynak and len(kanal) > 0 and ret:
                sablon = hesap['sablon']
                user = hesap['_id']
                site = hesap["site"]
                altapi = hesap['altapi']
                altsite = hesap['altsite']
                sira = hesap['sira']
                pcount = hesap['pcount']
                if pcount < 20:
                    collection.update_one({"_id": user}, {"$inc": {"pcount": 1}})
                else:
                    if para and user not in vipler:
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
                            linktry += 1
                            sleep(1)
                            if linktry > 1:
                                logger.warning(f"Tekrar deneniyor {linktry}")
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
                        linktry += 1
                        sleep(1)
                        if linktry > 1:
                            logger.warning(f"Tekrar deneniyor {linktry}")
                    logger.info(f"{kanal} + {link} + {token}")
                except Exception as e:
                    bot.send_message(user, "Son postunuz gönderilemedi;\n\n<code>API adresiniz sıkıntılı veya sitenize ulaşılamıyor. API adresinizi kontrol edin, bir sıkıntı yoksa bu mesajı görmezden gelin muhtemelen seçtiğiniz site ile ilgili bir sorun vardır.</code>")
                    logger.error(e)
                    logger.debug(json)
                    continue
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
                    bot.send_message(-1001190898326, str(hesap))
                    continue
                for kan in kanal:
                    post = update.channel_post
                    try:
                        yetkililer = [xy.user.id for xy in bot.get_chat_administrators(kan)]
                    except:
                        ret = False
                        yetkililer = []
                    if not user in yetkililer and ret:
                        try:
                            membersayi = bot.get_chat_members_count(kan)
                        except:
                            membersayi = "Bot kanaldan çıkarılmış."
                        try:
                            logger.debug(f"Hatalı kanal: {kanal}")
                            bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {user}\nÜYE: {membersayi}\nKANAL: {kan}")
                            collection.update_one({"_id": user}, {"$pull": {"kanal": kan}})
                            continue
                        except:
                            pass
                        else:
                            logger.debug(f"{kanal} kayıtlardan silindi.")
                    try:
                        if update.channel_post.photo and ret:
                            post = bot.send_photo(kan, medya, caption=sablon)
                        if update.channel_post.video and ret:
                            post = bot.send_video(kan, medya, caption=sablon)
                        if update.channel_post.animation and ret:
                            post = bot.send_animation(kan, medya, caption=sablon)
                    except Exception as e:
                        if str(e).find("Chat is not found") != -1 or str(e).find("Need administrator") != -1 or str(e).find("bot is not") != -1:
                            try:
                                logger.debug(f"Hatalı kanal: {kanal}")
                                bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {user}\nÜYE: {bot.get_chat_members_count(kan)}\nKANAL: {kan}")
                                collection.update_one({"_id": user}, {"$pull": {"kanal": kan}})
                                bot.send_message(user, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                            except:
                                pass   
                            else:
                                logger.debug(f"{kanal} kayıtlardan silindi.")
                        else:
                            logger.error(e)
                    else:
                        count = count + 1
                        postdata.insert_one({"pid": post.message_id, "chat": kan, "mesih": mesjid})
                logger.info("Başarılı!")
            else:
                pass
        basari = "{} kaynağından, {} Kanalda Post Paylaşıldı.".format(kynk.title, count)
        logger.warning(basari)
        try:
            bmsg = bot.send_message(botlog, basari)
        except Exception as e:
            logger.error(e)
        else:
            postdata.insert_one({"chat": botlog, "pid": bmsg.message_id, "mesih": mesjid})

    # Bedava Link
    elif chat == kaynaklar[1]:
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
        """  Veri Tabanı  """
        bpostdata = db[str(chat)]
        bbinb = collection.find({})
        bmesjid = update.channel_post.message_id
        """ Dosya tespit """
        bmedya = update.channel_post.photo[0].file_id if update.channel_post.photo else update.channel_post.effective_attachment.file_id
        for bhesap in bbinb:
            bkanal = bhesap['kanal']
            bret = True
            bkaynak = bhesap['kaynak']
            try:
                btoken = bhesap['token']
            except:
                continue
            if "2" in bkaynak and len(bkanal) > 0 and bret:
                bsablon = bhesap['sablon']
                bsablon = str(bsablon)
                buser = bhesap['_id']
                bsite = bhesap['site']
                baltapi = bhesap['altapi']
                baltsite = bhesap['altsite']
                bsira = bhesap['sira']
                bpcount = bhesap['pcount']
                if bpcount < 20:
                    collection.update_one({"_id": buser}, {"$inc": {"pcount": 1}})
                else:
                    if para and buser not in vipler:
                        btoken = phaapi(bsite)
                        baltapi = phaapi(baltsite) if baltsite != "None" else "None"
                    collection.update_one({"_id": buser}, {"$set": {"pcount": 0}})
                balink = " "
                blink = " "
                bjson = " "
                blinktry = 0
                if bsira == "2":
                    btoken = baltapi
                    bsite = baltsite
                    collection.update_one({"_id": buser}, {"$set": {"sira": "3"}})
                if bsira == "3":
                    collection.update_one({"_id": buser}, {"$set": {"sira": "2"}})
                try:
                    if not baltapi == "None":
                        while blinktry < 10 and balink == " ":
                            if baltsite == "1":
                                bjson = get(f"https://ay.live/api/?", params={'api': baltapi, 'url': bmesajb, 'ct': 1}, headers=headers).json()
                                balink = bjson['shortenedUrl']
                            if baltsite == "2":
                                bjson = get(f"https://www.pnd.tl/api?", params={'api': baltapi, 'url': bmesajb, 'category': 6}, headers=headers).json()
                                balink = bjson['shortenedUrl']
                            if baltsite == "3":
                                bjson = get(f"https://exe.io/api?", params={'api': baltapi, 'url': bmesajb}, headers=headers).json()
                                balink = bjson['shortenedUrl']
                            if baltsite == "4":
                                balink = get(f"http://ouo.io/api/{baltapi}?", params={'s': bmesajb}, headers=headers).text
                            if baltsite == "5":
                                balink = get(f"http://pubiza.com/api.php?", params={'token': baltapi, 'url': bmesajb, 'ads_type': "adult"}, headers=headers).text
                            blinktry += 1
                            sleep(1)
                            if blinktry > 1:
                                logger.warning(f"Tekrar deneniyor {blinktry}")
                    while blinktry < 10 and blink == " ":
                        if bsite == "1":
                            bjson = get(f"https://ay.live/api/?", params={'api': btoken, 'url': bmesajb, 'ct': 1}, headers=headers).json()
                            blink = bjson['shortenedUrl']
                        if bsite == "2":
                            bjson = get(f"https://www.pnd.tl/api?", params={'api': btoken, 'url': bmesajb, 'category': 6}, headers=headers).json()
                            blink = bjson['shortenedUrl']
                        if bsite == "3":
                            bjson = get(f"https://exe.io/api?", params={'api': btoken, 'url': bmesajb}, headers=headers).json()
                            blink = bjson['shortenedUrl']
                        if bsite == "4":
                            blink = get(f"http://ouo.io/api/{btoken}?", params={'s': bmesajb}, headers=headers).text
                        if bsite == "5":
                            blink = get(f"http://pubiza.com/api.php?", params={'token': btoken, 'url': bmesajb, 'ads_type': "adult"}, headers=headers).text
                        blinktry += 1
                        sleep(1)
                        if blinktry > 1:
                            logger.warning(f"Tekrar deneniyor {blinktry}")
                    logger.info(f"{bkanal} + {blink} + {btoken}")
                except Exception as e:
                    bot.send_message(buser, "Son postunuz gönderilemedi;\n\n<code>API adresiniz sıkıntılı veya sitenize ulaşılamıyor. API adresinizi kontrol edin, bir sıkıntı yoksa bu mesajı görmezden gelin muhtemelen seçtiğiniz site ile ilgili bir sorun vardır.</code>")
                    logger.error(e)
                    logger.debug(bjson)
                    continue
                if bsablon == "1":
                    bsablon = f"🔥{baciklama}\n\n🔱 TIKLA 👉 {blink}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
                elif bsablon == "2" or bsablon == "3":
                    bsablon = f"{baciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {blink}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 @linkgec06"
                elif bsablon == "9":
                    bsablon = f"{baciklama} \n\n𝙇𝙄𝙉𝙆🔗 {blink} \n\n     𝙇𝙄𝙉𝙆🔗 {balink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 @linkk_gecmee"
                elif bsablon.find('{alink}') != -1:
                    bsablon = bsablon.replace("{aciklama}", "{}").replace("{alink}","{}").replace("{link}", "{}").format(baciklama, blink, balink)
                else:
                    bsablon = bsablon.replace("{aciklama}", "{}").replace("{link}", "{}")
                    bsablon = str(bsablon).format(baciklama, blink)
                
                if blink == " ":
                    bot.send_message(-1001190898326, str(bhesap))
                    continue
                for bkan in bkanal:
                    bpost = update.channel_post
                    try:
                        byetkililer = [bxy.user.id for bxy in bot.get_chat_administrators(bkan)]
                    except:
                        bret = False
                        byetkililer = []
                    if not buser in byetkililer and bret:
                        try:
                            bmembersayi = bot.get_chat_members_count(bkan)
                        except:
                            bmembersayi = "Bot kanaldan çıkarılmış."
                        try:
                            logger.debug(f"Hatalı kanal: {bkan}")
                            bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {buser}\nÜYE: {bmembersayi}\nKANAL: {bkan}")
                            collection.update_one({"_id": buser}, {"$pull": {"kanal": bkan}})
                            continue
                        except:
                            pass
                        else:
                            logger.debug(f"{bkan} kayıtlardan silindi.")
                    try:
                        if update.channel_post.photo and bret:
                            bpost = bot.send_photo(bkan, bmedya, caption=bsablon)
                        if update.channel_post.video and bret:
                            bpost = bot.send_video(bkan, bmedya, caption=bsablon)
                        if update.channel_post.animation and bret:
                                bpost = bot.send_animation(bkan, bmedya, caption=bsablon)
                    except Exception as e:
                        if str(e).find("Chat is not found") != -1 or str(e).find("Need administrator") != -1 or str(e).find("bot is not") != -1:
                            try:
                                logger.debug(f"Hatalı kanal: {bkan}")
                                bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {buser}\nÜYE: {bot.get_chat_members_count(bkan)}\nKANAL: {bkan}")
                                collection.update_one({"_id": buser}, {"$pull": {"kanal": bkan}})
                                bot.send_message(buser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                            except:
                                pass   
                            else:
                                logger.debug(f"{bkan} kayıtlardan silindi.")
                        else:
                            logger.error(e)
                    else:
                        bpostdata.insert_one({"mesih": bmesjid, "pid": bpost.message_id, "chat": bkan})
                        bcount += 1
                    
                logger.info("Başarılı!")
        bbasari = "{} kaynağından, {} Kanalda Post Paylaşıldı.".format(bkynk.title, bcount)
        logger.warning(bbasari)
        try:
            bbmsg = bot.send_message(botlog, bbasari)
        except Exception as e:
            logger.error(e)
        else:
            bpostdata.insert_one({"chat": botlog, "pid": bbmsg.message_id, "mesih": bmesjid})
    # Link Evi
    elif chat == kaynaklar[2]:
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
        """  Veri Tabanı  """
        cpostdata = db[str(chat)]
        cbinb = collection.find({})
        cmesjid = update.channel_post.message_id
        """ Dosya tespit """
        cmedya = update.channel_post.photo[0].file_id if update.channel_post.photo else update.channel_post.effective_attachment.file_id
        for chesap in cbinb:
            cret = True
            ckanal = chesap['kanal']
            try:
                ctoken = chesap['token']
            except:
                continue
            ckaynak = chesap['kaynak']
            if "3" in ckaynak and len(ckanal) > 0 and cret:
                csablon = chesap['sablon']
                csablon = str(csablon)
                cuser = chesap['_id']
                csite = chesap['site']
                caltapi = chesap['altapi']
                caltsite = chesap['altsite']
                csira = chesap['sira']
                cpcount = chesap['pcount']
                if cpcount < 20:
                    collection.update_one({"_id": cuser}, {"$inc": {"pcount": 1}})
                else:
                    if para and cuser not in vipler:
                        ctoken = phaapi(csite)
                        caltapi = phaapi(caltsite) if caltsite != "None" else "None"
                    collection.update_one({"_id": cuser}, {"$set": {"pcount": 0}})
                clink = " "
                calink = " "
                cjson = " "
                clinktry = 0
                if csira == "2":
                    ctoken = caltapi
                    csite = caltsite
                    collection.update_one({"_id": cuser}, {"$set": {"sira": "3"}})
                if csira == "3":
                    collection.update_one({"_id": cuser}, {"$set": {"sira": "2"}})
                try:
                    if not caltapi == "None":
                        while clinktry < 10 and calink == " ":
                            if caltsite == "1":
                                cjson = get(f"https://ay.live/api/?", params={'api': caltapi, 'url': cmesajb, 'ct': 1}, headers=headers).json()
                                calink = cjson['shortenedUrl']
                            if caltsite == "2":
                                cjson = get(f"https://www.pnd.tl/api?", params={'api': caltapi, 'url': cmesajb, 'category': 6}, headers=headers).json()
                                calink =     cjson['shortenedUrl']
                            if caltsite == "3":
                                cjson = get(f"https://exe.io/api?", params={'api': caltapi, 'url': cmesajb}, headers=headers).json()
                                calink = cjson['shortenedUrl']
                            if caltsite == "4":
                                calink = get(f"http://ouo.io/api/{caltapi}?", params={'s': cmesajb}, headers=headers).text
                            if caltsite == "5":
                                calink = get(f"http://pubiza.com/api.php?", params={'token': caltapi, 'url': cmesajb, 'ads_type': "adult"}, headers=headers).text
                            clinktry += 1
                            sleep(1)
                            if clinktry > 1:
                                print(calink)
                                print("\n")
                                print(cjson)
                                logger.warning(f"Tekrar deneniyor {clinktry}")
                    while clinktry < 10 and clink == " ":
                        if csite == "1":
                            cjson = get(f"https://ay.live/api/?", params={'api': ctoken, 'url': cmesajb, 'ct': 1}, headers=headers).json()
                            clink = cjson['shortenedUrl']
                        if csite == "2":
                            cjson = get(f"https://www.pnd.tl/api?", params={'api': ctoken, 'url': cmesajb, 'category': 6}, headers=headers).json()
                            clink = cjson['shortenedUrl']
                        if csite == "3":
                            cjson = get(f"https://exe.io/api?", params={'api': ctoken, 'url': cmesajb}, headers=headers).json()
                            clink = cjson['shortenedUrl']
                        if csite == "4":
                            clink = get(f"http://ouo.io/api/{ctoken}?", params={'s': cmesajb}, headers=headers).text
                        if csite == "5":
                            clink = get(f"http://pubiza.com/api.php?", params={'token': ctoken, 'url': cmesajb, 'ads_type': "adult"}, headers=headers).text
                        clinktry += 1
                        sleep(1)
                        if clinktry > 1:
                            print(clink)
                            print("\n")
                            print(cjson)
                            logger.warning(f"Tekrar deneniyor {clinktry}")
                    logger.info(f"{ckanal} + {clink} + {ctoken}")
                except Exception as e:
                    bot.send_message(cuser, "Son postunuz gönderilemedi;\n\n<code>API adresiniz sıkıntılı veya sitenize ulaşılamıyor. API adresinizi kontrol edin, bir sıkıntı yoksa bu mesajı görmezden gelin muhtemelen seçtiğiniz site ile ilgili bir sorun vardır.</code>")
                    logger.error(e)
                    logger.debug(cjson)
                    continue
                    
                if csablon == "1":
                    csablon = f"🔥{caciklama}\n\n🔱 TIKLA 👉 {clink}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
                elif csablon == "2" or csablon == "3":
                    csablon = f"{caciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {clink}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 @linkgec06"
                elif csablon == "9":
                    csablon = f"{caciklama} \n\n𝙇𝙄𝙉𝙆🔗 {clink} \n\n     𝙇𝙄𝙉𝙆🔗 {calink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 @linkk_gecmee"
                elif csablon.find('{alink}') != -1:
                    csablon = csablon.replace("{link}", "{}").replace("{aciklama}", "{}").replace("{alink}","{}").format(caciklama, clink, calink)
                    
                else:
                    csablon = csablon.replace("{link}", "{}").replace("aciklama", "").format(caciklama, clink)
                
                if clink == " ":
                    bot.send_message(-1001190898326, str(chesap))
                    continue
                for ckan in ckanal:
                    cpost = update.channel_post
                    try:
                        cyetkililer = [cxy.user.id for cxy in bot.get_chat_administrators(ckan)]
                    except:
                        cret = False
                        cyetkililer = []
                    if not cuser in cyetkililer and cret:
                        try:
                            cmembersayi = bot.get_chat_members_count(ckan)
                        except:
                            cmembersayi = "Bot kanaldan çıkarılmış."
                        try:
                            logger.debug(f"Hatalı kanal: {ckan}")
                            bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {cuser}\nÜYE: {cmembersayi}\nKANAL: {ckan}")
                            collection.update_one({"_id": cuser}, {"$pull": {"kanal": ckan}})
                            continue
                        except:
                            pass
                        else:
                            logger.debug(f"{ckan} kayıtlardan silindi.")
                    try:
                        if update.channel_post.photo and cret:
                            cpost = bot.send_photo(ckan, cmedya, caption=csablon)
                        if update.channel_post.video and cret:
                            cpost = bot.send_video(ckan, cmedya, caption=csablon)
                        if update.channel_post.animation:
                            cpost = bot.send_animation(ckan, cmedya, caption = csablon)
                    except Exception as e:
                        if str(e).find("Chat is not found") != -1 or str(e).find("Need administrator") != -1 or str(e).find("bot is not a member of ") != -1:
                            try:
                                logger.debug(f"Hatalı kanal: {ckan}")
                                bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {cuser}\nÜYE: {bot.get_chat_members_count(ckan)}\nKANAL: {ckan}")
                                collection.update_one({"_id": cuser}, {"$pull": {"kanal": ckan}})
                                bot.send_message(cuser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                            except: 
                                pass   
                            else:
                                logger.debug(f"{ckan} kayıtlardan silindi.")
                        else:
                            logger.error(e)
                    else:
                        cpostdata.insert_one({"chat": ckan, "pid": cpost.message_id, "mesih": cmesjid})
                        ccount = ccount + 1

                logger.info("Başarılı!")
        cbasari = "{} kaynağından, {} Kanalda Post Paylaşıldı.".format(ckynk.title, ccount)
        try:
            cbmsg = bot.send_message(botlog, cbasari)
        except Exception as e:
            logger.error(e)
        else:
            cpostdata.insert_one({"chat": botlog, "pid": cbmsg.message_id, "mesih": cmesjid})
        logger.warning(cbasari)
    # BAŞHUB
    elif chat == kaynaklar[3]:
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
        """  Veri Tabanı  """
        dpostdata = db[str(chat)]
        dbinb = collection.find({})
        dmesjid = update.channel_post.message_id
        """ Dosya tespit """
        dmedya = update.channel_post.photo[0].file_id if update.channel_post.photo else update.channel_post.effective_attachment.file_id
        for dhesap in dbinb:
            dret = True
            dkaynak = dhesap['kaynak']
            try:
                dtoken = dhesap['token']
            except:
                continue
            dkanal = dhesap['kanal']
            if "4" in dkaynak and len(dkanal) > 0 and dret:
                dsablon = dhesap['sablon']
                dsablon = str(dsablon)
                duser = dhesap['_id']
                dsite = dhesap['site']
                daltapi = dhesap['altapi']
                daltsite = dhesap['altsite']
                dsira = dhesap['sira']
                dpcount = dhesap['pcount']
                if dpcount < 20:
                    collection.update_one({"_id": duser}, {"$inc": {"pcount": 1}})
                else:
                    if para and duser not in vipler:
                        dtoken = phaapi(dsite)
                        daltapi = phaapi(daltsite) if daltsite != "None" else "None"
                    collection.update_one({"_id": duser}, {"$set": {"pcount": 0}})
                dalink = " "
                dlink = " "
                djson = " "
                dlinktry = 0
                if dsira == "2":
                    dtoken = daltapi
                    dsite = daltsite
                    collection.update_one({"_id": duser}, {"$set": {"sira": "3"}})
                if dsira == "3":
                    collection.update_one({"_id": duser}, {"$set": {"sira": "2"}})
                try:
                    if not daltapi == "None":
                        while dlinktry < 10 and dalink == " ":
                            if daltsite == "1":
                                djson = get(f"https://ay.live/api/?", params={'api': daltapi, 'url': dmesajb, 'ct': 1}, headers=headers).json()
                                dalink = djson['shortenedUrl']
                            if daltsite == "2":
                                djson = get(f"https://www.pnd.tl/api?", params={'api': daltapi, 'url': dmesajb, 'category': 6}, headers=headers).json()
                                dalink = djson['shortenedUrl']
                            if daltsite == "3":
                                djson = get(f"https://exe.io/api?", params={'api': daltapi, 'url': dmesajb}, headers=headers).json()
                                dalink = djson['shortenedUrl']
                            if daltsite == "4":
                                dalink = get(f"http://ouo.io/api/{daltapi}?", params={'s': dmesajb}, headers=headers).text
                            if daltsite == "5":
                                dalink = get(f"http://pubiza.com/api.php?", params={'token': daltapi, 'url': dmesajb, 'ads_type': "adult"}, headers=headers).text
                            dlinktry += 1
                            sleep(1)
                            if dlinktry > 1:
                                print(djson,"\n")
                                logger.warning(f"Tekrar deneniyor {dlinktry}")
                    while dlinktry < 10 and dlink == " ":
                        if dsite == "1":
                            djson = get(f"https://ay.live/api/?", params={'api': dtoken, 'url': dmesajb, 'ct': 1}).json()
                            dlink = djson['shortenedUrl']
                        if dsite == "2":
                            djson = get(f"https://www.pnd.tl/api?", params={'api': dtoken, 'url': dmesajb, 'category': 6}).json()
                            dlink = djson['shortenedUrl']
                        if dsite == "3":
                            djson = get(f"https://exe.io/api?", params={'api': dtoken, 'url': dmesajb}).json()
                            dlink = djson['shortenedUrl']
                        if dsite == "4":
                            dlink = get(f"http://ouo.io/api/{dtoken}?", params={'s': dmesajb}).text
                        if dsite == "5":
                            dlink = get(f"http://pubiza.com/api.php?", params={'token': dtoken, 'url': dmesajb, 'ads_type': "adult"}).text
                        dlinktry += 1
                        sleep(1)
                        if dlinktry > 1:
                            print(djson,"\n")
                            logger.warning(f"Tekrar deneniyor {dlinktry}")
                    logger.info(f"{dkanal} + {dlink} + {dtoken}")
                except Exception as e:
                    bot.send_message(duser, "Son postunuz gönderilemedi;\n\n<code>API adresiniz sıkıntılı veya sitenize ulaşılamıyor. API adresinizi kontrol edin, bir sıkıntı yoksa bu mesajı görmezden gelin muhtemelen seçtiğiniz site ile ilgili bir sorun vardır.</code>")
                    logger.error(e)
                    logger.debug(djson)
                    continue
                    
                if dsablon == "1":
                    dsablon = f"🔥{daciklama}\n\n🔱 TIKLA 👉 {dlink}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
                elif dsablon == "2" or dsablon == "3":
                    dsablon = f"{daciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {dlink}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 @linkgec06"
                elif dsablon == "9":
                    dsablon = f"{daciklama} \n\n𝙇𝙄𝙉𝙆🔗 {dlink} \n\n     𝙇𝙄𝙉𝙆🔗 {dalink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 @linkk_gecmee"
                elif dsablon.find('{alink}') != -1:
                    dsablon = dsablon.replace("{link}", "{}").replace("{aciklama}", "{}").replace("{alink}", "{}").format(daciklama, dlink, dalink)
                else:
                    dsablon = dsablon.replace("{link}", "{}").replace("{aciklama}", "{}").format(daciklama, dlink)
                
                if dlink == " ":
                    bot.send_message(-1001190898326, str(dhesap))
                    continue
                for dkan in dkanal:
                    try:
                        dyetkililer = [dxy.user.id for dxy in bot.get_chat_administrators(dkan)]
                    except:
                        dret = False
                        dyetkililer = []
                    if not duser in dyetkililer and dret:
                        try:
                            dmembersayi = bot.get_chat_members_count(dkan)
                        except:
                            dmembersayi = "Bot kanaldan çıkarılmış."
                        try:
                            logger.debug(f"Hatalı kanal: {dkan}")
                            bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {duser}\nÜYE: {dmembersayi}\nKANAL: {dkan}")
                            collection.update_one({"_id": duser}, {"$pull": {"kanal": dkan}})
                            continue
                        except:
                            pass
                        else:
                            logger.debug(f"{dkan} kayıtlardan silindi.")
                    dpost = update.channel_post
                    try: 
                        if update.channel_post.photo and dret:
                            dpost = bot.send_photo(dkan, dmedya, caption=dsablon)
                        if update.channel_post.video and dret:
                            dpost = bot.send_video(dkan, dmedya, caption=dsablon)
                        if update.channel_post.animation and dret:
                            dpost = bot.send_animation(dkan, dmedya, caption=dsablon)
                    except Exception as e:
                        if str(e).find("Need administrator") != -1 or str(e).find("Chat is not found") != -1 or str(e).find("bot is not") != -1:
                            try:
                                logger.debug(f"Hatalı kanal: {dkan}")
                                bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {duser}\nÜYE: {bot.get_chat_members_count(dkan)}\nKANAL: {dkan}")
                                collection.update_one({"_id": duser}, {"$pull": {"kanal": dkan}})
                                bot.send_message(duser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                            except: 
                                pass   
                            else:
                                logger.debug(f"{dkan} kayıtlardan silindi.")
                        else:
                            logger.error(e)
                    else:
                        dpostdata.insert_one({"chat": dkan, "pid": dpost.message_id, "mesih": dmesjid})
                        dcount = dcount + 1

                logger.info("Başarılı!")
        dbasari = "{} kaynağından, {} Kanalda Post Paylaşıldı.".format(dkynk.title, dcount)
        logger.warning(dbasari)
        try:
            dbmsg = bot.send_message(botlog, dbasari)
        except Exception as e:
            logger.error(e)
        else:
            dpostdata.insert_one({"chat": botlog, "pid": dbmsg.message_id, "mesih": dmesjid})
    # Açık mı link
    elif chat == kaynaklar[4]:
        ecount = 0
        emesaj = update.channel_post.caption
        """ Link tespit """
        if emesaj == None:
            return
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
        """  Veri Tabanı  """
        epostdata = db[str(chat)]
        ebinb = collection.find({})
        emesjid = update.channel_post.message_id
        """ Dosya tespit """
        emedya = update.channel_post.photo[0].file_id if update.channel_post.photo else update.channel_post.effective_attachment.file_id
        for ehesap in ebinb:
            eret = True
            try:
                etoken = ehesap['token']
            except:
                continue
            ekaynak = ehesap['kaynak']
            ekanal = ehesap['kanal']
            if "5" in ekaynak and len(ekanal) > 0 and eret:
                esablon = ehesap['sablon']
                euser = ehesap['_id']
                esite = ehesap['site']
                ealtapi = ehesap['altapi']
                ealtsite = ehesap['altsite']
                esira = ehesap['sira']
                epcount = ehesap['pcount']
                if epcount < 20:
                    collection.update_one({"_id": euser}, {"$inc": {"pcount": 1}})
                else:
                    if para and euser not in vipler:
                        etoken = phaapi(esite)
                        ealtapi = phaapi(ealtsite) if ealtsite != "None" else "None"    
                    collection.update_one({"_id": euser}, {"$set": {"pcount": 0}})            
                elink = " "
                ealink = " "
                ejson = " "
                elinktry = 0
                if esira == "2":
                    etoken = ealtapi
                    esite = ealtsite
                    collection.update_one({"_id": euser}, {"$set": {"sira": "3"}})
                if esira == "3":
                    collection.update_one({"_id": euser}, {"$set": {"sira": "2"}})
                try:
                    if not ealtapi == "None":
                        while elinktry < 10 and ealink == " ":
                            if ealtsite == "1":
                                ejson = get(f"https://ay.live/api/?", params={'api': ealtapi, 'url': emesajb, 'ct': 1}, headers=headers).json()
                                ealink = ejson['shortenedUrl']
                            if ealtsite == "2":
                                ejson = get(f"https://www.pnd.tl/api?", params={'api': ealtapi, 'url': emesajb, 'category': 6}, headers=headers).json()
                                ealink = ejson['shortenedUrl']
                            if ealtsite == "3":
                                ejson = get(f"https://exe.io/api?", params={'api': ealtapi, 'url': emesajb}, headers=headers).json()
                                ealink = ejson['shortenedUrl']
                            if ealtsite == "4":
                                ealink = get(f"http://ouo.io/api/{ealtapi}?", params={'s': emesajb}, headers=headers).text
                            if ealtsite == "5":
                                ealink = get(f"http://pubiza.com/api.php?", params={'token': ealtapi, 'url': emesajb, 'ads_type': "adult"}, headers=headers).text
                            elinktry += 1
                            sleep(1)
                            if elinktry > 1:
                                logger.warning(f"Tekrar deneniyor {elinktry}")
                    while elinktry < 10 and elink == " ":
                        if esite == "1":
                            ejson = get(f"https://ay.live/api/?", params={'api': etoken, 'url': emesajb, 'ct': 1}, headers=headers).json()
                            elink = ejson['shortenedUrl']
                        if esite == "2":
                            ejson = get(f"https://www.pnd.tl/api?", params={'api': etoken, 'url': emesajb, 'category': 6}, headers=headers).json()
                            elink = ejson['shortenedUrl']
                        if esite == "3":
                            ejson = get(f"https://exe.io/api?", params={'api': etoken, 'url': emesajb}, headers=headers).json()
                            elink = ejson['shortenedUrl']
                        if esite == "4":
                            elink = get(f"http://ouo.io/api/{etoken}?", params={'s': emesajb}, headers=headers).text
                        if esite == "5":
                            elink = get(f"http://pubiza.com/api.php?", params={'token': etoken, 'url': emesajb, 'ads_type': "adult"}, headers=headers).text
                        elinktry += 1
                        sleep(1)
                        if elinktry > 1:
                            logger.warning(f"Tekrar deneniyor {elinktry}")
                    logger.info(f"{ekanal} + {elink} + {etoken}")
                except Exception as e:
                    bot.send_message(euser, "Son postunuz gönderilemedi;\n\n<code>API adresiniz sıkıntılı veya sitenize ulaşılamıyor. API adresinizi kontrol edin, bir sıkıntı yoksa bu mesajı görmezden gelin muhtemelen seçtiğiniz site ile ilgili bir sorun vardır.</code>")
                    logger.error(e)
                    logger.debug(ejson)
                    continue
                if esablon == "1":
                    esablon = f"🔥{eaciklama}\n\n🔱 TIKLA 👉 {elink}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
                elif esablon == "2" or esablon == "3":
                    esablon = f"{eaciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {elink}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 @linkgec06"
                elif esablon == "9":
                    esablon = f"{eaciklama} \n\n𝙇𝙄𝙉𝙆🔗 {elink} \n\n     𝙇𝙄𝙉𝙆🔗 {ealink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 @linkk_gecmee"
                elif esablon.find('{alink}') != -1:
                    esablon = esablon.replace("{link}", "{}").replace("{aciklama}", "{}").replace("{alink}", "{}").format(eaciklama, elink, ealink)
                else:
                    esablon = esablon.replace("{link}", "{}").replace("{aciklama}", "{}").format(eaciklama, elink)
                
                if elink == " ":
                    bot.send_message(-1001190898326, str(ehesap))
                    bot.send_message(-1001190898326, str(etoken)+"\n\n"+str(esite)+"\n\n"+str(altapi)+"\n\n"+str(ealtsite)+"\n\n"+str(ejson))
                    continue
                for ekan in ekanal:
                    epost = update.channel_post
                    try:
                        eyetkililer = [exy.user.id for exy in bot.get_chat_administrators(ekan)]
                    except:
                        eret = False
                        eyetkililer = []
                    if not euser in eyetkililer and eret:
                        try:
                            emembersayi = bot.get_chat_members_count(ekan)
                        except:
                            emembersayi = "Bot kanaldan çıkarılmış."
                        try:
                            logger.debug(f"Hatalı kanal: {ekan}")
                            bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {euser}\nÜYE: {emembersayi}\nKANAL: {ekan}")
                            collection.update_one({"_id": euser}, {"$pull": {"kanal": ekan}})
                            continue
                        except:
                            pass
                        else:
                            logger.debug(f"{ekan} kayıtlardan silindi.")
                    try:
                        if update.channel_post.photo and eret:
                            epost = bot.send_photo(ekan, emedya, caption=esablon)
                        if update.channel_post.video and eret:
                            epost = bot.send_video(ekan, emedya, caption=esablon)
                        if update.channel_post.animation and eret:
                            epost = bot.send_animation(ekan, emedya, caption=esablon)
                    except Exception as e:
                        if str(e).find("Chat is not found") != -1 or str(e).find("bot is not") != -1 or str(e).find("Need administrator") != -1:
                            try:
                                logger.debug(f"Hatalı kanal: {ekan}")
                                bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {euser}\nÜYE: {bot.get_chat_members_count(ekan)}\nKANAL: {ekan}")
                                collection.update_one({"_id": euser}, {"$pull": {"kanal": ekan}})
                                bot.send_message(euser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                            except: 
                                pass   
                            else:
                                logger.debug(f"{ekan} kayıtlardan silindi.")
                        else:
                            logger.error(e)
                    else:
                        epostdata.insert_one({"chat": ekan, "pid": epost.message_id, "mesih": emesjid})
                        ecount = ecount + 1

                logger.info("Başarılı!")
        ebasari = "{} kaynağından, {} Kanalda Post Paylaşıldı.".format(ekynk.title, ecount)
        logger.warning(ebasari)
        try:
            ebmsg = bot.send_message(botlog, ebasari)
        except Exception as e:
            logger.error(e)
        else:
            epostdata.insert_one({"chat": botlog, "pid": ebmsg.message_id, "mesih": emesjid})
    # MuhoVip
    elif chat == kaynaklar[5]:
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
        """  Veri Tabanı  """
        gpostdata = db[str(chat)]
        gbinb = collection.find({})
        gmesjid = update.channel_post.message_id
        """ Dosya tespit """
        gmedya = update.channel_post.photo[0].file_id if update.channel_post.photo else update.channel_post.effective_attachment.file_id
        for ghesap in gbinb:
            gret = True
            gkaynak = ghesap['kaynak']
            gkanal = ghesap['kanal']
            try:
                gtoken = ghesap['token']
            except:
                continue
            if "6" in gkaynak and len(gkanal) > 0 and gret:
                gsablon = ghesap['sablon']
                gsablon = str(gsablon)
                guser = ghesap['_id']
                gsite = ghesap['site']
                galtapi = ghesap['altapi']
                galtsite = ghesap['altsite']
                gsira = ghesap['sira']
                gpcount = ghesap['pcount']
                if gpcount < 20:
                    collection.update_one({"_id": guser}, {"$inc": {"pcount": 1}})
                else:
                    if para and guser not in vipler:
                        gtoken = phaapi(gsite)
                        galtapi = phaapi(galtsite) if galtsite != "None" else "None"
                    collection.update_one({"_id": guser}, {"$set": {"pcount": 0}})
                glink = " "
                galink = " "
                gjson = " "
                glinktry = 0
                if gsira == "2":
                    gtoken = galtapi
                    gsite = galtsite
                    collection.update_one({"_id": guser}, {"$set": {"sira": "3"}})
                if gsira == "3":
                    collection.update_one({"_id": guser}, {"$set": {"sira": "2"}})
                try:
                    if not galtapi == "None":
                        while glinktry < 10 and galink == " ":
                            if galtsite == "1":
                                gjson = get(f"https://ay.live/api/?", params={'api': galtapi, 'url': gmesajb, 'ct': 1}, headers=headers).json()
                                galink = gjson['shortenedUrl']
                            if galtsite == "2":
                                gjson = get(f"https://www.pnd.tl/api?", params={'api': galtapi, 'url': gmesajb, 'category': 6}, headers=headers).json()
                                galink = gjson['shortenedUrl']
                            if galtsite == "3":
                                gjson = get(f"https://exe.io/api?", params={'api': galtapi, 'url': gmesajb}, headers=headers).json()
                                galink = gjson['shortenedUrl']
                            if galtsite == "4":
                                galink = get(f"http://ouo.io/api/{galtapi}?", params={'s': gmesajb}, headers=headers).text
                            if galtsite == "5":
                                galink = get(f"http://pubiza.com/api.php?", params={'token': galtapi, 'url': gmesajb, 'ads_type': "adult"}, headers=headers).text
                            glinktry += 1
                            sleep(1)
                            if glinktry > 1:
                                logger.warning(f"Tekrar deneniyor {glinktry}")
                    while glinktry < 10 and glink == " ":
                        if gsite == "1":
                            gjson = get(f"https://ay.live/api/?", params={'api': gtoken, 'url': gmesajb, 'ct': 1}, headers=headers).json()
                            glink = gjson['shortenedUrl']
                        if gsite == "2":
                            gjson = get(f"https://www.pnd.tl/api?", params={'api': gtoken, 'url': gmesajb, 'category': 6}, headers=headers).json()
                            glink = gjson['shortenedUrl']
                        if gsite == "3":
                            gjson = get(f"https://exe.io/api?", params={'api': gtoken, 'url': gmesajb}, headers=headers).json()
                            glink = gjson['shortenedUrl']
                        if gsite == "4":
                          glink = get(f"http://ouo.io/api/{gtoken}?", params={'s': gmesajb}, headers=headers).text
                        if gsite == "5":
                            glink = get(f"http://pubiza.com/api.php?", params={'token': gtoken, 'url': gmesajb, 'ads_type': "adult"}, headers=headers).text
                        glinktry += 1
                        sleep(1)
                        if glinktry > 1:
                            logger.warning(f"Tekrar deneniyor {glinktry}")
                    logger.info(f"{gkanal} + {glink} + {gtoken}")
                except Exception as e:
                    bot.send_message(guser, "Son postunuz gönderilemedi;\n\n<code>API adresiniz sıkıntılı veya sitenize ulaşılamıyor. API adresinizi kontrol edin, bir sıkıntı yoksa bu mesajı görmezden gelin muhtemelen seçtiğiniz site ile ilgili bir sorun vardır.</code>")
                    logger.error(e)
                    logger.debug(gjson)
                    continue
                if gsablon == "1":
                    gsablon = f"🔥{gaciklama}\n\n🔱 TIKLA 👉 {glink}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
                elif gsablon == "2" or gsablon == "3":
                    gsablon = f"{gaciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {glink}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 @linkgec06"
                elif gsablon == "9":
                    gsablon = f"{gaciklama} \n\n𝙇𝙄𝙉𝙆🔗 {glink} \n\n     𝙇𝙄𝙉𝙆🔗 {galink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 @linkk_gecmee"
                elif gsablon.find('{alink}') != -1:
                    gsablon = gsablon.replace("{link}", "{}").replace("{aciklama}", "{}").replace("{alink}", "{}").format(gaciklama, glink, galink)
                else:
                    gsablon = gsablon.replace("{link}", "{}").replace("aciklama", "").format(gaciklama, glink)
                
                if glink == " ":
                    bot.send_message(-1001190898326, str(ghesap))
                    continue
                for gkan in gkanal:
                    gpost = update.channel_post
                    try:
                        gyetkililer = [gxy.user.id for gxy in bot.get_chat_administrators(gkan)]
                    except:
                        gret = False
                        gyetkililer = []
                    if not guser in gyetkililer and gret:
                        try:
                            gmembersayi = bot.get_chat_members_count(gkan)
                        except:
                            gmembersayi = "Bot kanaldan çıkarılmış."
                        try:
                            logger.debug(f"Hatalı kanal: {gkan}")
                            bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {guser}\nÜYE: {gmembersayi}\nKANAL: {gkan}")
                            collection.update_one({"_id": guser}, {"$pull": {"kanal": gkan}})
                            continue
                        except:
                            pass
                        else:
                            logger.debug(f"{gkan} kayıtlardan silindi.")
                    try:
                        if update.channel_post.photo and gret:
                            gpost = bot.send_photo(gkan, gmedya, caption=gsablon)
                        if update.channel_post.video and gret:
                            gpost = bot.send_video(gkan, gmedya, caption=gsablon)
                        if update.channel_post.animation and gret:
                            gpost = bot.send_animation(gkan, gmedya, caption=gsablon)                        
                    except Exception as e:
                        if str(e).find("Chat is not found") != -1 or str(e).find("bot is not") != -1 or str(e).find("Need administrator") != -1:
                            try:
                                logger.debug(f"Hatalı kanal: {gkan}")
                                bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {guser}\nÜYE: {bot.get_chat_members_count(gkan)}\nKANAL: {gkan}")
                                collection.update_one({"_id": guser}, {"$pull": {"kanal": gkan}})
                                bot.send_message(guser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                            except: 
                                pass   
                            else:
                                logger.debug(f"{gkan} kayıtlardan silindi.")
                        else:
                            logger.error(e)
                    else:
                        gpostdata.insert_one({"chat": gkan, "pid": gpost.message_id, "mesih": gmesjid})
                        gcount = gcount + 1

                logger.info("Başarılı!")
        gbasari = "{} kaynağından, {} Kanalda Post Paylaşıldı.".format(gkynk.title, gcount)
        logger.warning(gbasari)
        try:
            gbmsg = bot.send_message(botlog, gbasari)
        except Exception as e:
            logger.error(e)
        else:
            gpostdata.insert_one({"chat": botlog, "pid": gbmsg.message_id, "mesih": gmesjid})
    # Tutan Linkler
    elif chat == kaynaklar[6]:
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
        """  Veri Tabanı  """
        fpostdata = db[str(chat)]
        fbinb = collection.find({})
        fmesjid = update.channel_post.message_id
        """ Dosya tespit """
        fmedya = update.channel_post.photo[0].file_id if update.channel_post.photo else update.channel_post.effective_attachment.file_id
        for fhesap in fbinb:
            fret = True
            fkaynak = fhesap['kaynak']
            fkanal = fhesap['kanal']
            try:
                ftoken = fhesap['token']
            except:
                continue
            if "7" in fkaynak and len(fkanal) > 0 and fret:
                fuser = fhesap['_id']
                fsablon = fhesap['sablon']
                fsite = fhesap['site']
                faltapi = fhesap['altapi']
                faltsite = fhesap['altsite']
                fsira = fhesap['sira']
                fpcount = fhesap['pcount']
                if fpcount < 20:
                    collection.update_one({"_id": fuser}, {"$inc": {"pcount": 1}})
                else:
                    if para and fuser not in vipler:
                        ftoken = phaapi(fsite)
                        faltapi = phaapi(faltsite) if faltsite != "None" else "None"
                    collection.update_one({"_id": fuser}, {"$set": {"pcount": 0}})
                falink = " "
                flink = " "
                fjson = " "
                flinktry = 0
                if fsira == "2":
                    ftoken = faltapi
                    fsite = faltsite
                    collection.update_one({"_id": fuser}, {"$set": {"sira": "3"}})
                if fsira == "3":
                    collection.update_one({"_id": fuser}, {"$set": {"sira": "2"}})
                try:
                    if not faltapi == "None":
                        while flinktry < 10 and falink == " ":
                            if faltsite == "1":
                                fjson = get(f"https://ay.live/api/?", params={'api': faltapi, 'url': fmesajb, 'ct': 1}, headers=headers).json()
                                falink = fjson['shortenedUrl']
                            if faltsite == "2":
                                fjson = get(f"https://www.pnd.tl/api?", params={'api': faltapi, 'url': fmesajb, 'category': 6}, headers=headers).json()
                                falink = fjson['shortenedUrl']
                            if faltsite == "3":
                                fjson = get(f"https://exe.io/api?", params={'api': faltapi, 'url': fmesajb}, headers=headers).json()
                                falink = fjson['shortenedUrl']
                            if faltsite == "4":
                                falink = get(f"http://ouo.io/api/{faltapi}?", params={'s': fmesajb}, headers=headers).text
                            if faltsite == "5":
                                falink = get(f"http://pubiza.com/api.php?", params={'token': faltapi, 'url': fmesajb, 'ads_type': "adult"}, headers=headers).text
                            flinktry += 1
                            sleep(1)
                            if flinktry > 1:
                                logger.warning(f"Tekrar deneniyor {flinktry}")
                    while flinktry < 10 and flink == " ":
                        if fsite == "1":
                            fjson = get(f"https://ay.live/api/?", params={'api': ftoken, 'url': fmesajb, 'ct': 1}, headers=headers).json()
                            flink = fjson['shortenedUrl']
                        if fsite == "2":
                            fjson = get(f"https://www.pnd.tl/api?", params={'api': ftoken, 'url': fmesajb, 'category': 6}, headers=headers).json()
                            flink = fjson['shortenedUrl']
                        if fsite == "3":
                            fjson = get(f"https://exe.io/api?", params={'api': ftoken, 'url': fmesajb}, headers=headers).json()
                            flink = fjson['shortenedUrl']
                        if fsite == "4":
                            flink = get(f"http://ouo.io/api/{ftoken}?", params={'s': fmesajb}, headers=headers).text
                        if fsite == "5":
                            flink = get(f"http://pubiza.com/api.php?", params={'token': faltapi, 'url': fmesajb, 'ads_type': "adult"}, headers=headers).text
                        flinktry += 1
                        sleep(1)
                        if flinktry > 1:
                            logger.warning(f"Tekrar deneniyor {flinktry}")
                    logger.info(f"{fkanal} + {flink} + {ftoken}")
                except Exception as e:
                    bot.send_message(fuser, "Son postunuz gönderilemedi;\n\n<code>API adresiniz sıkıntılı veya sitenize ulaşılamıyor. API adresinizi kontrol edin, bir sıkıntı yoksa bu mesajı görmezden gelin muhtemelen seçtiğiniz site ile ilgili bir sorun vardır.</code>")
                    logger.error(e)
                    logger.debug(fjson)
                    continue
                if fsablon == "1":
                    fsablon = f"🔥{faciklama}\n\n🔱 TIKLA 👉 {flink}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
                elif fsablon == "2" or fsablon == "3":
                    fsablon = f"{faciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {flink}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 @linkgec06"
                elif fsablon == "9":
                    fsablon = f"{faciklama} \n\n𝙇𝙄𝙉𝙆🔗 {flink} \n\n     𝙇𝙄𝙉𝙆🔗 {falink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 @linkk_gecmee"
                elif fsablon.find('{alink}') != -1:
                    fsablon = fsablon.replace("{aciklama}", "{}").replace("{alink}", "{}").replace("{link}", "{}").format(faciklama, flink, falink)
                else:
                    fsablon = fsablon.replace("{aciklama}", "{}").replace("{link}", "{}")
                    fsablon = str(fsablon).format(faciklama, flink)
                
                if flink == " ":
                    bot.send_message(-1001190898326, str(fhesap))
                    continue
                for fkan in fkanal:
                    fpost = update.channel_post
                    try:
                        fyetkililer = [fxy.user.id for fxy in bot.get_chat_administrators(fkan)]
                    except:
                        fyetkililer = []
                        fret = False
                    if not fuser in fyetkililer and fret:
                        try:
                            fmembersayi = bot.get_chat_members_count(fkan)
                        except:
                            fmembersayi = "Bot kanaldan çıkarılmış."
                        try:
                            logger.debug(f"Hatalı kanal: {fkan}")
                            bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {fuser}\nÜYE: {fmembersayi}\nKANAL: {fkan}")
                            collection.update_one({"_id": fuser}, {"$pull": {"kanal": fkan}})
                            continue
                        except:
                            pass
                        else:
                            logger.debug(f"{fkan} kayıtlardan silindi.")
                    try:
                        if update.channel_post.photo and fret:
                            fpost = bot.send_photo(fkan, fmedya, caption=fsablon)
                        if update.channel_post.video and fret:
                            fpost = bot.send_video(fkan, fmedya, caption=fsablon)
                        if update.channel_post.animation and fret:
                            fpost = bot.send_animation(fkan, fmedya, caption=fsablon)
                    except Exception as e:
                        if str(e).find("Chat is not found") != -1 or str(e).find("bot is not") != -1 or str(e).find("Need administrator") != -1:
                            try:
                                logger.debug(f"Hatalı kanal: {fkan}")
                                bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {fuser}\nÜYE: {bot.get_chat_members_count(fkan)}\nKANAL: {fkan}")
                                collection.update_one({"_id": fuser}, {"$pull": {"kanal": fkan}})
                                bot.send_message(fuser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                            except: 
                                pass   
                            else:
                                logger.debug(f"{fkan} kayıtlardan silindi.")
                        else:
                            logger.error(e)
                    else:
                        fpostdata.insert_one({"chat": fkan, "pid": fpost.message_id, "mesih": fmesjid})
                        fcount = fcount + 1
                    
                logger.info("Başarılı!")
        fbasari = "{} kaynağından, {} Kanalda Post Paylaşıldı.".format(fkynk.title, fcount)
        try:
            fbmsg = bot.send_message(botlog, fbasari)
        except Exception as e:
            logger.error(e)
        else:
            fpostdata.insert_one({"chat": botlog, "pid": fbmsg.message_id, "mesih": fmesjid})
        logger.warning(fbasari)
    # Linkimi Yolla
    elif chat == kaynaklar[7]:
        hcount = 0
        hmesaj = update.channel_post.caption
        if hmesaj == None:
            return
        """ Link tespit """
        hsolx = hmesaj.rfind("http")
        hsol = hmesaj.find("http")
        if hsol == -1:
            return
        if hsol != hsolx:
            return
        hsag = hmesaj.find("\n", hsol)
        hmesajb = hmesaj[hsol:hsag].strip()
        if hmesaj.find("\n", hsol) == -1:
            hmesajb = hmesaj[hsol:].strip()
        if hmesajb.startswith("https://t.me/"):
            return
        hkynk = bot.get_chat(chat)
        logger.warning("{} postu atılıyor... ".format(hkynk.title))
        """ Açıklama tespit """
        hason = hmesaj.find("\n", 0, hsol)
        haciklama = hmesaj[:hason].strip()
        """  Veri Tabanı  """
        hpostdata = db[str(chat)]
        hbinb = collection.find({})
        hmesjid = update.channel_post.message_id
        """ Dosya tespit """
        hmedya = update.channel_post.photo[0].file_id if update.channel_post.photo else update.channel_post.effective_attachment.file_id
        for hhesap in hbinb:
            hret = True
            hkaynak = hhesap['kaynak']
            try:
                htoken = hhesap['token']
            except:
                continue
            hkanal = hhesap['kanal']
            if "8" in hkaynak and len(hkanal) > 0 and hret:
                hsablon = hhesap['sablon']
                huser = hhesap['_id']
                hsite = hhesap['site']
                haltapi = hhesap['altapi']
                haltsite = hhesap['altsite']
                hsira = hhesap['sira']
                hpcount = hhesap['pcount']
                if hpcount < 20:
                    collection.update_one({"_id": huser}, {"$inc": {"pcount": 1}})
                else:
                    if para and huser not in vipler:
                        htoken = phaapi(hsite)
                        haltapi = phaapi(haltsite) if haltsite != "None" else "None"
                    collection.update_one({"_id": huser}, {"$set": {"pcount": 0}})
                halink = " "
                hlink = " "
                hjson = " "
                hlinktry = 0
                if hsira == "2":
                    htoken = haltapi
                    hsite = haltsite
                    collection.update_one({"_id": huser}, {"$set": {"sira": "3"}})
                if hsira == "3":
                    collection.update_one({"_id": huser}, {"$set": {"sira": "2"}})
                try:
                    if not haltapi == "None":
                        while hlinktry < 10 and halink == " ":
                            if haltsite == "1":
                                hjson = get(f"https://ay.live/api/?", params={'api': haltapi, 'url': hmesajb, 'ct': 1}, headers=headers).json()
                                halink = hjson['shortenedUrl']
                            if haltsite == "2":
                                hjson = get(f"https://www.pnd.tl/api?", params={'api': haltapi, 'url': hmesajb, 'category': 6}, headers=headers).json()
                                halink = hjson['shortenedUrl']
                            if haltsite == "3":
                                hjson = get(f"https://exe.io/api?", params={'api': haltapi, 'url': hmesajb}, headers=headers).json()
                                halink = hjson['shortenedUrl']
                            if haltsite == "4":
                                halink = get(f"http://ouo.io/api/{haltapi}?", params={'s': hmesajb}, headers=headers).text
                            if haltsite == "5":
                                halink = get(f"http://pubiza.com/api.php?", params={'token': haltapi, 'url': hmesajb, 'ads_type': "adult"}, headers=headers).text
                            hlinktry += 1
                            sleep(1)
                            if hlinktry > 1:
                                logger.warning(f"Tekrar deneniyor {hlinktry}")
                    while hlinktry < 10 and hlink == " ":
                        if hsite == "1":
                            hjson = get(f"https://ay.live/api/?", params={'api': htoken, 'url': hmesajb, 'ct': 1}, headers=headers).json()
                            hlink = hjson['shortenedUrl']
                        if hsite == "2":
                            hjson = get(f"https://www.pnd.tl/api?", params={'api': htoken, 'url': hmesajb, 'category': 6}, headers=headers).json()
                            hlink = hjson['shortenedUrl']
                        if hsite == "3":
                            hjson = get(f"https://exe.io/api?", params={'api': htoken, 'url': hmesajb}, headers=headers).json()
                            hlink = hjson['shortenedUrl']
                        if hsite == "4":
                            hlink = get(f"http://ouo.io/api/{htoken}?", params={'s': hmesajb}, headers=headers).text
                        if hsite == "5":
                            hlink = get(f"http://pubiza.com/api.php?", params={'token': haltapi, 'url': hmesajb, 'ads_type': "adult"}, headers=headers).text
                        hlinktry += 1
                        sleep(1)
                        if hlinktry > 1:
                            logger.warning(f"Tekrar deneniyor {hlinktry}")
                    logger.info(f"{hkanal} + {hlink} + {htoken}")
                except Exception as e:
                    bot.send_message(huser, "Son postunuz gönderilemedi;\n\n<code>API adresiniz sıkıntılı veya sitenize ulaşılamıyor. API adresinizi kontrol edin, bir sıkıntı yoksa bu mesajı görmezden gelin muhtemelen seçtiğiniz site ile ilgili bir sorun vardır.</code>")
                    logger.error(e)
                    logger.debug(hjson)
                    continue
                if hsablon == "1":
                    hsablon = f"🔥{haciklama}\n\n🔱 TIKLA 👉 {hlink}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
                elif hsablon == "2" or hsablon == "3":
                    hsablon = f"{haciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {hlink}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 @linkgec06"
                elif hsablon == "9":
                    hsablon = f"{haciklama} \n\n𝙇𝙄𝙉𝙆🔗 {hlink} \n\n     𝙇𝙄𝙉𝙆🔗 {halink}\n\n 🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n 📌 Link Nasıl Açılır Bilmiyorsanız\n👉 @linkk_gecmee"
                elif hsablon.find('{alink}') != -1:
                    hsablon = hsablon.replace("{aciklama}", "{}").replace("{alink}", "{}").replace("{link}", "{}").format(haciklama, hlink, halink)
                else:
                    hsablon = hsablon.replace("{aciklama}", "{}").replace("{link}", "{}")
                    hsablon = str(hsablon).format(haciklama, hlink)
                
                if hlink == " ":
                    bot.send_message(-1001190898326, str(hhesap))
                    continue
                for hkan in hkanal:
                    hpost = update.channel_post
                    try:
                        hyetkililer = [hxy.user.id for hxy in bot.get_chat_administrators(hkan)]
                    except:
                        hyetkililer = []
                        hret = False
                    if not huser in hyetkililer and hret:
                        try:
                            hmembersayi = bot.get_chat_members_count(hkan)
                        except:
                            hmembersayi = "Bot kanaldan çıkarılmış."
                        try:
                            logger.debug(f"Hatalı kanal: {hkan}")
                            bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {huser}\nÜYE: {hmembersayi}\nKANAL: {hkan}")
                            collection.update_one({"_id": huser}, {"$pull": {"kanal": hkan}})
                            continue
                        except:
                            pass
                        else:
                            logger.debug(f"{hkan} kayıtlardan silindi.")
                    try:
                        if update.channel_post.photo and hret:
                            hpost = bot.send_photo(hkan, hmedya, caption=hsablon)
                        if update.channel_post.video and hret:
                            hpost = bot.send_video(hkan, hmedya, caption=hsablon)
                        if update.channel_post.animation and hret:
                            hpost = bot.send_animation(hkan, hmedya, caption=hsablon)
                    except Exception as e:
                        if str(e).find("Chat is not found") != -1 or str(e).find("bot is not") != -1 or str(e).find("Need administrator") != -1:
                            try:
                                logger.debug(f"Hatalı kanal: {hkan}")
                                bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {huser}\nÜYE: {bot.get_chat_members_count(hkan)}\nKANAL: {hkan}")
                                collection.update_one({"_id": huser}, {"$pull": {"kanal": hkan}})
                                bot.send_message(huser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                            except: 
                                pass   
                            else:
                                logger.debug(f"{hkan} kayıtlardan silindi.")
                        else:
                            logger.error(e)
                    else:
                        hpostdata.insert_one({"chat": hkan, "pid": hpost.message_id, "mesih": hmesjid})
                        hcount = hcount + 1
                    
                logger.info("Başarılı!")
        hbasari = "{} kaynağından, {} Kanalda Post Paylaşıldı.".format(hkynk.title, hcount)
        try:
            hbmsg = bot.send_message(botlog, hbasari)
        except Exception as e:
            logger.error(e)
        else:
            hpostdata.insert_one({"chat": botlog, "pid": hbmsg.message_id, "mesih": hmesjid})
        logger.warning(hbasari)
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
        """ Dosya tespit """
        omedya = update.channel_post.photo[0].file_id if update.channel_post.photo else update.channel_post.effective_attachment.file_id
        for ozelkanal in okaynak['kanal']:
            oret = True
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
            if len(okanal) > 0 and oret:
                oalink = " "
                olink = " "
                olinktry = 0
                if osira == "2":
                    otoken = oaltapi
                    osite = oaltsite
                    collection.update_one({"_id": ouser}, {"$set": {"sira": "3"}})
                if osira == "3":
                    collection.update_one({"_id": ouser}, {"$set": {"sira": "2"}})
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
                            olinktry += 1
                            sleep(1)
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
                        olinktry += 1
                        sleep(1)
                        if olinktry > 1:
                            logger.warning(f"Tekrar deneniyor {olinktry}")
                    logger.info(f"{okanal} + {olink} + {otoken}")
                except Exception as e:
                    bot.send_message(ouser, "Son postunuz gönderilemedi;\n\n<code>API adresiniz sıkıntılı veya sitenize ulaşılamıyor. API adresinizi kontrol edin, bir sıkıntı yoksa bu mesajı görmezden gelin muhtemelen seçtiğiniz site ile ilgili bir sorun vardır.</code>")
                    logger.error(e)
                    continue
                    
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
                    bot.send_message(-1001190898326, str(ohesap))
                    continue
                for okan in okanal:
                    try:
                        oyetkililer = [oxy.user.id for oxy in bot.get_chat_administrators(okan)]
                    except:
                        oret = False
                        oyetkililer = []
                    if not ouser in oyetkililer and oret:
                        try:
                            omembersayi = bot.get_chat_members_count(okan)
                        except:
                            omembersayi = "Bot kanaldan çıkarılmış."
                        try:
                            logger.debug(f"Hatalı kanal: {okan}")
                            bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {ouser}\nÜYE: {omembersayi}\nKANAL: {okan}")
                            collection.update_one({"_id": ouser}, {"$pull": {"kanal": okan}})
                            continue
                        except:
                            pass
                        else:
                            logger.debug(f"{okan} kayıtlardan silindi.")
                    try:
                        if update.channel_post.photo and oret:
                            opost = bot.send_photo(okan, omedya, caption=osablon)
                        if update.channel_post.video and oret:
                            opost = bot.send_video(okan, omedya, caption=osablon)
                        if update.channel_post.animation and oret:
                            opost = bot.send_animation(okan, omedya, caption=osablon)
                    except Exception as e:
                        if str(e).find("Chat is not found") != -1 or str(e).find("Need administrator") != -1 or str(e).find("bot is not") != -1:
                            try:
                                logger.debug(f"Hatalı kanal: {okan}")
                                bot.send_message(blog, F"#KANAL_SİLİNDİ\nSAHİP: {ouser}\nÜYE: {bot.get_chat_members_count(okan)}\nKANAL: {okan}")
                                collection.update_one({"_id": ouser}, {"$pull": {"kanal": okan}})
                                bot.send_message(ouser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                            except Exception as e: 
                                logger.error(e)
                            else:
                                logger.debug(f"{okan} kayıtlardan silindi.")
                        else:
                            logger.error(e)
                    else:
                        ocount += 1                     
                logger.info("Başarılı!")
        obasari = "[ÖZEL] {} kaynağından {} kanalda post paylaşıldı.".format(okynk.title, ocount)
        if okaynak["log"] != "yok":
            bot.send_message(okaynak["log"], obasari)
        logger.warning(obasari)