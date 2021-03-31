import pymongo
from pymongo import MongoClient

client = MongoClient("os.environ["MONGO_URI"]")
db = cluster["txt"]
collection = db["txt"]

api = {"_id": 1, "api": "***REMOVED-SHORTENER-KEY***"}

collection.insert_one(api)
