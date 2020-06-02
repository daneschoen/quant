import os
import datetime
import json
import copy
# from pprint import pprint

import requests

from bson.objectid import ObjectId

from apps.settings.constants import *

from apps.app_util import mongodb, col_coin_spec, col_coin_top, \
    col_coin_hist_daily, col_coin_hist_hour, col_coin_hist_min, \
    mongodb_geo, logger_flask

#from apps.app_auth import requires_auth


# ==============================================================================
# dev:
col_coin_hist_daily2 = mongodb['coin_hist_daily2']

# ------------------------------------------------------------------------------

# PATH, FILENAME CONSTANTS
PATH_ = os.path.dirname(os.path.abspath(__file__))

FILE_COINLIST_ALL_SPEC = "coinlist_all_spec.json"
FILE_COINLIST_TOP_IN  = "coinlist_top_scraped.txt"
FILE_COINLIST_TOP_OUT = "coinlist_top.json"

PATH_FILE_COINLIST_ALL_SPEC  = os.path.join(PATH_, FILE_COINLIST_ALL_SPEC)
PATH_FILE_COINLIST_TOP_IN  = os.path.join(PATH_, FILE_COINLIST_TOP_IN)
PATH_FILE_COINLIST_TOP_OUT  = os.path.join(PATH_, FILE_COINLIST_TOP_OUT)

# ------------------------------------------------------------------------------
# API'S
API_DATA_CRYPTOCOMPARE_ALL_SPEC = "https://min-api.cryptocompare.com/data/all/coinlist"
# https://min-api.cryptocompare.com/data/histoday?fsym=BTC&tsym=USD&limit=7
API_DATA_CRYPTOCOMPARE_HIST0 = "https://min-api.cryptocompare.com/data/histoday?fsym="
API_DATA_CRYPTOCOMPARE_HIST1 = "&tsym=USD&limit="

# ------------------------------------------------------------------------------

TOP_COINLIST_100_STR  = 'BTC,ETH,XRP,BCH,LTC,EOS,ADA,XLM,TRX,NEO,IOT,XMR,VEN,DASH,BNB,XEM,ETC,QTUM,XVG,LSK,HT,ICX,BTM*,BTG,ZEC,XRB,IOST,SNT,ZRX,ZIL,NAS,DGD,WAVES,ORME,LINK,STORJ,POWR,BAT,NCASH,STORM,GNX,SALT,HSR,SUB,MTL,KNC,CVC,GNT,MANA,GTO,MTX,ELF,SRN,REQ,SYS,MDS,BLZ,EDO,RDN*,NEBL,ABT,THETA,DTA,RCN,ENJ,ITC,RUFF,OCN,GTC,POA,CMT*,SWFTC,PRO,GVT,NULS,TNT,WPR,INS,MTN*,ADX,SOC,RPX,QUN,TRIG,MEE,SNC,OC,WAN,ACT*,ETHOS,OMG,ELA,AION,ONT,STRAT,PAY,WAX,GAS,MCO,QSP'
TOP_COINLIST_10_STR = 'BTC,ETH,XRP,BCH,LTC,EOS,ADA,XLM,TRX,NEO'

PER_GET_UPDATE_COIN_HIST_DAILY = 7
PER_GET_UPDATE_COIN_HIST_MIN = 2000

# ==============================================================================

def load_coinlist_all_spec():
    #with open(FILENAME_ALL_IN, 'w') as fin:
    f = open(PATH_FILE_COINLIST_ALL_SPEC, 'r')
    d = json.load(f)
    return d

def get_coinlist_all_spec():
    return requests.get(API_DATA_CRYPTOCOMPARE_ALL_SPEC).json()


def convert_symbol_dot(d):
    '''
    import coinlist_parse as cm
    dot_test = {'x':{'.a':'y'}, 'z*':{'b.':'z'}, '.dot':{'c':3.41}, 'm.':{'d':'m.'}, 'h.j':{'a':'h.j'}}
    dot_test2 = {'x':{'a':'y'}, 'z*':{'b':'z'}, '.dot':{'c*':3.41}, 'm.':{'c':'m.'}, 'h.j':{'a':'h.j'}}
    pprint(dot_test, width=4)
    cm.convert_symbol_dot(dot_test)
    pprint(d_new, width=4)
    '''
    d_new = copy.deepcopy(d)
    for k, v in d_new.items():
        if "." in k:
            k_new = k.replace('.', '__p__')
            d_new[k_new] = d_new.pop(k)
    return d_new


