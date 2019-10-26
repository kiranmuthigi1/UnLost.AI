# import sys

from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint
# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
print("sdf")
client = MongoClient("mongodb://13.77.127.99/moscow")
db=client.mongo
print("sdfj")
# Issue the serverStatus command and print the results
serverStatusResult=db.command("serverStatus")
print("serverstatus")
print(serverStatusResult)
# sys.stdout.flush()