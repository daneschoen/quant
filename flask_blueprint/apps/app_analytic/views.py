import sys, os
import json, datetime, calendar  # from datetime import timedelta, timezone
import pytz  # from pytz import utc, timezone
import string, ast
from pprint import pprint

import pandas as pd
import numpy as np

from flask import Flask, render_template, request, redirect, url_for, \
    abort, session, \
    make_response, Response, \
    jsonify, send_from_directory

from flask_login import login_user, logout_user, current_user, login_required, \
    confirm_login, fresh_login_required

import requests
import urllib.parse
from bson.objectid import ObjectId

from apps import app
# from flask import current_app as app
from apps.app_analytic import app_analytic
from apps.app_util import col_equitycurve, logger
from apps.app_util.mongodb_debug import check_mongodb

from . import import_data
from .instr_models import *
from .api_util import *
from .grapher import *
from .stats import *

from apps.settings.constants import *


# ==============================================================================
# Routes
# ==============================================================================

# -------------------------
# Testing
# -------------------------

@app_analytic.route('test/protected')
@login_required
def protected():
    return "Working - login required working. U r: " #+ str(current_user.username) #current_user.id
    #return render_template('secret.html')

@app_analytic.route('test/test_endpoints')
def test_endpoints():
    return render_template('test_endpoints.html')

@app_analytic.route('test/logging')
def test_logging():
    logger.warning('A warning occurred (%d alert)', 91)
    logger.debug('this is debug - occurred')
    logger.error('An error occurred')
    logger.info('Info occurred')
    print('print test')
    return 'tail -20 /var/log/uwsgi/rivercast_uwsgi.log'


@app_analytic.route('test/session')
def test3():
    # X res = jsonify(session)

    session['foo'] = 'bar'
    session['user'] = current_user.username
    session['pd_'] = {'pi': 3.14, 'k': 'poo'}

    d = {}
    for k, v in session.items():
        if k == 'data':
            if 'es' in session['data']:
                d[k] = str(session[k]) #+ str(df.iloc[0,0])
            if 'us' in session['data']:
                d[k] = str(session[k]) #+ str(df.iloc[0,0])
        else:
            d[k] = v

    return jsonify(d)

@app_analytic.route('test/app_config')
def test_app_config():
    return app.config['PORT']


@app_analytic.route('test/json')
def test4():
    # old json version:
    #return make_response(jsonify({'error': 'Not found'}), 404)

    res = {
      'status': 'ok',
      'foo': 3.14,
      'instr_meta': [
        { 'instr_name': 'es',
          'dt_lst': ['12/23/2015','12/24/2015','12/25/2015']
        },
        { 'instr_name': 'cl',
          'dt_lst': ['---']
        }
      ]
    }

    res = jsonify(res)
    res.status_code = 200
    return res


@app_analytic.route('graph/chartstock_line_basic')
def chartstock_line_basic():
    return render_template('chartstock_line_basic.html')

@app_analytic.route('graph/charts_scatter_regression')
def charts_scatter_regression():
    return render_template('charts_scatter_regression.html')

@app_analytic.route('graph/charts_line_stdev')
def charts_line_stdev():
    return render_template('charts_line_stdev.html')

@app_analytic.route('graph/charts_line_zoom2_grid')
def charts_line_zoom2_grid():
    return render_template('line_zoom2_grid.html')


# ------------------------------------------------------------------------------
# Health - zdorovye
# ------------------------------------------------------------------------------
#@app.route('zdorovye/check', defaults={'component': None}')
@app_analytic.route('zdorovye/check')
@app_analytic.route('zdorovye/check/<component>')
def zdorovye_check(component=None):
    if not component:
        return "ok: Flask ok"
    elif component == "root_path":
        return app.root_path
    elif component == "api_java":
        return "ok: Received from apijava: "+ requests.get(get_api_server_url(current_user.username) + '/test').text
    elif component == "api_flask":
        return "ok: api_flask"
    elif component == 'kaktebyazovut':
        return check_kaktebyazovut()
    elif component == "mongo":
        return check_mongodb()
    return 'ok'


@app_analytic.route('zdorovye/kaktebyazovut')
def check_kaktebyazovut():
    return 'Under Construction'

@app_analytic.route('zdorovye/whoami')
def zdorovye_whoami():

    return current_user.username


@app_analytic.route('zdorovye/get_instr_info/<instr_str>', methods=['GET', 'POST'])
@login_required
def get_instr_info(instr_str):

    res_jsn = { 'msg': '',
                'status_msg': 'ERROR - Obtaining meta instrument info',
                'status_code': 500
              }

    res = requests.get(get_api_server_url(current_user.username) + '/api/instr_info', params={'instr': instr_str})

    if res.status_code == 200 and res.text[:5] != 'ERROR':
      res_jsn['status_code'] = 200
      res_jsn['status_msg'] = 'ok'
      res_jsn['msg'] = res.text
    else:
      res_jsn['status_code'] = 400
      res_jsn['status_msg'] = res.text

    res_jsn = jsonify(res_jsn)
    return res_jsn


# ------------------------------------------------------------------------------
# Main template and static templates
# ------------------------------------------------------------------------------
@app_analytic.route('analytics')
@login_required
def analytics():
    return render_template('admin_flat_boot.html')

@app_analytic.route('models_report')
@login_required
def models_report():
    return render_template('stats_instr.html')


