from . import *
from .markups import *
import logging


def deep(u_kod, user):
    kat = collection.find_one({"_id": user})
    key = {"_id": user, "kanal": [], "sablon": "1", "kaynak": ["32"], "site": "1", "altapi": "None", "altsite": "None", "sira": "0", "ozel": True, "time": 0, "vakit": 0, "pcount": 0, "eski": [], "begeni": []}
    if int(u_kod) > 100:
        try:
            ref_kanal_ismi = bot.get_chat(OzelCol.find_one({"_id": int(u_kod)})['okaynak']).title
        except:
            ref_kanal_ismi = "Kanala ulaşılamıyor."
        if kat == None:
            if OzelCol.find_one({"_id": int(u_kod)}) == None:
                bot.send_message(user, "Kaynak silinmiş veya bulunamadı!")
                return False
            for koy in KaynakCol.find({}):
                if user in koy['kaynak']:
                    KaynakCol.update_one({"_id": koy['_id']}, {"$pull": {"kaynak": user}})
            if not user in OzelCol.find_one({"_id": int(u_kod)})['kanal']:
                OzelCol.update_one({"_id": int(u_kod)}, {"$push": {"kanal": user}})
            collection.insert_one(key)
            if len(OzelCol.find_one({"okaynak": kanal})['kanal']) == 6:
                bot.send_message(OzelCol.find_one({"okaynak": kanal})['_id'], "<i>Özel Kaynağınız 5 kişiyi geçtiği için artık 20 linkte 1 olayı sizin için de geçerilidir.</i>")
            bot.send_message(user, "🏋🏻 {} referansı ile geldiniz!".format(ref_kanal_ismi))
            bot.send_message(user, "📝 API adresinizi gönderin.", reply_markup=imark())
            return False
        else:
            if OzelCol.find_one({"_id": int(u_kod)}) == None:
                bot.send_message(user, "Kaynak silinmiş veya bulunamadı!")
                return True
            if user in OzelCol.find_one({"_id": int(u_kod)})['kanal']:
                bot.send_message(user, "Zaten Bu Kaynağı Kullanıyorsunuz!", reply_markup=dugme(user))
                return True
            for koy in KaynakCol.find({}):
                if user in koy['kaynak']:
                    KaynakCol.update_one({"_id": koy['_id']}, {"$pull": {"kaynak": user}})
            collection.update_one({"_id": user}, {"$set": {"ozel": True, "kaynak": ["32"]}})
            if not user in OzelCol.find_one({"_id": int(u_kod)})['kanal']:
                OzelCol.update_one({"_id": int(u_kod)}, {"$push": {"kanal": user}})
            if len(OzelCol.find_one({"_id": int(u_kod)})['kanal']) == 6:
                bot.send_message(OzelCol.find_one({"okaynak": kanal})['_id'], "<i>Özel Kaynağınız 5 kişiyi geçtiği için artık 20 linkte 1 olayı sizin için de geçerilidir.</i>")
            bot.send_message(user, "🏋🏻 {} referansı ile geldiniz!".format(ref_kanal_ismi), reply_markup=dugme(user))
            return True
    key = {"_id": user, "kanal": [], "sablon": "1", "kaynak": [str(u_kod)], "site": "1", "altapi": "None", "altsite": "None", "sira": "0", "ozel": False, "pcount": 0, "time": 0, "vakit": 0}
    if kat == None:
        if KaynakCol.find_one({"no": int(u_kod)}) == None:
            bot.send_message(user, "Kaynak silinmiş veya bulunamadı!")
            return False
        ref_kanal_ismi = bot.get_chat(KaynakCol.find_one({"no": int(u_kod)})['_id']).title
        if OzelCol.find_one({"_id": int(u_kod)}) == None:
                bot.send_message(user, "Kaynak silinmiş veya bulunamadı!")
                return True
        if not user in KaynakCol.find_one({"no": int(u_kod)})['kaynak']:
            KaynakCol.update_one({"no": int(u_kod)}, {"$push": {"kaynak": int(user)}})
        bot.send_message(user, "🏋🏻 {} referansı ile geldiniz!".format(ref_kanal_ismi))
        bot.send_message(user, "📝 API adresinizi gönderin.", reply_markup=imark())
        return False
    else:
        if KaynakCol.find_one({"no": int(u_kod)}) == None:
            bot.send_message(user, "Kaynak silinmiş veya bulunamadı!")
            return True
        ref_kanal_ismi = bot.get_chat(KaynakCol.find_one({"no": int(u_kod)})['_id']).title
        if not kat['ozel']:
            if not user in KaynakCol.find_one({"no": int(u_kod)})['kaynak']:
                KaynakCol.update_one({"no": int(u_kod)}, {"$push": {"kaynak": int(user)}})
            for ktyo in kat['kanal']:
                KaynakCol.update_one({"no":int(u_kod)}, {"$push": {"kanal": ktyo}})
            bot.send_message(user, "Kaynağınız Eklendi!", reply_markup=dugme(user))
        else:
            bot.send_message(user, "Özel kaynağınız olduğu için başka kaynak kullanamazsınız!")
        return True

