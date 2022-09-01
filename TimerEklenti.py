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

app = Client(session_string=app_str, api_id=api_id, api_hash=api_hash, name="app31", in_memory=True)

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
            await sleep(fdd.value+1)
            chatoo = app.join_chat(mesaj[1])
            chato = app.resolve_peer(chatoo.id)
        except Exception as e:
            print(e)
            return
        IstekCol.update_one({"_id": 0}, {"$set": {f"{chatoo.id}.hash": chato.access_hash}})
        chatoo.leave()
    elif mesaj[0] == "istek":
        try:
            app.join_chat(mesaj[1].replace("+", "joinchat/"))
        except errors.FloodWait as fd:
            await sleep(fd.value)
            try:
                app.join_chat(mesaj[1].replace("+", "joinchat/"))
            except:
                pass
        except:
            pass
        app.send_message("OtoPosterBot", f"yetki+{mesaj[2]}")
        
            

logger.info("Bot Başlatıldı!")
app.run()



