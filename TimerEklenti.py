import logging, os, datetime, time, asyncio, pytz, threading
from ssl import CERT_NONE
from pymongo import *
from pyrogram import *

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

opb = 1742595887
sahip = 1302980840

mpass = os.environ['MONGOPASS']
mongo = f"os.environ["MONGO_URI"]"
cluster = MongoClient(mongo, tls=True, tlsAllowInvalidCertificates=True)

db = cluster["OtoPost"]
collection = db["Kanallar"]
IstekCol = db["İstekler"]

maindata = collection.find_one({"_id": 0})
api_id = maindata['aid']
api_hash = maindata['hash']
app_str = maindata['appstr']
bottoken = maindata['bottoken']

app = Client(app_str, api_id, api_hash)
pyrobot = Client("pyrobot", bot_token=bottoken, api_id=***REMOVED-API-ID***, api_hash="***REMOVED-API-HASH***")
pyrobot.start()

@app.on_message(filters.bot)
def islem(client, message):
    mesaj = message.text.split("*")
    if mesaj[0] == "ios":
        try:
            chat = app.join_chat(mesaj[2].replace("+", "joinchat/"))
        except:
            chat = app.get_chat(mesaj[2].replace("+", "joinchat/"))
        iosrespond = f"<b>Kanalınızdaki Kısıtlamalar;</b>\n\n"
        if not chat.is_restricted:
            iosrespond = f"<i>Kanalınızda herhangi bir kısıtlama bulunamadı.</i>"
        else:
            for il in list(chat.restrictions):
                iosrespond += f"Platform: {'iOS' if il['platform'] == 'ios' else il['platform']}\nSebep: {il['reason'].upper()}\nKısıtlama: <b>Var</b>"
        return_text = f"ios+{mesaj[1]}+{chat.id}+{iosrespond}"
        message.reply(return_text)
        chat.leave()
    elif mesaj[0] == "hash":
        try:
            chatoo = app.join_chat(mesaj[1])
            chato = app.resolve_peer(chatoo.id)
        except errors.FloodWait as fdd:
            time.sleep(fdd.x+1)
            chatoo = app.join_chat(mesaj[1])
            chato = app.resolve_peer(chatoo.id)
        except Exception as e:
            
            print(e)
            return
        chato.leave()
    elif mesaj[0] == "istek":
        try:
            app.join_chat(mesaj[1].replace("+", "joinchat/"))
        except errors.FloodWait as fd:
            time.sleep(fd.x)
            try:
                app.join_chat(mesaj[1].replace("+", "joinchat/"))
            except:
                pass
        except:
            pass
        app.send_message("OtoPosterBot", f"yetki+{mesaj[2]}")
        
            

def istekonay(client, message):
    wliste = collection.find_one({"_id": 0})['istek']
    chat = str(message.chat.id)
    print("3")
    if chat in wliste:
        print("1")
        try:
            message.chat_join_request.approve()
        except Exception as e:
            if str(e).lower() in ["user_already_participant", "user is deactivated", "user_channels_too_much", "hide_requester_missing"]:
                return
            else:
                logger.exception(e)
                return
            
        if IstekCol.find_one({"_id": 0}).get(chat, None) != None:
            IstekCol.update_one({"_id": 0}, {"$inc": {f"{chat}.count": 1}})
        else:
            IstekCol.update_one({"_id": 0}, {"$set": {f"{chat}": {"user": collection.find_one({"kanal": {"$in": [chat]}}).get('_id', sahip) if collection.find_one({"kanal": {"$in": [chat]}}) != None else sahip, "count": 1, "istekler": []}}})
    else:
        print("2)")
        if IstekCol.find_one({"_id": 0}).get(chat, None) == None:
            IstekCol.update_one({"_id": 0}, {"$set": {f"{chat}": {"user": collection.find_one({"kanal": {"$in": [chat]}}).get('_id', sahip) if collection.find_one({"kanal": {"$in": [chat]}}) != None else sahip, "count": 0, "istekler": []}}})
        if IstekCol.find_one({"_id": 0})[chat].get("istekler", None) == None:
            IstekCol.update_one({"_id": 0}, {"$set": {f"{chat}": {"user": collection.find_one({"kanal": {"$in": [chat]}}).get('_id', sahip) if collection.find_one({"kanal": {"$in": [chat]}}) != None else sahip, "count": 0, "istekler": []}}})
        if not message.from_user.id in IstekCol.find_one({"_id": 0})[chat]['istekler']:
            IstekCol.update_one({"_id": 0}, {"$push": {f"{chat}.istekler": message.from_user.id}})
        if not message.from_user.username in IstekCol.find_one({"_id": 1})['istekler'] or message.from_user.username != None:
            IstekCol.update_one({"_id": 1}, {"$push": {"istekler": message.chat_join_request.from_user.username}})

def thre():
    while True:
        for istekanal in collection.find_one({"_id": 0})["istek"]:
            acchash = IstekCol.find_one({"_id": 0})[istekanal].get('hash', None)
            if acchash == None:
                app.send_message("OtoPosterBot", f"hash+{istekanal}")
                continue
            count = 0
            
            kanaloo = InputPeerChannel(istekanal, access_hash=acchash)
            try:
                istekler = pyrobot.send(raw.functions.messages.GetChatInviteImporters(peer=kanaloo, limit=10000, offset_date=0, offset_user=raw.types.InputPeerEmpty(), requested=True), retries=1, timeout=10.0, sleep_threshold=5.0)
           except FloodWait:
               pass
            except:
                app.send_message("OtoPosterBot", f"link+{istekanal}")
                continue
            for istek in istekler.users:
                time.sleep(0.05)
                try:
                    pyrobot.approve_chat_join_request(istekanal, istek.id)
                except Exception as e:
                    logger.error(e)
                    continue
                else:
                    count += 1
                if count >= limit:
                    break
            
        print("2")
        time.sleep(60)


threading.Thread(target=thre).start()
app.add_handler(handlers.ChatJoinRequestHandler(istekonay))

logger.info("Bot Başlatıldı!")
app.run()



