import sys, os
import datetime, calendar    # from datetime import timedelta, timezone
import pytz    # from pytz import utc, timezone
import string, re   # ast,
import json, pickle
from pprint import pprint
import copy
import html.parser   # python 3.0
from operator import itemgetter
import requests
# import urllib.parse

import numpy as np
import pandas as pd

from flask import render_template, request, redirect, url_for, g, \
    abort, session, flash, logging, make_response, Response, jsonify

from flask_login import login_user, logout_user, current_user, login_required, \
    confirm_login, fresh_login_required

from flask_restful import reqparse, Resource, Api, fields   #, abort, marshal_with

from bson.objectid import ObjectId
from bson import json_util

from apps import app
from apps import cache, redis_db, PLOT_ROUTES

from . import app_quant

from apps.app_auth import requires_auth

from apps.app_util import mongodb, col_coin_spec, col_coin_top, \
    col_coin_hist_daily, col_coin_hist_daily2, col_coin_hist_hour, col_coin_hist_min, \
    mongodb_geo, logger_flask

from apps.app_util.mongodb_debug import check_mongodb
from apps.app_util import data_crypto
from apps.app_util.data_crypto_process import get_update_coin_hist, _test_logger_auth

from apps.app_plot import plot

from . import stats
# from .stats import convert_pctcum_np, calc_pct_np

from apps.settings.constants import *

###todo from apps.settings.settings_server import EMAIL_FINTECH_ADMIN #,
from apps.app_util.util_email import email_smtp
    #EMAIL_SERVER_PORT_GMAIL
# from apps.settings._w import _w_g, _w_z
w_g = ""
w_z = ""


# ==============================================================================
# Routes
# ==============================================================================

# ------------------------------------------------------------------------------
# CONTROLLERS - test
# ------------------------------------------------------------------------------

# ----------------
# Test: Templates
# ----------------
@app_quant.route('izmeginat/tpl/resize')
def izmeginat_tpl_resize():
    return render_template('nav_bs4_resize.html')

@app_quant.route('izmeginat/tpl/resize_logo')
def izmeginat_tpl_resize_logo():
    return render_template('nav_bs4_resize_logo.html')

@app_quant.route('izmeginat/tpl/scienceismeta')
def izmeginat_tpl_scienceismeta():
    return render_template('index_scienceismeta.html')

@app_quant.route('izmeginat/tpl/sciencestrange')
def izmeginat_tpl_sciencestrange():
    return render_template('index_sciencestrange.html')


@app_quant.route('izmeginat/tpl/lapas')
def izmeginat_tpl_lapas():
    return render_template('index_quant_lapas.html')


@app_quant.route('izmeginat/article')
def test_article():
    return render_template('article_tribal.html')

@app_quant.route('izmeginat/modal')
def test_index():
    return render_template('index_test.html')

@app_quant.route('test/jwplayer')
def test_jwplayer():
    return render_template('jwplayer.html')

@app_quant.route('test/markdown0')
def test_markdown0():
    return render_template('markdown_0.html')

@app_quant.route('test/markdown1')
def test_markdown1():
    return render_template('markdown_1.html')


# -------------
# Test: CHARTS
# -------------
@app_quant.route('demo/dia/3d_ribbon_demo')
def demo_dia_3d_ribbon_demo():
    return render_template('3d_ribbon_demo.html')


@app_quant.route('izmeginat/dia/3d_ribbon_parbaude')
def demo_dia_3d_ribbon_parbaude():
    return render_template('3d_ribbon_parbaude.html')

@app_quant.route('izmeginat/dia/basic_3d_surface')
def izmeginat_chart_3d_surface():
    return render_template('basic_3d_surface.html')

@app_quant.route('izmeginat/dia/test_template_3d')
def izmeginat_chart_template_3d():
    # d_data = api_plot_3d_ribbon()
    #return render_template('index_3d_ribbon2.html',
    #                        d_data=d_data,
    #                      )
    pass


# ----------
# Test: log
# ----------
@app_quant.route('izmeginat/log0')
@requires_auth
def izmeginat_log0():

    logger.info('from view')
    logger.info({'foo':'bar'})
    logger.error({'foo':'bar'})

    _test_logger_auth()

    return 'ok'


@app_quant.route('izmeginat/log1')
def izmeginat_log1():

    logger_flask.info("============ <       > ===========")

    return 'ok'