def insert_mongo_coinlist_all_spec(l_coin_spec_data):
    #d_coin_spec = load_coinlist_all_spec()

    # mongoclient = MongoClient()
    # mongodb = MongoClient()[MONGODB_FINTECH]
    # col_coin_spec = mongodb[COL_COIN_SPEC]

    #res = col_coin_spec.insert_one(d_coin_spec_data)
    res = col_coin_spec.insert_many(l_coin_spec_data)

    """
    col_coin_spec.find_one()
    for doc in col_coin_spec.find():
        pprint(doc, width=4)
    """

"""
# ------------------------------------------------------------------------------
# HISTORY
# ------------------------------------------------------------------------------
> db.coin_hist_daily.count()
100

> doc = db.coin_hist_daily.findOne();
> for (key in doc) print(key);
_id
hist
sym

> doc = db.coin_hist_daily.findOne({sym:'BTC'})
> doc.hist.length
2001
> doc.hist[doc.hist.length-1]  //* is last date

"""

def get_hist_cryptocompare(sym, per):
    api_ = "{}{}{}{}".format(API_DATA_CRYPTOCOMPARE_HIST0, sym, API_DATA_CRYPTOCOMPARE_HIST1, per)
    res = requests.get(api_).json()
    return res


def get_insert_coin_hist_lst(l_coin, per):
    for sym in l_coin:
        res = get_hist_cryptocompare(sym, per)
        l_hist = res['Data']
        for rec in l_hist:
            rec['dtime'] = datetime.datetime.utcfromtimestamp(rec['time'])

        insert_mongo_hist_coinlist(sym, l_hist)

    '''
    Usage:

    l_top_10 = col_coin_top.find_one({},{'top_10':1, '_id':0})['top10']
    l_top_100 = col_coin_top.find_one({},{'top_100':1, '_id':0})['top100']

    get_insert_coin_hist_lst(l_top_100)

    sanity:
    col_coin_hist_daily.count()
    l_res = col_coin_hist_daily.find_one({'sym': 'BTC'},{'hist':1, '_id':0})['hist']
    len(l_res)
    for r in l_res: pprint(r)
    l_res[0]
    l_res[-1]
    '''


def get_update_coin_hist(per=PER_GET_UPDATE_COIN_HIST_DAILY):
    '''
    Usage: usually run by cron

    MUST BE IDEMPOTENT! in case needs to be run manually
    '''
    l_sym = col_coin_hist_daily.distinct('sym')   #db.coin_hist_daily.distinct('sym')
    res = get_update_coin_hist_lst(l_sym, PER_GET_UPDATE_COIN_HIST_DAILY)
    if res['status_msg'] == 'success':
        logger_flask.info(res)
    else:
        logger_flask.error(res)


def _test_logger_auth():
    records = {'john': 55, 'tom': 66}
    logger_flask.debug('foo_test - Records: %s', records)


def get_update_coin_hist_lst(l_sym, per):
    status = {'status_msg': 'success'}

    for sym in l_sym:
        res = get_hist_cryptocompare(sym, per)

        logger_flask.info("Got get_hist_cryptocompare({},{})".format(sym, per))

        l_hist_s = res['Data']
        for doc in l_hist_s:
            doc['dtime'] = datetime.datetime.utcfromtimestamp(doc['time'])

        # logger_flask.info("update_mongo_hist_coinlist({},l_hist_s)".format(sym))
        # res = update_mongo_hist_coinlist(sym, l_hist_s)
        logger_flask.info("update_replace_mongo_hist_coinlist({},l_hist_s)".format(sym))
        res = update_replace_mongo_hist_coinlist(sym, l_hist_s)
        logger_flask.info(res)

    return status

    '''
    Usage to run manually (IDEMPOTENT):

    from apps.app_util.data_crypto_process import *

    get_update_coin_hist()

    l_top_10 = col_coin_top.find_one({},{'top_10':1, '_id':0})['top_10']
    l_top_100 = col_coin_top.find_one({},{'top_100':1, '_id':0})['top_100']
    l_sym = col_coin_hist_daily.distinct('sym')
    l_sym = ['BTC']

    get_update_coin_hist_lst(l_top_100 | l_sym, 5|10|50)

    sym = 'BTC'
    res = get_hist_cryptocompare(sym, 20)
    l_hist_s = res['Data']
    len(l_hist_s)

    update_mongo_hist_coinlist(sym, l_hist_s)

    col_coin_hist_daily2 = mongodb['coin_hist_daily2']
    hist_s_t = l_hist_s[-10]
    col_coin_hist_daily2.update(
        { 'sym': sym,  'hist.time': {'$ne': hist_s_t['time']} },
        { '$push':{'hist': hist_s_t} }
    )


    sanity:
    col_coin_hist_daily.count()
    l_hist_s = col_coin_hist_daily.find_one({'sym': 'BTC'},{'hist':1, '_id':0})['hist']
    l_hist_s = col_coin_hist_daily2.find_one({'sym': 'BTC'},{'hist':1, '_id':0})['hist']
    len(l_hist_s)
    for r in l_res: pprint(r)
    l_res[0]
    l_res[-1]

    '''


