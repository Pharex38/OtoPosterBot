import pymongo
from pymongo import MongoClient

cluster = pymongo.MongoClient("os.environ["MONGO_URI"]")
db = cluster["txt"]
collection = db["txt"]

keyler = collection.find({"tgid": f"{user.id}"}).json()
for key in keyler:
    token = key["api"]

print(token)