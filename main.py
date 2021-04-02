from requests import get
import pymongo
from pymongo import MongoClient
from bson.json_util import dumps, loads

cluster = pymongo.MongoClient("mongodb+srv://Pharex:545456@cluster0.teii1.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["txt"]
collection = db["txt"]

cursor = collection.find_one({"_id": 1302980840})
token = cursor['api']
text = "www.google.com"
link = get(f"https://ay.live/api/?api={token}&url={text}&alias=&ct=1").json()
top = link['shortenedUrl']
print(f"{top}")
