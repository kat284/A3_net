import pymongo
from pymongo import MongoClient

client = MongoClient('localhost:27017')

db = client['test_database']
coll = db.test_collection

doc1 = {"user": "16", "pwd": "qwe"}
doc2 = {"user": "15", "pwd": "asd"}
doc3 = {"user": "14", "pwd": "zxc"}

posts = db.posts
post_id1 = posts.insert_one(doc1).inserted_id
post_id2 = posts.insert_one(doc2).inserted_id
post_id3 = posts.insert_one(doc3).inserted_id