# ---------------------
# Test: session, redis
# ---------------------
@app_quant.route('izmeginat/session_put')
def izmeginat_session_put():
    # X res = jsonify(session)
    # X return jsonify(session)

    session['cow'] = 'moo'
    session['dtime'] = datetime.datetime.utcnow()
    session['sid2'] = session.sid
    #session['_id'] = session._id
    session['user'] = current_user.username
    session['pd_'] = {'pi': 3.14, 'k': 'poo'}

    return jsonify(current_user.username)

@app_quant.route('izmeginat/session_get')
def izmeginat_session_get():
    # X res = jsonify(session)
    res = {}

    res['sid'] = session.sid
    res['uid'] = session.get('uid')
    res['dtime'] = session.get('dtime', None)
    res['foo'] = session.get('foo', None)
    res['cow'] = session.get('cow', None)
    res['_id'] = session.get('_id', None)
    res['user'] = session.get('user', None)
    res['pd_'] = session.get('pd_', None)

    return jsonify(res)

# -----

@app_quant.route('izmeginat/redis_put')
def izmeginat_redis_put():
    session_data_obj = dict(
      reg_model = 3.14,
      dtime = datetime.datetime.utcnow()
    )
    #res = redis_db.set('key', json.dumps(session_data_str))

    session_data_str = dict(
      reg_model = 3.14,
      dtime = str(datetime.datetime.utcnow())
    )
    res = redis_db.set('key', pickle.dumps(session_data_obj))

    return str(res)

@app_quant.route('izmeginat/redis_get')
def izmeginat_redis_get():
  #redis_store = current_app.extensions['redis']
  #cached_val = redis_store.get('key')

  #redisClient.set('test_redis', 'Hello Python'.encode('utf-8'))
  #redisClient.get('test_redis').decode('utf-8')

  #session_data = json.loads(redis_db.get('key').decode('utf-8'))
  session_data = pickle.loads(redis_db.get('key'))

  return str(session_data.get('dtime', 'no dtime'))


# ------------------------------
# Test: ROUTE
# ------------------------------
@app_quant.route('izmeginat/route_host')
def izmeginat_route_host():
    import flask
    # http://www.plotopia.com/ www.plotopia.com
    return flask.request.url_root + "   " + flask.request.headers['Host']


# ------------------------------
# Test: ASYNC PROIMSE, DEFERRED
# ------------------------------
"""
@app_quant.route('test/api_async0/')
@app_quant.route('test/api_async0/<foo>')
def test_async0(foo=None):
    l = ['I', 'am', 'tired.\n', 'Wait ', 3.14 ]
    for x in l:
       yield x
       time.sleep(3)

    #return jsonify(x)
    #return jsonify({'foo':foo})  # => js = {foo: null}
"""
# -----------------------
# Test: paramaters in url
# -----------------------
# 2 params MUST - required
@app_quant.route('test/api0/<foo>/<bar>')
def test_api0(foo, bar):
    return jsonify({'foo':foo, 'bar':bar})

# X same!
@app_quant.route('test/api1/<foo>/<bar>')
def test_api1(foo='foo', bar='bar'):
    return jsonify({'foo':foo, 'bar':bar})

# X same!
@app_quant.route('test/api2/<foo>/<bar>/')
def test_api2(foo='foo', bar=None):
    return jsonify({'foo':foo, 'bar':bar})


@app_quant.route('test/api3/<foo>/<bar>')
def test_api3(foo, bar):
    return jsonify(ret={'foo':foo, 'bar':bar})

@app_quant.route('test/api4/<foo>/cow/<bar>')
def test_api4(foo, bar):
    return jsonify({'foo':foo, 'bar':bar})


"""
For optional-default paramters: Have to have TWO ROUTES, TWO, TWOOOOO:
"""
@app_quant.route('test/api_default0/')
@app_quant.route('test/api_default0/<foo>')
def test_api_default0(foo=None):
    return jsonify({'foo':foo})  # => js = {foo: null}

# ok - for 1 default nicer to use below
@app_quant.route('test/api_default1/<user_id>', defaults={'username': 'Anonymous'})
@app_quant.route('test/api_default1/<user_id>/<username>')
def test_api_default1(user_id, username):
    return user_id + ':' + username

# ok - *
@app_quant.route('test/api_default2A/<user_id>')
@app_quant.route('test/api_default2A/<user_id>/<username>')
def test_api_default2(user_id, username="Anonymous"):
    return user_id + ':' + username

