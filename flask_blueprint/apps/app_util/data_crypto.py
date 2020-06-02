import os
import datetime
import json
from pprint import pprint
import pprint
import requests

from apps.settings.constants import *


URL_COINLIST = "https://www.cryptocompare.com/api/data/coinlist/"

# "PROJ_ROOT/projects/fintech/data_symbol/cryptocurrencies.json"
FILE_CRYPTO_SYMBOL = "cryptocurrencies.json"
FILE_CRYPTO_NAME = "cryptocurrencies_name.json"
PATH_CRYPTO_SYMBOL = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..', 'apps/settings'))
PATH_FILE_CRYPTO_SYMBOL = os.path.join(PATH_CRYPTO_SYMBOL, FILE_CRYPTO_SYMBOL)
PATH_FILE_CRYPTO_NAME = os.path.join(PATH_CRYPTO_SYMBOL, FILE_CRYPTO_NAME)

FILE_TOP_COINLIST = "coinlist_top.json"
PATH_FILE_TOP_COINLIST = os.path.join(PATH_CRYPTO_SYMBOL, FILE_TOP_COINLIST)

TOP_COINLIST_100_STR  = 'BTC,ETH,XRP,BCH,LTC,EOS,ADA,XLM,TRX,NEO,IOT,XMR,VEN,DASH,BNB,XEM,ETC,QTUM,XVG,LSK,HT,ICX,BTM*,BTG,ZEC,XRB,IOST,SNT,ZRX,ZIL,NAS,DGD,WAVES,ORME,LINK,STORJ,POWR,BAT,NCASH,STORM,GNX,SALT,HSR,SUB,MTL,KNC,CVC,GNT,MANA,GTO,MTX,ELF,SRN,REQ,SYS,MDS,BLZ,EDO,RDN*,NEBL,ABT,THETA,DTA,RCN,ENJ,ITC,RUFF,OCN,GTC,POA,CMT*,SWFTC,PRO,GVT,NULS,TNT,WPR,INS,MTN*,ADX,SOC,RPX,QUN,TRIG,MEE,SNC,OC,WAN,ACT*,ETHOS,OMG,ELA,AION,ONT,STRAT,PAY,WAX,GAS,MCO,QSP'
TOP_COINLIST_1_50_STR = 'BTC,ETH,XRP,BCH,LTC,EOS,ADA,XLM,TRX,NEO,IOT,XMR,VEN,DASH,BNB,XEM,ETC,QTUM,XVG,LSK,HT,ICX,BTM*,BTG,ZEC,XRB,IOST,SNT,ZRX,ZIL,NAS,DGD,WAVES,ORME,LINK,STORJ,POWR,BAT,NCASH,STORM,GNX,SALT,HSR,SUB,MTL,KNC,CVC,GNT,MANA,GTO'
TOP_COINLIST_51_100_STR = 'MTX,ELF,SRN,REQ,SYS,MDS,BLZ,EDO,RDN*,NEBL,ABT,THETA,DTA,RCN,ENJ,ITC,RUFF,OCN,GTC,POA,CMT*,SWFTC,PRO,GVT,NULS,TNT,WPR,INS,MTN*,ADX,SOC,RPX,QUN,TRIG,MEE,SNC,OC,WAN,ACT*,ETHOS,OMG,ELA,AION,ONT,STRAT,PAY,WAX,GAS,MCO,QSP'

PATH_FILE_CRYPTO_NOW = "/srv/static/data/crypto_now_.json"


"""
https://developers.coinbase.com/api/v2#introduction
"""
API_DATA_COINDESK = "http://api.coindesk.com/v1/bpi/"
API_DATA_COINDESK_NOW = "{}currentprice.json".format(API_DATA_COINDESK)
API_DATA_COINDESK_HIST = ""

"""
https://api.coinmarketcap.com/v1/ticker/ethereum/
"""
API_DATA_COINMARKETCAP = "http://api.coindesk.com/v1/bpi/"
API_DATA_COINMARKETCAP_NOW = "{}currentprice.json".format(API_DATA_COINMARKETCAP)
API_DATA_COINMARKETCAP_HIST = ""

