
from globals import *
import datetime
from pymongo import MongoClient
from pprint import pprint



client = MongoClient()         # MongoClient('localhost', 27017) 
# PUT THIS IN SYSTEM INIT SETUP
mongodb = client[MONGODB_NAME]  #> use mydb
col_equitycurve = mongodb[COL_EQUITYCURVE]


def check_mongodb():
    result = ""
    result += "database_names: " + str(client.database_names()) + "\n" #> show dbs;
    result += "collection_names:" + str(mongodb.collection_names()) + "\n"    
    #print("posts" in db.collection_names())     
    result += "equitycurve.count: " + str(col_equitycurve.count()) + "\n"
    # for doc in col_equitycurve.find(): pprint(doc)
    return result


if __name__ == "__main__":
    print(check_mongodb())
    for doc in col_equitycurve.find(): pprint(doc)


