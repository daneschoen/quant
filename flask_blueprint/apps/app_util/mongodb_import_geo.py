import os, sys
import datetime
import csv

from bson.objectid import ObjectId

from apps import app
from apps.app_util import mongodb, col_geo_city, col_geo_cnty, col_fx #, mongodb_kik, mongodb_api, logger
from apps.settings.constants import *


# ------------------------------------------------------------------------------
"""geodatasouce """

mongoimport -d mydb -c things --type csv --file locations.csv --headerline
mongoimport --db users --collection contacts --type csv --headerline --file /opt/backups/contacts.csv

mongoimport -d geo -c geo_cnty --type tsv --file GEODATASOURCE-COUNTRY.TXT --headerline

mongoimport -d geo -c geo_cnty --type tsv --file GEODATASOURCE-COUNTRY.TXT --drop --headerline --fields "code_fips,code_iso,code_tld,country"
mongoimport -d geo -c region --type tsv --file geodatasouce/GEODATASOURCE-REGION.TXT --drop --headerline --fields "region_num,region"

--type <json|csv|tsv>

db.geo_cnty.updateMany( { }, { $rename: { 'CC_FIPS': 'code_fips', 'CC_ISO': 'code_iso', 'TLD': 'code_tld', 'cnty_name': 'country' } } )
db.geo_cnty.find( { CC_ISO: { $exists: true} } )
db.geo_cnty.find( { code_fips: 'CC_FIPS'  } )
db.geo_cnty.deleteOne( { code_fips: 'CC_FIPS'  } )


mongoexport --db mydb --collection traffic --out traffic.json

mongodump -d <database_name> -o <directory_backup>

mongorestore -d <database_name> <directory_backup>



from pymongo import MongoClient
import csv

db_geo = MongoClient().geo
col_geo_cnty = db_geo.geo_cnty


for cnty in col_cnty.find():
    print(cnty['cnty_name'])

lst_cnty = [doc['cnty_name'] for doc in col_cnty.find()]


""" maxmind
geoname_id,locale_code,continent_code,continent_name,country_iso_code,cnty_name
49518,en,AF,Africa,RW,Rwanda
"""
reader = csv.reader(open("maxmind/GeoLite2-Country-CSV_20160105/GeoLite2-Country-Locations-en.csv"))
lst_cnty2=[]
for row in reader:
    #print(row)
    lst_cnty2.append(row[5])

sorted(list(set(lst_cnty) - set(lst_cnty2)))

db.geo_cnty.findOne({"cnty_name" : {$regex : ".*Bahamas.*"}})
db.geo_cnty.findOne({"cnty_name" : {$regex : "Bahamas"}})
db.geo_cnty.findOne({"cnty_name" : /bahamas/i})

db.geo_cnty.updateOne({"_id" : ObjectId("5b141731b7f7564f9a4860ac")},{$set: {cnty_name: "Bahamas"}})
db.geo_cnty.updateOne({"_id" : ObjectId("5b141731b7f7564f9a4860c8")},
  {$set: {id_geoname: 1547376, continent_code:"AS", continent_name:"Asia"}}
)



# ------------------------------------------------------------------------------

""" geonames  """
fname_city = 'cities15000.txt'
fname_cnty = 'countryInfo.txt'
fname_timezone = 'timeZones.txt'

fnamepath_city = os.path.join(app.config['APP_PATH'], 'app_geo/data/geonames/', fname_city)
fnamepath_cnty = os.path.join(app.config['APP_PATH'], 'app_geo/data/geonames/', fname_cnty)
fnamepath_timezone = os.path.join(app.config['APP_PATH'], 'app_geo/data/geonames/', fname_timezone)

CONTINENT = {
'AF' : 'Africa',
'AS' : 'Asia',
'EU' : 'Europe',
'NA' : 'North America',
'OC' : 'Oceania',
'SA' : 'South America',
'AN' : 'Antarctica'
}