# ==============================================================================
# Controller + views: Main, calc, import, ...
# ==============================================================================
# Init routine for frontend
@app_analytic.route('analytics/get_instr_meta/<instr_str>', methods=['GET', 'POST'])
@login_required
def get_instr_meta(instr_str):

    res_jsn = { 'instr_meta': {},   # old: []
                'instr_lst': INSTRS_NAME,
                'time_entry_lst': [],
                'status_msg': 'ERROR - Obtaining meta instrument info',
                'status_code': 500
              }

    if instr_str != 'all' and instr_str not in INSTRS_NAME:
        res_jsn['status_msg'] = 'ERROR - Invalid instrument: ' + instr_str
        res_jsn['status_code'] = 500
        return jsonify(res_jsn)

    time_entry_lst = ['C', 'O']
    dtime = datetime.datetime(2000,1,1)
    for t in range(24*60):
        time_entry_lst.append(dtime.strftime('%H:%M'))
        dtime += datetime.timedelta(minutes=MIN_INCR)
    res_jsn['time_entry_lst'] = time_entry_lst

    if instr_str == 'all':
        for instr in INSTRS_NAME:
            # InstrX = Instr_Singleton(instr)
            # res['instr_meta'].append(
            #   { 'instr_name': instr,
            #     'dt_lst': InstrX.dt_lst
            #   })

            if instr in session['data']:
                res_jsn['instr_meta'][instr] = {
                  # 'df_data': df_data,
                  'dt_lst': session['data'][instr]['dt_lst']
                }
            else:
                res_jsn['instr_meta'][instr] = {
                  # 'df_data': df_data,
                  'dt_lst': ['---']
                }

    else:
        instr = instr_str
        if instr in session['data']:
            res_jsn['instr_meta'][instr] = {
              # 'df_data': df_data,
              'dt_lst': session['data'][instr]['dt_lst']
            }
        else:
            res_jsn['instr_meta'][instr] = {
              # 'df_data': df_data,
              'dt_lst': ['---']
            }

    res_jsn['status_msg'] = 'ok'
    res_jsn['status_code'] = 200

    return jsonify(res_jsn)


# -------------------------
# Import
# -------------------------
# function getJsonAjax_import(instr){   ==>
@app_analytic.route('analytics/import_data/<instr_str>')
@login_required
def import_tick(instr_str):
    """
    http://192.241.219.240/analytics/all | es | es---us---da
    http://localhost:8007/api/import?instr=es---us---da
    """
    if instr_str == 'all':
        instr_lst = INSTRS_NAME
    else:
        instr_lst = instr_str.split(INSTRS_SEP)

    res_jsn = import_data.go(instr_lst)

    #if res[status[:5]] == 'ERROR':
    #     return jsonify(res)
    #elif ret_status[:2] == 'ok':

    #res = {}
    #for instr in instr_lst:
    #    res[instr] = Instr_Singleton(instr).dts_lst

    return jsonify(res_jsn)



# <td><a href="{{ url_for('download', filename=probleme.facture) }}">Facture</a></td>
@app_analytic.route('analytics/download/<time_per>/<instr_str>', methods=['GET', 'POST'])
@login_required
def download(time_per, instr_str):
    """ SHOULD activate either X-Sendfile support in your webserver or (if no authentication happens)
        to tell the webserver to serve files for the given path on its own without calling into the
        web application for improved performance.
    """

    if time_per == '10':
        instr_fname_suffix = INSTR_FILENAME_OUT_10MIN_SUFFIX
    elif time_per == '5':
        instr_fname_suffix = INSTR_FILENAME_OUT_5MIN_SUFFIX
    elif time_per == '1':
        instr_fname_suffix = INSTR_FILENAME_OUT_1MIN_SUFFIX
    else:
        return

    #instr_lst = instr_str.split(INSTRS_SEP)
    #for instr in instr_lst:
    # abspath = os.path.join(current_app.root_folder, app.config['UPLOAD_FOLDER'])
    filename = instr_str + instr_fname_suffix + '.' + OUT_FILE_EXT
    file_path = get_data_out_dir(current_user.username) + filename
    if not os.path.isfile(file_path):
        return "ERROR -  Not found: " + filename
    return download_file(file_path)

def download_file(file_path):
    fname = os.path.basename(file_path)
    if not os.path.isfile(file_path):
        # head, tail = os.path.split("/tmp/d/a.dat")
        #return "ERROR: " + os.path.basename(file_path) + " not found"
        return "ERROR - Not found: " + fname
    #return send_file('sample_simple.csv', as_attachment=True)
    #return send_from_directory(app.config['UPLOAD_FOLDER'],
    return send_from_directory(get_data_out_dir(current_user.username)[:-1], fname, as_attachment=True)