# ok - careful with None
@app_quant.route('test/api_default2B/<user_id>')
@app_quant.route('test/api_default2B/<user_id>/<username>')
def test_api_default2B(user_id, username=None):
    # return user_id + ':' + username    X!
    return jsonify({'user_id':user_id, 'username':username})


#! X CANNOT HAVE BOTH W DEFAULT PARAM this way - works ONLY for 2nd default param
@app_quant.route('test/api_default3A/<user_id>')
@app_quant.route('test/api_default3A/<user_id>/<username>')
def test_api_default3A(user_id='-123', username=None):
    return jsonify({'user_id':user_id, 'username':username})


# ok - * this is 1/2 ways to have MULTIPLE DEFAULT PARAMS
@app_quant.route('test/api_default3B/')
@app_quant.route('test/api_default3B/<user_id>/')
@app_quant.route('test/api_default3B/<user_id>/<username>')
def test_api_default3B(user_id='-123', username=None):
    return jsonify({'user_id':user_id, 'username':username})


# X! cant get this to work ...
@app_quant.route('test/api_default4', defaults={'user_id': -123})
@app_quant.route('test/api_default4/<user_id>', defaults={'username': 'Anonymous'})
@app_quant.route('test/api_default4/<user_id>/<username>')
def test_api_default4(user_id, username):
    if username is None:
        username = 'override'
    return jsonify({'user_id':user_id, 'username':username})


# X! NOT WORKING
@app_quant.route('/test/api_catchall', defaults={'path': ''})
@app_quant.route('/test/api_catchall/<path:path>')
def test_api_catch_all(path):
    return jsonify({'the path':path})


"""
$ curl 127.0.0.1:5000          # Matches the first rule
You want path:
$ curl 127.0.0.1:5000/foo/bar  # Matches the second rule
You want path: foo/bar
"""


# ------------------------------------------------------------------------------
# Health здоровье - veselība
# ------------------------------------------------------------------------------
#@app.route('zdorovye/check|verify', defaults={'component': None}')
@app_quant.route('zdorovye/parbaudit')
@app_quant.route('zdorovye/parbaudit/<component>')
def zdorovye_check(component=None):
    if not component:
        return "ok: Flask"
    elif component == "root_path":
        return app.root_path
    #elif component == "api_java":
    #    return "ok: Received from apijava: " #+ requests.get(get_api_server_url(current_user.username) + '/test').text
    elif component == "mongo":
        return check_mongodb()
    #elif component == "api_flask":
    #    return "ok: api_flask"
    #elif component == 'kakvaszovut':
    #    return check_kakvaszovut()

    return 'ok'


@app_quant.route('zdorovye/vesture')
@app_quant.route('zdorovye/vesture/<sym>')
@app_quant.route('zdorovye/vesture/<sym>/<last_per>')
def zdorovye_vesture(sym="BTC", last_per=5):
    '''
    https://min-api.cryptocompare.com/data/histoday?fsym=BTC&tsym=USD&limit=7
    last_dtime =
    = col_coin_hist_daily.find_one(
      { 'sym':sym },
      { '_id':0, 'hist': 1 }
    )['hist'][-1]['time']

    = col_coin_hist_daily.find_one(
      { 'sym': sym },
      { '_id':0, 'sym':1, 'hist': { '$slice':-1 }  }
    )['hist'][0]['time']
    '''
    last_per = int(last_per)
    sym = sym.upper()

    last_docs = col_coin_hist_daily.find_one(
      { 'sym': sym },
      { '_id':0, 'sym':1, 'hist': { '$slice':-last_per }  }
    )['hist']

    return jsonify(last_docs)


"""
# ------------------------------------------------------------------------------
# CONTROLLERS - get & API - private - data and plots
# ------------------------------------------------------------------------------
api/data/get_crypto_now
api/data/get_crypto_live
api/data/coin_top
api/data/get_hist_daily/<sym0>/<sym1>

api/plot/2d_btc_sp
api/plot/3d_ribbon
api/plot/3D_volatility
api/plot/3d_scatter_crypto_sp_

api/data/get_coin_spec/<sym>
api/tron/run_get_update_coin_hist
"""
### Todo - protect!
@app_quant.route('api/data/get_crypto_now')
def get_crypto_now():
    return get_crypto_live()
    # get_crypto_mongo()


