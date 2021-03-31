import pymongo
from pymongo import MongoClient

cluster = pymongo.MongoClient("mongodb+srv://Pharex:545456@cluster0.teii1.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["TRLinkShortener"]
collection = db["txt"]

post = {"_id": 1, "name": "sa"}

collection.insert_one(post)
