

from requests import get, Session
from requests import post as ReqPost
from requests.exceptions import *
from asyncio import sleep
from pymongo import MongoClient
import time, datetime, calendar
from collections import OrderedDict
import threading, pytz, os, asyncio, logging
from ssl import CERT_NONE
from random import choice, randint, shuffle
from telegram import *
from telegram.error import *
from telegram.ext import *
from telegram.request import *
from functools import wraps
from urllib3.exceptions import ReadTimeoutError
from telegram.helpers import *
from telegram.constants import *
import json as jason
import traceback, sys, html
from matplotlib import pyplot

try:
    os.environ['HEROKU']
except:
    import Colorer

pid = open("pid.txt", "w")
pid.write(str(os.getpid()))
pid.close()
print(os.getpid())

mpass = os.environ['MONGOPASS']
mongo = f"os.environ["MONGO_URI"]"


cluster = MongoClient(mongo, tls=True, tlsAllowInvalidCertificates=True)
db = cluster["OtoPost"]
collection = db["Kanallar"]
KaynakCol = db["Kaynaklar"]
OzelCol = db["Özel Kaynaklar"]
ButonCol = db["Butonlar"]
IstekCol = db["İstekler"]

maindata = collection.find_one({"_id": 0})
kara = maindata['kara']
apikara = maindata['apikara']
bottoken = os.environ['BOTTOKEN']
para = maindata['para']
appstr = maindata['appstr']
aid = maindata['aid']
hash = maindata['hash']
ptimeout = maindata['timeout']
begstate = maindata['beg']
mainsiralimit = maindata['mainsira']

bot = ExtBot(bottoken)

eklenti = 1654723447
blog = -1001391561285
botlog = -1001352123979
sahip = 1302980840
fixer = 1687646994
adminlist = [sahip]
postsirasi = []
opostsirasi = []
isteklistesi = []
isteklistesi2 = []
tips = [
    "En fazla 10 kanal ekleyebilirsiniz.",
    "Kaynak menüsünden kendinize özel kaynak oluşturabilirsiniz.",
    "20 linkte 1 olayı Elle Post Paylaş butonu için geçerli değildir.",
    "Oluşturduğunuz özel kaynağı siz de isterseniz başkaları da kullanabilir.",
    "Şablon kısmında Markdown(kalın, italik vs.) kullanabilirsiniz.",
    "Elle Post Paylaşırken post zamanlayabilirsiniz.",
    "Her kanlınıza farklı kaynak seçebilirsiniz."
    ]
ignorejob = ["yedekleme", "istekjob", "gunluk", "resetleme", "arsivanaposter", "ozelposter", "anaposter", "anapostersiralayici", "ozelpostersiralayici", "panelcleaner", "kisitlamakontrol", "istekonaylayici"]
ignorekaynak = [4]


komutisimleri = []

kansillog = "#KANAL_SİLİNDİ\n_ID: <a href='tg://user?id={user}'>{user}</a>\nÜYE: {membersayi}\nKANAL: <a href='tg://privatepost?channel={kan}&post=9999999'>{kan}</a>\n#kan10{kan}\n#id{user}"
yenikanlog ="#YENİ_KANAL\n_ID: <a href='tg://user?id={user}'>{user}</a>\nÜYE: {membersayi}\nKANAL: <a href='tg://privatepost?channel={kan}&post=9999999'>{kan}</a>\n#id{user}\n#kan10{kan}"
yeniuserlog = "#YENİ_KULLANİCİ\n_ID: <a href='tg://user?id={user}'>{user}</a>\nAPI: {token}\n#id{user}\n#api{token}"
istekonaylog = "#İSTEK_ONAYLANDİ\n_ID: <a href='tg://user?id={user}'>{user}</a>\nİSTEK: {istek}\nKANAL: <a href='tg://privatepost?channel={kan}&post=9999999'>{kan}</a>\n#id{user}\n#kan10{kan}"
POSTMENU, APIMENU, KANALMENU, EKSTRAMENU, TSBASLIK, TSPOST, BEGENI, APIDEGISTIR, KANALKAYDET, SABLONA, PANELZAMAN, PANELBUL, PATPOST, POSTZAMAN, PATZAMAN, CALLALT, ALTAPI, OZELBOTLOG, OZELKAYNAK= range(19)
headerss = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
    "Accept-Encoding": "*",
    "Connection": "keep-alive"}