"""
Run from APP_PATH: ~/Agape/awork_Flask_Django/kiklearn/flask_blueprint/ :
~/APP_PATH$ python -m apps.app_util.mongodb_import

# OR

~/APP_PATH$ python run_util.py

# OR >>>

from pymongo import MongoClient
mongoclient = MongoClient()  #hostname, port)
mongodb = mongoclient.geo
col_geo_cnty = mongodb.geo_cnty
col_geo_city = mongodb.geo_city

# OR REST

# ------------------------------------------------------------------------------
cities5000.txt

['3428928', 'San José', 'San Jose', 'San Jose,San José', '-27.76979', '-55.7826', 'P', 'PPL', 'AR', '', '14', '54007', '', '', '6452', '', '169', 'America/Argentina/Cordoba', '2015-04-22']
['3837675', 'San Francisco', 'San Francisco', 'San Francisco,San Fransiskas,san fransyskw,sheng fu lang xi si ke,سان فرانسیسکو,聖弗朗西斯科', '-31.42797', '-62.08266', 'P', 'PPLA2', 'AR', '', '05', '', '', '', '59062', '', '118', 'America/Argentina/Cordoba', '2014-03-07']
['6942553', 'Paris', 'Paris', '', '43.2', '-80.38333', 'P', 'PPL', 'CA', '', '08', '', '', '', '11177', '', '255', 'America/Toronto', '2009-06-25']
['3621841', 'San José', 'San Jose', '', '10.95173', '-85.1361', 'P', 'PPL', 'CR', '', '01', '', '', '', '31430', '', '50', 'America/Costa_Rica', '2006-01-17']
['3621849', 'San José', 'San Jose', 'Gorad San-Khaseh,SJO,San Chose,San Chosė,San Jose,San Jose de Costa Rica,San Jose i Costa Rica,San José,San José de Costa Rica,San José i Costa Rica,San Joze,San Jozé,San Jusiy,San Khose,San Khoze,San Xose,San Xosé,San-Joseo,San-Khose,San-Xose,Sanhose,Sanhosē,can hoce,san khwsyh  kwstaryka,san khwzh,san-khose,sana hoje,sana hose,sana hoze,sanhose,sheng he xi,sn hwsh,syana hose,Σαν Χοσέ,Горад Сан-Хасэ,Сан Хозе,Сан Хосе,Сан-Хосе,Սան Խոսե,סאן חוסה,סן חוסה,سان خوزه,سان خوسيه، كوستاريكا,سان خوسې,سان ہوزے,सान होज़े,सान होजे,স্যান হোসে,ਸਾਨ ਹੋਸੇ,சான் ஹொசே,ซันโฮเซ,སན་ཇོ་སེ།,სან-ხოსე,ሳን ሆዜ,サンホセ,聖荷西,산호세', '9.93333', '-84.08333', 'P', 'PPLC', 'CR', '', '08', '', '', '', '335007', '', '1161', 'America/Costa_Rica', '2012-01-18']
['3621911', 'San Francisco', 'San Francisco', '', '9.99299', '-84.12934', 'P', 'PPL', 'CR', '', '04', '', '', '', '55923', '', '1128', 'America/Costa_Rica', '2011-04-19']
['2988507', 'Paris', 'Paris', "Baariis,Bahliz,Gorad Paryzh,Lungsod ng Paris,Lutece,Lutetia,Lutetia Parisorum,Lutèce,PAR,Pa-ri,Paarys,Palika,Paname,Pantruche,Paraeis,Paras,Pari,Paries,Parigge,Pariggi,Parighji,Parigi,Pariis,Pariisi,Pariizu,Pariižu,Parij,Parijs,Paris,Parisi,Parixe,Pariz,Parize,Parizh,Parizh osh,Parizh',Parizo,Parizs,Pariž,Parys,Paryz,Paryzius,Paryż,Paryžius,Paräis,París,Paríž,Parîs,Parĩ,Parī,Parīze,Paříž,Páras,Párizs,Ville-Lumiere,Ville-Lumière,ba li,barys,pairisa,pali,pari,paris,parys,paryzh,perisa,pryz,pyaris,pyarisa,pyrs,Παρίσι,Горад Парыж,Париж,Париж ош,Парижь,Париз,Парис,Паріж,Փարիզ,פאריז,פריז,باريس,پارىژ,پاريس,پاریس,پیرس,ܦܐܪܝܣ,पॅरिस,पेरिस,पैरिस,প্যারিস,ਪੈਰਿਸ,પૅરિસ,பாரிஸ்,పారిస్,ಪ್ಯಾರಿಸ್,പാരിസ്,ปารีส,ཕ་རི།,ပါရီမြို့,პარიზი,ፓሪስ,ប៉ារីស,パリ,巴黎,파리", '48.85341', '2.3488', 'P', 'PPLC', 'FR', '', 'A8', '75', '751', '75056', '2138551', '', '42', 'Europe/Paris', '2015-12-12']
['3692482', 'San José', 'San Jose', 'San Jose,San José', '-6.73813', '-79.8275', 'P', 'PPL', 'PE', '', '14', '1401', '140105', '', '7434', '', '1', 'America/Lima', '2015-12-06']
['1689416', 'San Jose', 'San Jose', 'San Jose', '17.15', '121.6', 'P', 'PPL', 'PH', '', '02', '31', '', '', '5905', '', '65', 'Asia/Manila', '2012-02-01']
['1689448', 'San Jose', 'San Jose', 'San Jose', '15.0333', '120.7833', 'P', 'PPL', 'PH', '', '03', '50', '', '', '7461', '', '13', 'Asia/Manila', '2012-01-17']
['1689498', 'San Jose', 'San Jose', 'Macaagnay,San Jose', '13.35', '123.55', 'P', 'PPL', 'PH', 'PH', '05', '16', '', '', '35768', '', '199', 'Asia/Manila', '2012-01-17']
['1689510', 'San Jose', 'San Jose', 'Pandurucan,SJI,San Jose', '12.35275', '121.06761', 'P', 'PPL', 'PH', '', '41', '40', '', '', '118807', '', '9', 'Asia/Manila', '2012-01-17']
['1689554', 'San Jose', 'San Jose', '', '9.80056', '118.75694', 'P', 'PPL', 'PH', '', '41', '49', '', '', '6079', '', '9', 'Asia/Manila', '2010-08-14']
['1689562', 'San Jose', 'San Jose', 'San Jose', '7.73667', '125.07028', 'P', 'PPL', 'PH', '', '10', '12', '', '', '6345', '', '271', 'Asia/Manila', '2012-02-01']
['1689973', 'San Francisco', 'San Francisco', 'Caysyan,San Francisco', '15.35566', '120.84001', 'P', 'PPL', 'PH', '', '03', '47', '', '', '19570', '', '21', 'Asia/Manila', '2012-12-05']
['1690011', 'San Francisco', 'San Francisco', 'San Francisco', '10.6461', '124.3816', 'P', 'PPLA3', 'PH', '', '07', '21', '1690021', '', '8989', '', '7', 'Asia/Manila', '2011-07-31']
['1690014', 'San Francisco', 'San Francisco', 'San Francisco', '10.16018', '124.31098', 'P', 'PPL', 'PH', '', '07', '11', '', '', '5047', '', '8', 'Asia/Manila', '2012-02-01']
['1690019', 'San Francisco', 'San Francisco', 'San Francisco', '8.53556', '125.95', 'P', 'PPLA3', 'PH', '', '13', '03', '1690024', '', '18542', '', '39', 'Asia/Manila', '2011-07-31']
['3437074', 'San José', 'San Jose', 'San Jose,San Jose de los Arroyos,San José,San José de los Arroyos', '-25.53333', '-56.73333', 'P', 'PPL', 'PY', '', '04', '', '', '', '5117', '', '125', 'America/Asuncion', '2012-01-18']
['3583747', 'San Francisco', 'San Francisco', 'Gotera,San Francisco,San Francisco Gotera', '13.7', '-88.1', 'P', 'PPLA', 'SV', '', '08', '', '', '', '16152', '', '270', 'America/El_Salvador', '2012-01-14']
['4246659', 'Paris', 'Paris', 'Parizh,Peris,Париж,Перис', '39.61115', '-87.69614', 'P', 'PPLA2', 'US', '', 'IL', '045', '', '', '8837', '220', '223', 'America/Chicago', '2011-05-14']
['4303602', 'Paris', 'Paris', 'Paris,Parizh,ba li,parys  kntaky,Париж,Парис,پاریس، کنتاکی,巴黎', '38.2098', '-84.25299', 'P', 'PPLA2', 'US', '', 'KY', '017', '', '', '8553', '257', '258', 'America/New_York', '2011-05-14']
['4647963', 'Paris', 'Paris', 'PHT,Paris,Parizh,parys  tnsy,Париж,Парис,پاریس، تنسی', '36.302', '-88.32671', 'P', 'PPLA2', 'US', '', 'TN', '079', '', '', '10156', '157', '158', 'America/Chicago', '2011-05-14']
['5391959', 'San Francisco', 'San Francisco', "Franciscopolis,Frisco,Gorad San-Francyska,Kapalakiko,Khiu-kim-san,Khiu-kîm-sân,Lungsod ng San Francisco,SF,SFO,San Francisco,San Franciscu,San Francisko,San Fransisco,San Fransiskas,San Fransisko,San Frantzisko,San Phransisko,San-Francisko,San-Fransisko,Sanfrancisko,Sao Francisco,São Francisco,can pirancisko,jiu jin shan,saenpeulansiseuko,saina pharansisako,saina phransisko,san f ran si s ko,san fan shi,san fransskw,san fransyskw,san fransyskۆ,san phransisko,sana phransisako ka'unti,sana phransisko,sanfuranshisuko,sena phransisko,sn prnsysqw,syana phransisko,Σαν Φρανσίσκο,Горад Сан-Францыска,Сан Франсиско,Сан Франциско,Сан-Франциско,Сан-Франціско,Սան Ֆրանցիսկո,סאן פראנציסקא,סן פרנסיסקו,سان فرانسسکو,سان فرانسيسكو,سان فرانسیسکو,سان فرانسیسکۆ,सॅन फ्रान्सिस्को,सैन फ्रांसिस्को,स्यान फ्रान्सिस्को,সান ফ্রান্সিসকো কাউন্টি,সান ফ্রান্সিস্কো,ਸੈਨ ਫਰਾਂਸਿਸਕੋ,சான் பிரான்சிஸ்கோ,శాన్ ఫ్రాన్సిస్కో,സാൻ ഫ്രാൻസിസ്കോ,සැන් ෆ්\u200dරැන්සිස්කෝ,ซานฟรานซิสโก,སན་ཧྥུ་རན་སིས་ཁོ,ဆန်ဖရန်စစ္စကိုမြို့,სან-ფრანცისკო,サンフランシスコ,三藩市,旧金山,舊金山,샌프란시스코", '37.77493', '-122.41942', 'P', 'PPLA2', 'US', '', 'CA', '075', '', '', '805235', '16', '28', 'America/Los_Angeles', '2015-01-18']
['5392171', 'San Jose', 'San Jose', "Fanum Sancti Iosephi,Gorad San-Khaseh,SJC,San Chose,San Chosė,San Jose,San Jose i California,San José,San Khose,San Khoze,San Xose,San Xosé,San-Joseo,San-Khose,Sanhose,Sanhosē,can hoce,sa n jwz,saina hoze,san hwzyh  kalyfwrnya,san ose,san'noze,san-khose,sana hose,sanhose,sena hoje,sena josa,sheng he xi,sn hwzh,sn\u200ckhwzh  kalyfrnya,Σαν Χοσέ,Горад Сан-Хасэ,Сан Хозе,Сан Хосе,Сан-Хосе,Սան Խոսե,סן חוזה,سا ن جوز,سان هوزيه، كاليفورنيا,سن\u200cخوزه، کالیفرنیا,सान होसे,सॅन होजे,सैन होज़े,સેન જોસ,சான் ஹொசே,శాన్ ఓసె,ಸ್ಯಾನ್\u200c ಜೋಸ್\u200c\u200c,แซนโฮเซ,სან-ხოსე,サンノゼ,聖荷西,산호세", '37.33939', '-121.89496', 'P', 'PPLA2', 'US', '', 'CA', '085', '', '', '945942', '26', '23', 'America/Los_Angeles', '2014-02-14']

['588335', 'Tartu', 'Tartu', "Derpt,Dorpat,TAY,Tarbatum,Tartto,Tartu,Terbata,Tērbata,Yur'yev,Yurev,taleutu,taruto~u,trtw,Тарту,טרטו,ტარტუ,タルトゥ,타르투", '58.38062', '26.72509', 'P', 'PPLA', 'EE', '', '18', '0795', '', '', '101092', '', '39', 'Europe/Tallinn', '2013-02-22']
['589580', 'Pärnu', 'Parnu', 'Paernu,Parnawa,Parnu,Pernau,Pernava,Pernavia,Pernov,Piarnu,Pjarnu,Pyaonu,Pyarnu,Pärnu,Pērnava,Пярну,პიარნუ', '58.38588', '24.49711', 'P', 'PPLA', 'EE', '', '11', '0625', '', '', '44192', '', '6', 'Europe/Tallinn', '2010-12-18']
['3201047', 'Dubrovnik', 'Dubrovnik', 'Communitas Ragusina,DBV,Dubrava,Dubrounik,Dubrovacka Republika,Dubrovačka Republika,Dubrovnik,Dubrovnikas,Dubrovník,Dubrownik,Dùbrōvnik,Laus,Pearl of the Adriatic,Ragusa,Repubblica di Ragusa,Republic of Ragusa,Respublica Ragusina,do~uburovuniku,du bu luo fu ni ke,dwbrwbnyq,la perla del Adriatico,la perla del Adriático,Дубровник,Дуброўнік,דוברובניק,ドゥブロヴニク,杜布羅夫尼克', '42.64807', '18.09216', 'P', 'PPLA', 'HR', '', '03', '7577034', '', '', '28428', '', '52', 'Europe/Zagreb', '2015-07-07']
['456172', 'Riga', 'Riga', 'Gorad Ryga,RIX,Reiga,Riga,Rigae,Rige,Rigg-a,Rigo,Riia,Riigaa,Riika,Rija,Riqa,Ryga,Ríga,Ríge,Rīga,li jia,liga,ri ka,riga,rika,ryga,rygh,rygha,ryja,Ρίγα,Горад Рыга,Ригæ,Рига,Ріґа,Ռիգա,ריגה,ריגע,رىگا,ريجا,ريغا,ریگا,रिगा,रीगा,রিগা,ரீகா,รีกา,རི་ག,რიგა,ሪጋ,リガ,里加,리가', '56.946', '24.10589', 'P', 'PPLC', 'LV', '', '25', '', '', '', '742572', '', '6', 'Europe/Riga', '2011-09-24']

countryInfo
['EE', 'EST', '233', 'EN', 'Estonia', 'Tallinn', '45226', '1291170', 'EU', '.ee', 'EUR', 'Euro', '372', '#####', '^(\\d{5})$', 'et,ru', '453733', 'RU,LV', '']
['GB', 'GBR', '826', 'UK', 'United Kingdom', 'London', '244820', '62348447', 'EU', '.uk', 'GBP', 'Pound', '44', '@# #@@|@## #@@|@@# #@@|@@## #@@|@#@ #@@|@@#@ #@@|GIR0AA', '^(([A-Z]\\d{2}[A-Z]{2})|([A-Z]\\d{3}[A-Z]{2})|([A-Z]{2}\\d{2}[A-Z]{2})|([A-Z]{2}\\d{3}[A-Z]{2})|([A-Z]\\d[A-Z]\\d[A-Z]{2})|([A-Z]{2}\\d[A-Z]\\d[A-Z]{2})|(GIR0AA))$', 'en-GB,cy-GB,gd', '2635167', 'IE', '']
['US', 'USA', '840', 'US', 'United States', 'Washington', '9629091', '310232863', 'NA', '.us', 'USD', 'Dollar', '1', '#####-####', '^\\d{5}(-\\d{4})?$', 'en-US,es-US,haw,fr', '6252001', 'CA,MX,CU', '']

['#ISO', 'ISO3', 'ISO-Numeric', 'fips', 'Country', 'Capital', 'Area(in sq km)', 'Population', 'Continent', 'tld', 'CurrencyCode', 'CurrencyName', 'Phone', 'Postal Code Format', 'Postal Code Regex', 'Languages', 'geonameid', 'neighbours', 'EquivalentFipsCode']

"""
def get_city(city, cnty):
    with open(fnamepath_city, 'r') as fin:
      fin_csv = csv.reader(fin, delimiter=',')   #, quotechar='|')
      next(fin_csv, None)
      for row in fin_csv:
        if row[-3].lower() == city.lower() and row[4].lower() == cnty:
            print(row)

