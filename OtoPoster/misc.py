from . import *
from .markups import *
import logging


 
def deep(u_kod, user):
    kat = collection.find_one({"_id": user})
    key = {"_id": user, "kanal": [], "sablon": "1", "kaynak": ["32"], "site": "1", "altapi": "None", "altsite": "None", "sira": 0, "ozel": True, "time": 0, "vakit": 0, "pcount": 0, "eski": [], "begeni": [], "pin": [], "icerik": []}
    if int(u_kod) > 100:
        ozelkaynak = OzelCol.find_one({"_id": int(u_kod)})
        kanal = ozelkaynak['okaynak']
        try:
            ref_kanal_ismi = bot.get_chat(kanal).title
        except:
            ref_kanal_ismi = "Kanala ulaşılamıyor."
        if kat == None:
            if ozelkaynak == None:
                bot.send_message(user, "Kaynak silinmiş veya bulunamadı!")
                return False
            for koy in KaynakCol.find({}):
                if user in koy['kaynak']:
                    KaynakCol.update_one({"_id": koy['_id']}, {"$pull": {"kaynak": user}})
            if not user in ozelkaynak['kanal']:
                OzelCol.update_one({"_id": int(u_kod)}, {"$push": {"kanal": user}})
            collection.insert_one(key)
            if len(OzelCol.find_one({"okaynak": kanal})['kanal']) == 6:
                try:
                    bot.send_message(OzelCol.find_one({"okaynak": kanal})['_id'], "<i>Özel Kaynağınız 5 kişiyi geçtiği için artık 20 linkte 1 olayı sizin için de geçerilidir.</i>")
                except RetryAfter as rtry:
                    sleep(rtry.retry_after+1)
                    try:
                        bot.send_message(OzelCol.find_one({"okaynak": kanal})['_id'], "<i>Özel Kaynağınız 5 kişiyi geçtiği için artık 20 linkte 1 olayı sizin için de geçerilidir.</i>")
                    except:
                        pass
            bot.send_message(user, "🏋🏻 {} referansı ile geldiniz!".format(ref_kanal_ismi))
            bot.send_message(user, "📝 API adresinizi gönderin.", reply_markup=imark())
            return False
        else:
            if ozelkaynak == None:
                bot.send_message(user, "Kaynak silinmiş veya bulunamadı!")
                return True
            if user in ozelkaynak['kanal']:
                bot.send_message(user, "Zaten Bu Kaynağı Kullanıyorsunuz!", reply_markup=dugme(user))
                return True
            if OzelCol.find_one({"kanal": {"$in": [user]}}) != None:
                bot.send_message(user, "Zaten bir özel kaynak kullanıyorsunuz!", reply_markup=dugme(user))
                return True
            if len(kat['icerik']) == 0 and ozelkaynak['icerik'] == "arsiv":
                bot.send_message(user, "Bu bir Arşiv Kaynak ama sizin hiç arşiv türünde kanalınız yok 😕")
                return True
            collection.update_one({"_id": user}, {"$set": {"ozel": True, "kaynak": ["32"]}})
            if not user in ozelkaynak['kanal']:
                OzelCol.update_one({"_id": int(u_kod)}, {"$push": {"kanal": user}})
            for ktyo in kat['kanal']:
                if ozelkaynak['icerik'] == "arsiv":
                    if ktyo in kat['icerik']:
                        OzelCol.update_one({"_id":int(u_kod)}, {"$push": {"kaynak": ktyo}})
                else:    
                    if not ktyo in kat['icerik']:
                        OzelCol.update_one({"_id":int(u_kod)}, {"$push": {"kaynak": ktyo}})
            if len(ozelkaynak['kanal']) == 6:
                try:
                    bot.send_message(OzelCol.find_one({"okaynak": kanal})['_id'], "<i>Özel Kaynağınız 5 kişiyi geçtiği için artık 20 linkte 1 olayı sizin için de geçerilidir.</i>")
                except RetryAfter as ortf:
                    sleep(ortf.retry_after+1)
                    try:
                        bot.send_message(OzelCol.find_one({"okaynak": kanal})['_id'], "<i>Özel Kaynağınız 5 kişiyi geçtiği için artık 20 linkte 1 olayı sizin için de geçerilidir.</i>")
                    except:
                        pass
            bot.send_message(user, "🏋🏻 {} kaynağına bağlandınız!".format(ref_kanal_ismi), reply_markup=dugme(user))
            return True
    key = {"_id": user, "kanal": [], "sablon": "1", "kaynak": [], "site": "1", "altapi": "None", "altsite": "None", "sira": 0, "ozel": False, "pcount": 0, "time": 0, "vakit": 0, "begeni": [], "pin": [], "eski": [], "icerik": []}
    rkaynak = KaynakCol.find_one({"no": int(u_kod)})
    if kat == None:
        if rkaynak == None:
            bot.send_message(user, "Kaynak silinmiş veya bulunamadı!")
            return False
        ref_kanal_ismi = bot.get_chat(rkaynak['_id']).title
        if not user in rkaynak['kaynak']:
            KaynakCol.update_one({"no": int(u_kod)}, {"$push": {"kaynak": int(user)}})
        bot.send_message(user, "🏋🏻 {} referansı ile geldiniz!".format(ref_kanal_ismi))
        bot.send_message(user, "📝 API adresinizi gönderin.", reply_markup=imark())
        return False
    else:
        if rkaynak == None:
            bot.send_message(user, "Kaynak silinmiş veya bulunamadı!")
            return True
        ref_kanal_ismi = bot.get_chat(rkaynak['_id']).title
        if len(kat['icerik']) == 0 and rkaynak['icerik'] == "arsiv":
            bot.send_message(user, "Bu bir Arşiv Kaynak ama sizin hiç arşiv türünde kanalınız yok 😕")
            return True
        if not user in rkaynak['kaynak']:
            KaynakCol.update_one({"no": int(u_kod)}, {"$push": {"kaynak": int(user)}})
        for ktyo in kat['kanal']:
            if rkaynak['icerik'] == "arsiv":
                if ktyo in kat['icerik']:
                    KaynakCol.update_one({"no":int(u_kod)}, {"$push": {"kanal": ktyo}})
            else:    
                if not ktyo in kat['icerik']:
                    KaynakCol.update_one({"no":int(u_kod)}, {"$push": {"kanal": ktyo}})
        bot.send_message(user, "Kaynağınız Eklendi!")
        return True

