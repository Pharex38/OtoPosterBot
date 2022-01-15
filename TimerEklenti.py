from pyrogram import *
import logging, os, datetime, time, asyncio, pytz, threading
from ssl import CERT_NONE
from pymongo import *

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

opb = 1742595887
sahip = 1302980840

mpass = os.environ['MONGOPASS']
mongo = f"os.environ["MONGO_URI"]"
cluster = MongoClient(mongo, tls=True, tlsAllowInvalidCertificates=True)

db = cluster["OtoPost"]
collection = db["Kanallar"]

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
    if ".me" in message.text:
        try:
            chat = app.join_chat(mesaj[1].replace("+", "joinchat/"))
        except:
            chat = app.get_chat(mesaj[1].replace("+", "joinchat/"))
        iosrespond = f"<b>Kanalınızdaki Kısıtlamalar;</b>\n\n"
        if not chat.is_restricted:
            iosrespond = f"<i>Kanalınızda herhangi bir kısıtlama bulunamadı.</i>"
        else:
            for il in list(chat.restrictions):
                iosrespond += f"Platform: {'iOS' if il['platform'] == 'ios' else il['platform']}\nSebep: {il['reason'].upper()}\nKısıtlama: <b>Var</b>"
        return_text = f"{mesaj[0]}+{chat.id}+{iosrespond}"
        message.reply(return_text)
        chat.leave()


def thre():
    for istekanal in collection.find_one({"_id": 0})["istek"]:
        count = 0
        try:
            kanaloo = InputPeerChannel(istekanal, acces_hash=0)
        istekler = pyrobot.send(pyrogram.raw.functions.messages.GetChatInviteImporters(peer=kanaloo, limit=10000, offset_date=0, offset_user=pyrogram.raw.types.InputPeerEmpty(), requested=True), retries=1, timeout=10.0, sleep_threshold=5.0)
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
    time.sleep(30)


threading.Thread(target=thre).start()


logger.info("Bot Başlatıldı!")
app.run()



