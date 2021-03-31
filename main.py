import pymongo
from pymongo import MongoClient

client = pymongo.MongoClient("mongodb+srv://Pharex:545456@cluster0.teii1.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["txt"]
collection = db["txt"]

api = {"_id": 1, "api": "13c86bc3b625bf15995d018810d38737e6e70197"}

collection.insert_one(api)