"""
"""
API_DATA_POLONIEX = ""
API_DATA_POLONIEX_NOW = "{}".format(API_DATA_POLONIEX)
API_DATA_POLONIEX_HIST = ""

"""
https://www.cryptocompare.com/api
https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,EUR,GBP,JPY,KRW
https://min-api.cryptocompare.com/data/pricemulti?fsyms=BTC,ETH&tsyms=USD,EUR,GPB,JPY,KRW
https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,ETH&tsyms=USD,EUR,GPB,JPY,KRW
https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,ETH,XRP,BCH,LTC,EOS,ADA,XLM,TRX,NEO,IOT,XMR,VEN,DASH,BNB,XEM,ETC,QTUM,XVG,LSK,HT,ICX,BTM*,BTG,ZEC,XRB,IOST,SNT,ZRX,ZIL,NAS,DGD,WAVES,ORME,LINK,STORJ,POWR,BAT,NCASH,STORM,GNX,SALT,HSR,SUB,MTL,KNC,CVC,GNT,MANA,GTO&tsyms=USD,EUR,GPB,JPY,KRW
"""
API_DATA_CRYPTOCOMPARE = "https://min-api.cryptocompare.com/data/"
#API_DATA_CRYPTOCOMPARE_NOW = "{}price?fsym=BTC&tsyms=USD,JPY,EUR,KRW".format(API_DATA_CRYPTOCOMPARE)
API_DATA_CRYPTOCOMPARE_ONLY_1_50_NOW   = "{}pricemulti?fsyms={}&tsyms=USD,EUR,GBP,JPY,KRW".format(API_DATA_CRYPTOCOMPARE, TOP_COINLIST_1_50_STR)
API_DATA_CRYPTOCOMPARE_ONLY_51_100_NOW = "{}pricemulti?fsyms={}&tsyms=USD,EUR,GBP,JPY,KRW".format(API_DATA_CRYPTOCOMPARE, TOP_COINLIST_51_100_STR)
API_DATA_CRYPTOCOMPARE_FULL_1_50_NOW   = "{}pricemultifull?fsyms={}&tsyms=USD,EUR,GBP,JPY,KRW".format(API_DATA_CRYPTOCOMPARE, TOP_COINLIST_1_50_STR)
API_DATA_CRYPTOCOMPARE_FULL_51_100_NOW = "{}pricemultifull?fsyms={}&tsyms=USD,EUR,GBP,JPY,KRW".format(API_DATA_CRYPTOCOMPARE, TOP_COINLIST_51_100_STR)
API_DATA_CRYPTOCOMPARE_HIST = ""


