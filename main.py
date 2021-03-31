import pymongo
from pymongo import MongoClient

cluster = pymongo.MongoClient("mongodb+srv://pha38:878789@cluster0.teii1.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["TRLinkShortener"]
collection = db["txt"]

post = {"surname": dea, "name": "sa"}

collection.insert_one(post)