def insert_mongo_hist_coinlist(sym, l_hist_s):

    # mongodb = MongoClient()[MONGODB_FINTECH]
    # col_coin_hist_daily = mongodb[COL_COIN_HIST_DAILY]

    d_sym_hist = { 'sym': sym,
                   'hist': l_hist_s
                 }

    res = col_coin_hist_daily.insert_one(d_sym_hist)
    #res = col_coin_spec.insert_many(l_coin_spec_data)
    return res


def update_mongo_hist_coinlist(sym, l_new_hist_s):
    '''
    # FIRST ALWAYS OVERWRITE THE LATEST EXISTING REC
    # So, get latest 'time'stamp

    col_coin_hist_daily.find_one(
      { 'sym':sym },
      { '_id':0, 'hist': 1 }
    )['hist'][-1]['time']
    '''
    last_timestamp_s = col_coin_hist_daily.find_one(
      { 'sym': sym },
      { '_id':0, 'sym':1, 'hist': { '$slice':-1 }  }
    )['hist'][0]['time']

    res_lst=[sym]
    for new_hist_s_t in l_new_hist_s:
        if last_timestamp_s == new_hist_s_t['time']:
            # this just modifies fields within that doc-record
            # res = col_coin_hist_daily.update_one(
            #         { 'sym': sym,  'hist.time': new_hist_s_t['time']},
            #         { '$set': {'hist$time': new_hist_s_t,
            #                    'hist$dtime': datetime.datetime.utcfromtimestamp(new_hist_s_t['time'])
            #                   }
            #         }
            #       )
            # Instead need to replace:
            res = col_coin_hist_daily.update_one(
                    { 'sym': sym,  'hist.time': new_hist_s_t['time']},
                    { '$set': {'hist$': new_hist_s_t}
                    }
                  )

            res_lst.append(str(res.raw_result))
        elif last_timestamp_s < new_hist_s_t['time']:
            # need this elif cond bec would need $position to $set insert in between for gaps
            res = col_coin_hist_daily.update_one(
                    { 'sym': sym,  'hist.time': {'$ne': new_hist_s_t['time']} },
                    { '$push': {'hist': new_hist_s_t} }
                  )

            # may be problem if col.hist array has gaps:
            # res = col_coin_hist_daily.update_one(
            #         { 'sym': sym },
            #         { '$push':{'hist': new_hist_s_t} }
            #       )
            res_lst.append(str(res.raw_result))
        # to fill in gaps - need $position so need position


    return res_lst


def update_replace_mongo_hist_coinlist(sym, l_new_hist_s):
    '''
    Replace regardless given l_new_hist_s, not just latest
    But still need to push for nonexisting
    '''
    last_timestamp_s = col_coin_hist_daily.find_one(
      { 'sym': sym },
      { '_id':0, 'sym':1, 'hist': { '$slice':-1 }  }
    )['hist'][0]['time']

    res_l=[sym]
    for new_hist_s_t in l_new_hist_s:

        if last_timestamp_s >= new_hist_s_t['time']:

            res = col_coin_hist_daily.update_one(
                    { 'sym': sym,  'hist.time': new_hist_s_t['time']},
                    { '$set': {'hist$': new_hist_s_t}
                    }
                  )
            res_l.append(str(res.raw_result))

        elif last_timestamp_s < new_hist_s_t['time']:

            res = col_coin_hist_daily.update_one(
                    { 'sym': sym,  'hist.time': {'$ne': new_hist_s_t['time']} },
                    { '$push': {'hist': new_hist_s_t} }
                  )

            res_l.append(str(res.raw_result))
    return res_l


# ------------------------------------------------------------------------------
# Fixers:
# ------------------------------------------------------------------------------
def pull_mongo_hist_coinlist(l_sym, timestamp_gte):
    '''
    Manually run:
    $ cd ~/projects/fintech/flask_blueprint
    $ p3
    from apps.app_util.data_crypto_process import *
    l_sym = ['BTC']
    l_sym = col_coin_top.find_one({},{'top_100':1, '_id':0})['top_100']
    l_sym = col_coin_hist_daily.distinct('sym')
    l_sym

    pull_mongo_hist_coinlist(k_sym, 1524960000)

    '''
    res_l=[]
    for sym in l_sym:
        res_l.append(sym + ": ")
        res = col_coin_hist_daily.update_one(
                { 'sym': sym },
                { '$pull': { 'hist': { 'time': { '$gte': timestamp_gte } } }
                }
              )
        res_l.append(str(res.raw_result))
    return res_l