"""
# https://min-api.cryptocompare.com/data/pricemulti?fsyms=BTC,ETH&tsyms=USD,EUR
{"BTC":{"USD":8115.76,"EUR":6585.38},"ETH":{"USD":514.09,"EUR":417.51}}

# https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC&tsyms=USD,EUR
{
  "RAW":{"BTC":
    {"USD":
       {"TYPE":"5","MARKET":"CCCAGG","FROMSYMBOL":"BTC","TOSYMBOL":"USD","FLAGS":"4","PRICE":8085.55,"LASTUPDATE":1523629709,"LASTVOLUME":0.02,"LASTVOLUMETO":161.314,"LASTTRADEID":"226357770","VOLUMEDAY":94594.57410224268,"VOLUMEDAYTO":761447477.1666741,"VOLUME24HOUR":149090.38508229656,"VOLUME24HOURTO":1185397516.414891,"OPENDAY":7927.73,"HIGHDAY":8237.16,"LOWDAY":7758.8,"OPEN24HOUR":7667.28,"HIGH24HOUR":8248.06,"LOW24HOUR":7591.15,"LASTMARKET":"Bitfinex","CHANGE24HOUR":418.27000000000044,"CHANGEP CT24HOUR":5.455259231435404,"CHANGEDAY":157.82000000000062,"CHANGEPCTDAY":1.9907337913879588,"SUPPLY":16968900,"MKTCAP":137202889395,"TOTALVOLUME24H":644612.9629005137,"TOTALVOLUME24HTO":5191970095.492976},
     "EUR":
       {"TYPE":"5","MARKET":"CCCAGG","FROMSYMBOL":"BTC","TOSYMBOL":"EUR","FLAGS":"4","PRICE":6561.99,"LASTUPDATE":1523629699,"LASTVOLUME":0.5,"LASTVOLUMETO":3277.55,"LASTTRADEID":"1523629699.2818","VOLUMEDAY":15085.222322352205,"VOLUMEDAYTO":98561866.9151552,"VOLUME24HOUR":23429.425383179976,"VOLUME24HOURTO":150905252.32781532,"OPENDAY":6421.46,"HIGHDAY":6690.9,"LOWDAY":6294.86,"OPEN24HOUR":6212.78,"HIGH24HOUR":6695.57,"LOW24HOUR":6132.35,"LASTMARKET":"Kraken","CHANGE24HOUR":349.21000000000004,"CHANGEPCT24HOUR":5.620833185788006,"CHANGEDAY":140.52999999999975,"CHANGEPCTDAY":2.188443126640978,"SUPPLY":16968900,"MKTCAP":111349752111,"TOTALVOLUME24H":644612.9629005137,"TOTALVOLUME24HTO":4227105413.6811833}}},
  "DISPLAY":{"BTC":{
    "USD":
      {"FROMSYMBOL":"Ƀ","TOSYMBOL":"$","MARKET":"CryptoCompare Index","PRICE":"$ 8,085.55",
       "LASTUPDATE":"Just now","LASTVOLUME":"Ƀ 0.02000","LASTVOLUMETO":"$ 161.31","LASTTRADEID":"226357770",
       "VOLUMEDAY":"Ƀ 94,594.6","VOLUMEDAYTO":"$ 761,447,477.2","VOLUME24HOUR":"Ƀ 149,090.4",
       "VOLUME24HOURTO":"$ 1,185,397,516.4","OPENDAY":"$ 7,927.73","HIGHDAY":"$ 8,237.16",
       "LOWDAY":"$ 7,758.80","OPEN24HOUR":"$ 7,667.28","HIGH24HOUR":"$ 8,248.06","LOW24HOUR":
       "$7,591.15","LASTMARKET":"Bitfinex","CHANGE24HOUR":"$ 418.27","CHANGEPCT24HOUR":"5.46",
       "CHANGEDAY":"$ 157.82","CHANGEPCTDAY":"1.99","SUPPLY":"Ƀ 16,968,900.0",
       "MKTCAP":"$ 137.20 B","TOTALVOLUME24H":"Ƀ 644.61 K","TOTALVOLUME24HTO":"$ 5,191.97 M"
      },
    "EUR":
      {"FROMSYMBOL":"Ƀ","TOSYMBOL":"€","MARKET":"CryptoCompare Index","PRICE":"€ 6,561.99","LASTUPDATE":"Just now","LASTVOLUME":"Ƀ 0.5000","LASTVOLUMETO":"€ 3,277.55","LASTTRADEID":"1523629699.2818","VOLUMEDAY":"Ƀ 15,085.2","VOLUMEDAYTO":"€ 98,561,866.9","VOLUME24HOUR":"Ƀ 23,429.4","VOLUME24HOURTO":"€ 150,905,252.3","OPENDAY":"€ 6,421.46","HIGHDAY":"€ 6,690.90","LOWDAY":"€ 6,294.86","OPEN24HOUR":"€ 6,212.78","HIGH24HOUR":"€ 6,695.57","LOW24HOUR":
       "€6,132.35","LASTMARKET":"Kraken","CHANGE24HOUR":"€ 349.21","CHANGEPCT24HOUR":"5.62","CHANGEDAY":"€ 140.53","CHANGEPCTDAY":"2.19","SUPPLY":"Ƀ 16,968,900.0","MKTCAP":"€ 111.35 B","TOTALVOLUME24H":"Ƀ 644.61 K","TOTALVOLUME24HTO":"€ 4,227.11 M"
      }
    }}
}



COINDESK:
---------
print(json.dumps(price_now_response, sort_keys=True, indent=2))
{
  "bpi": {
    "EUR": {
      "code": "EUR",
      "description": "Euro",
      "rate": "5,778.7376",
      "rate_float": 5778.7376,
      "symbol": "&euro;"
    },
    "GBP": {
      "code": "GBP",
      "description": "British Pound Sterling",
      "rate": "5,031.8957",
      "rate_float": 5031.8957,
      "symbol": "&pound;"
    },
    "USD": {
      "code": "USD",
      "description": "United States Dollar",
      "rate": "7,093.3913",
      "rate_float": 7093.3913,
      "symbol": "&#36;"
    }
  },
  "chartName": "Bitcoin",
  "disclaimer": "This data was produced from the CoinDesk Bitcoin Price Index (USD). Non-USD currency data converted using hourly conversion rate from openexchangerates.org",
  "time": {
    "updated": "Apr 9, 2018 01:32:00 UTC",
    "updatedISO": "2018-04-09T01:32:00+00:00",
    "updateduk": "Apr 9, 2018 at 02:32 BST"
  }
}



COINMARKETCAP:
--------------
[
    {
        "id": "ethereum",
        "name": "Ethereum",
        "symbol": "ETH",
        "rank": "2",
        "price_usd": "411.476",
        "price_btc": "0.0578533",
        "24h_volume_usd": "1019390000.0",
        "market_cap_usd": "40613709337.0",
        "available_supply": "98702499.0",
        "total_supply": "98702499.0",
        "max_supply": null,
        "percent_change_1h": "0.94",
        "percent_change_24h": "6.32",
        "percent_change_7d": "7.44",
        "last_updated": "1523238554"
    }
]


"""