def send_typing_action(func):

    @wraps(func)
    async def command_func(update, context, *args, **kwargs):
        await context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        return await func(update, context,  *args, **kwargs)

    return command_func

def linkkisalt(site, token, text, icerik):
    json = {"shortenedUrl": "", "message": "", "status": ""}
    link = " "
    if icerik == "arsiv":
        trlinkcat = 3
        pndcat = 7
        pubizacat = "mainstream"
    else:
        trlinkcat = 1
        pndcat = 6
        pubizacat = "adult"
    if site == "1":
        json = get(f"https://ay.live/api/?", params={'api': token, 'url': text, 'ct': trlinkcat}, headers=headers, timeout=ptimeout).json()
        link = json['shortenedUrl']
    elif site == "2":
        json = get(f"https://www.pnd.tl/api?", params={'api': token, 'url': text, 'category': pndcat}, headers=headers, timeout=ptimeout).json()
        link = json['shortenedUrl']
    elif site == "3":
        json = get(f"https://exe.io/api?", params={'api': token, 'url': text}, headers=headers, timeout=ptimeout).json()
        link = json['shortenedUrl']
    elif site == "4":
        link = get(f"http://ouo.io/api/{token}?", params={'s': text}, headers=headerss, timeout=ptimeout).text
    elif site == "5":
        #link = cscraper.get(f"http://pubiza.com/api.php?token={token}&url={text}&ads_type={pubizacat}").text
        link = get(f"http://pubiza.com/api.php?", params={'token': token, 'url': text, 'ads_type': pubizacat}).text
    elif site == "6":
        json = get("http://gir.ist/api?", params={"api": token, "url": text}, headers=headerss, timeout=ptimeout).json()
        link = json['shortenedUrl']
    elif site == "7":
        json = get("https://urlably.com/api?", params={"api": token, "url": text}, headers=headerss, timeout=ptimeout).json()
        link = json['shortenedUrl']
    elif site == "8":
        json = get("https://api.cuty.io/quick?", params={"token": token, "url": text}, headers=headerss, timeout=ptimeout).json()
        link = json['short_url']
    elif site == "0":
        json = get("https://urlcik.com/api?", params={"api": token, "url": text}, headers=headerss, timeout=ptimeout).json()
        link = json['shortenedUrl']

    return link, json

