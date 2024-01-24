from pymongo import MongoClient
from pymongo.read_preferences import ReadPreference
import certifi

conn = "mongodb+srv://kwonshzzang:kkpig1484@cluster0.7rkwg4n.mongodb.net/?retryWrites=true&w=majority&readPreference=secondary"
client = MongoClient(conn, tlsCAFile=certifi.where())
db = client.test

db.fruits.insert_many([
    {
       "name": "melon",
       "qty": 1000,
       "price": 16000 
    },
    {
       "name": "strawberry",
       "qty": 100,
       "price": 10000 
    },
    {
       "name": "grape",
       "qty": 1500,
       "price": 5000 
    }
])

query_filter = {"name": "melon"}
while True:
    res =db.fruits.find_one(query_filter)
   #  res = db.fruits.with_options(read_preference=ReadPreference.SECONDARY).find_one(query_filter)
    print(res)
    