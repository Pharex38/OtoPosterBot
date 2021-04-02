from requests import get
import pymongo
from pymongo import MongoClient
from bson.json_util import dumps, loads

cluster = pymongo.MongoClient("os.environ["MONGO_URI"]")
db = cluster["txt"]
collection = db["txt"]

cursor = collection.find_one({"_id": 1302980840})
token = cursor['api']
print(token)
link = get(f"https://ay.live/api/?api=***REMOVED-SHORTENER-KEY***&url=https://www.google.com&alias=&ct=1").json()
mesaj = link['shortenedUrl']

print(mesaj)