def AdminCommandHandler(command, callback, *args, **kwargs):
    komutisimleri.append(command)
    return CommandHandler(command, callback, filters=filters.User(sahip))

def apiscraper(apitoken):
    if "ouo" in apitoken:
        apitoken = apitoken.split("/")
        apitoken = apitoken[4][:apitoken[4].find("?")]
    elif "pubiza" in apitoken:
        apitoken = apitoken.split("=")
        apitoken = apitoken[1][:apitoken[1].find("&url")]
    
        
    return apitoken

async def bildir(neyi='Boş Bildirim Testi !'):
    for i in adminlist:
        try:
            await bot.send_message(i,neyi)
        except RetryAfter as rtr:
            sleep(rtr.retry_after+1)
            try:
                await bot.send_message(i,neyi)
            except:
                pass
        except:
            pass

def Deb(msg = None):
    print(f"Debug {sys._getframe().f_back.f_lineno}: {msg if msg is not None else ''}")

def phaapi(sit):
    if sit == "0":
        return "***REMOVED-SHORTENER-KEY***"
    if sit == "1":
        return "***REMOVED-SHORTENER-KEY***"
    if sit == "2":
        return "***REMOVED-SHORTENER-KEY***"
    if sit == "3":
        return "***REMOVED-SHORTENER-KEY***"
    if sit == "4":
        return "***REMOVED-SHORTENER-KEY***"
    if sit == "5":
        return "***REMOVED-SHORTENER-KEY***"
    if sit == "6":
        return "***REMOVED-SHORTENER-KEY***"
    if sit == "7":
        return "***REMOVED-KEY***"

async def FloodControl(komand, *argos, **kwargos):
    try:
        return await komand(*argos, **kwargos)
    except RetryAfter as trf:
        logger.warning(f"FloodWait - {trf.retry_after} - Line: {sys._getframe().f_back.f_lineno}")
        sleep(trf.retry_after+1)
        return await komand(*argos, **kwargos)

def site_isim(no):
    if no == "0":
        return "URLcik"
    elif no == "1":
        return "TRLink"
    elif no == "2":
        return "PND.TL"
    elif no == "3":
        return "Exe.io"
    elif no == "4":
        return "Ouo.io"
    elif no == "5":
        return "Pubiza"
    elif no == "6":
        return "Gir.ist"
    elif no == "7":
        return "URLAbly"
    elif no == "8":
        return "Cuty.io"
    else:
        return "Bulunamadı"

async def kan_mention_html(kanid):
    try:
        kanmh = await bot.get_chat(kanid)
    except RetryAfter as mhafter:
        sleep(mhafter.retry_after)
        try:
            kanmh = await bot.get_chat(kanid)
        except:
            return f"<a href='tg://privatepost?channel={str(kanid)[3:]}&post=9999999'>'Kanala Ulaşılamadı.'</a>"
    except:
        return f"<a href='tg://privatepost?channel={str(kanid)[3:]}&post=9999999'>'Kanala Ulaşılamadı.'</a>"
    return f"<a href='{kanmh.invite_link}'>{kanmh.title}</a>" if kanmh.invite_link else f"<a href='tg://privatepost?channel={str(kanid)[3:]}&post=9999999'>{kanmh.title}</a>"

