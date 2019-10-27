from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint
# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
client = MongoClient("mongodb://localhost/moscow")
#print("on way")
db=client.mongo
# Issue the serverStatus command and print the results
serverStatusResult=db.command("serverStatus")
print("serverstatus")
#pprint(serverStatusResult)
db = client.moscow
collection = db.losts
for document in collection.find({"isEncoding": False}):
	print(document)