def send_typing_action(func):

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        return func(update, context,  *args, **kwargs)

    return command_func

def bildir(neyi='Boş Bildirim Testi !'):
    for i in adminlist:
        try:
            bot.send_message(i,neyi)
        except:
            pass

def phaapi(sit):
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
    
def site_isim(no):
    if no == "1":
        return "TRLink"
    if no == "2":
        return "PND.TL"
    if no == "3":
        return "Exe.io"
    if no == "4":
        return "Ouo.io"
    if no == "5":
        return "Pubiza"
    if no == "6":
        return "Gir.ist"

def setup_logger():
    global logger
    aps_logger = logging.getLogger('apscheduler')
    aps_logger.setLevel(logging.WARNING)
    zaman = datetime.datetime.now()
    logd = "{}.{}.{} - {}.{}".format(zaman.year, zaman.month, zaman.day, zaman.hour, zaman.minute)
    logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", handlers=[logging.FileHandler(f'Loglar/{logd}.txt', 'w', 'utf-8'), logging.StreamHandler()], level=logging.INFO)
    logger = logging.getLogger("OtoPosterBot")


def eklentiiletisim(update, context):
    ileti = update.message.text
    if ileti.split("+")[0].isdigit():
        ileti = ileti.split("+")
        bot.send_message(ileti[0], ileti[1])
        return

def comment(update, context):
    if update.edited_message or update.effective_message.text == None:
        return
    if update.message.text.find("kanalda post paylaşıldı.") == -1 and update.message.text.find("paylaşılıyor") == -1:
        return
    bot.delete_message(update.message.chat.id, update.effective_message.message_id)

def error_handler(update: object, context: CallbackContext) -> None:
    try:
        global postsirasi, opostsirasi
        logger.error(msg="Bir Hata oluştu:", exc_info=context.error)
        tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
        tb_string = ''.join(tb_list)
        update_str = update.to_dict() if isinstance(update, Update) else str(update)
        try:
            update.message.chat.id
        except:
            pass
        else:
            if update.message.chat.id in postsirasi:
                for er in postsirasi:
                    if update.message.chat.id == er['chatid']:
                        try:
                            postsirasi.remove(er)
                        except Exception as e:
                            print(e)
            elif update.message.chat.id in opostsirasi:
                for oer in opostsirasi:
                    if update.message.chat.id == oer['chatid']:
                        try:
                            postsirasi.remove(oer)
                        except Exception as e:
                            print(e)
        message1 = (
        f'BİR HATA OLUŞTU!\n'
        f'<pre>update = {html.escape(jason.dumps(update_str, indent=2, ensure_ascii=False))}</pre>')
        message2 = (
        f'<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n'
        f'<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n'
        f'{jason.dumps(collection.find_one({"_id": update.effective_user.id if update.effective_user else 0}))}')
        message3 = (
        f'<pre>{html.escape(tb_string)}</pre>'
        )

        context.bot.send_message(chat_id=sahip, text=message1, parse_mode=ParseMode.HTML)
        context.bot.send_message(chat_id=sahip, text=message2, parse_mode=ParseMode.HTML)
        context.bot.send_message(chat_id=sahip, text=message3, parse_mode=ParseMode.HTML)
    except Exception as es:
        print(es)


setup_logger()