@app_quant.route('api/data/get_crypto_live')
def get_crypto_live():
    d_res = data_crypto.get_crypto_live_()
    if d_res is None:
        d_res = {'status_msg':'error'}
    d_res['status_msg'] = 'ok'
    return jsonify(d_res)


@app_quant.route('api/data/coin_top')
def get_coin_top():
    """
    l_top_10_pop = col_coin_top.find_one({'top_10_pop': {'$exists': True}},{'_id':0})['top_10_pop']
    l_top_10_mkt = col_coin_top.find_one({'top_10_mkt': {'$exists': True}},{'_id':0})['top_10_mkt']
    l_top_100    = col_coin_top.find_one({'top_100': {'$exists': True}},{'_id':0})['top100']
    d_res = {
      'top_10_pop': l_top_10_pop,
      'top_10_mkt': l_top_10_mkt,
      'top_100': l_top_100,
    }
    """
    d_top = col_coin_top.find_one({'top_10_pop': {'$exists': True}},{'_id':0})

    if d_top is None:
        d_top = {'status_msg': 'error'}

    d_top['status_msg'] = 'ok'
    return jsonify(d_top)


@app_quant.route('api/plot/2d_btc_sp')
def api_plot_2d_btc_sp():
    '''
    -> jsonify(
    { 'div': 'div_plot_2d_btcusd_sp',
      'data': traces,
      'layout': layout,
      'config': config
    })
    '''

    d_fig = plot.get_plot_2d_btc_sp()

    return jsonify(d_fig)


@app_quant.route('api/data/get_hist_daily/<sym0>/<sym1>')
def get_hist_daily_pair(sym0, sym1):
    ###todo try  add
    d_res0 = col_coin_hist_daily.find_one({'sym': sym0},{'hist':1, '_id':0})
    d_res1 = col_coin_hist_daily.find_one({'sym': sym1},{'hist':1, '_id':0})

    if d_res0 is None or d_res1 is None:
        d_res = {'status_msg':'error'}
        return jsonify(d_res)

    l_res0 = d_res0['hist']
    l_res1 = d_res1['hist']

    l_sym0_x = []
    l_sym0_y = []
    l_sym1_x = []
    l_sym1_y = []

    for d in l_res0:
        # d['datestr'] = d[dtime].strftiime('%Y-%m-%d %H:%M:%S')
        l_sym0_x.append(d['dtime'].strftime('%Y-%m-%d'))
        l_sym0_y.append(d['close'])

    for d in l_res1:
        # d['datestr'] = d[dtime].strftiime('%Y-%m-%d %H:%M:%S')
        l_sym1_x.append(d['dtime'].strftime('%Y-%m-%d'))
        l_sym1_y.append(d['close'])

    d_res = {'status_msg': 'ok'}
    d_res['sym0'] = {'x': l_sym0_x, 'y': l_sym0_y, 'sym': sym0, 'name':''}
    d_res['sym1'] = {'x': l_sym1_x, 'y': l_sym1_y, 'sym': sym1, 'name':''}

    return jsonify(d_res)


@app_quant.route('api/plot/3d_ribbon')
def api_plot_3d_ribbon():
    '''
    -> jsonify(
    { 'div': 'div_',
      'data': traces,
      'layout': layout,
      'config': config
    })
    '''

    d_fig = plot.get_plot_3d_ribbon()
    return jsonify(d_fig)

@app_quant.route('api/plot/3d_ribbon_demo')
def api_plot_3d_ribbon_demo():
    '''
    -> jsonify(
    { 'div': 'div_',
      'data': traces,
      'layout': layout,
      'config': config
    })
    '''
    d_fig = plot.get_plot_3d_ribbon_demo()
    return jsonify(d_fig)


@app_quant.route('api/plot/3d_volatility')
def api_plot_3d_volatility():
    '''
    -> jsonify(
      { 'div': 'div_plot_2d_btcusd_sp',
        'data': traces,
        'layout': layout,
        'config': config
      })
    '''
    d_fig = plot.get_plot_3d_volatility()
    return jsonify(d_fig)


@app_quant.route('api/plot/3d_scatter_crypto_sp_')
def api_plot_3d_scatter_crypto_sp_():
#@app_quant.route('api/plot/3d_scatter_crypto_sp_time')
#def api_plot_3d_scatter_crypto_sp_time():

    d_fig = plot.get_plot_3d_scatter_crypto_sp_()
    return jsonify(d_fig)