DATE_FORMAT = '%Y-%m-%d'


# ------------------------------------------------------------------------------
# symbol name list
# ------------------------------------------------------------------------------
def load_crypto_symbol():
    with open(PATH_FILE_CRYPTO_SYMBOL, 'r') as f:
        d_crypto_symbol = json.load(f)
        return d_crypto_symbol

def load_crypto_name():
    with open(PATH_FILE_CRYPTO_NAME, 'r') as f:
        d_crypto_name = json.load(f)
        return d_crypto_name

def load_top_coinlist():
    with open(PATH_FILE_TOP_COINLIST, 'r') as f:
        top_coinlist = json.load(f)
        return top_coinlist

def gen_top_coinlist_str():
    s100 = ""
    s1_50 = ""
    s51_100 = ""
    top_coinlist = load_top_coinlist()
    cnt=1
    for t in top_coinlist:
        s100 = s100 + t[1] + ","
        if cnt <= 50:
            s1_50 = s1_50 + t[1] + ","
        else:
            s51_100 = s51_100 + t[1] + ","
        cnt+=1
    s100 = s100[:-1]
    s1_50 = s1_50[:-1]
    s51_100 = s51_100[:-1]
    return s100, s1_50, s51_100


def invert_crypto_symbol():
    '''
    list(d_crypto_symbol.keys())[list(d_crypto_symbol.values()).index("Bitcoin")]
    crypto_sym = [k for k,v in d_crypto_symbol.items() if v.lower() == "bitcoin"][0]
    '''
    d_crypto_symbol = load_crypto_symbol()

    d_crypto_name = {v:k for k, v in d_crypto_symbol.items()}
    return d_crypto_name


def get_crypto_list():
    pass



# ------------------------------------------------------------------------------
# get price now
# ------------------------------------------------------------------------------

def get_crypto_live_():
    return get_crypto_live_full()


def get_crypto_live_full():
    d_crypto_live_ = get_crypto_live_full_cryptocompare()
    nwutc = datetime.datetime.utcnow()
    d_crypto_live_['timestamp'] = nwutc.strftime("%B %d, %Y  %I:%M %p UTC")   # strftime("%Y-%m-%d %H:%M:%S")
    return d_crypto_live_