# -------------------------
# Calc
# -------------------------
@app_analytic.route('analytics/calc', methods=['GET','POST'])
@login_required
def calc():
    """
    - in js: clean up all inputs and validate before sending
    - in python: clean up all inputs and validate, instr loaded etc
    - call java api: clean up all inputs and validate, instr loaded etc

    Test in python:
    from flask_apps.api_util import *
    from flask_apps.globals import *
    calc_param_apijava = {'depInstr':'es', 'condition':'c >c1+5\n  hol(-1)\n hi + 3.4<= p@1226', 'viewoptions':'foobar(-1)'}
    api_get(API_SERVER_URL + '/api/calc', **calc_param_apijava)

    import requests
    r = requests.get("http://localhost:8007/test")
    r = requests.get("http://localhost:8007/api/calc", params=calc_param_apijava)
    """

    res_jsn = {
      'status_msg': 'ERROR - Calc',
      'status_code': 500,
      'msg': ''
    }
    calc_param = {}
    calc_param_apijava = {}
    if request.method == 'POST':
      calc_param['condition'] = request.form.get('condition')
      calc_param['instr_dep'] = request.form.get('instr')
      calc_param['dt_beg_indx'] = request.form.get('dt_beg_indx')
      calc_param['dt_end_indx'] = request.form.get('dt_end_indx')
      calc_param['dt_beg'] = request.form.get('dt_beg')
      calc_param['dt_end'] = request.form.get('dt_end')
      calc_param['time_entry'] = request.form.get('time_entry')
      calc_param['viewoption'] = request.form.get('viewoptions')
      calc_param['bl_postscenario_hilo'] = request.form.get('bl_scenario_hilo')
      calc_param['bl_postfilter_recprof'] = request.form.get('bl_scenario_recprof')
      calc_param['postscenario'] = request.form.get('scenario')
    else:
      calc_param['condition'] = request.args.get('condition')
      calc_param['instr_dep'] = request.args.get('instr')
      calc_param['dt_beg_indx'] = request.args.get('dt_beg_indx')
      calc_param['dt_end_indx'] = request.args.get('dt_end_indx')
      calc_param['dt_beg'] = request.args.get('dt_beg')
      calc_param['time_entry'] = request.args.get('time_entry')
      calc_param['dt_end'] = request.args.get('dt_end')
      calc_param['viewoption'] = request.args.get('viewoptions')
      calc_param['bl_postscenario_hilo'] = request.args.get('bl_scenario_hilo')
      calc_param['bl_postfilter_recprof'] = request.args.get('bl_scenario_recprof')
      calc_param['postscenario'] = request.args.get('scenario')

    # Clean up
    for k, v in calc_param.items():
      calc_param[k] = v.strip().lower()

    condition_lst_tmp = []
    for l in calc_param['condition'].split('\n'):
      if not l.lstrip():
        continue
      condition_lst_tmp.append(l.strip())
    calc_param['condition'] = condition_lst_tmp

    viewoption_lst_tmp = [l.strip() for l in calc_param['viewoption'].split('\n') if l.strip()]
    calc_param['viewoption'] = viewoption_lst_tmp
    postscenario_lst_tmp = [l.strip() for l in calc_param['postscenario'].split('\n') if l.strip()]
    calc_param['postscenario'] = postscenario_lst_tmp

    #for cmdline in calc_param['postscenario']:
    #  if 'hilo' in cmdline:
    #    calc_param['postscenario_hilo'] = cmdline
    #  if 'recprof' in cmdline:
    #    calc_param['postfilter_recprof'] = cmdline

    # Java api stuff
    calc_param_apijava['InstrDep'] = calc_param['instr_dep']
    calc_param_apijava['dt_beg'] = calc_param['dt_beg']
    calc_param_apijava['dt_end'] = calc_param['dt_end']
    calc_param_apijava['dt_beg_indx'] = calc_param['dt_beg_indx']
    calc_param_apijava['dt_end_indx'] = calc_param['dt_end_indx']
    calc_param_apijava['timeEnter'] = calc_param['time_entry']
    calc_param_apijava['condition'] = '\n'.join(calc_param['condition']).replace(' ','___').replace('=','__eq')
    calc_param_apijava['viewoption'] = '\n'.join(calc_param['viewoption']).replace(' ','___').replace('=','__eq')
    calc_param_apijava['postscenario'] = '\n'.join(calc_param['postscenario']).replace(' ','___').replace('=','__eq')
    calc_param_apijava['bl_postscenario_hilo'] = calc_param['bl_postscenario_hilo']
    calc_param_apijava['bl_postfilter_recprof'] = calc_param['bl_postfilter_recprof']
    #calc_param_apijava['postscenario_hilo'] = urllib.parse.quote_plus('p > r2 + 3.14= 20')
    #calc_param_apijava['postfilter_recprof'] = calc_param['postfilter_recprof']
    calc_param_apijava['username'] = current_user.username

    # DEBUG
    ## res  = { 'condition': calc_param_apijava['condition'] }

    # ', '.join(map(str, list_of_ints))
    #getparamstr = ""
    #for k, v in calc_params_apijava.items():
    #    getparamstr += (k + '=' + v + '&')
    #getparamstr = getparamstr[:-1]
    #getparamstr = '&'.join("{0}={1}".format(k,v) in calc_params_apijava.items())
    # JS: s = "0,1"
    #     var array = JSON.parse("[" + string + "]"); gives array of numbers
    # s.split()  ==>  ["0", "1"]
    # Call java api
    #res = api_get(API_SERVER_URL + '/api/calc', **calc_param_apijava)
    res = requests.get(get_api_server_url(current_user.username) + '/api/calc', params=calc_param_apijava)

    if res.status_code == 200 and res.text[:5] != 'ERROR':
      res_jsn['status_code'] = 200
      res_jsn['status_msg'] = 'ok'

      if calc_param['bl_postscenario_hilo'] != 'true':
        res_jsn['msg'] = res.text
      else:
        # Parse out 2 sections:
        # - statistics+hilo, 'CHART_DATA_LONG:'
        statistics_hilo_chart =  res.text.split('CHART_DATA_LONG:')
        statistics_hilo = statistics_hilo_chart[0].strip()
        chart_data_str = statistics_hilo_chart[1].strip()

        # Date.parse("12/25/2015") => 1450994400000
        lst_chart_series = convert_str_epoch([chart_data_str])
        #lst_chart_series = [[[1278190800000, 3.14], [1450994400000, 6.22]],
        #                    [[1278190800000, 3.14], [1450994400000, 6.22]]]

        # Mongodb insert into capped collection
        dict_chart_data = {
          "user": current_user.username,
          "chart_type": "equitycurve",
          "chart_data_long": lst_chart_series[0],    #[[12345,3.14],[67899,6.22]],
          "date": datetime.datetime.utcnow()
        }

        result = col_equitycurve.update(
          {"user": current_user.username, "chart_type": "equitycurve"},
          dict_chart_data,
          upsert=True
        )
        res_jsn['msg'] = statistics_hilo

    else:
      res_jsn['status_code'] = 400
      res_jsn['status_msg'] = res.text

    res_jsn = jsonify(res_jsn)
    return res_jsn


