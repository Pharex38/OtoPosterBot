
import pymongo
from pymongo import MongoClient
from bson.json_util import dumps, loads

cluster = pymongo.MongoClient("mongodb+srv://Pharex:545456@cluster0.teii1.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["txt"]
collection = db["txt"]

cursor = collection.find_one({"_id": 1302980840})
token = cursor['api']

print(cursor)
