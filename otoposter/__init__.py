import os
import logging
import datetime, time
from telegram import ParseMode
from pymongo import MongoClient
from telegram.ext import ExtBot, Defaults

mpass = os.environ['MONGOPASS']
mongo = f"os.environ["MONGO_URI"]"

zaman = datetime.datetime.now()
saat = zaman.hour 
dakika = zaman.minute
logd = "{}.{}.{} - {}.{}".format(zaman.year, zaman.month, zaman.day, saat, dakika)

pid = os.getpid()
open("pid.txt", "w").write(str(pid))
print(pid)

cluster = MongoClient(mongo)
db = cluster["OtoPost"]
collection = db["Kanallar"]
OzelCol = db["Özel Kaynaklar"]
karaliste = collection.find_one({"_id": 0})
bottoken = karaliste['bottoken']


bot = ExtBot(bottoken, defaults=Defaults(parse_mode=ParseMode.HTML, run_async=True, timeout=9))

blog = -1001391561285
botlog = -1001352123979
sahip = 1302980840
fixer = 1687646994
adminlist = [1687646994,1302980840]

def setup_logger():
    global logger
    file_handler = logging.FileHandler(f'Loglar/{logd}.txt', 'w', 'utf-8')
    stream_handler = logging.StreamHandler()
    logger = logging.getLogger("main_log")
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

#logger = getLogger(__name__)

setup_logger()