# -------------------------
# Modules
# -------------------------

@app_analytic.route('analytics/module/survival', methods=['GET','POST'])
@login_required
def module_survival():
    """
    - in js: clean up all inputs and validate before sending
    - in python: clean up all inputs and validate, instr loaded etc
    - call java api: clean up all inputs and validate, instr loaded etc
    """
    res_jsn = {
      'status_msg': 'ERROR - Module Survival',
      'status_code': 500,
      'msg': ''
    }

    param = {}
    param_apijava = {}
    if request.method == 'POST':
      param['feature'] = request.form.get('feature')
      param['instr_dep'] = request.form.get('instr_dep')
      param['dt_beg_indx'] = request.form.get('dt_beg_indx')
      param['dt_end_indx'] = request.form.get('dt_end_indx')
      param['dt_beg'] = request.form.get('dt_beg')
      param['dt_end'] = request.form.get('dt_end')
      param['entry_time'] = request.form.get('entry_time')
      param['mod_timetarget_day'] = request.form.get('mod_timetarget_day')
      param['mod_timetarget_time'] = request.form.get('mod_timetarget_time')
      param['mod_wait_time'] = request.form.get('mod_wait_time')

    else:
      param['feature'] = request.args.get('feature')
      param['instr_dep'] = request.args.get('instr_dep')
      param['dt_beg_indx'] = request.args.get('dt_beg_indx')
      param['dt_end_indx'] = request.args.get('dt_end_indx')
      param['dt_beg'] = request.args.get('dt_beg')
      param['dt_end'] = request.args.get('dt_end')
      param['entry_time'] = request.args.get('entry_time')
      param['mod_timetarget_day'] = request.args.get('mod_timetarget_day')
      param['mod_timetarget_time'] = request.args.get('mod_timetarget_time')
      param['mod_wait_time'] = request.args.get('mod_wait_time')

    # Clean up
    for k, v in param.items():
      param[k] = v.strip().lower()

    feature_lst_tmp = []
    for l in param['feature'].split('\n'):
      if not l.lstrip():
        continue
      feature_lst_tmp.append(l.strip())
    param['feature_lst'] = feature_lst_tmp

    # Java api
    param_apijava['instr_dep'] = param['instr_dep']
    param_apijava['dt_beg'] = param['dt_beg']
    param_apijava['dt_end'] = param['dt_end']
    param_apijava['dt_beg_indx'] = param['dt_beg_indx']
    param_apijava['dt_end_indx'] = param['dt_end_indx']
    param_apijava['entry_time'] = param['entry_time']
    param_apijava['feature'] = '\n'.join(param['feature_lst']).replace(' ','___').replace('=','__eq')
    param_apijava['mod_timetarget_day'] = param['mod_timetarget_day']
    param_apijava['mod_timetarget_time'] = param['mod_timetarget_time']
    param_apijava['mod_wait_time'] = param['mod_wait_time']
    param_apijava['username'] = current_user.username

    ## DEBUG
    #res_jsn['msg']  = \
    #  { 'mod_timetarget_day': param_apijava['mod_timetarget_day'],
    #    'mod_timetarget_time': param_apijava['mod_timetarget_time'],
    #    'mod_wait_time': param_apijava['mod_wait_time']
    #  }
    #res_jsn['status_msg'] = 'ok'
    #res_jsn['status_code'] = 200
    #return jsonify(res_jsn)
    # ', '.join(map(str, list_of_ints))
    #getparamstr = ""
    #for k, v in calc_params_apijava.items():
    #    getparamstr += (k + '=' + v + '&')
    #getparamstr = getparamstr[:-1]
    #getparamstr = '&'.join("{0}={1}".format(k,v) in param_apijava.items())

    # Call java api
    res = requests.get(get_api_server_url(current_user.username) + '/api/module/survival', params=param_apijava)

    if res.status_code == 200 and res.text[:5] != 'ERROR':
      res_jsn['status_code'] = res.status_code
      res_jsn['status_msg'] = 'ok'
      res_jsn['msg'] = res.text
    else:
      res_jsn['status_code'] = res.status_code
      res_jsn['status_msg'] = res.text

    res_jsn = jsonify(res_jsn)
    return res_jsn