def get_crypto_now_only_live(bl_save=False):
    d_crypto_now = get_crypto_now_cryptocompare()
    nwutc = datetime.datetime.utcnow()
    d_crypto_now['timestamp'] = nwutc.strftime("%B %d, %Y  %I:%M %p UTC")   # strftime("%Y-%m-%d %H:%M:%S")

    if bl_save is False:
        return d_crypto_now

    with open(PATH_FILE_CRYPTO_NOW, 'w') as out:
        #res = json.dumps(d, sort_keys=True, indent=4, separators=(',', ': '))
        jsn = json.dumps(d_crypto_now)
        out.write(jsn)


def get_crypto_now_full_mongo():
    pass


def get_crypto_live_only_cryptocompare():
    # api_data_cryptocompare_now = API_DATA_CRYPTOCOMPARE_1_50_NOW
    price_1_50_now_resp = requests.get(API_DATA_CRYPTOCOMPARE_ONLY_1_50_NOW).json()
    price_51_100_now_resp = requests.get(API_DATA_CRYPTOCOMPARE_ONLY_51_100_NOW).json()
    price_100_now = {**price_1_50_now_resp , **price_51_100_now_resp}
    return price_100_now


def get_crypto_live_full_cryptocompare():
    # api_data_cryptocompare_now = API_DATA_CRYPTOCOMPARE_1_50_NOW
    price_1_50_now_resp = requests.get(API_DATA_CRYPTOCOMPARE_FULL_1_50_NOW).json()
    price_51_100_now_resp = requests.get(API_DATA_CRYPTOCOMPARE_FULL_51_100_NOW).json()

    price_100_now = {}
    price_100_now['DISPLAY'] = {**price_1_50_now_resp['DISPLAY'] , **price_51_100_now_resp['DISPLAY']}
    price_100_now['RAW'] = {**price_1_50_now_resp['RAW'] , **price_51_100_now_resp['RAW']}
    return price_100_now


def get_crypto_now_coindesk():
    # url_price_current = "{}currentprice.json".format(DATA_API_COINDESK)
    price_now_response = requests.get(API_DATA_COINDESK_NOW).json()
    return price_now_response


def get_crypto_now_coinmarketcap():
    pass


# --------------------------------------
# get price hist - differnt api's
# --------------------------------------
def get_crypto_hist_coindesk():

    dtime_utcnw = datetime.datetime.utcnow()
    last_year = datetime.datetime.strftime(dtime_utcnw - datetime.timedelta(days=366), DATE_FORMAT)
    last_year2 = datetime.datetime.strftime(dtime_utcnw - datetime.timedelta(days=367), DATE_FORMAT)

    historic_price_url = "{}historical/close.json?start={}&end={}".format(
        DATA_API_COINDESK,
        last_year2,
        last_year)


    # Query CoinDesk historical API
    historic_price_response = requests.get(historic_price_url).json()

    current_price = round(current_price_response['bpi']['USD']['rate_float'], 2)
    historic_price = round(historic_price_response['bpi'][last_year], 2)





"""
================================================================================

import data_crypto_get as cm
from pprint import pprint
import json

crypto_price_now = cm.get_crypto_now_()
print(json.dumps(crypto_price_now, sort_keys=True, indent=4))
len(crypto_price_now['DISPLAY'])
len(crypto_price_now['RAW'])
crypto_price_now.keys()
crypto_price_now['DISPLAY'].keys()
crypto_price_now['RAW'].keys()

pprint(crypto_price_now['DISPLAY']['BTC']['USD'])
pprint(crypto_price_now['RAW']['BTC']['USD'])
crypto_price_now['DISPLAY']['BTC']['USD']['PRICE']
crypto_price_now['RAW']['BTC']['USD']['PRICE']



d_crypto_symbol = cm.get_crypto_symbol()
print(json.dumps(d_crypto_symbol, sort_keys=True, indent=4))

d_crypto_symbol.get("BTC", "not found")


coin100str, coin1_50str, coin51_100str =  cm.gen_top_coinlist_str()
coin100str.count(',')
coin1_50str.count(',')
coin51_100str.count(',')
coin100str
coin1_50str
coin51_100str
coin1_50str + ',' + coin51_100str == coin100str



print('Today\'s Price $USD$ {} , {}'.format(current_price, today.strftime(time_format)))

print('Last Years Price $USD$ {} , {}'.format(historic_price, last_year))

================================================================================
"""
