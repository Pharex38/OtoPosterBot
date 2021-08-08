
from requests import get, Session
from os import environ
from time import sleep
from pymongo import MongoClient
import time, datetime
import threading, pytz, os, asyncio, logging
from ssl import CERT_NONE
from random import choice
import Colorer
from telegram import *
from telegram.error import *
from telegram.ext import *
from functools import wraps
from telegram.utils.helpers import *
from telegram.utils.request import Request
from telegram.constants import *
import html
import json as jason
import traceback

pid = os.getpid()
open("pid.txt", "w").write(str(pid))
print(pid)

mpass = os.environ['MONGOPASS']
mongo = f"os.environ["MONGO_URI"]"

cluster = MongoClient(mongo, ssl_cert_reqs=CERT_NONE)
db = cluster["OtoPost"]
collection = db["Kanallar"]
KaynakCol = db["Kaynaklar"]
OzelCol = db["Özel Kaynaklar"]

maindata = collection.find_one({"_id": 0})
kara = maindata['kara']
apikara = maindata['apikara']
bottoken = maindata['bottoken']
para = maindata['para']

reqs = Request(con_pool_size=100, connect_timeout=100, read_timeout=100)
bot = ExtBot(bottoken, request=reqs, defaults=Defaults(parse_mode=ParseMode.HTML, run_async=True, timeout=90, disable_web_page_preview=True, allow_sending_without_reply=True, tzinfo=pytz.timezone('Turkey')))

eklenti = 815899066
blog = -1001391561285
botlog = -1001352123979
sahip = 1302980840
fixer = 1687646994
adminlist = [sahip]
postsirasi = []
opostsirasi = []
tips = [
    "En fazla 10 kanal ekleyebilirsiniz.",
    "Kaynak menüsünden kendinize özel kaynak oluşturabilirsiniz.",
    "20 linkte 1 olayı Elle Post Paylaş butonu için geçerli değildir.",
    "Oluşturduğunuz özel kaynağı siz de isterseniz başkaları da kullanabilir.",
    "Şablon kısmında Markdown(kalın, italik vs.) kullanabilirsiniz.",
    "Elle Post Paylaşırken post zamanlayabilirsiniz.",
    "Her kanlınıza farklı kaynak seçebilirsiniz."
    ]
ignorejob = ["yedekleme", "gunluk", "resetleme", "ozelposter", "anaposter", "anapostersiralayici", "ozelpostersiralayici"]


SEND_MEDIA_TYPES = {"document": bot.send_document, "photo": bot.send_photo, "video": bot.send_video, "animation": bot.send_animation}
POSTMENU, APIMENU, KANALMENU, APIDEGISTIR, KANALKAYDET, SABLONA, PATPOST, POSTZAMAN, PATZAMAN, CALLALT, ALTAPI, OZELBOTLOG, OZELKAYNAK= range(13)
headerss = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
    "Accept-Encoding": "*",
    "Connection": "keep-alive"}