@app_analytic.route('analytics/module/systrade', methods=['GET','POST'])
@login_required
def module_systrade():
    """
    - in js: clean up all inputs and validate before sending
    - in python: clean up all inputs and validate, instr loaded etc
    - call java api: clean up all inputs and validate, instr loaded etc
    """
    res_jsn = {
      'status_msg': 'ERROR - Module SysTrade',
      'status_code': 500,
      'msg': '',
      'chart_data_long': '',
      'chart_data_short': ''
    }

    param = {}
    param_apijava = {}
    if request.method == 'POST':
      param['feature'] = request.form.get('feature')
      #param['viewoption'] = request.form.get('viewoption')
      param['instr_dep'] = request.form.get('instr_dep')
      param['dt_beg_indx'] = request.form.get('dt_beg_indx')
      param['dt_end_indx'] = request.form.get('dt_end_indx')
      param['dt_beg'] = request.form.get('dt_beg')
      param['dt_end'] = request.form.get('dt_end')
      param['entry_time'] = request.form.get('entry_time')
      param['mod_maxopencontract'] = request.form.get('mod_maxopencontract')
      param['mod_bl_exit_feature'] = request.form.get('mod_bl_exit_feature')
      param['mod_bl_profittarget'] = request.form.get('mod_bl_profittarget')
      param['mod_profittarget'] = request.form.get('mod_profittarget')
      param['mod_bl_stoploss'] = request.form.get('mod_bl_stoploss')
      param['mod_stoploss'] = request.form.get('mod_stoploss')
      param['mod_bl_timetarget'] = request.form.get('mod_bl_timetarget')
      param['mod_timetarget_day'] = request.form.get('mod_timetarget_day')
      param['mod_timetarget_time'] = request.form.get('mod_timetarget_time')
      param['bl_postfilter_recprof'] = request.form.get('bl_scenario_recprof')
      param['postscenario'] = request.form.get('scenario')

    else:
      param['feature'] = request.args.get('feature')
      #param['viewoption'] = request.args.get('viewoption')
      param['instr_dep'] = request.args.get('instr_dep')
      param['dt_beg_indx'] = request.args.get('dt_beg_indx')
      param['dt_end_indx'] = request.args.get('dt_end_indx')
      param['dt_beg'] = request.args.get('dt_beg')
      param['dt_end'] = request.args.get('dt_end')
      param['entry_time'] = request.args.get('entry_time')
      param['mod_maxopencontract'] = request.args.get('mod_maxopencontract')
      param['mod_bl_exit_feature'] = request.args.get('mod_bl_exit_feature')
      param['mod_bl_profittarget'] = request.args.get('mod_bl_profittarget')
      param['mod_profittarget'] = request.args.get('mod_profittarget')
      param['mod_bl_stoploss'] = request.args.get('mod_bl_stoploss')
      param['mod_stoploss'] = request.args.get('mod_stoploss')
      param['mod_bl_timetarget'] = request.args.get('mod_bl_timetarget')
      param['mod_timetarget_day'] = request.args.get('mod_timetarget_day')
      param['mod_timetarget_time'] = request.args.get('mod_timetarget_time')
      param['bl_postfilter_recprof'] = request.args.get('bl_scenario_recprof')
      param['postscenario'] = request.args.get('scenario')

    # Clean up
    for k, v in param.items():
      param[k] = v.strip().lower()

    feature_lst_tmp = []
    for l in param['feature'].split('\n'):
      if not l.lstrip():
        continue
      feature_lst_tmp.append(l.strip())
    param['feature_lst'] = feature_lst_tmp

    #viewoption_lst_tmp = [l.strip() for l in param['viewoption'].split('\n') if l.strip()]
    #param['viewoption'] = viewoption_lst_tmp
    postscenario_lst_tmp = [l.strip() for l in param['postscenario'].split('\n') if l.strip()]
    param['postscenario'] = postscenario_lst_tmp

    # Java api stuff
    param_apijava['instr_dep'] = param['instr_dep']
    param_apijava['dt_beg'] = param['dt_beg']
    param_apijava['dt_end'] = param['dt_end']
    param_apijava['dt_beg_indx'] = param['dt_beg_indx']
    param_apijava['dt_end_indx'] = param['dt_end_indx']
    param_apijava['entry_time'] = param['entry_time']
    param_apijava['feature'] = '\n'.join(param['feature_lst']).replace(' ','___').replace('=','__eq')
    #param_apijava['viewoption'] = '\n'.join(param['viewoption']).replace(' ','___').replace('=','__eq')
    param_apijava['mod_maxopencontract'] = param['mod_maxopencontract']
    param_apijava['mod_bl_exit_feature'] = param['mod_bl_exit_feature']
    param_apijava['mod_bl_profittarget'] = param['mod_bl_profittarget']
    param_apijava['mod_profittarget'] = param['mod_profittarget']
    param_apijava['mod_bl_stoploss'] = param['mod_bl_stoploss']
    param_apijava['mod_stoploss'] = param['mod_stoploss']
    param_apijava['mod_bl_timetarget'] = param['mod_bl_timetarget']
    param_apijava['mod_timetarget_day'] = param['mod_timetarget_day']
    param_apijava['mod_timetarget_time'] = param['mod_timetarget_time']
    param_apijava['postscenario'] = '\n'.join(param['postscenario']).replace(' ','___').replace('=','__eq')
    param_apijava['bl_postfilter_recprof'] = param['bl_postfilter_recprof']
    param_apijava['username'] = current_user.username

    ## D
    #logger.debug(param_apijava['postscenario'])
    #logger.debug(param_apijava['bl_postfilter_recprof'])
    #res_jsn = {'status_code': 200}
    ##res['text'] = ' => '.join(param_apijava)
    #res_jsn['msg'] = ' !! '.join([k + ' : '+ v for k,v in param_apijava.items()])
    #res_jsn['status_msg'] = 'ok'
    #return jsonify(res_jsn)

    # Call java api
    res = requests.get(get_api_server_url(current_user.username) + '/api/module/systrade', params=param_apijava)

    if res.status_code == 200 and res.text[:5] != 'ERROR':
      res_jsn['status_code'] = res.status_code
      res_jsn['status_msg'] = 'ok'

      # Parse out 3 sections:
      # - the systrade statistics, 'CHART_DATA_LONG:', 'CHART_DATA_SHORT:'
      systrade_all =  res.text.split('CHART_DATA_LONG:')
      systrade_statistics_str = systrade_all[0].strip()
      systrade_chart_data_str = systrade_all[1].strip()
      systrade_chart_data_str = systrade_chart_data_str.split('CHART_DATA_SHORT:')
      systrade_chart_data_str_long = systrade_chart_data_str[0].strip()
      systrade_chart_data_str_short = systrade_chart_data_str[1].strip()

      lst_chart_series = convert_str_epoch([systrade_chart_data_str_long, systrade_chart_data_str_short])

      # Mongodb UPSERT into capped collection
      dict_chart_data = {
        "user": current_user.username,
        "chart_type": "equitycurve",
        "chart_data_long": lst_chart_series[0],    #[[12345,3.14],[67899,6.22]],
        "chart_data_short": lst_chart_series[1],    #[[654321,-89],[99876,-21]],
        "date": datetime.datetime.utcnow()
      }

      #from copy import deepcopy
      #dict_chart_data = deepcopy(dict_chart_data)
      #dict_chart_data.pop("_id", None)

      #result_id = col_equitycurve.insert_one(dict_chart_data).inserted_id
      #result = col_equitycurve.replace_one(
      #    {"user": current_user.username},
      #    dict_chart_data
      #)
      result = col_equitycurve.update(
        {"user": current_user.username, "chart_type": "equitycurve"},
        dict_chart_data,
        upsert=True
      )

      # no longer really need to return chart_data series now ...
      res_jsn['msg'] = systrade_statistics_str
      res_jsn['chart_data_long'] = str(lst_chart_series[0])
      res_jsn['chart_data_short'] = str(lst_chart_series[1])

    else:
      res_jsn['status_code'] = res.status_code
      res_jsn['status_msg'] = res.text

    res_jsn = jsonify(res_jsn)
    return res_jsn


