import pymongo
from pymongo import MongoClient

cluster = pymongo.MongoClient("mongodb+srv://Pharex:545456@cluster0.teii1.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["txt"]
collection = db["txt"]

keyler = collection.find({"tgid": 1302980840}).json()
for key in keyler:
    token = key["api"]
    
print(token)
