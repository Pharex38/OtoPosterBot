from pyrogram import *
import logging, os, datetime, time, asyncio, pytz
from ssl import CERT_NONE
from pymongo import *

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

opb = 1742595887
sahip = 1302980840

mpass = os.environ['MONGOPASS']
mongo = f"os.environ["MONGO_URI"]"
cluster = MongoClient(mongo, ssl_cert_reqs=CERT_NONE)

db = cluster["OtoPost"]
collection = db["Kanallar"]

maindata = collection.find_one({"_id": 0})
api_id = maindata['aid']
api_hash = maindata['hash']
app_str = maindata['appstr']

app = Client(app_str, api_id, api_hash)

@app.on_message(filters.bot)
def islem(client, message):
    mesaj = message.text.split("+")
    if ".me" in message.text:
        try:
            chat = app.join_chat(mesaj[1])
        except:
            chat = app.get_chat(mesaj[1])
        iosrespond = f"<b>Kanalınızdaki Kısıtlamalar;</b>\n\n"
        if len(chat.restrictions) == 0:
            iosrespond = f"<i>Kanalınızda herhangi bir kısıtlama bulunamadı.</i>"
        else:
            for il in list(chat.restrictions):
                iosrespond += f"Platform: {'iOS' if il['platform'] == 'ios' else il['platform']}\nSebep: {il['reason']}"
        return_text = f"{mesaj[0]}+{chat.id}+{iosrespond}"
        message.reply(return_text)
        chat.leave()


logger.info("Bot Başlatıldı!")
app.run()



