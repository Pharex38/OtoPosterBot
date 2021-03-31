import pymongo
from pymongo import MongoClient

cluster = pymongo.MongoClient("os.environ["MONGO_URI"]")
db = cluster["TRLinkShortener"]
collection = db["txt"]

post = {"_id": 1, "name": "sa"}

collection.insert_one(post)