@app_analytic.route('analytics/module/systrade/chart_equitycurve/<side>')
@login_required
def chart_equitycurve(side):
    bl_rm = False
    if side == 'long_rm':
      side = 'long'
      bl_rm = True
    elif side == 'short_rm':
      side = 'short'
      bl_rm = True
    # retrieve fr mongodb
    result = col_equitycurve.find_one({"user": current_user.username, 'chart_type':'equitycurve'})
    chart_data = result['chart_data_' + side]
    chart_title = 'Equity Curve - ' + side
    chart_title = chart_title.title()

    #col_equitycurve.drop()
    #col_equitycurve.delete_many({})
    if bl_rm:
      #result = col_equitycurve.delete_many({"user": current_user.username})
      result = col_equitycurve.remove({'user': current_user.username, 'chart_type':'equitycurve'})
    return render_template('chart_equitycurve.html',
                            chart_title=chart_title,
                            chart_data=chart_data)

@app_analytic.route('analytics/module/systrade/chart_data_equitycurve/<side>')
@login_required
def chart_data_equitycurve(side):
    # retrieve fr mongodb BUT KEEP CHART DATA
    result = col_equitycurve.find_one({"user": current_user.username, 'chart_type':'equitycurve'})
    chart_data = result['chart_data_' + side]
    # keep chart data
    # result = col_equitycurve.delete_many({"user": current_user.username})
    return jsonify(chart_data)

@app_analytic.route('analytics/module/systrade/chart_equitycurve2', methods=['GET', 'POST'])
@login_required
def chart_equitycurve_post():
    if request.method == 'POST':
      side = request.json['side']
      chart_data = request.json['chart_data']
      return render_template('chart_equitycurve.html',
                            chart_data=chart_data, chart_title='SysTrade - ' + string.capwords(side))