import csv
import sys
# csv.field_size_limit(sys.maxsize)
def check_cities():
    with open('cities1000.txt', 'r') as fin:
      fin_csv = csv.reader(fin, delimiter='\t', quoting=csv.QUOTE_NONE)   #, quotechar='|')
      # next(fin_csv, None)
      for row in fin_csv:
          #if row[1].lower() in ['paris','new york','san francisco','san jose'] or \
          #  row[2].lower() in ['paris','new york','san francisco','san jose']:
          if row[2].lower() in ['hvar','dubrovnik','riga','tartu', 'parnu']:
            print(row[1],row[2], row[4],row[5], row[8], row[14], row[17])

          # return  # break


def check_countryinfo():
    row_num=0
    with open('countryInfo.txt', 'r') as fin:
      fin_csv = csv.reader(fin, delimiter='\t')   #, quotechar='|')
      # next(fin_csv, None)
      for row in fin_csv:
          #if row[0].lower() in ['us','gb','ee']:
          if row[0] == '#ISO':
            print(row)
            print(row_num)
            return
          row_num+=1    # 50


# ------------------------------------------------------------------------------
# IMPORT ROUTINES
# ------------------------------------------------------------------------------
"""
geonameid
name              : name of geographical point (utf8) varchar(200)
asciiname         : name of geographical point in plain ascii characters, varchar(200)
alternatenames    : alternatenames, comma separated, ascii names automatically transliterated, convenience attribute from alternatename table, varchar(10000)
latitude          : latitude in decimal degrees (wgs84)
longitude         : longitude in decimal degrees (wgs84)
feature class     : see http://www.geonames.org/export/codes.html, char(1)
feature code      : see http://www.geonames.org/export/codes.html, varchar(10)
country code      : ISO-3166 2-letter country code, 2 characters
cc2               : alternate country codes, comma separated, ISO-3166 2-letter country code, 200 characters
admin1 code       : fipscode (subject to change to iso code), see exceptions below, see file admin1Codes.txt for display names of this code; varchar(20)
admin2 code       : code for the second administrative division, a county in the US, see file admin2Codes.txt; varchar(80)
admin3 code       : code for third level administrative division, varchar(20)
admin4 code       : code for fourth level administrative division, varchar(20)
population        : bigint (8 byte int)
elevation         : in meters, integer
dem               : digital elevation model, srtm3 or gtopo30, average elevation of 3''x3'' (ca 90mx90m) or 30''x30'' (ca 900mx900m) area in meters, integer. srtm processed by cgiar/ciat.
timezone          : the timezone id (see file timeZone.txt) varchar(40)
modification date : date of last modification in yyyy-MM-dd format
"""
def import_cnty(bl_drop_col=True):
    if bl_drop_col:
        col_geo_cnty.remove( { } )

    BEG_ROW = 51
    row_num=0
    cnt=0
    with open(fnamepath_cnty, 'r') as fin:
      fin_csv = csv.reader(fin, delimiter='\t')   #, quotechar='|')

      for row in range(BEG_ROW):
          next(fin_csv, None)
          row_num+=1

      """
      ['#ISO', 'ISO3', 'ISO-Numeric', 'fips', 'Country', 'Capital', 'Area(in sq km)',
       7: 'Population', 'Continent', 'tld', 'CurrencyCode', 'CurrencyName',
       12: 'Phone', 'Postal Code Format', 'Postal Code Regex', 'Languages', 'geonameid',
       17: 'neighbours', 'EquivalentFipsCode']
      AD      AND     020     AN      Andorra Andorra la Vella        468     84000   EU      .ad     EUR   Euro ...
      ['EE', 'EST', '233', 'EN', 'Estonia', 'Tallinn', '45226', '1291170', 'EU', '.ee', 'EUR', 'Euro', '372', '#####', '^(\\d{5})$', 'et,ru', '453733', 'RU,LV', '']
      ['GB', 'GBR', '826', 'UK', 'United Kingdom', 'London', '244820', '62348447', 'EU', '.uk', 'GBP', 'Pound', '44', '@# #@@|@## #@@|@@# #@@|@@## #@@|@#@ #@@|@@#@ #@@|GIR0AA', '^(([A-Z]\\d{2}[A-Z]{2})|([A-Z]\\d{3}[A-Z]{2})|([A-Z]{2}\\d{2}[A-Z]{2})|([A-Z]{2}\\d{3}[A-Z]{2})|([A-Z]\\d[A-Z]\\d[A-Z]{2})|([A-Z]{2}\\d[A-Z]\\d[A-Z]{2})|(GIR0AA))$', 'en-GB,cy-GB,gd', '2635167', 'IE', '']
      ['US', 'USA', '840', 'US', 'United States', 'Washington', '9629091', '310232863', 'NA', '.us', 'USD', 'Dollar', '1', '#####-####', '^\\d{5}(-\\d{4})?$', 'en-US,es-US,haw,fr', '6252001', 'CA,MX,CU', '']
      """
      print(row_num, ' <= starting at')
      for row in fin_csv:
          cnt+=1
          print(cnt,row)
          doc = {
            'cnty_code': row[0],
            'cnty_code3': row[1],
            'cnty_name': row[4],
            'cnty_capital': row[5],
            'cnty_area': row[6],
            'cnty_population': row[7],
            'continent_code': row[8],
            'continent_name': CONTINENT[row[8]],
            'cnty_tld': row[9],
            'ccy_code': row[10],
            'ccy_name': row[11],
            'cnty_phone_code': row[12],
            'cnty_postal_format': row[13],
            'cnty_postal_regex': row[14],
            'cnty_language_lst': row[15].split(','),
            'cnty_neighbor_lst': row[17].split(',')
          }
          col_geo_cnty.insert(doc)


