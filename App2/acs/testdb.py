import pymongo
from pymongo import MongoClient

MdbURI = "mongodb://a:a123456@ds125381.mlab.com:25381/crawlerdata"
client = MongoClient(MdbURI,connectTimeoutMS=30000)
db = client.get_database("crawlerdata")
mycol = db.Wiley


def getRECORD():
    records = mycol.find_one()
    return records['authors'][0]['country']

def pushRECORD(record):
    mycol.insert_one(record)

def updateRecord(record, updates):
    mucol.update_one({'_id': record['_id']},{
                              '$set': updates
                              }, upsert=False)


record  =  {
    "user_id" : 6,
    "name": "Nikhil",
    "college": "DTU",
    "arr" : ['a','b'],
    "authors" : [
                    {
                        "name":"Card",
                        "test1" : ["a1", "b1" , "b3"],
                        "test 2" : ["a2","b2","c2"]},
                    {
                        "name":"Ken",
                        "test1" : ["a1", "b1" , "b3"],
                        "test 2" : ["a2","b2","c2"]
                    }
                ]
}
# pushRECORD(record)
record = getRECORD()
print(record)