@app_analytic.route('analytics/module/equitycurve', methods=['GET','POST'])
def module_equitycurve():
    """
    - in js: clean up all inputs and validate before sending
    - in python: clean up all inputs and validate, instr loaded etc
    - call java api: clean up all inputs and validate, instr loaded etc
    """

    res_jsn = {
      'status_msg': 'ERROR - Module EquityCurve',
      'status_code': 500,
      'msg': '',
      'chart_data_long': '',
      'chart_data_short': ''
    }

    param = {}
    param_apijava = {}
    if request.method == 'POST':
      param['feature'] = request.form.get('feature')
      param['instr_dep'] = request.form.get('instr_dep')
      param['dt_beg_indx'] = request.form.get('dt_beg_indx')
      param['dt_end_indx'] = request.form.get('dt_end_indx')
      param['dt_beg'] = request.form.get('dt_beg')
      param['dt_end'] = request.form.get('dt_end')
      param['entry_time'] = request.form.get('entry_time')
      param['mod_timetarget_day'] = request.form.get('mod_timetarget_day')
      param['mod_timetarget_time'] = request.form.get('mod_timetarget_time')
      param['bl_postfilter_recprof'] = request.form.get('bl_scenario_recprof')
      param['postscenario'] = request.form.get('scenario')

    else:
      param['feature'] = request.args.get('feature')
      param['instr_dep'] = request.args.get('instr_dep')
      param['dt_beg_indx'] = request.args.get('dt_beg_indx')
      param['dt_end_indx'] = request.args.get('dt_end_indx')
      param['dt_beg'] = request.args.get('dt_beg')
      param['dt_end'] = request.args.get('dt_end')
      param['entry_time'] = request.args.get('entry_time')
      param['mod_timetarget_day'] = request.args.get('mod_timetarget_day')
      param['mod_timetarget_time'] = request.args.get('mod_timetarget_time')
      param['bl_postfilter_recprof'] = request.args.get('bl_scenario_recprof')
      param['postscenario'] = request.args.get('scenario')

    # Clean up
    for k, v in param.items():
      param[k] = v.strip().lower()

    feature_lst_tmp = []
    for l in param['feature'].split('\n'):
      if not l.lstrip():
        continue
      feature_lst_tmp.append(l.strip())
    param['feature_lst'] = feature_lst_tmp

    #viewoptions_lst_tmp = [l.strip() for l in param['viewoptions'].split('\n') if l.strip()]
    #param['viewoptions'] = viewoptions_lst_tmp
    postscenario_lst_tmp = [l.strip() for l in param['postscenario'].split('\n') if l.strip()]
    param['postscenario'] = postscenario_lst_tmp

    # Java api stuff
    param_apijava['instr_dep'] = param['instr_dep']
    param_apijava['dt_beg'] = param['dt_beg']
    param_apijava['dt_end'] = param['dt_end']
    param_apijava['dt_beg_indx'] = param['dt_beg_indx']
    param_apijava['dt_end_indx'] = param['dt_end_indx']
    param_apijava['entry_time'] = param['entry_time']
    param_apijava['feature'] = '\n'.join(param['feature_lst']).replace(' ','___').replace('=','__eq')
    param_apijava['mod_timetarget_day'] = param['mod_timetarget_day']
    param_apijava['mod_timetarget_time'] = param['mod_timetarget_time']
    param_apijava['postscenario'] = '\n'.join(param['postscenario']).replace(' ','___').replace('=','__eq')
    param_apijava['bl_postfilter_recprof'] = param['bl_postfilter_recprof']
    param_apijava['username'] = current_user.username

    # Call java api
    res = requests.get(get_api_server_url(current_user.username) + '/api/module/equitycurve', params=param_apijava)

    if res.status_code == 200 and res.text[:5] != 'ERROR':
      # Parse out 2 sections:
      # - the systrade statistics, 'CHART_DATA_LONG:'
      statistics_chart_data_str =  res.text.split('CHART_DATA_LONG:')
      statistics_str = statistics_chart_data_str[0].strip()
      chart_data_str = statistics_chart_data_str[1].strip()

      lst_chart_series = convert_str_epoch([chart_data_str])

      # Mongodb insert into capped collection
      dict_chart_data = {
        "user": current_user.username,
        "chart_type": "equitycurve",
        "chart_data_long": lst_chart_series[0],    #[[12345,3.14],[67899,6.22]],
        "date": datetime.datetime.utcnow()
      }

      result = col_equitycurve.update(
        {"user": current_user.username, "chart_type": "equitycurve"},
        dict_chart_data,
        upsert=True
      )

      res_jsn['status_code'] = res.status_code
      res_jsn['status_msg'] = 'ok'
      res_jsn['msg'] = statistics_str   # res.text
    else:
      res_jsn['status_code'] = res.status_code
      res_jsn['status_msg'] = res.text

    res_jsn = jsonify(res_jsn)
    return res_jsn


@app_analytic.route('analytics/module/regression/chart_scatter/<rm>', methods=['GET', 'POST'])
@login_required
def chart_regression(rm):
    bl_rm = True
    if rm != 'rm' or rm == 'false':
      bl_rm = False
    # retrieve fr mongodb
    #result = col_regression.find_one({"user": current_user.username, 'chart_type':'regression'})
    #chart_data = result['chart_data_' + side]

    #if bl_rm:
    #  result = col_equitycurve.remove({'user': current_user.username, 'chart_type':'regression'})
    return render_template('chart_scatter_regression.html')
                            #chart_title='Regression - Scatter Chart'
                            #chart_data=chart_data)


