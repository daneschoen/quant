import sys, os
import json, datetime, calendar  # from datetime import timedelta, timezone
import pytz  # from pytz import utc, timezone
import string, ast, re
from pprint import pprint

import copy
import html.parser   # python 3.0
from operator import itemgetter

from flask import render_template, request, redirect, url_for, g, \
    abort, session, flash, \
    make_response, Response, jsonify

from flask_login import login_user, logout_user, current_user, login_required, \
    confirm_login, fresh_login_required

from flask_restful import reqparse, abort, Resource, Api, fields, marshal_with

import requests
import urllib.parse

from bson.objectid import ObjectId
from bson import json_util
import json

from apps import app
from . import app_geo

from apps.app_util import mongodb, mongodb_geo, \
  col_geo_city, col_geo_cnty

from apps.settings.constants import *


api_rest = Api(app)


# ==============================================================================
# API for GEO | FX, WEATHER,
# ==============================================================================
@app_geo.route('/')
def index():
    return "Hello this is index of geo"


@app_geo.route('test/test0')
@login_required
def test0():

    res = {
      'objectId': ObjectId(1234),
      'status': True,
      'foo': 3.14,
      'dtime': datetime.datetime.utcnow(),
      'instr_meta': [
        { 'instr_name': 'es',
          'dt_lst': ['12/23/2015','12/24/2015','12/25/2015']
        },
        { 'instr_name': 'cl',
          'dt_lst': ['---']
        }
      ]
    }

    return jsonify(res)

@app_geo.route('test/test1')
@login_required
def test1():

    res = {
      'status': True,
      'foo': 3.14,
      # 'dtime': datetime.datetime.utcnow(),  JSON.DUMPS CANNOT HANDLE THIS!
      'instr_meta': [
        { 'instr_name': 'es',
          'dt_lst': ['12/23/2015','12/24/2015','12/25/2015']
        },
        { 'instr_name': 'cl',
          'dt_lst': ['---']
        }
      ]
    }

    return Response(json.dumps([res,res]), mimetype='application/json')


@app_geo.route('test/test2')
@login_required
def test2():

    res = {
      'status': True,
      'foo': 3.14,
      'dtime': datetime.datetime.utcnow(),
      'instr_meta': [
        { 'instr_name': 'es',
          'dt_lst': ['12/23/2015','12/24/2015','12/25/2015']
        },
        { 'instr_name': 'cl',
          'dt_lst': ['---']
        }
      ]
    }

    """
    result = {
      'result': [
        res, res
      ]
    }
    return jsonify(result)
    """

    # ok - perfect
    return jsonify(result = [res,res])


@app_geo.route('test/test3')
@login_required
def test3():

    res = {
      'status': True,
      'foo': 3.14,
      'dtime': datetime.datetime.utcnow(),
      'instr_meta': [
        { 'instr_name': 'es',
          'dt_lst': ['12/23/2015','12/24/2015','12/25/2015']
        },
        { 'instr_name': 'cl',
          'dt_lst': ['---']
        }
      ]
    }

    # X
    lst_jsn = [json.dumps(res, default=json_util.default), json.dumps(res, default=json_util.default)]
    #return jsonify(result = lst_jsn)
    return Response(json.dumps(res), mimetype='application/json')


