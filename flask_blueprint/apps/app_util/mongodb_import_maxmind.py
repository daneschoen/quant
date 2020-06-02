import os, sys
import datetime
import csv

from bson.objectid import ObjectId

from apps import app
from apps.app_util import mongodb, col_geo_city, col_geo_cnty, col_fx #, mongodb_kik, mongodb_api, logger
from apps.settings.constants import *

# ------------------------------------------------------------------------------


""" maxmind
fname_city = 'GeoLite2-City-Locations-en.csv'
geo_city_dt_dir = 'GeoLite2-City-CSV_20160105'
fname_cnty = 'GeoLite2-Country-Locations-en.csv'
geo_cnty_dt_dir = 'GeoLite2-Country-CSV_20160105'
fname_city_loc = 'worldcitiespop.csv'
fname_city_ip = 'GeoLite2-City-Blocks-IPv6.csv'

fnamepath_city = os.path.join(app.config['APP_PATH'], 'app_geo/data/maxmind/', geo_city_dt_dir, fname_city)
fnamepath_cnty = os.path.join(app.config['APP_PATH'], 'app_geo/data/maxmind/', geo_cnty_dt_dir, fname_cnty)
fnamepath_city_loc  = os.path.join(app.config['APP_PATH'], 'app_geo/data/maxmind/', fname_city_loc)
"""

"""
Run from APP_PATH: ~/fintech/flask_blueprint/

~/APP_PATH$ p3 -m apps.app_util.mongodb_import

# OR

~/APP_PATH$ p3 run_util.py

# OR >>>

from pymongo import MongoClient
mongoclient = MongoClient()  #hostname, port)
mongodb = mongoclient.geo
col_geo_cnty = mongodb.geo_cnty
col_geo_city = mongodb.geo_city

# OR REST

# ------------------------------------------------------------------------------
worldcitiespop.txt | wc -l   3,173,959
Country,City,AccentCity,Region,Population,Latitude,Longitude
----------------------------------
lv,riga beach,Riga Beach,25,,56.9608333,23.75

lv,riga,Riga,25,742570,56.95,24.1

lv,rigas iurmala,Rigas Iurmala,25,,56.9608333,23.75
lv,rigas jormalas pilseta,Rigas Jormalas Pilseta,25,,56.9608333,23.75
lv,rigas jurmala,Rigas Jurmala,25,,56.9608333,23.75
lv,riga-strand,Riga-Strand,25,,56.9608333,23.75
lv,rigas yurmala,Rigas Yurmala,25,,56.9608333,23.75

lv,jurmala,Jurmala,25,54088,56.9608333,23.75
lv,rigas jurmala,Rigas Jurmala,25,,56.9608333,23.75

gb,new york,New York,H7,,53.083333,-.15
hn,new york,New York,16,,14.8,-88.3666667
jm,new york,New York,09,,18.25,-77.1833333
jm,new york,New York,10,,18.1166667,-77.1333333
mx,new york,New York,05,,16.266667,-93.233333
us,little new york,Little New York,AL,,34.3877778,-86.1858333
us,new york,New York,FL,,30.8383333,-87.2008333
us,new york,New York,IA,,40.8516667,-93.2597222
us,new york,New York,KY,,36.9888889,-88.9525000
us,new york mills,New York Mills,MN,,46.5180556,-95.3758333
us,new york,New York,MO,,39.6852778,-93.9266667
us,west new york,West New York,NJ,46010,40.7877778,-74.0147222
us,new york,New York,NM,,35.0586111,-107.5266667
us,east new york,East New York,NY,,40.6666667,-73.8827778

us,new york,New York,NY,8107916,40.7141667,-74.0063889

us,new york mills,New York Mills,NY,,43.1052778,-75.2916667
us,little new york,Little New York,TX,,29.5508333,-97.3063889
us,new york,New York,TX,,32.1677778,-95.6688889

GeoLite2-City-Locations-en.csv   93,330
------------------------------
geoname_id,locale_code,
continent_code*,continent_name*,country_iso_code*,country_name*,
subdivision_1_iso_code,subdivision_1_name*,subdivision_2_iso_code,subdivision_2_name,
city_name,metro_code,time_zone

456172,en,EU,Europe,LV,Latvia,RIX,Riga,,,Riga,,Europe/Riga
459593,en,EU,Europe,LV,Latvia,RIX,Riga,,,Ilguciems,,Europe/Riga

GeoLite2-Country-Locations-en.csv
---------------------------------
geoname_id,locale_code,
continent_code*,continent_name*,country_iso_code*,country_name*
49518,en,AF,Africa,RW,Rwanda
51537,en,AF,Africa,SO,Somalia
69543,en,AS,Asia,YE,Yemen

"""
def get_city(city, cnty):
    with open(fnamepath_city, 'r') as fin:
      fin_csv = csv.reader(fin, delimiter=',')   #, quotechar='|')
      next(fin_csv, None)
      for row in fin_csv:
        if row[-3].lower() == city.lower() and row[4].lower() == cnty:
            print(row)