@app_analytic.route('analytics/module/regression', methods=['GET','POST'])
@login_required
def module_regression():
    res_jsn = {
      'status_msg': 'ERROR - Module Regression',
      'status_code': 500,
      'msg': ''
    }

    param = {}
    param_apijava = {}

    if request.method == 'POST':
      #param['feature'] = request.form.get('feature')
      #param['viewoption'] = request.form.get('viewoption')
      param['instr_dep'] = request.form.get('instr_dep')
      param['dt_beg_indx'] = request.form.get('dt_beg_indx')
      param['dt_end_indx'] = request.form.get('dt_end_indx')
      param['dt_beg'] = request.form.get('dt_beg')
      param['dt_end'] = request.form.get('dt_end')
      param['entry_time'] = request.form.get('entry_time')
      param['mod_y'] = request.form.get('mod_y')
      param['mod_x1'] = request.form.get('mod_x1')
      param['mod_x2'] = request.form.get('mod_x2')
      param['mod_x3'] = request.form.get('mod_x3')
      param['mod_x4'] = request.form.get('mod_x4')
      param['mod_x5'] = request.form.get('mod_x5')
      param['mod_x6'] = request.form.get('mod_x6')

    else:
      #param['feature'] = request.args.get('feature')
      #param['viewoption'] = request.args.get('viewoption')
      param['instr_dep'] = request.args.get('instr_dep')
      param['dt_beg_indx'] = request.args.get('dt_beg_indx')
      param['dt_end_indx'] = request.args.get('dt_end_indx')
      param['dt_beg'] = request.args.get('dt_beg')
      param['dt_end'] = request.args.get('dt_end')
      param['entry_time'] = request.args.get('entry_time')
      param['mod_y'] = request.args.get('mod_y')
      param['mod_x1'] = request.args.get('mod_x1')
      param['mod_x2'] = request.args.get('mod_x2')
      param['mod_x3'] = request.args.get('mod_x3')
      param['mod_x4'] = request.args.get('mod_x4')
      param['mod_x5'] = request.args.get('mod_x5')
      param['mod_x6'] = request.args.get('mod_x6')

    # Clean up
    for k, v in param.items():
      param[k] = v.strip().lower()

    #feature_lst_tmp = []
    #for l in param['feature'].split('\n'):
    #  if not l.lstrip():
    #    continue
    #  feature_lst_tmp.append(l.strip())
    #param['feature_lst'] = feature_lst_tmp

    #viewoption_lst_tmp = [l.strip() for l in param['viewoption'].split('\n') if l.strip()]
    #param['viewoption'] = viewoption_lst_tmp

    # Java api stuff
    param_apijava['instr_dep'] = param['instr_dep']
    param_apijava['dt_beg'] = param['dt_beg']
    param_apijava['dt_end'] = param['dt_end']
    param_apijava['dt_beg_indx'] = param['dt_beg_indx']
    param_apijava['dt_end_indx'] = param['dt_end_indx']
    param_apijava['entry_time'] = param['entry_time']
    #param_apijava['feature'] = '\n'.join(param['feature_lst']).replace(' ','___').replace('=','__eq')
    #param_apijava['viewoption'] = '\n'.join(param['viewoption']).replace(' ','___').replace('=','__eq')
    param_apijava['mod_y'] = urllib.parse.quote_plus(param['mod_y'])
    param_apijava['mod_x1'] = urllib.parse.quote_plus(param['mod_x1'])
    param_apijava['mod_x2'] = urllib.parse.quote_plus(param['mod_x2'])
    param_apijava['mod_x3'] = urllib.parse.quote_plus(param['mod_x3'])
    param_apijava['mod_x4'] = urllib.parse.quote_plus(param['mod_x4'])
    param_apijava['mod_x5'] = urllib.parse.quote_plus(param['mod_x5'])
    param_apijava['mod_x6'] = urllib.parse.quote_plus(param['mod_x6'])
    param_apijava['username'] = current_user.username

    # Call java api
    res = requests.get(get_api_server_url(current_user.username) + '/api/module/regression', params=param_apijava)

    if res.status_code == 200 and res.text[:5] != 'ERROR':
      # Retrieves str ver of lst of lst of
      # "DATA_SERIES_NAME:" + Arrays.deepToString(grapher.series_name));
      # "DATA_SERIES_DTSTR:" + Arrays.deepToString(grapher.series_dtstr));
      # "DATA_SERIES_FD:" + Arrays.deepToString(grapher.series_fd));
      #
      # fd: [[val_y_0, val_y_1], ..., val_y_M],
      #      [val_x1_0, val_x1_1], .. , val_x1_M],
      #      ...
      #      N
      #     ]
      #
      # 0> Parse name, dtstr, fd
      # 1> convert to lst of obj
      # 2> statsmodels linear regression
      # 3> mongo upsert stats + chart data
      # 4> render stats => js frontend => render chart

      # 0) Parse out 3 sections, all series:
      str_serieset =  res.text.split('DATA_SERIES_NAME:')
      str_serieset1 =  str_serieset[1].split('DATA_SERIES_DTSTR:')
      strlst_series_namestr = str_serieset1[0].strip()
      str_serieset2 = str_serieset1[1].split('DATA_SERIES_FD:')
      strlst_series_dtstr = str_serieset2[0].strip()
      strlst_series_fd = str_serieset2[1].strip()

      # 1) convert to lst of obj
      lst_series_namestr = convert_strlst_str(strlst_series_namestr)
      lst_series_epoch = convert_strlst_dtstr_epoch(strlst_series_dtstr)
      lst_series_fd = convert_strlst_fd(strlst_series_fd)

      # 2) statsmodels linear regression
      blstr_plot = "false"
      stats, series_regression = go_regression(lst_series_namestr, lst_series_fd[0], lst_series_fd[1:], **{'bl_matplotlib': True})
      if len(lst_series_fd[1:]) == 1:
          blstr_plot = "true"
      #D stats = str(lst_series_namestr) + "  " + str(lst_series_epoch[0:5]) + "  " + str(lst_series_fd)

      # 3) Mongodb insert into capped collection:
      dict_chart_data = {
        "user": current_user.username,
        "chart_type": "regression_scatter_line",
        "stats": stats,
        #"series_scatter": lst_series_namestr,
        "series_scatter": (lst_series_fd[0], lst_series_fd[1:]),
        #"series_regression": series_regression.tolist(),
        "date": datetime.datetime.utcnow()
      }
      # Replaces entire doc - should use $set ... but ok either way here
      result = col_equitycurve.update(
        {"user": current_user.username, "chart_type": "regression_scatter_line"},
        dict_chart_data,
        upsert=True
      )

      # 4) render stats => js frontend => render chart
      res_jsn['status_code'] = res.status_code
      res_jsn['status_msg'] = 'ok'
      res_jsn['blstr_plot'] = blstr_plot
      res_jsn['username'] = current_user.username
      res_jsn['msg'] = stats
    else:
      res_jsn['status_code'] = res.status_code
      res_jsn['status_msg'] = res.text

    res_jsn = jsonify(res_jsn)
    return res_jsn
