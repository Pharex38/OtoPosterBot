from requests import get
import pymongo
from pymongo import MongoClient
from bson.json_util import dumps, loads

cluster = pymongo.MongoClient("mongodb+srv://Pharex:545456@cluster0.teii1.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["txt"]
collection = db["txt"]

cursor = collection.find_one({"_id": 1302980840})
token = cursor['api']
print(token)
link = get(f"https://ay.live/api/?api=13c86bc3b625bf15995d018810d38737e6e70197&url=https://www.google.com&alias=&ct=1").json()
mesaj = link['shortenedUrl']

print(mesaj)