def setup_logger():
    global logger
    logging.getLogger('apscheduler').setLevel(logging.WARNING)
    logging.getLogger('matplotlib').setLevel(logging.WARNING)
    zaman = datetime.datetime.now()
    logd = "{}.{}.{} - {}.{}".format(zaman.year, zaman.month, zaman.day, zaman.hour, zaman.minute)
    logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", handlers=[logging.FileHandler(f'Loglar/{logd}.txt', 'w', 'utf-8'), logging.StreamHandler()], level=logging.INFO)
    logger = logging.getLogger("OtoPosterBot")

async def eklentiiletisim(update, context):
    ileti = update.message.text_html_urled
    ileti = ileti.split("+")
    if ileti[0] == "ios":
        imsgid = context.dispatcher.user_data[int(ileti[1])]['iosmsgid']
        await bot.edit_message_text("<b>"+str(bot.get_chat(ileti[2]).title)+"</b> "+ileti[3], ileti[1], imsgid)
        return
    elif ileti[0] == "hash":
        try:
            haslink = await bot.get_chat(ileti[1]).invite_link
        except RetryAfter:
            return
        except:
            collection.update_one({"_id":0}, {"$pull": {"istek": str(ileti[1])}})
            
        await bot.send_message(eklenti, f"hash*{haslink}")
    elif ileti[0] == "yetki":
        try:
            await bot.promote_chat_member(ileti[1], eklenti, can_invite_users=True)
        except RetryAfter as rf:
            sleep(rf.retry_after)
            await bot.promote_chat_member(ileti[1], eklenti, can_invite_users=True)
    elif ileti[0] == "link":
        try:
            haslink = await bot.get_chat(ileti[1]).invite_link
        except RetryAfter:
            return
        except:
            collection.update_one({"_id":0}, {"$pull": {"istek": str(ileti[1])}})
            
        await bot.send_message(eklenti, f"istek*{haslink}*{ileti[1]}")
            
        

async def komutisimleristart(_):
    komutisimleris = []
    for komi in komutisimleri:
        komutisimleris.append(BotCommand(komi, komi.capitalize()))
    await bot.set_my_commands(commands=komutisimleris, scope=BotCommandScopeChat(sahip))
    await bot.set_my_commands(commands=komutisimleris, scope=BotCommandScopeChatAdministrators(blog))

async def comment(update, context):
    if update.edited_message or update.effective_message.text == None:
        return
    if update.message.text.find("kanalda post paylaşıldı.") == -1 and update.message.text.find("paylaşılıyor") == -1:
        return
    await bot.delete_message(update.message.chat.id, update.effective_message.message_id)

async def error_handler(update: object, context: CallbackContext) -> None:
    try:
        global postsirasi, opostsirasi
        logger.error(msg="Bir Hata oluştu:", exc_info=context.error)
        tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
        tb_string = ''.join(tb_list)
        if update:
            updateerr = update.effective_user if update.effective_user else update
        else:
            updateerr = None
        update_str = update.to_dict() if isinstance(update, Update) else str(update)
        message1 = (
        f'BİR HATA OLUŞTU!\n'
        f'<pre>update = {html.escape(jason.dumps(update_str, indent=2, ensure_ascii=False))}</pre>')
        message2 = (
        f'<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n'
        f'<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n'
        f'{jason.dumps(collection.find_one({"_id": update.effective_user.id if updateerr else 0}))}')
        message3 = (
        f'<pre>{html.escape(tb_string)}</pre>'
        )

        try:
            await context.bot.send_message(chat_id=sahip, text=message1, parse_mode=ParseMode.HTML)
        except:
            pass
        try:
            await context.bot.send_message(chat_id=sahip, text=message2, parse_mode=ParseMode.HTML)
        except:
            pass
        try:
            await context.bot.send_message(chat_id=sahip, text=message3, parse_mode=ParseMode.HTML)
        except:
            pass
    except Exception as es:
        print(es)


setup_logger()
