import datetime
from pprint import pprint

from pymongo import MongoClient
from pymongo import version as pymongo_version
from bson.objectid import ObjectId

from apps.app_util import mongodb, mongoclient, col_coin_spec, col_coin_top, \
    col_coin_hist_daily, col_coin_hist_hour, col_coin_hist_min, \
    mongodb_geo

"""

Kiklearn db:
mongoclient = MongoClient()         # MongoClient('localhost', 27017)
mongodb = mongoclient.kiklearn

for doc in col_kiklearn.find(): pprint(doc)

u = mongodb.user.find_one({'username':'duncan'})

result = mongodb.user.find()
result.count()

for r in result: pprint(r)


pwd_hashed = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt())
pwd_hashed == bcrypt.hashpw(pwd.encode(), pwd_hashed)

pw_hash = bcrypt.generate_password_hash(pwd)
bcrypt.check_password_hash(pw_hash, pwd) # returns True


mongodb.user.update(
  { 'username': 'admin'
  },
  { '$set':
    { 'pwd': pwd_hashed
    }
  },
  upsert=False, multi=False
)


user_jsn = {
  'username': 'duncan',                     # MUST BE UNIQUE
  'email': 'duncan@rivercastcapital.com',   # MUST BE UNIQUE
  'pwd': 'UrU',
  'register_date': new Date(),
  'note': "Droplet Name: Rivercast ssh admin@192.241.219.240",

  'name_first': 'duncan',
  'name_last': 'coker',
  'cty': 'usa',
  'city': 'boulder',
  'state': 'co',
  'zip': '80302',
  'tel': '303.261.8883',
  'addr': '1942 Broadway, Suite 314',
  'addr2': ''
}

mongodb.user.insert(jsn)

--------------------------------------------------------------------------------

{
    "_id" : ObjectId("5500165de50c050005e4b29f"),
    "title" : "Using MongoDB as your primary Django database",
    "message" : "This presentation introduces MongoDB to Django de...",
    "author" : ObjectId("5182953ba50c051575e4b29c"),
    "creation_date" : ISODate("2013-05-21T12:44:31.408Z"),
    "tags" : ["django","python","mongodb","mongoengine","nosql"],
    "comments" : [
        {
            "author" :  ObjectId("50c90b3128650a004200961a"),
            "message" : "Nice, I didn't know this was possible."
        }
    ],

--------------------------------------------------------------------------------

# PUT THIS IN SYSTEM INIT SETUP
# mongodb = client[MONGODB_NAME]  #> use mydb
col_equitycurve = mongodb[COL_EQUITYCURVE]
"""

# ==============================================================================
# Database routines
# ==============================================================================

#from flask.ext.sqlalchemy import Pagination

def check_mongodb():

    result = 'mongo version: ' + mongoclient.server_info()['version'] + '\n'
    result = 'pymongo version: ' + pymongo_version + '\n'
    result = str(mongodb.command("dbstats")) + '\n'

    #result = mongodb.command("collstats", "fintech") + '\n'

    result += "database_names: " + str(mongoclient.database_names()) + "\n" #> show dbs;
    result += "collection_names:" + str(mongodb.collection_names()) + "\n"
    #print("posts" in db.collection_names())
    result += "col_kiklearn.count: " + str(col_coin_hist_daily.count()) + "\n"
    # for doc in col_equitycurve.find(): pprint(doc)
    return result

"""
if __name__ == "__main__":
    print(check_mongodb())
    for doc in col_kiklearn.find(): pprint(doc)
"""