def check_cnty_missing():
    pass

# 47,980
def check_city_missing_pop():
    cnt=0
    with open(fnamepath_city_loc, 'r', encoding='latin_1') as fin:
      fin_csv = csv.reader(fin, delimiter=',')   #, quotechar='|')
      next(fin_csv, None)
      # for row in islice(fin_csv, 1, None)
      for row in fin_csv:
          if row[4].strip() != "":
            cnt+=1
            if row[1].lower() == 'san francisco':
              print(row)
            if row[1].lower() == 'new york':
              print(row)
            if row[1].lower() == 'san jose':
              print(row)
            if row[1].lower() == 'paris':
              print(row)

    print(cnt)


# 47,980
def check_city():
    cnt=0
    with open(fnamepath_city_loc, 'r', encoding='latin_1') as fin:
      fin_csv = csv.reader(fin, delimiter=',')   #, quotechar='|')
      next(fin_csv, None)
      # for row in islice(fin_csv, 1, None)
      for row in fin_csv:
          if row[4].strip() != "":
            cnt+=1
            if row[1].lower() == 'san francisco':
              print(row)
            if row[1].lower() == 'new york':
              print(row)
            if row[1].lower() == 'san jose':
              print(row)

    print(cnt)


def import_geo_cnty(bl_drop_col_geo_cnty=True):
    if bl_drop_col_geo_cnty:
        col_geo_cnty.remove( { } )

    cnt=0
    with open(fnamepath_cnty, 'r') as fin:
      fin_csv = csv.reader(fin, delimiter=',')   #, quotechar='|')
      next(fin_csv, None)
      # for row in islice(fin_csv, 1, None)
      for row in fin_csv:
          cnt+=1
          print(cnt,row)
          doc = {
            'continent_code': row[2],
            'continent_name': row[3],
            'cnty_code': row[4],
            'cnty_name': row[5]
          }
          col_geo_cnty.insert(doc)


def import_geo_city(bl_dropcol):
    if bl_dropcol:
        col_geo_city.remove( { } )
    with open(fnamepath_city, 'r') as fin:
      fin_csv = csv.reader(fin, delimiter=',')   #, quotechar='|')
      next(fin_csv, None)
      # for row in islice(fin_csv, 1, None)
      for row in fin_csv:
          print(row)
          doc = {
            'continent_code': row[2],
            'continent_name': row[3],
            'cnty_code': row[4],
            'cnty_name': row[5]
          }
          col_geo_city.insert(doc)

# ------------------------------------------------------------------------------

def import_data_alzheimers():
    f_name = "data_alzheimers.csv"

    with open(f_name, 'rb') as csvfile:
        f = csv.reader(csvfile, delimiter=',')   #, quotechar='|')
        for row in f:
            doc = {
             "disease": "alzheimer",
             "rank": row[0],
             "cty": row[1].lower(),
             "rate": row[2]
            }
            #mongodb.demographics.save(doc)
            mongodb.demographics.insert(doc)



if __name__ == '__main__':

    #mongodb = get_mongodb()
    #import_data(mongodb)

    #client = MongoClient()  #hostname, port)
    #mongodb = client['geo_?']
    pass