def import_city(bl_drop_col=True):
    if bl_drop_col:
        col_geo_city.remove( { } )

    cnt=0
    with open(fnamepath_city, 'r') as fin:
      fin_csv = csv.reader(fin, delimiter='\t', quoting=csv.QUOTE_NONE)
      # next(fin_csv, None)
      # for row in islice(fin_csv, 1, None)
      for row in fin_csv:
          #print(row)
          cnt+=1
          doc = {
            'city_name': row[1],
            'city_name_ascii': row[2],

            'loc':{
              'type': 'Point',
              'coordinates': [row[5],row[4]]  # longitude, latitude
            },
            'cnty_code': row[8],
            ###'cnty_name':
            'city_population': row[14],
            'city_elevation': row[15],
            'city_dem': row[16],
            'city_timezone_name': row[17],
            ###'city_timezone':
          }
          col_geo_city.insert(doc)
    print('Inserted: ', cnt)

# ------------------------------------------------------------------------------
# UPDATE ROUTINES
# ------------------------------------------------------------------------------
# Update city: timezone, cnty_name
def update_city():


    cnt=0
    with open(fnamepath_timezone, 'r') as fin:
      fin_csv = csv.reader(fin, delimiter='\t')  #, quoting=csv.QUOTE_NONE)
      # next(fin_csv, None)
      # for row in islice(fin_csv, 1, None)
      for row in fin_csv:
          #print(row)
          cnt+=1
          doc = {
            'city_name': row[1],
            'city_name_ascii': row[2],

            'loc':{
              'type': 'Point',
              'coordinates': [row[5],row[4]]  # longitude, latitude
            },
            'cnty_code': row[8],
            ###'cnty_name':
            'city_population': row[14],
            'city_elevation': row[15],
            'city_dem': row[16],
            'city_timezone_name': row[17],
            ###'city_timezone':
          }
          col_geo_city.insert(doc)

    cnt=0
    for doc in col_geo_city.find():
        # print(doc.cnty_code, doc.city_name)
        doc['cnty_name'] = ''
        doc['city_timezone_utc'] = ''
        doc['city_timezone_dst'] = ''
        doc['city_timezone_dst_start'] = ''
        doc['city_timezone_dst_end'] = ''
        col_post.update(
          { '_id': r._id
          },
          doc,
          upsert=False, multi=False
        )

        cnt+=1

    print('Updated: ', cnt)


# ------------------------------------------------------------------------------

if __name__ == '__main__':

    #mongodb = get_mongodb()
    #import_data(mongodb)

    #client = MongoClient()  #hostname, port)
    #mongodb = client['geo_?']

    import_cnty()
