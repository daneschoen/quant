import os
import datetime
import pandas as pd

import requests

from flask import session
from flask_login import login_user, logout_user, current_user, login_required, \
    confirm_login, fresh_login_required

# from apps.app_analytic.api_util import *
from .api_util import *
from apps.app_util import logger
from .instr_models import *


# from apps import app
from apps.settings.constants import *

# ==============================================================================

def go(instr_lst):
    '''
    http://localhost:8007/api/import?instr=es---us

    - return json

    - Check for files:
      instr_missing = esdata1min24hr.asc,
      econhol = excludees.txt, holes.txt, econXYZ.txt
    - Call java api
    - set InstrX.imported = True if no errors
    - import_data_pandas(instr_lst)
    '''

    if type(instr_lst) != list:
        return {
          'status_code': 500,
          'status_msg': "ERROR INTERNAL - " + "Must send list to 'import_data.go(list)'"
        }
    instr_missing, econhol_missing = verifie_datafiles_exist(instr_lst)
    if instr_missing or econhol_missing:
        err_msg = "ERROR "
        if instr_missing:
            err_msg += "- Instrument file(s) missing: "
            for instr in instr_missing:
                err_msg += instr + ', '
        if econhol_missing:
            err_msg += " - File(s) missing: "
            for x in econhol_missing:
                err_msg += x + ', '
        #sys.exit() # 0 success, 1... error
        #raise FileNotFoundError('Parameter should...')
        return {'status_code': 500, 'status_msg': err_msg}

    #verifie_javaserverapi_test()
    res_jsn = import_data_api(instr_lst)
    if res_jsn['status_code'] != 200 or res_jsn['status_msg'] != "ok":
        return res_jsn

    res_jsn = import_data_pandas_session(instr_lst)
    #if ret['status'][:5] == "ERROR":
    #    return ret

    return res_jsn   # should contain dates for each instr or ERROR for status


def verifie_datafiles_exist(instr_lst):
    instr_missing = []
    econhol_missing = []

    for instr in instr_lst:
        filename = instr + INSTR_FILENAME_1MIN24HR_SUFFIX + '.' + INSTR_FILE_EXT
        file_path = get_data_in_dir(current_user.username) + filename
        # os.path.exists(...)
        if not os.path.isfile(file_path):
            instr_missing.append(filename)
            #try:
            #  open(path_to_file)
            #  # ...
            #except  FileNotFoundError()
            #except OSError as e:
            #  print(e.args)
            #  print(os.strerror(e.errno))

        filename = 'hol' + instr + '.' + ECON_HOL_FILE_EXT
        file_path = get_data_in_dir(current_user.username) + filename
        if not os.path.isfile(file_path):
            econhol_missing.append(filename)

        filename = 'exclude' + instr + '.' + ECON_HOL_FILE_EXT
        file_path = get_data_in_dir(current_user.username) + filename
        if not os.path.isfile(file_path):
            econhol_missing.append(filename)

    for econ in ECON:
        filename = econ +  '.' + ECON_HOL_FILE_EXT
        file_path = get_data_in_dir(current_user.username) + filename
        if not os.path.isfile(file_path):
            econhol_missing.append(filename)

    return instr_missing, econhol_missing


def import_data_api(instr_lst):
    """
    http://localhost:8007/api/import?instr=es---us
    """
    res_jsn = {
      'status_code': 500,
      'status_msg': "ERROR - Importing: " + str(instr_lst)
    }
    instr_str = instr_lst[0]
    for instr in instr_lst[1:]:
        instr_str += INSTR_SEP + instr

    r = requests.get(get_api_server_url(current_user.username) + '/api/import', params={'instr': instr_str})

    #logger.info(r.status_code)  logger.info(r.text)

    if r.status_code == 200 and r.text == "ok":
        res_jsn['status_code'] = 200
        res_jsn['status_msg'] = 'ok'
    elif r.status_code == 200:
        res_jsn['status_code'] = 200
        res_jsn['status_msg'] = r.text

    return res_jsn


def import_data_pandas_session(instr_lst, instr_file_base=INSTR_FILENAME_OUT_1MIN_SUFFIX):
    '''
    data put into sessions so is cached to mongodb!

    TODO: Abstract this so next login, dont have to pd.read_csv from file:
    - insert_one({}) into mongodb,
    - update profile w id's of data
    - return profile w id's of data
      ? OR put into Session OR col_user.find_one({username})['profile'] from mongodb
    - PUT pd.df_data into Session!
    '''

    # this res_jsn gets finally returned to js
    res_jsn = { 'instr_meta': {},
                'status_msg': 'ERROR - Pandas',
                'status_code': 500
              }
    for instr in instr_lst:
        file = instr + instr_file_base + '.' + OUT_FILE_EXT   # 'esdata1col.csv'

        path_file = get_data_out_dir(current_user.username) + file
        if not os.path.isfile(path_file):
            res_jsn['status_msg'] = "ERROR - Locating: " + file
            return res_jsn

        res = import_data_pandas(path_file)
        if res['status_msg'] != 'ok':
            res_jsn['status_msg'] = res['status_msg']
            return res_jsn

        df_data = res['df_data']

        dt_lst = [str(dt)[:10] for dt in df_data.index]

        session['data'][instr] = { 'df_data': df_data,
                                   'dt_lst': dt_lst
                                 }

        #res['instr_meta'].append(
        #  { 'instr_name': instr,
        #    'dt_lst': InstrX.dt_lst
        #  })

        res_jsn['instr_meta'][instr] = {
          'dt_lst': dt_lst
        }

    res_jsn['status_msg'] = 'ok'
    res_jsn['status_code'] = 200

    return res_jsn


def import_data_pandas(path_file):
    '''
    $ cd ~/projects/rivercast/flask_blueprint; p3
    >>> import pandas as pd
    >>> from apps.app_analytic.import_data import import_data_pandas
    >>> res = import_data_pandas('~/sandbox/esdata1col.csv')
    >>> df_data = res['df_data']

    >>> df_data.columns

    >>> se_1615_1 = df_data.loc[:,'1615'].diff(periods=1)
    >>> se_ = df_data.loc[:,'1615'].diff(periods=2)

    '''

    res_jsn = {
      'df_data': None,
      'status_msg': 'ERROR'
    }
    try:
      """
      with open(file_path) as f:
        #buf = f.readlines()  # reads the entire file
        f.readline()
        for row in csv.reader(f):
            dt = datetime.datetime(int(row[2]), int(row[0]), int(row[1]))
            dt_lst.append(dt.strftime('%m/%d/%Y'))

      InstrX = Instr_Singleton(instr)
      InstrX.imported = True
      InstrX.dt_lst = dt_lst
      """

      parser = lambda M_D_Y: pd.datetime.strptime(M_D_Y, '%m %d %Y')
      df_data = pd.read_csv(path_file, parse_dates=[[0,1,2]], date_parser=parser, index_col=0)
      df_data.rename(columns=lambda x: x.replace(':', ''), inplace=True)
      df_data.index.names = ['date']

      res_jsn = {
        'df_data': df_data,
        'status_msg': 'ok'
      }

      return res_jsn

    except EnvironmentError as e: # parent of IOError, OSError *and* WindowsError where available
      res_jsn['status_msg'] = "ERROR - Reading: " + path_file + " - " + str(e)
      return res_jsn
