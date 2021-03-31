import pymongo
from pymongo import MongoClient

cluster = pymongo.MongoClient("os.environ["MONGO_URI"]")
db = cluster["TRLinkShortener"]
collection = db["txt"]

post = {"surname": dea, "name": "sa"}

collection.insert_one(post)