@app_geo.route('geo_cnty/')  # trailing / needed, and will default to trailing slash if omitted
@app_geo.route('geo_cnty/<cnty_name>')
#@login_required
def geo_cnty(cnty_name=None):
    """
    result = mongodb_geo['geo_cnty'].find_one({'code_iso':'cz'.upper()})
             col_geo_cnty.find_one({'code_iso':'cz'.upper()})
    result = col_geo_cnty.find_one({'country_name':string.capwords('belgium')})
    pprint(result)

    > db.geo_cnty.findOne({"cnty_name" : /bahamas/i})
    > col_geo_cnty.find_one({'cnty_name': /belg/i})

    col_geo_cnty.find_one({ 'country_name': {'$regex':'belg','$options':'i'} })

    import re
    regx_file = re.compile("^foo", re.IGNORECASE)
    regx_ip = re.compile('.*IP.*', re.IGNORECASE)

    db.users.find_one({"files": regx_file})
    db.collectionname.find({'files':{'$regex':'^File', '$options':'i'}})

    cursor = db.tweets.find({'text':regx_ip},{'text':1,'created_at':1})

    # To avoid the double compilation you can use the bson regex wrapper that comes with PyMongo:
    regx = bson.regex.Regex('^foo')
    db.users.find_one({"files": regx})

    # Regex just stores the string without trying to compile it, so find_one can then
    # detect the argument as a 'Regex' type and form the appropriate Mongo query.

    """

    # cursor = col_geo_cnty.find()
    # for n, r in enumerate(cursor):
    #    print('\n>', n)
    #    pprint(r)

    """ method 0
    lst_jsn = []
    for doc in cursor:
        jsn_doc = json.dumps(doc, default=json_util.default)
        lst_jsn.append(jsn_doc)

    return Response(json.dumps(lst_jsn), mimetype='application/json')
    """

    """ method 1
    result = {
      'result': json_util.dumps(cursor, default=json_util.default)
    }
    return jsonify(result)
    """
    # ok but font, date
    #return json_util.dumps(cursor, default=json_util.default)
    # ok but date
    #return Response(json_util.dumps(cursor, default=json_util.default), mimetype='application/json')

    """ ok
    lst_jsn=[]
    cursor = col_geo_cnty.find({},{'_id':False})  # also ok {'_id':0}
    for n, r in enumerate(cursor):
    #    print('\n>', n)
    #    pprint(r)
        lst_jsn.append(r)

    #lst_jsn = JSONEncoder().encode(lst_jsn)
    return jsonify(result=lst_jsn)
    """
    """ ok but font
    cursor = col_geo_cnty.find({},{'_id':0})
    return str(json.dumps({'results': list(cursor)},
        default = json_util.default,
        indent = 4))
    """

    if not cnty_name:
        cursor = col_geo_cnty.find( {}, {'_id':0} ).sort(
            [ ("cnty_name", 1)]
          )
        # l = [doc['cnty_name'] for doc in cursor]
        # > db.geo_cnty.find().sort( { cnty_name: 1 } )
    else:
        #regex = "/^" + cnty_name + "$/i"
        cursor = col_geo_cnty.find(
            #{'cnty_name': re.compile(cnty_name, re.IGNORECASE) },
            #{"cnty_name":{"$regex":"" + cnty_name + "$", "$options": "-i"}}, # X
            {'cnty_name':{"$regex": cnty_name, '$options':'i'}},              # ok
            {'_id':0 }
          ).sort(
            [ ("cnty_name", 1) ]
          )
    return jsonify(result=list(cursor))


@app_geo.route('geo_cnty_code/', defaults={'cnty_name': None})
@app_geo.route('geo_cnty_code/<cnty_name>')
@login_required
def geo_cnty_code(cnty_name):
    """
    result = mongodb_geo['geo_cnty'].find_one({'cnty_code':'cz'.upper()})
    pprint(result)
    result = mongodb_geo['geo_cnty'].find_one({'cnty_name':string.capwords('belgium')})
    pprint(result)
    """

    """ sql injection: placeholders and variables
    sql = ".... LIMIT %s, %s"
    g.db.execute(sql, (limit_offset, limit_count))
    """

    search = {}
    if cnty_name:
        search = {'cnty_name': re.compile(cnty_name, re.IGNORECASE)}

    #regex = "/^" + cnty_name + "$/i"
    cursor = col_geo_cnty.find(
      search,
      #{"cnty_name":{"$regex":"" + cnty_name + "$", "$options": "-i"}},
      #{"cnty_name":{"$regex":regex}},
      {'cnty_name':1, 'cnty_code':1, 'cnty_code3':1,
       '_id':0
      }
    )
    return jsonify(result=list(cursor))


@app_geo.route('geo_city/<city_name>')
@login_required
def geo_city(city_name=None):

    cursor = col_geo_cnty.find( { }, {
      'cnty_name':1, 'cnty_code':1, 'cnty_code3':1,
      '_id':0
      }
    )
    return jsonify(result=list(cursor))

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