@app_quant.route('api/data/get_coin_spec/<sym>')
def get_coin_spec(sym):
    d_res = col_coin_spec.find_one({'Symbol': sym.upper()}, {'_id':0})
    return jsonify(d_res)



@app_quant.route('api/tron/run_get_update_coin_hist')
@requires_auth
def run_get_update_coin_hist():
    get_update_coin_hist()
    return "."


# ------------------------------------------------------------------------------
# CONTROLLER - Routes public
# ------------------------------------------------------------------------------
@app_quant.route('/')
def index():
    return render_template('index_quant.html')

@app_quant.route('dev')
def index_dev():
    return render_template('index_quant_dev.html')


@app_quant.route(PLOT_ROUTES['pair'])
def datascience():
    return render_template('datascience.html')


@app.route('/pitch_private')
def pitch_private():
    #return redirect(url_for('foo'))
    return redirect("/laplacian/pitch_private", code=302)


# ------------------------
# - Routes public: Charts
# ------------------------
@app_quant.route('3D-line')
def index_3d_ribbon():
    """
    d_data = api_plot_3d_ribbon()
    return render_template('3d_ribbon2.html',
                            d_data=d_data,
                          )
    """
    return render_template('3d_ribbon.html')


@app_quant.route('3D-volatility')
def index_3d_volatility():
    return render_template('3d_volatility.html')


@app_quant.route('3D-correlation')
def index_3d_correl():
    return render_template('3d_volatility.html')


@app_quant.route('3D-correlation-scatter')
def index_3d_correl_scatter():
    return render_template('3d_correl_scatter.html')


# -------------------
# Routes: Raksts
# -------------------
@app_quant.route('/article/causes-bitcoin-decline')
def index_article_causes_bitcoin_decline():
    return render_template('raks_.html')


@app_quant.route('article/<slug>')
def article_():
    return render_template('article_ ' +  + '.html')


# ------------------------------------------------------------------------------
# CONTROLLERS - login_required
# ------------------------------------------------------------------------------
@app_quant.route('contact/')
@app_quant.route('contact/<name>')
@login_required
def contact(name=None):

    # cursor = col_contact.find()
    # for n, r in enumerate(cursor):
    #     print('\n>', n)
    #     pprint(r)

    search = {}
    if name:
        # search = {
        #  "$or": [{'name_first': re.compile(name, re.IGNORECASE)},
        #          {'name_last': re.compile(name, re.IGNORECASE)}
        #         ]
        # }
        # search = {'name': re.compile(name, re.IGNORECASE)}  # ok
        search = {'name': {"$regex":name, '$options':'i'}}

    cursor = col_contact.find(
      search,
      # {'cnty_name':1, 'cnty_code':1, 'cnty_code3':1, '_id':0 }
    )
    #return jsonify(result=list(cursor))

    """
    lst_jsn=[]
    enc = CustomJSONEncoder()
    for r in cursor:
        r = enc.encode(r)
        lst_jsn.append(r)
    return Response(lst_jsn, mimetype='application/json')   # ok, just no pretty
    return json.dumps({'result': lst_jsn},                  # ok, just no pretty
            default = json_util.default,
            indent = 4)
    """

    lst_jsn=[]
    result_count = cursor.count()
    for r in cursor:
        r['_id'] = str(r['_id'])
        lst_jsn.append(r)

    result ={
      'result_count': result_count,
      'result': lst_jsn,
    }
    return jsonify(result)


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        elif isinstance(o, datetime.datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)
# enc = CustomJSONEncoder
# enc.encode(doc)


@app_quant.route('contact_get', methods=['GET'])
@login_required
def contact_get():

    group = request.args.get('group', None)
    name = request.args.get('name', None)

    search = {}
    if name:
        # search = {
        #  "$or": [{'name_first': re.compile(name, re.IGNORECASE)},
        #          {'name_last': re.compile(name, re.IGNORECASE)}
        #         ]
        # }
        search['name'] = re.compile(name, re.IGNORECASE)
    if group:
        # db.blogpost.find({ 'tags' : 'tag1'}); //1
        # db.blogpost.find({ 'tags' : { $all : [ 'tag1', 'tag2' ] }}); //2
        # db.blogpost.find({ 'tags' : { $in : [ 'tag3', 'tag4' ] }}); //3
        search['group'] = group

    cursor = col_contact.find(
      search,
      # {'cnty_name':1, 'cnty_code':1, 'cnty_code3':1, '_id':0 }
    ).sort([
      ("name_last", 1),
      #("address.zipcode", pymongo.DESCENDING)
    ])

    lst_jsn=[]
    result_count = cursor.count()
    for r in cursor:
        r['_id'] = str(r['_id'])
        lst_jsn.append(r)

    result ={
      'result_count': result_count,
      'result': lst_jsn,
    }
    return jsonify(result)