def load_hist_cryptocompare():
    f = open("btc_hist_min_cryptocompare.json", 'r')
    d = json.load(f)
    return d


# ------------------------------------------------------------------------------
# COIN TOP
# ------------------------------------------------------------------------------
def insert_mongo_top():

    # col_coin_top = MongoClient()[MONGODB_FINTECH][COL_COIN_TOP]
    # l_top10 = TOP_COINLIST_10_STR.split(',')
    # l_top100 = TOP_COINLIST_100_STR.split(',')

    # top_100 = []
    # top_1_50 = []
    # top_50_100 = []
    # top_10up = []
    # top_10dn = []
    top_10_mkt = ['BTC','ETH','XRP','BCH','EOS','LTC','ADA','XLM','IOT','NEO']
    top_10_pop = ['BTC','ETH','XRP','BCH','EOS','LTC','ADA','DASH','ZEC','XMR']

    d_top = {
      'top_10_pop': top_10_pop,
      'top_10_mkt': top_10_mkt,
      'top_100': COIN_TOP_100,
      'top_1_50': COIN_TOP_1_50,
      'top_51_100': COIN_TOP_51_100,
    }

    # METHOD # 0
    res = col_coin_top.insert_one(d_top)

    # OR! :
    """
    res = col_coin_top.insert_one({'top100': l_top100})
    res = col_coin_top.insert_one({'top10_mktcap': top10_mktcap})
    res = col_coin_top.insert_one({'top10_pop': top10_pop})
    """

    """
    res = col_coin_top.replace_one(
            {'top10_pop': {'$exists': True}},
            {'top10_pop': top10_pop}
          )
    """

    """
    sanity:

    d_top = col_coin_top.find_one({'top_10_pop': {'$exists': True}},{'_id':0})
    d_top.keys()
    d_top['top_10_pop']

    l_top_10_pop = col_coin_top.find_one({'top_10_pop': {'$exists': True}},{'_id':0})['top_10_pop']
             = col_coin_top.distinct('top10str')[0].split(',')
       X!    = col_coin_top.distinct('top10_pop')



    top10str = col_coin_top.distinct('top10str')[0]

    """


def parse_coinlist_top():

    f = open(FILE_COINLIST_TOP_IN, 'r')

    coin_list = []

    line_cnt=0

    for line in f:
        line_cnt += 1

        if line_cnt % 10 == 1:
            coin_rank = line.strip()

        if line_cnt % 10 == 3:
            coin_name = line.strip()

        if line_cnt % 10 == 4:
            coin_sym = line.strip()

            coin_list.append((int(coin_rank), coin_sym, coin_name))

    print(coin_list)

    with open(PATH_FILE_COINLIST_TOP_OUT, 'w') as fout:
        #res = json.dumps(d, sort_keys=True, indent=4, separators=(',', ': '))
        jsn = json.dumps(coin_list)
        fout.write(jsn)




# ==============================================================================

# if __name__ == "__main__":
# parse_coinlist_top()

"""
$ cd ~/projects/fintech/flask_blueprint
>>>
from apps.app_util.coinlist_parse import *

import coinlist_parse as cm
       data_symbol.coinlist_parse as cm

d_coinlist_all_spec = cm.get_coinlist_all_spec()
                    = cm.load_coinlist_all_spec()

d_coinlist_all_spec.keys()
# dict_keys(['DefaultWatchlist', 'BaseImageUrl', 'Data', 'Response', 'Message', 'Type', 'BaseLinkUrl'])
len(d_coinlist_all_spec['Data'])  # 2426
pprint(d_coinlist_all_spec['Data']['BTC'])


d_convert_dot = cm.convert_symbol_dot(d_coinlist_all_spec['Data'])
pprint(d_coinlist_all_spec['Data']['DCS.'], width=4)
pprint(d_convert_dot['DCS.'], width=4)
pprint(d_convert_dot['DCS__p__'], width=4)


# ------------------------------------------------------------------------------
# cm.insert_mongo_coinlist_all_spec(d_convert_dot)
# cm.insert_mongo_coinlist_all_spec(d_coinlist_all_spec['Data'].values())

col_coin_spec = MongoClient()['fintech']['coin_spec']
col_coin_spec.count()   # 2426
for doc in col_coin_spec.find():
    pprint(doc)

res = col_coin_spec.find_one({'Symbol':'XMR'})
pprint(res)

# ------------------------------------------------------------------------------

f = open(PATH_FILE_COINLIST_TOP_OUT, 'r')
coinlist_top = json.load(f)


with open(PATH_FILE_COINLIST_TOP_OUT, 'r') as f:
    d = json.load(f)


"""
