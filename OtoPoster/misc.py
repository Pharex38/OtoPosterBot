from . import *
from .anafonks import *
from .callbacks import *
from .poster import *
from .komutlar import *
from .jobs import *
from .markups import *
from .main import *
import Colorer, logging


def deep(u_kod, user):
    kat = collection.find_one({"_id": user})
    key = {"_id": user, "kanal": [], "sablon": "1", "kaynak": ["32"], "site": "1", "altapi": "None", "altsite": "None", "sira": "0", "ozel": True, "time": 0, "vakit": 0, "pcount": 0}
    if int(u_kod) > 10:
        ref_kanal_ismi = bot.get_chat(OzelCol.find_one({"_id": int(u_kod)})['okaynak']).title
        if kat == None:
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
    ref_kanal_ismi = bot.get_chat(KaynakCol.find_one({"no": int(u_kod)})['_id']).title
    if kat == None:
        if not user in KaynakCol.find_one({"no": int(u_kod)})['kaynak']:
            KaynakCol.update_one({"no": int(u_kod)}, {"$push": {"kaynak": int(user)}})
        bot.send_message(user, "🏋🏻 {} referansı ile geldiniz!".format(ref_kanal_ismi))
        bot.send_message(user, "📝 API adresinizi gönderin.", reply_markup=imark())
        return False
    else:
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
    if update.edited_message:
        return
    if update.message.text.find("kanalda post paylaşıldı.") == -1 and update.message.text.find("paylaşılıyor") == -1:
        return
    bot.delete_message(update.message.chat.id, update.effective_message.message_id)




setup_logger()