# ------------------------------------------------------------------------------
# public API
# ------------------------------------------------------------------------------
@app_quant.route('email/contactme', methods=['GET', 'POST'])
def contactme():
    res_jsn = {
      'status_msg': 'ERROR - Email contactme',
      'status_code': 500,
      'msg': ''
    }

    if request.method == "POST":
        # get url that the user has entered

        email = request.form['input_contactme_email']
        name = request.form['input_contactme_name']
        msg_body = request.form['textarea_contactme_msg']
        # checkbox_addmailinglist = request.form.getlist('checkbox_contactme_addmailinglist')

        #if checkbox_addmailinglist:
        #    logger.info("CEHCKBOX: " + str(checkbox_addmailinglist))

        msg_subject = "CONTACTME - From: " + email + "  Name: " + name
        logger.info("EMAIL " + msg_subject + " Body: " + msg_body)
        ret_email = email_smtp(_w_g, EMAIL_SERVER_PORT_GMAIL, EMAIL_GMAIL, EMAIL_ACROSSPOND, msg_subject, msg_body)

        # Using requsts post:
        # url = 'http://192.168.3.45:8080/api/v2/event/log'
        # data = {"eventType": "AAS_PORTAL_START", "data": {"uid": "hfe3hf45huf33545", "aid": "1", "vid": "1"}}
        # params = {'sessionKey': '9ebbd0b25760557393a43064a92bae539d962103', 'format': 'xml', 'platformId': 1}
        # requests.post(url, params=params, json=data)
        mailinglist_insert(email)

        if not ret_email:
            res_jsn['status_code'] = 200
            res_jsn['status_msg'] = 'ok'
            res_jsn['msg'] = ""
        else:
            res_jsn['status_code'] = 400
            res_jsn['status_msg'] = str(ret_email)

    res_jsn = jsonify(res_jsn)
    return res_jsn


@app_quant.route('email/mailinglist_insert', methods=['GET', 'POST'])
@login_required
def mailinglist_insert(email=None):
    res_jsn = {
      'status_msg': 'ERROR - mailinglist_insert',
      'status_code': 500,
      'msg': ''
    }

    if request.method == "POST" or email:
        if not email:
            email = request.form['input_mailinglist_email']

        # First check if email exists
        result = col_contact.find_one({"email": email})
        if result:
            res_jsn['status_code'] = 400
            res_jsn['status_msg'] = 'ERROR: exists'

        else:
            dict_user = {
              'email': email,
              'group': ['mailinglist'],
              'register_date': datetime.datetime.utcnow(),
            }

            result = col_contact.insert(dict_user)

            logger.info("MAILINGLIST_INSERT: " + email)
            if not result:
                res_jsn['status_code'] = 400
                res_jsn['status_msg'] = 'ERROR - email insert: ' + str(result)
            else:
                res_jsn['status_code'] = 200
                res_jsn['status_msg'] = 'ok'

        res_jsn = jsonify(res_jsn)
        return res_jsn


@app_quant.route('email/mailinglist_delete', methods=['GET', 'POST'])
@login_required
def mailinglist_delete(email=None):
    res_jsn = {
      'status_msg': 'ERROR - MAILINGLIST_DELETE',
      'status_code': 500,
      'msg': ''
    }

    if request.method == "POST" or email:
        if not email:
            email = request.form['input_mailinglist_email']

        # First check if email exists
        result = col_contact.find_one({"email": email})
        if not result:
            res_jsn['status_code'] = 400
            res_jsn['status_msg'] = "ERROR: email does not exist"
        else:
            result = col_contact.remove({'email': email})
            res_jsn['status_code'] = 200
            res_jsn['status_msg'] = 'ok'

    return jsonify(res_jsn)


@app_quant.route('email/mailinglist_send', methods=['GET', 'POST'])
@login_required
def mailinglist_send():
    pass
