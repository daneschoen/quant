
"""
utils_geo.py

sudo apt-get install libsqlite3-dev
pip3 install pyzipcode

"""

from pyzipcode import ZipCodeDatabase

def zip_():
  zcdb = ZipCodeDatabase()
  zipcode = zcdb[54115]

"""
>>> zipcode.zip
u'54115'
>>> zipcode.city
u'De Pere'
>>> zipcode.state
u'WI'
>>> zipcode.longitude
-88.078959999999995
>>> zipcode.latitude
44.42042
>>> zipcode.timezone
-6

x = zcdb.find_zip(city="Oshkosh")
len(x)
x[0]



x = [z.zip for z in zcdb.get_zipcodes_around_radius(54901, 50)]
[54901, 54904, 54932, 54952, 54956, 54979]

x = [z.zip for z in zcdb.get_zipcodes_around_radius(10016, 10)]
"""
