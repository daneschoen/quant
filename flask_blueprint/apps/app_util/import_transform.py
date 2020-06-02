import inspect
import builtins

import os, sys
import datetime
import re
import zipfile

import pandas as pd
import numpy as np

# /Users/acrosspond/Agape/development/ml_stat_quant/trade_quant/trade_strategy/
pth_wrk = os.getcwd()  # X! - ONLY in IPYTHON
pth_wrk = os.path.abspath(os.path.dirname( __file__ ))

print(pth_wrk, end="\n\n")

if pth_wrk[:6] == '/Users':
    os.system('touch /var/log/uwsgi/flask.log')
    pth_root = pth_wrk[:pth_wrk.find('development')+12]
else:
    pth_root = pth_wrk[:pth_wrk.find('Agape')]
# pth_proj_fin = "projects/fintech/"
pth_proj_fin_app = "projects/fintech/flask_blueprint/"
# pth_proj_fin_app_quant = "projects/fintech/flask_blueprint/apps/app_quant"
# pth_proj_fin_app_constants = "projects/fintech/flask_blueprint/apps/settings"
# pth_proj_fin_data_in = "projects/fintech/data_in/"

# # PATH_FIN_FLASK = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../..', PROJ_FIN_FLASK))
# path_proj = os.path.abspath(os.path.join(pth_wrk, rel_pth, pth_proj_fin))
path_app = os.path.abspath(os.path.join(pth_root, pth_proj_fin_app))
# path_app_quant = os.path.abspath(os.path.join(pth_wrk, rel_pth, pth_proj_fin_app_quant))
# path_app_constants = os.path.abspath(os.path.join(pth_wrk, rel_pth, pth_proj_fin_app_constants))
# path_data_in = os.path.abspath(os.path.join(pth_wrk, rel_pth, pth_proj_fin_data_in))

# sys.path.append(path_proj)
sys.path.append(path_app)
# sys.path.append(path_app_constants)
# sys.path.append(path_data_in)

from apps.app_util.util_json import jprint

from apps.settings.constants_fin import *  # INSTR_SPECS as InstrX
from apps.settings.settings import PATH_PROJ, PATH_APP, PATH_DATA_IN

# ==============================================================================
# pth_wrk = os.path.join(PATH_PROJ, "data_in")

# pth_equity = "data_in/equity/"
# pth_com_fx = "data_in/com_fx/"
# pth_econ = "data_in/econ/"
# pth_crypto = "data_in/crypto/"

# PATH_FUT = os.path.join(PATH_PROJ, pth_fut)
# PATH_DATA_SP500 = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../..', pth_sp500))
# pth_stk_SP500 = os.path.join(PATH_PROJ, pth_stk_sp500)
    # cur_path = os.getcwd()
    # if cur_path[:7] == '/Users/':
    #     PROJ_ROOT = cur_path.rsplit('/', 3)
"""
# ------------------------------------------------------------------------------
# CONVENTION:
# pth_[asset]_[group]
# ------------------------------------------------------------------------------
"""
pth_fut_use = "fut/use_1min/"  # "fut/fut_2005__2018/"   INSTR_SPECS['fut']['path']   #
pth_stk_sp500 = "stk/sp500_1min/"  # INSTR_SPECS['stk']['sp500']['path']    #
pth_stk_nasdaq100 = "stk/nasdaq100_1min/"  # INSTR_SPECS['stk']['sp500']['path']   #

#PATH_CRYPTO = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../..', pth_crypto))
PATH_CRP = os.path.join(PATH_DATA_IN, 'crp')


DES_SUFFIX = "_1min_col"   #  "_data1col.csv"
SRC_EXT = '.txt'
DES_EXT = ".csv"
DES_SUFFIX_EXT = DES_SUFFIX + DES_EXT

TIME_PREFIX = 'p'   # 't_'


TIME_LST = [(datetime.datetime(2019, 1, 1, 0, 0) + datetime.timedelta(minutes=m)).strftime("%H%M") for m in range(0, 60*24)]

cols_lst = ['o', 'ob', 'c', 'cb', 'cc',
            'hdy','ldy','hdyb','ldyb','hdyc','ldyc','hdyd','ldyd','hdye','ldye','hdyf','ldyf','hdyg','ldyg','hdyh','ldyh','hdyi','ldyi','hdyj','ldyj',
            'h', 'l', 'ha', 'la', 'hb', 'lb', 'hc', 'lc']
COLS_TIME = [*cols_lst, *TIME_LST]
COL_IDX_0000 = len(cols_lst)
COL_IDX_2359 = len(COLS_TIME) - 1

#unzip 'equity/sp500_1min/*.zip'
# for z in *.zip; do unzip $z; done

dirs_extract = [("equity/z", "equity/sp500_1min")]
dirs_transform = ["future/z"]  #["future/fut_1min"]

dirs_clean = ["equity/sp500_1min"]

'''
# ------------------------------------------------------------------------------
Used by:
~/Agape/development/ml_stats_quant/trade_quant/trade_strategy/strategy.py
  ~/Agape/development/ml_stats_quant/trade_quant/trade_strategy/fut_setup.py

sys.path.append(... "projects/fintech/flask_blueprint/apps/app_quant")
~/Agape/development/ml_stats_quant/statsmodels_regression_scikit/regression_stats.ipynb

~/Agape/development/ml_stats_quant/trade_quant/trade_strategy/*.py
~/projects/fintech/flask_blueprint/apps/app_plot_pair, app_plot_ml
~/projects/fintech/flask_blueprint/apps/app_quant/import_transform


#fut_files = ['esdata1col.csv', 'usdata1col.csv']
#fut_files_dct = {fut[:2].lower():fut for fut in fut_files}

df_fut = strategy.import_fut_dct_df(sym_lst=['es','us'])

df_fut_pctchg = {fut: df_.pct_change()[1:] for fut, df_ in df_fut.items()}

display( df_fut_pctchg['es'].columns )
display( df_fut['es'].head() )


dct_stk_sp500 = strategy.import_equity_sp500_dct_df()
dct_stk_nasdaq100 = strategy.import_equity_nasdaq100_dct_df()

dct_stk = strategy.import_equity_dct_df()
dct_stk['sp500']
dct_stk.keys())

dct_stk['aapl'].head()
dct_stk['goog'].tail()

dct_stk_pctchg = {sym: df_.pct_change()[1:] for sym, df_ in dct_stk.items()}
dct_stk['aapl'].head()
dct_stk_pctchg['aapl'].head()

dct_stk_pctchg['aapl'].columns

dct_stk_pctchg = {sym: df_.pct_change()[1:] for sym, df_ in dct_stk.items()}
--------------------------------------------------------------------------------
'''

def extract_zip(lst_dir=dirs_extract):
    '''
    extract('~/Agape/development/projects/fintech/data_in/stk/sp500_1min')
    '''
    if type('s') == str:
        lst_dir = [lst_dir]
    for dir_extract in lst_dir:
        #pth_src = os.path.join(pth_wrk, dir_extract[0])
        pth_src = os.path.expanduser(dir_extract)
        l = os.listdir(pth_src)
        for fname in l:
            if fname[-3:] != "zip":
                continue
            pth_file_src = os.path.join(pth_src, fname)
            # pth_des = os.path.join(pth_wrk, dir_extract[1])
            pth_des = pth_src
            with zipfile.ZipFile(pth_file_src, 'r') as zip_ref:
                zip_ref.extractall(pth_des)
                print("Unzip: " + pth_file_src + " to " + pth_des)


def clean_dup_zip(dirs=dirs_clean):
    for dir in dirs:
        pth = os.path.join(pth_wrk, dir)

        print(pth)
        #os.chdir(pth)

        l = os.listdir(pth)
        for fname in l:
            pth_file = os.path.join(pth, fname)
            if pth_file[-3:] == 'zip':
                if os.path.isfile(pth_file[:-3]+"txt"):
                    os.remove(pth_file)
                    print("rm " + pth_file)

        print(len(os.listdir(pth)))

# ------------------------------------------------------------------------------

class Dict_dot(dict):
    '''
    Instr = {'fut_es': None}
    Instr = Dict_dot(Instr)

    nested = { 'specs':INSTR_SPECS['fut']['use']['es'],
               'df': df_grid
             }
    Instr.fut_es = Dict_dot(nested)

    Instr.fut_es.df
    Instr.fut_es.specs

    '''
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class InstrX(dict, metaclass=Singleton):
    '''
    Instr = InstrX()
    Instr = InstrX(asset_sym, specs, df_grid, hol)
    Instr.attach(asset_sym, specs, df_grid, hol)

    Instr['fut_es'], Instr['stk_sp500_appl']
    Instr.fut_es.df.loc[pd.Timestamp('2002-09-11'),'fut_es_0914':'fut_es_0931']
    Instr.fut_es.df.columns
    Instr.fut_es.columns
    Instr.fut_es.specs.o_time

    Instr.fut_es.hol

    Instr.cols_time

    fut_es = fut_es

    After merge:
    Instr.df['fut_es_0930']
    '''
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, asset_sym=None, specs=None, df=None, hol=None):

        if asset_sym:
            self.attach(asset_sym, specs, df, hol)

    def attach(self, asset_sym, specs, df_grid, hol):
        asset_sym_time_lst = list(df_grid.columns)

        def delta_dytime_idx(asset_sym_time, min_incr=0):
            '''
            Instr.fut_es.delta_dytime_idx('fut_es_0000', 0)  == (0, 33)
            Instr.fut_es.delta_dytime_idx('fut_es_2359', 0)  == (0, 1472)
            Instr.fut_es.delta_dytime_idx('fut_es_2359', 1)  == (1, 33)

            Instr.fut_es.delta_dytime_idx('fut_es_0000', -1)    == (-1, 1456)
            Instr.fut_es.delta_dytime_idx('fut_es_0000', -1440) == (-1, 33)
            Instr.fut_es.delta_dytime_idx('fut_es_0000', -2880) == (-2, 33)

            Instr.stk_amgn.delta_dytime_idx('stk_amgn_0930', 0) == (0, 4)
            Instr.stk_amgn.delta_dytime_idx('stk_amgn_1600', 1) == (1, 4)
            Instr.stk_amgn.delta_dytime_idx('stk_amgn_0930', -1) == (0, 394)
            Instr.stk_amgn.df_grid.columns[394] == 'stk_amgn_1600'

            6 + 0   = 6 - (0*7)    => (0, 6)
            5 + 3   = 8 - (1*7)    => (1, 1)
            5 + 11  = 16 - (2*7)   => (1, 2)
            6 - 0   = 6   =>  7 + 6 - (0+1)*7  => (0, 6)
            6 - 6   = 0   =>  7 + 0 - (0+1)*7  => (0, 0)
            5 - 8   = -3  =>  7 + -3 - (-1+1)*7  => (-1, 4)
            5 - 15  = -10 =>  7 + -10 - (-2+1)*7 => (-2, 4)
            '''
            # if len(col_time) > 4:  # 'fut_es_0930' | '0930' => col index
            #    return cols_time.index(col_time[-4:])
            dy_incr=0
            col_idx = self[asset_sym].df_grid.columns.get_loc(asset_sym_time) + min_incr
            if min_incr == 0:
                return (dy_incr, col_idx)

            col_beg_idx = self[asset_sym].df_grid.columns.get_loc(self[asset_sym].col_beg_asset_sym_time)
            col_end_idx = self[asset_sym].df_grid.columns.shape[0] - 1
            tot_min_cols = col_end_idx - col_beg_idx + 1
            col_num = self[asset_sym].df_grid.columns.get_loc(asset_sym_time) + min_incr - col_beg_idx
            dy_incr = int(np.floor((col_num)/tot_min_cols))

            if col_idx > col_end_idx:
                col_idx = col_num - (dy_incr * tot_min_cols) + col_beg_idx
            elif col_idx < col_beg_idx:
                col_idx = tot_min_cols + col_num - ((dy_incr+1) * tot_min_cols) + col_beg_idx
            return (dy_incr, col_idx)

        def delta_dytime(asset_sym_time, min_incr=0, dtimestamp=None):
            '''
            Instr.fut_es.delta_dytime('fut_es_0000')     == (0, None, 'fut_es_0000')
            Instr.fut_es.delta_dytime('fut_es_2359', 1)  == (1, None, 'fut_es_0000')
            Instr.fut_es.delta_dytime('fut_es_0000', -1) == (-1, None, 'fut_es_2359')

            Instr.fut_es.delta_dytime('fut_es_o', -1)    == (0, None, 'fut_es_0929')
            Instr.fut_es.delta_dytime('fut_es_c', -1)    == (0, None, 'fut_es_1559')

            Instr.fut_es.delta_dytime('fut_es_0000', -1, dtimestamp)
            Instr.fut_es.delta_dytime('fut_es_0000', -1, pd.Timestamp('2002-09-11')) == (-1, Timestamp('2002-09-10 00:00:00'), 'fut_es_2359')
            Instr.fut_es.delta_dytime('fut_es_0000', -1, pd.Timestamp('07/29/2019')) == (-1, Timestamp('2019-07-28 00:00:00'), 'fut_es_2359')

            Instr.stk_amgn.delta_dytime('stk_amgn_0930') == (0, None, 'stk_amgn_0930')
            Instr.stk_amgn.delta_dytime('stk_amgn_0930', -1) == (-1, None, 'stk_amgn_1600')
            Instr.stk_amgn.delta_dytime('stk_amgn_1600', 1, ts('2020-03-20')) == (1, Timestamp('2020-03-23 00:00:00'), 'stk_amgn_0930')
            Instr.stk_amgn.delta_dytime('stk_amgn_0930', -1, ts('2020-03-23')) == (-1, Timestamp('2020-03-20 00:00:00'), 'stk_amgn_1600')
            '''

            asset, sym, time = asset_sym_time.split('_')
            asset_sym_ = asset+'_'+sym+'_'
            if time[0] == 'o' or time[0] == 'c':
                time = specs[time + '_time'][0]
                asset_sym_time = asset_sym_ + time

            dy_incr, col_idx = delta_dytime_idx(asset_sym_time, min_incr)
            dy_dtimestamp = dtimestamp
            if dy_dtimestamp:
                dy_idx = self[asset_sym].df_grid.index.get_loc(dtimestamp)
                dy_dtimestamp = self[asset_sym].df_grid.index[dy_idx + dy_incr]
            return (dy_incr, dy_dtimestamp, asset_sym_time_lst[col_idx])

        def search_val(cond, fwd_bak, dtimestamp_beg,
                       time_beg, time_end=None, dy_max=None,
                       min_max=None, bl_bracket=False):
            ''' val, dy_incr, dtimestamp_found, asset_sym_time, min_incr =
            Instr[asset_sym].search_val('== 2945.25', 'f', dtimestamp, '0000')
            Instr[asset_sym].search_val('== 3019.25', 'b', dtimestamp, '1615')

            Instr[asset_sym].search_val('== 3015.50', 'f', dtimestamp, '0930', '1000', dy_max=0)
            Instr[asset_sym].search_val('== 3015.50', 'b', dtimestamp, '1000', '0930', dy_max=0)

            Instr[asset_sym].search_val('== 2984.25', 'f', dtimestamp, '2353', '0010', dy_max=1)
            Instr[asset_sym].search_val('== 2984.25', 'b', dtimestamp+pd.Timedelta(days=1), '0007', '2350', dy_max=1)

            Instr[asset_sym].search_val('> 2984.75', 'f', dtimestamp, '2350')
            Instr[asset_sym].search_val('< 2984', 'f', dtimestamp, '2350')
            Instr[asset_sym].search_val('< 2984', 'b', dtimestamp+pd.Timedelta(days=1), '0015')
            '''
            asset_sym_ = asset_sym+'_'
            eq = re.findall(r'[><!=]+', cond)[0]
            val = float(cond.split(eq)[-1])

            if fwd_bak[0] == 'f':
                incr=1
            elif fwd_bak[0] == 'b':
                incr=-1
            min_incr=0
            dy_incr=0

            time_beg = time_beg[-4:]
            if time_end:
                time_end = time_end[-4:]
            else:
                if incr == 1:
                    time_end = self.time_lst[-1]
                else:
                    time_end = self.time_lst[0]
            # dy_incr, dy_dtimestamp, asset_sym_time = delta_dytime(time_beg, min_incr, dtimestamp)
            dy_dtimestamp = dtimestamp_beg # + pd.Timedelta(days=dy_incr))

            if not dy_max:
                if incr == 1:
                    dy_max = (df_grid.index.max() - dtimestamp_beg).days - 1
                else:
                    dy_max = (dtimestamp_beg - df_grid.index.min()).days - 1

            time_found=None
            val_found=None
            while not time_found:
            # while dy_dtimestamp >= df_grid.index.min() and dy_dtimestamp <= df_grid.index.max():
                # col_idx = np.nonzero(df_grid.loc[row_dtimestamp, asset_sym_time_beg:asset_sym_time_end].values != 0)[0][0] - 1 + 123
                # asset_sym_+specs['o_time'][0] == 'fut_es_0930'
                if incr == 1:
                    time_0 = time_beg
                    time_1 = self.time_lst[-1]
                    if bl_bracket:
                        time_1 = time_end
                    elif dy_max > abs(dy_incr) and abs(dy_incr) > 0:
                        time_0 = self.time_lst[0]
                        time_1 = self.time_lst[-1]
                    elif dy_max == abs(dy_incr) and abs(dy_incr) > 0:
                        time_0 = self.time_lst[0]
                        time_1 = time_end
                else:
                    time_0 = self.time_lst[0]
                    time_1 = time_beg
                    if bl_bracket:
                        time_0 = time_end
                    elif dy_max > abs(dy_incr) and abs(dy_incr) > 0:
                        time_0 = self.time_lst[0]
                        time_1 = self.time_lst[-1]
                    elif dy_max == abs(dy_incr) and abs(dy_incr) > 0:
                        time_0 = time_end
                        time_1 = self.time_lst[-1]

                if eq == '>':
                    cols_cond = np.nonzero(df_grid.loc[dy_dtimestamp, asset_sym_+time_0:asset_sym_+time_1].values > val)[0]
                elif eq == '>=':
                    cols_cond = np.nonzero(df_grid.loc[dy_dtimestamp, asset_sym_+time_0:asset_sym_+time_1].values >= val)[0]
                elif eq == '<':
                    cols_cond = np.nonzero(df_grid.loc[dy_dtimestamp, asset_sym_+time_0:asset_sym_+time_1].values < val)[0]
                elif eq == '<=':
                    cols_cond = np.nonzero(df_grid.loc[dy_dtimestamp, asset_sym_+time_0:asset_sym_+time_1].values <= val)[0]
                elif eq == '==':
                    cols_cond = np.nonzero(df_grid.loc[dy_dtimestamp, asset_sym_+time_0:asset_sym_+time_1].values == val)[0]
                elif eq == '!=':
                    cols_cond = np.nonzero(df_grid.loc[dy_dtimestamp, asset_sym_+time_0:asset_sym_+time_1].values != val)[0]

                if cols_cond.size > 0:
                    if fwd_bak[0] == 'f':
                        col_cond = cols_cond[0]
                    else:
                        col_cond = cols_cond[-1]
                    #col_cond += self.delta_dytime_idx(self.time_lst[0])[1]
                    #val = df_grid.loc(dy_incr+, col_cond) # df_grid.iloc(dy_incr+, col_cond)
                    time_found = df_grid.loc[dy_dtimestamp, asset_sym_+time_0:asset_sym_+time_1].index[col_cond]
                    val_found = df_grid.loc[dy_dtimestamp, asset_sym_+time_0:asset_sym_+time_1][col_cond]
                    break

                # if asset_sym_time[-4:] == self.time_lst[-1] and fwd_bak[0] == 'f':
                # min_incr += incr
                # dy_incr, dy_dtimestamp, asset_sym_time = delta_dytime(time_beg, min_incr, dtimestamp)
                if dy_max == abs(dy_incr):
                    break
                dy_incr += incr
                dy_dtimestamp = dtimestamp_beg + pd.Timedelta(days=dy_incr)

            # se = df_grid.loc[row_dtimestamp]
            # for i, val in enumerate(se, 0):
            #     if val == 0:
            #         print(i, x)
            #         se.iloc[i] = se.iloc[i-1]
            if time_found:
                # return val, dy_incr, dy_dtimestamp, self.cols_time[col_cond], min_incr
                return val_found, dy_incr, dy_dtimestamp, time_found, min_incr
            return None, None, None, None

        # setattr(self, asset_sym, Dict_dot(nested))
        print("Update InstrX dict:", asset_sym)

        self[asset_sym] = Dict_dot(
          dict(
            asset_sym=asset_sym,
            specs=specs,
            df_grid = df_grid,
            hol=hol,
            col_beg_asset_sym_time = asset_sym+'_'+specs['beg_time'],
            asset_sym_time_lst = asset_sym_time_lst,
            delta_dytime_idx = delta_dytime_idx,
            delta_dytime = delta_dytime,
            search_val = search_val
          )
        )

"""
class InstrX2(metaclass=Singleton):
    df = {}

    def __init__(self):
        pass

    def append_instr(self, asset_sym, df_grid, df_hol, instr_specs):
        df[asset_sym] = df_grid
        # test.__dict__[a_string]
        setattr(self, asset_sym, '')
        self.df_grid = df_grid
        self.df_hol = df_hol
        self.specs = instr_spec
        self.columns = list(self.df_grid.columns)

    def col_idx(self, col_time):
        col_time = col_time[-4:]   # 'fut_es_1200'
        return self.columns.index(col_time)

    def df(self, asset_sym):
        return df
"""
"""
class InstrX3(InstrX_Base, metaclass=Singleton):
    pass
"""

# ------------------------------------------------------------------------------
def get_aliases(asset_sym, Instr):
    df_grid, specs, df_hol = Instr[asset_sym].df_grid, Instr[asset_sym].specs, Instr[asset_sym].hol
    asset_sym_time_lst = Instr[asset_sym].asset_sym_time_lst   # list(df_grid.columns)
    asset_sym_ = asset_sym + '_'  # = df_grid.columns[-1][:-4]  # 'fut_es_2359'
    return df_grid, specs, df_hol, asset_sym_time_lst, asset_sym_


def update_alias_time(Instr, asset_sym):
    print('\nUpdating alias times')
    df_grid = Instr[asset_sym].df_grid
    specs = Instr[asset_sym].specs
    asset_sym_ = asset_sym + '_'

    df_grid[asset_sym_ + specs['o_time'][1]] = df_grid[asset_sym_ + specs['o_time'][0]]
    df_grid[asset_sym_ + specs['ob_time'][1]] = df_grid[asset_sym_ + specs['ob_time'][0]]
    df_grid[asset_sym_ + specs['c_time'][1]] = df_grid[asset_sym_ + specs['c_time'][0]]
    df_grid[asset_sym_ + specs['cb_time'][1]] = df_grid[asset_sym_ + specs['cb_time'][0]]
    df_grid[asset_sym_ + specs['cc_time'][1]] = df_grid[asset_sym_ + specs['cc_time'][0]]


def update_hilo(Instr, asset_sym):
    print('\nUpdating hilo')
    df_grid = Instr[asset_sym].df_grid
    specs = Instr[asset_sym].specs
    hilo_specs = specs['hilo']
    asset_sym_ = asset_sym + '_'

    row_max_prev = 0  # df_grid.iloc[0][asset_sym_+specs['ob_time'][0]:].max()
    row_min_prev = 0  # df_grid.iloc[0][asset_sym_+specs['ob_time'][0]:].min()
    for row_dtimestamp in df_grid.index:
        for k,v in hilo_specs.items():

            time_hilo_beg = v[0]
            time_hilo_end = v[1]
            if v[0].isalpha():
                time_hilo_beg = specs[v[0]+'_time'][0]
            if v[1].isalpha():
                time_hilo_end = specs[v[1]+'_time'][0]

            row_max = df_grid.loc[row_dtimestamp, asset_sym_+time_hilo_beg:asset_sym_+time_hilo_end].max()
            row_min = df_grid.loc[row_dtimestamp, asset_sym_+time_hilo_beg:asset_sym_+time_hilo_end].min()
            if row_max > df_grid.loc[row_dtimestamp, asset_sym_ + k]:
                    df_grid.loc[row_dtimestamp, asset_sym_ + k] = row_max
                    print('Hilo override: ', row_dtimestamp, k)
            if row_min < df_grid.loc[row_dtimestamp, asset_sym_ + 'l' + k[1:]]:
                    df_grid.loc[row_dtimestamp, asset_sym_ + 'l' + k[1:]] = row_min
                    print('Hilo override: ', row_dtimestamp, 'l' + k[1:])

        # h/l: ob -> cc
        max_cur = max(row_max_prev,
                      df_grid.loc[row_dtimestamp, asset_sym_+'0000':asset_sym_+specs['cc_time'][0]].max())
        min_cur = min(row_min_prev,
                      df_grid.loc[row_dtimestamp, asset_sym_+'0000':asset_sym_+specs['cc_time'][0]].min())
        df_grid.loc[row_dtimestamp, asset_sym_ + 'h'] = max_cur
        df_grid.loc[row_dtimestamp, asset_sym_ + 'l'] = min_cur
        row_max_prev = df_grid.loc[row_dtimestamp, asset_sym_+specs['ob_time'][0]:].max()
        row_min_prev = df_grid.loc[row_dtimestamp, asset_sym_+specs['ob_time'][0]:].min()


    """
    df_grid[asset_sym_ + 'hdy'] = df_grid.loc[:, asset_sym_+specs['o_time'][0]:asset_sym_+specs['c_time'][0]].max(axis=1)
    df_grid[asset_sym_ + 'ldy'] = df_grid.loc[:, asset_sym_+specs['o_time'][0]:asset_sym_+specs['c_time'][0]].min(axis=1)
    df_grid[asset_sym_ + 'hdyb'] = df_grid.loc[:, asset_sym_+specs['o_time'][0]:asset_sym_+specs['cb_time'][0]].max(axis=1)
    df_grid[asset_sym_ + 'ldyb'] = df_grid.loc[:, asset_sym_+specs['o_time'][0]:asset_sym_+specs['cb_time'][0]].min(axis=1)
    df_grid[asset_sym_ + 'hdya'] = df_grid.loc[:, asset_sym_+specs['o_time'][0]:asset_sym_+specs['cb_time'][0]].max(axis=1)
    df_grid[asset_sym_ + 'ldya'] = df_grid.loc[:, asset_sym_+specs['o_time'][0]:asset_sym_+specs['cb_time'][0]].min(axis=1)

    asset_sym_time = Instr[asset_sym].delta_dytime('fut_es_o', -1)[2]  # == (0, None, 'fut_es_0929')
    df_grid[asset_sym_ + 'ha'] = df_grid.loc[:, asset_sym_+'0000':asset_sym_time].max(axis=1)
    df_grid[asset_sym_ + 'la'] = df_grid.loc[:, asset_sym_+'0000':asset_sym_time].min(axis=1)

    df_grid[asset_sym_ + 'hb'] = df_grid.loc[:, asset_sym_+'0000':].max(axis=1)
    df_grid[asset_sym_ + 'lb'] = df_grid.loc[:, asset_sym_+'0000':].min(axis=1)
    df_grid[asset_sym_ + 'hc'] = df_grid.loc[:, asset_sym_+'0000':asset_sym_+specs['c_time'][0]].max(axis=1)
    df_grid[asset_sym_ + 'lc'] = df_grid.loc[:, asset_sym_+'0000':asset_sym_+specs['c_time'][0]].min(axis=1)
    df_grid[asset_sym_ + 'hd'] = df_grid.loc[:, asset_sym_+specs['ob_time'][0]:].max(axis=1)
    df_grid[asset_sym_ + 'ld'] = df_grid.loc[:, asset_sym_+specs['ob_time'][0]:].min(axis=1)
    """

def clean_forward(row_dtimestamp, asset_sym, Instr):
    df_grid, specs, df_hol, asset_sym_time_lst, asset_sym_ = get_aliases(asset_sym, Instr)
    #for i, cont_row in enumerate(df_file.itertuples(), 0):
    if df_grid.loc[row_dtimestamp, asset_sym_+'0000'] == 0:
        dy_timestamp, asset_sym_time = Instr[asset_sym].search_val('!= 0', 'b', '0000', row_dtimestamp)
        ###df_grid.loc[row_dtimestamp, asset_sym_+'0000'] == 0:


def clean_fill_zeros(asset_sym, Instr):
    '''
    A) FIRST DAY: 0000 <= bfill
    B) LAST DAY: ffill

    C) HOL:
       # ffill
       # bfill

    D) 1800 == 0:
       # 1800 <- 1830-2359 - search first nonzero after 1800, then bfill to 1800
       # ffill 1800 -> 2359

    E) 0000 == 0:
       # prev day '2359' OR bfill, whichever is shorter distance
       # ffill to 0929

    FILL BACKWARDS
    B) late open - only back to Open
       0830, 0831, ... 0930, 0931, ..., 1200
             2765.50
       INSTR_SPECS[asset][group][sym]['o_time'][0] <= first non-zero
    C) 1600 <- 1615 <- 1700 <- 1800 <- 1830

    K) SUN:
       1) sun: 1800 -> ffill, then bfill
       2) sun's           <= prev fri's 0000:1759
       3) sun's 1800:2359 => prev fri

    FILL FORWARDS 03/09/2020, 10, 16, 18
    - early Close: eg 1300 -> 1800
    - Friday Close => Sunday Open-1: INSTR_SPECS[asset][group][sym]['o_time'][4]
    - new year 0630 or 1800

    time_idx += 1
    if TIME_LST.index(cont_row.Time) != time_idx:  # TIME_LST.index('1800') == 1080
    '''
    this_fn_name = inspect.currentframe().f_code.co_name
    # caller_fn_name = inspect.currentframe().f_back.f_code.co_name

    # aliases
    df_grid, specs, df_hol, asset_sym_time_lst, asset_sym_ = get_aliases(asset_sym, Instr)

    # --------------------------------------
    # A) FIRST DAY:
    #    0000 <- bfill first nonzero
    row_dtimestamp = df_grid.iloc[0].name
    beg_col = asset_sym_+'0000'
    if df_grid.loc[row_dtimestamp, beg_col] == 0:
        col_j = df_grid.loc[row_dtimestamp, beg_col:].to_numpy().nonzero()[0][0]
        # val = df_grid.loc[row_dtimestamp].iloc[col_j + COLS_TIME.index('0000')]
        col_name = df_grid.columns[col_j + df_grid.columns.get_loc(beg_col)]
        #        = df_grid.loc[row_dtimestamp,beg_col:].index[col_j]
        df_grid.loc[row_dtimestamp, beg_col:col_name] = df_grid.loc[row_dtimestamp, beg_col:col_name].replace(0, method='bfill')

    # --------------------------------------
    # B) LAST DAY: fill forwards
    row_dtimestamp = df_grid.iloc[-1,:].name
    se = df_grid.loc[row_dtimestamp, asset_sym_+'0000':]
    col_tar = se.index[se.to_numpy().nonzero()[0][-1]]
    print(f"{this_fn_name}: ffill - last row: {row_dtimestamp}, last nonzero col: {col_tar}")
    df_grid.loc[row_dtimestamp, col_tar:] = df_grid.loc[row_dtimestamp, col_tar:].replace(0, method='ffill')

    # -----------------------------------
    # C) HOL : ffill, then bfill
    beg_col = asset_sym_+'0000'
    zero_idxs = df_grid[ (df_grid.index.isin(df_hol.date)) ].index
    for row_dtimestamp in zero_idxs:
        df_grid.loc[row_dtimestamp, beg_col:] = df_grid.loc[row_dtimestamp, beg_col:].replace(0, method='ffill')
        df_grid.loc[row_dtimestamp, beg_col:] = df_grid.loc[row_dtimestamp, beg_col:].replace(0, method='bfill')

    # -----------------------------------
    # D) EARLY CLOSE 1600 == 0 - usually day bef hol
    #    find last nonero before 1600, then ffill -> 1600 |
    col_tar = asset_sym_+specs['c_time'][0]
    zero_idxs = df_grid[ (df_grid[col_tar]==0) & (df_grid.index.dayofweek != 6) ].index

    for row_dtimestamp in zero_idxs:
        col_j = df_grid.loc[row_dtimestamp, asset_sym_+'0000':col_tar].to_numpy().nonzero()[0][-1]
        col_name = df_grid.columns[col_j + df_grid.columns.get_loc(asset_sym_+'0000')]
        df_grid.loc[row_dtimestamp, col_name:col_tar] = df_grid.loc[row_dtimestamp, col_name:col_tar].replace(0, method='ffill')

    # ------------------------------------
    # E) 1600 > 1615 > 1700 > 1759 | ffill
    col_tar = asset_sym_+specs['c_time'][0]
    idxs = df_grid[ (df_grid.index.dayofweek != 6) ].index

    col_noinclude = asset_sym_+specs['ob_time'][0]
    col_prev_j = df_grid.columns.get_loc(col_noinclude) - 1
    col_prev_name = df_grid.columns[col_prev_j]
    # val_prev = df_grid.loc[row_prev, col_prev_name]

    for row_dtimestamp in idxs:
        df_grid.loc[row_dtimestamp, col_tar:col_prev_name] = df_grid.loc[row_dtimestamp, col_tar:col_prev_name].replace(0, method='ffill')

    # -----------------------------------
    # F) FRI ffill
    beg_col = asset_sym_+specs['c_time'][0]
    zero_idxs = df_grid[ (df_grid.index.dayofweek == 4) & (~df_grid.index.isin(df_hol.date)) ].index
    for row_dtimestamp in zero_idxs:
        df_grid.loc[row_dtimestamp, beg_col:] = df_grid.loc[row_dtimestamp, beg_col:].replace(0, method='ffill')

    # --------------------------------------
    # G) 0000 == 0:
    #    prev day '2359' OR bfill, whichever is shorter distance
    #    ffill to 0929
    beg_col = asset_sym_+'0000'
    zero_idxs = df_grid[ (df_grid[beg_col] == 0) & (df_grid.index.dayofweek != 6) ].index
    for row_dtimestamp in zero_idxs:
        col_j = df_grid.loc[row_dtimestamp, beg_col:].to_numpy().nonzero()[0][0]
        col_name = df_grid.columns[col_j + df_grid.columns.get_loc(beg_col)]
        # col = df_grid.loc[row_dtimestamp,beg_col:].index[col_j]
        # val = df_grid.loc[row_dtimestamp, col]  # value of first
        # get prev day last nonzero:
        row_prev_i = df_grid.index.get_loc(row_dtimestamp) - 1
        row_prev_name = df_grid.iloc[row_prev_i].name
        col_prev_j = df_grid.loc[row_prev_name, beg_col:].to_numpy().nonzero()[0][-1]
        col_prev_name = df_grid.columns[col_prev_j + df_grid.columns.get_loc(beg_col)]
        val_prev = df_grid.loc[row_prev_name, col_prev_name]
        # if (col_j - COLS_TIME.index('0000')) < ((COLS_TIME.index('2359')-COLS_TIME.index('0000')) - col_prev_j + 1):
        if (-(df_grid.columns.get_loc(asset_sym_+'0000') - (col_j + df_grid.columns.get_loc(beg_col))) <=
             (df_grid.columns.get_loc(asset_sym_+'2359') - (col_prev_j + df_grid.columns.get_loc(beg_col))) ):
            df_grid.loc[row_dtimestamp, beg_col:col_name] = df_grid.loc[row_dtimestamp, beg_col:col_name].replace(0, method='bfill')
        else:
            col_name = df_grid.columns[col_j - 1 + df_grid.columns.get_loc(beg_col)]
            df_grid.loc[row_dtimestamp, beg_col:col_name] = df_grid.loc[row_dtimestamp, beg_col:col_name].replace(0, val_prev)

        # ffill 0000 > 0929
        col_j = df_grid.columns.get_loc(asset_sym_+specs['o_time'][0])
        col_prev_name = df_grid.columns[col_j-1]
        df_grid.loc[row_dtimestamp, beg_col:col_prev_name] = df_grid.loc[row_dtimestamp, beg_col:col_prev_name].replace(0, method='ffill')

    # --------------------------------------------------------------------------
    # H) 1800 == 0:
    # 1800 <- 1830-2359 - search first nonzero after 1800, then bfill to 1800
    # ffill 1800 -> 2359
    col_tar = asset_sym_+specs['ob_time'][0]
    # zero_idxs = df_grid[(df_grid[beg_col] == 0) & (df_grid.index.dayofweek != 6) & (~df_grid.index.isin(df_hol.date))].index
    zero_idxs = df_grid[ (df_grid[col_tar] == 0) & (df_grid.index.dayofweek != 6) ].index
    for row_dtimestamp in zero_idxs:
        arr_nonzero = df_grid.loc[row_dtimestamp, col_tar:].to_numpy().nonzero()[0]
        if arr_nonzero.size > 0:
            col_name = df_grid.loc[row_dtimestamp, col_tar:].index[arr_nonzero[0]]
            # val = df_grid.loc[row_dtimestamp, col]  # value of first
            # df_grid.loc[row_dtimestamp, beg_col:] = df_grid.loc[row_dtimestamp, beg_col:].replace(0, val)
            df_grid.loc[row_dtimestamp, col_tar:col_name] = df_grid.loc[row_dtimestamp, col_tar:col_name].replace(0, method='bfill')
            df_grid.loc[row_dtimestamp, col_tar:] = df_grid.loc[row_dtimestamp, col_tar:].replace(0, method='ffill')
        else:
            col_beg = asset_sym_+specs['c_time'][0]
            df_grid.loc[row_dtimestamp, col_beg:] = df_grid.loc[row_dtimestamp, col_beg:].replace(0, method='ffill')

    # --------------------------------------
    # I) Late open
    #    bfill back to Open : 0930 <- 1559 first nonzero
    #    if not found: ffill 0000 -> 0930

    beg_col = asset_sym_+specs['o_time'][0]
    # zero_idxs = df_grid[(df_grid[beg_col] == 0) & (df_grid.index.dayofweek != 6) & (~df_grid.index.isin(df_hol.date))].index
    zero_idxs = df_grid[ (df_grid[beg_col] == 0) & (df_grid.index.dayofweek != 6) ].index
    for row_dtimestamp in zero_idxs:
        col_j = df_grid.columns.get_loc(asset_sym_+specs['c_time'][0])
        col_prev_name = df_grid.columns[col_j-1]
        arr_nonzero = df_grid.loc[row_dtimestamp,beg_col:col_prev_name].to_numpy().nonzero()[0]

        if arr_nonzero.size > 0:
            col_name = df_grid.loc[row_dtimestamp,beg_col:].index[arr_nonzero[0]]
            # val = df_grid.loc[row_dtimestamp, col]  # value of first
            # df_grid.loc[row_dtimestamp, beg_col:] = df_grid.loc[row_dtimestamp, beg_col:].replace(0, val)
            df_grid.loc[row_dtimestamp, beg_col:col_name] = df_grid.loc[row_dtimestamp, beg_col:col_name].replace(0, method='bfill')
            df_grid.loc[row_dtimestamp, beg_col:asset_sym_+specs['c_time'][0]] = df_grid.loc[row_dtimestamp, beg_col:asset_sym_+specs['c_time'][0]].replace(0, method='ffill')
        else:
            df_grid.loc[row_dtimestamp, asset_sym_+'0000':beg_col] = df_grid.loc[row_dtimestamp, asset_sym_+'0000':beg_col].replace(0, method='ffill')

        # col_firstnonzero = np.nonzero(df_grid.loc[row_dtimestamp, asset_sym_+specs['o_time'][0]:asset_sym_+'1300'].values != 0)[0][0]
        #
        # col_firstnonzero += Instr.delta_dytime_idx(asset_sym_+specs['o_time'][0])[1]
        # if col_firstnonzero < COL_IDX_0000 or col_firstnonzero > COL_IDX_2349:
        #     print("ERROR TRANSFORM: B) Late open - backwards only back to Open : 0930 <- 1300, 2359")
        # val_firstnonzero = df_grid.loc[row_dtimestamp, asset_sym_time_lst[col_firstnonzero]]
        # df_grid.loc[row_dtimestamp, asset_sym_+specs['o_time'][0]:asset_sym_time_lst[col_firstnonzero-1]] = val_firstnonzero
        #
        # # Forwards
        # df_grid = clean_row_alias_time(df_grid, row_dtimestamp, asset_sym_, specs)
        # col = df_grid.loc[row_dtimestamp, asset_sym_+'0000':].eq(0).any()
        # print(col)

    # ----------------------------------------------
    # J) 2359
    #   0000 => ffill
    col_tar = asset_sym_+'2359'
    zero_idxs = df_grid[(df_grid[col_tar] == 0) & (df_grid.index.dayofweek != 6) & (~df_grid.index.isin(df_hol.date))].index
    for row_dtimestamp in zero_idxs:
        df_grid.loc[row_dtimestamp, asset_sym_+'0000':] = df_grid.loc[row_dtimestamp, asset_sym_+'0000':].replace(0, method='ffill')

    # ----------------------------------------------
    # K) SUN:
    #    1) sun: 1800 -> ffill, then bfill
    #    2) sun's           <= prev fri's 0000:1759
    #    3) sun's 1800:2359 => prev fri
    df_sun = df_grid[(df_grid.index.dayofweek == 6)]
    # lst_dtimestamp_sun = df_grid[df_sun].index.tolist()
    # df_sun[df_sun['fut_es_1800'] == 0].index
    # df_sun[(df_sun.loc[:,'fut_es_2350':] == 0).any(axis=1)].index
    # for row_dtimestamp in (df_sun == 0).any(axis=1).index:
    col_j = df_grid.columns.get_loc(asset_sym_+specs['ob_time'][0])
    col_prev_name = df_grid.columns[col_j-1]

    for row_dtimestamp in df_sun.index:
        # 1) sun: 1800 -> ffill, then bfill
        df_grid.loc[row_dtimestamp, asset_sym_+specs['ob_time'][0]:] = df_grid.loc[row_dtimestamp, asset_sym_+specs['ob_time'][0]:].replace(0, method='ffill')
        df_grid.loc[row_dtimestamp, asset_sym_+specs['ob_time'][0]:] = df_grid.loc[row_dtimestamp, asset_sym_+specs['ob_time'][0]:].replace(0, method='bfill')

        # 2) sun's           <= prev fri's 0000:1759
        row_prev_i = df_grid.index.get_loc(row_dtimestamp) - 1
        row_prev_name = df_grid.iloc[row_prev_i].name   # 1759
        df_grid.loc[row_dtimestamp, asset_sym_+'0000':col_prev_name] = df_grid.loc[row_prev_name, asset_sym_+'0000':col_prev_name]
        # 3) sun's 1800:2359 => prev fri
        df_grid.loc[row_prev_name, asset_sym_+specs['ob_time'][0]:] = df_grid.loc[row_dtimestamp, asset_sym_+specs['ob_time'][0]:]

    # D:
    # row_dtimestamp = df_sun.index[-1]
    # row_prev_i = df_grid.index.get_loc(row_dtimestamp) - 1
    # row_prev_name = df_grid.iloc[row_prev_i].name

    # (Instr.fut_es.df_grid.loc[row_prev_name, 'fut_es_0000':] == Instr.fut_es.df_grid.loc[row_dtimestamp, 'fut_es_0000':]).all()
    # strategy.update_alias_time(Instr, 'fut_es')
    # (Instr.fut_es.df_grid.loc[row_prev_name, 'fut_es_o':'fut_es_cc'] == Instr.fut_es.df_grid.loc[row_dtimestamp, 'fut_es_o':'fut_es_cc']).all()
    # strategy.update_hilo(Instr, 'fut_es')
    # (Instr.fut_es.df_grid.loc[row_prev_name, 'fut_es_hdy':'fut_es_ldyb'] == Instr.fut_es.df_grid.loc[row_dtimestamp, 'fut_es_hdy':'fut_es_ldyb']).all()
    # (Instr.fut_es.df_grid.loc[row_prev_name] == Instr.fut_es.df_grid.loc[row_dtimestamp]).all()

    df_grid_sun = df_grid.loc[df_sun.index]   # (df_sun.index == df_grid_sun.index).all().all()
    print("\nSun still containing zeros:", df_grid_sun.loc[df_grid_sun.loc[(df_grid_sun.loc[:,'fut_es_0000':] == 0).any(axis=1)].index].index.to_list())

    # -----------------------------------
    # L) FINAL: ffill, bfill everything
    col_beg = asset_sym_+'0000'
    idxs_zero = df_grid.loc[(df_grid.loc[:, col_beg:] == 0).any(axis=1)].index
    for row_dtimestamp in idxs_zero:
        df_grid.loc[row_dtimestamp, col_beg:] = df_grid.loc[row_dtimestamp, col_beg:].replace(0, method='ffill')
        df_grid.loc[row_dtimestamp, col_beg:] = df_grid.loc[row_dtimestamp, col_beg:].replace(0, method='bfill')

    print('Any zeros left:', 0 in df_grid.loc[:, col_beg:].values)

    update_alias_time(Instr, asset_sym)
    update_hilo(Instr, asset_sym)

    df_grid.drop(df_grid.index[0], inplace=True)
    df_grid.drop(df_grid.index[-1], inplace=True)

    col_j = df_grid.columns.get_loc(asset_sym_+'0000') - 1
    col_end = df_grid.columns[col_j]
    print('Any hilo - hi left:', -999999 in df_grid.loc[:, :col_end].values)
    print('Any hilo - lo left:', 999999 in df_grid.loc[:, :col_end].values)

    print('Any zeros left:', 0 in df_grid.values)
    print()
    print(Instr.keys())
    print(Instr[asset_sym].keys())
    print(Instr[asset_sym].df_grid.index[0])
    print(Instr[asset_sym].df_grid.index[-1])
    print(Instr[asset_sym].df_grid.shape)

    # df_grid = clean_row_alias_time(df_grid, row_dtimestamp, asset_sym_, specs)

    #lst_dtimestamp_zero_sun_1800 = df_grid[(df_grid[asset_sym_+'1800']==0) & (df_grid.index.dayofweek == 6) & (~df_grid.index.isin(df_hol.date))].index.tolist()
    # df_grid = clean_row_alias_time(df_grid, row_dtimestamp, asset_sym_, specs)

    # FILL FORWARDS
    # 1500 -> 1600 -> 1700 - 1759
    ###cols_idx_zero = np.nonzero(df_grid.loc[row_dtimestamp].values == 0)[0]
    ###for col_idx in cols_idx_zero:

    ###df_grid = row_alias_time(df_grid, row_dtimestamp, asset_sym_, specs)

    return Instr


def transform_grid_import(src, sym_lst=[], bl_new=True, bl_out_zeros=True, bl_no_clean=False, bl_ret_grid=True):
    ''' Use:

    Instr = transform_grid_import(src='pth_fut_use', sym_lst=['es'])                      # prod
    Instr = transform_grid_import(src='pth_fut_use', sym_lst=['es'], bl_out_zeros=False)
    Instr = transform_grid_import(src='pth_fut_use', sym_lst=['es'], bl_no_clean=True)    # debug

    os.chdir(os.path.join(PATH_DATA_IN, 'fut/use_tmp/'))
    os.chdir(os.path.join(PATH_DATA_IN, 'fut/use_1min/'))
    df_grid = transform_grid_import(src='pwd', sym_lst=['es'], bl_ret_grid=True)
    df_grid = transform_grid_import(src=os.path.join(PATH_DATA_IN, 'fut/use_tmp/'), sym_lst=['es'], bl_ret_grid=True)

    missing_o = df_grid[(df_grid['asset_sym_O']==0) & (df_grid.index.dayofweek != 6) & (~df_grid.index.isin(df_hol.date))].index.tolist()
    df_grid.loc[df_grid.index.isin(missing_o),'asset_sym_0914':'asset_sym_0931'].iloc[0]

    (df_grid.iloc[:,:] == 0).any().any()
    (df_grid.iloc[:,:] == 3.14).any(axis=1)

    df_grid[df_grid.index.isin(df_hol.date)]
    df_hol.date.iloc[-23] == df_grid.index[-59]
                             df_grid.iloc[-59,:].name

    df_grid.loc[pd.Timestamp('2002-09-11'),'asset_sym_0914':'asset_sym_0931']
    df.A.ne('a').idxmax()
    df_grid.loc[pd.Timestamp('2002-09-11'),'asset_sym_0000':].eq(0).idxmax()

    df_grid[df_grid['asset_sym_O']==2943.50]  ==  df_grid.loc[df_grid['asset_sym_O']==2943.50]
    df_grid.loc[pd.Timestamp('2019-07-28'),'asset_sym_0500':'asset_sym_1000']

    df[df.apply(lambda r: r.str.contains('b', case=False).any(), axis=1)]

    print(df_file.index.max())
    print(df_file.iloc[0, :])
    print(df_file.iloc[-1, :])
    print(df_file.iloc[-1, :].Close)


    fill forward, backward ...

    "pth_fut_use"
    "pth_stk_sp500"
    '''
    if src[:4] == 'pth_':
        tmp_asset_group = src.split('_')
        asset, group = tmp_asset_group[1], tmp_asset_group[2]
        pth_src = os.path.join(PATH_DATA_IN, globals()[src])
    else:
        if src == 'pwd':
            pth_src = os.getcwd()
        elif '/' in src:
            if src[-1] == '/':
                src = src[:-1]
            pth_src = os.path.join(PATH_DATA_IN, src)
        tmp_asset_group = src.split('/')
        asset, group = tmp_asset_group[-2], tmp_asset_group[-1].split('_')[0]

    l = os.listdir(pth_src)
    print(pth_src)
    print(l)

    sym_lst = [x.lower() for x in sym_lst]

    # Assume hol is same per group: eg fut_use: es, nq, us
    # try:
    #   thevariable
    # except NameError:
    if 'df_hol'+'_'+asset+'_'+group not in globals():
        globals()['df_hol_'+asset+'_'+group] = import_hol(asset+'_'+group)
    df_hol = globals()['df_hol_'+asset+'_'+group]

    if bl_new:
        if 'Instr' in locals() or 'Instr' in globals():
            print("Destroying Instr")
            del Instr
    else:
        print("Instr not found - creating new singleton")
    Instr = InstrX()

    for fname in l:
        sym = fname[:-4].lower()
        if fname[-4:] != SRC_EXT:
            continue
        if sym_lst and sym not in sym_lst:
            continue

        print(f"\nProcessing: {fname} \n")

        #with open("es.csv","wt") as file_out, open("ES.txt") as file_in:
        #    reader=csv.reader(file_in)
        #
        #    for line in file_in:
        #        file_out.write(line)

        file_path_src = os.path.join(pth_src, fname)
        file_path_des_zero = os.path.join(pth_src, fname[:-4].lower() + '_zero' + DES_EXT)
        file_path_des_clean = os.path.join(pth_src, fname[:-4].lower() + DES_EXT)

        """ slow for some reason ...
        date_parser = lambda d, t: pd.datetime.strptime(d+' '+t, '%m/%d/%Y %H%M')
        df_file = pd.read_csv(pth_file_src, index_col='Dtime', parse_dates={'Dtime':['Date','Time']}, date_parser=date_parser)
        """
        df_file = pd.read_csv(file_path_src, dtype = {"Time" : "str"})
        dtimes = pd.to_datetime(df_file.Date + ' ' + df_file.Time, format= '%m/%d/%Y %H%M')
        df_file.set_index(dtimes, inplace=True)
        # df_file = df_file.drop(['Date','Time'], axis=1)

        # Pre-allocate
        if asset == 'fut':
            beg_date = INSTR_SPECS[asset][group][sym]['beg_date']
            asset_sym = asset + '_' + sym
            asset_sym_ = asset_sym + '_'
            specs = INSTR_SPECS[asset][group][sym]
        elif asset == 'stk':
            beg_date = INSTR_SPECS[asset][group]['beg_date']
            asset_sym = asset + '_' + group + '_' + sym
            asset_sym_ = asset_sym + '_'
            specs = INSTR_SPECS[asset][group]

        o_time = specs['o_time']
        ob_time = specs['ob_time']
        c_time = specs['c_time']
        cb_time = specs['cb_time']
        cc_time = specs['cc_time']
        hilo_specs = specs['hilo']

        # beg_dtimestamp = pd.to_datetime('01/01/' + str(beg_year))
        beg_dtimestamp = pd.Timestamp(beg_date)
        end_dtimestamp = pd.to_datetime(str(df_file.index[-1].date()) + ' 23:59')

        index = pd.date_range(beg_dtimestamp, end_dtimestamp, freq='D')   # '1min'
        index = index[index.dayofweek!=5]   # saturday

        asset_sym_time_lst = [asset_sym_ + x for x in COLS_TIME]

        df_grid = pd.DataFrame(0.0, index=index, columns=asset_sym_time_lst)   # numpy.int64
        cont_dtimestamp_prev = pd.Timestamp((df_file.index[0] - datetime.timedelta(days=1)).date())
        hilo_specs = INSTR_SPECS[asset][group][sym]['hilo']
        specs = INSTR_SPECS[asset][group][sym]

        num_row=0
        #for i, cont_row in enumerate(df_file.itertuples(), 0):
        for cont_row in df_file.itertuples():
            # if cont_row.Index.date().year < beg_date:
            if cont_row.Index < beg_dtimestamp:
                continue

            # if num_row % 100 == 0:
            #     print(cont_row)
            num_row += 1

            cont_dtimestamp_cur = pd.Timestamp(cont_row.Index.date())
            if cont_dtimestamp_prev != cont_dtimestamp_cur:
                # while df_grid.index[1].date() <= df_file.index[0].date():
                #     df_grid.drop(df_grid.index[2], inplace=True)
                # df_grid[(df_grid.index >= t0) & (df_grid.index <= t2)]
                #D: print(cont_dtimestamp_prev, cont_dtimestamp_cur)
                df_nodates = df_grid[(df_grid.index > cont_dtimestamp_prev) & (df_grid.index < cont_dtimestamp_cur)]
                if df_nodates.index.shape[0] > 0:
                    print(num_row, df_nodates.index)
                    df_grid.drop(df_nodates.index, inplace=True)

                # HILO
                if num_row != 1:
                    for k,v in hilo_specs.items():
                        df_grid.loc[cont_dtimestamp_prev, asset_sym_ + k] = hilo_cur[k]
                        df_grid.loc[cont_dtimestamp_prev, asset_sym_ + 'l' + k[1:]] = hilo_cur['l' + k[1:]]

                # reset
                hilo_cur = {}
                for k,v in hilo_specs.items():
                    # if v[0][0] == 'd' or v[1][0] == 'd':
                    #     print(v)
                    hilo_cur[k] = -999999
                    hilo_cur['l' + k[1:]] = 999999

                cont_dtimestamp_prev = cont_dtimestamp_cur

            # HILO
            for k,v in hilo_specs.items():
                time_hilo_beg = v[0]
                time_hilo_end = v[1]
                if v[0].isalpha():
                    time_hilo_beg = specs[v[0]+'_time'][0]
                if v[1].isalpha():
                    time_hilo_end = specs[v[1]+'_time'][0]
                if cont_row.Time >= time_hilo_beg and cont_row.Time <= time_hilo_end:
                    # this is the test - NOTE: for no trade periods this never gets tested
                    if cont_row.High > hilo_cur[k]:
                        hilo_cur[k] = cont_row.High
                    if cont_row.Low < hilo_cur['l' + k[1:]]:
                        hilo_cur['l' + k[1:]] = cont_row.Low

            if cont_row.Time == o_time[2]:
                df_grid.loc[cont_dtimestamp_cur, asset_sym_ + o_time[1]] = getattr(cont_row, o_time[3])
                df_grid.loc[cont_dtimestamp_cur, asset_sym_ + o_time[0]] = getattr(cont_row, o_time[3])  #cont_row.Open
            elif cont_row.Time == ob_time[2]:
                df_grid.loc[cont_dtimestamp_cur, asset_sym_ + ob_time[1]] = getattr(cont_row, ob_time[3])
                df_grid.loc[cont_dtimestamp_cur, asset_sym_ + ob_time[0]] = getattr(cont_row, ob_time[3])
            elif cont_row.Time == c_time[2]:
                df_grid.loc[cont_dtimestamp_cur, asset_sym_ + c_time[1]] = getattr(cont_row, c_time[3])
                df_grid.loc[cont_dtimestamp_cur, asset_sym_ + c_time[0]] = getattr(cont_row, c_time[3])
                df_grid.loc[cont_dtimestamp_cur, asset_sym_ + c_time[2]] = cont_row.Open
            elif cont_row.Time == c_time[0]:
                pass
            elif cont_row.Time == cb_time[2]:
                df_grid.loc[cont_dtimestamp_cur, asset_sym_ + cb_time[1]] = getattr(cont_row, cb_time[3])
                df_grid.loc[cont_dtimestamp_cur, asset_sym_ + cb_time[0]] = getattr(cont_row, cb_time[3])
                df_grid.loc[cont_dtimestamp_cur, asset_sym_ + cb_time[2]] = cont_row.Open
            elif cont_row.Time == cb_time[0]:
                pass
            elif cont_row.Time == cc_time[2]:
                df_grid.loc[cont_dtimestamp_cur, asset_sym_ + cc_time[1]] = getattr(cont_row, cc_time[3])
                df_grid.loc[cont_dtimestamp_cur, asset_sym_ + cc_time[0]] = getattr(cont_row, cc_time[3])
                df_grid.loc[cont_dtimestamp_cur, asset_sym_ + cc_time[2]] = cont_row.Open
            elif cont_row.Time == cc_time[0]:
                pass
            else:
                #D: print(cont_dtimestamp_cur, asset_sym_ + cont_row.Time)
                df_grid.loc[cont_dtimestamp_cur, asset_sym_ + cont_row.Time] = cont_row.Open

        for k,v in hilo_specs.items():
            df_grid.loc[cont_dtimestamp_cur, asset_sym_ + k] = hilo_cur[k]
            df_grid.loc[cont_dtimestamp_cur, asset_sym_ + 'l' + k[1:]] = hilo_cur['l' + k[1:]]

        # if (num_row-1) % 1000 != 0:
        #     print(cont_row)

        if asset_sym_[:-1] in Instr:
            del Instr[asset_sym_[:-1]]
        Instr.attach(asset_sym_[:-1], specs, df_grid, df_hol)

        if bl_out_zeros:
            print("Output zero:", file_path_des_zero)
            Instr[asset_sym_[:-1]].df_grid.to_csv(file_path_des_zero, index_label='Date')

        if not bl_no_clean:
            Instr = clean_fill_zeros(asset_sym_[:-1], Instr) # df_grid, specs, df_hol) #, )

            print("Output clean:", file_path_des_clean)
            Instr[asset_sym_[:-1]].df_grid.to_csv(file_path_des_clean, index_label='Date')

    if bl_ret_grid:
        return Instr


def transform_grid_stk(sym_lst=None, pth=pth_stk_sp500):
    '''
    stk_sp500_lst = import_transform.get_sym_lst()
    import_transform.transform_grid_stk(stk_sp500_lst[:100])
    import_transform.transform_grid_stk(stk_sp500_lst[100:200])
    import_transform.transform_grid_stk(stk_sp500_lst[200:300])
    import_transform.transform_grid_stk(stk_sp500_lst[300:400])
    import_transform.transform_grid_stk(stk_sp500_lst[400:])

    import_transform.transform_grid_stk()

    0930 - 1559 only
    '''
    ts = pd.Timestamp

    if pth[0] == '~' or pth[0] == '/':
        pth_src = os.path.expanduser(pth)
    else:
        pth_src = os.path.abspath(os.path.join(PATH_DATA_IN, pth))

    if not sym_lst:
        sym_lst = get_sym_lst(pth)

    Instr = getattr(builtins, 'Instr')
    df_hol_es = Instr['fut_es']['hol']
    df_es = Instr['fut_es'].df_grid
    specs = Instr['fut_es'].specs

    o_time = specs['o_time']
    c_time = specs['c_time']
    hilo_specs = specs['hilo']

    # col_beg = df_es.columns.get_loc('fut_es_0930')
    # df_es.drop(df_es.columns[col_beg], axis=1)
    df_es = df_es[ df_es.index.dayofweek.isin([0,1,2,3,4]) ]
    df_es = df_es[ ~df_es.index.isin(df_hol_es.date) ]

    col_beg = df_es.columns.get_loc('fut_es_0930')
    col_end = df_es.columns.get_loc('fut_es_1600')
    _asset_sym_time_lst = list(df_es.columns[col_beg: col_end+1])

    tot_sym = len(sym_lst)
    for num_sym, sym in enumerate(sym_lst):
        sym = sym.lower()
        asset_sym_ = 'stk_' + sym + '_'
        asset_sym_time_lst = [ x.replace('fut_es_', asset_sym_) for x in _asset_sym_time_lst ]
        asset_sym_time_lst = [asset_sym_+'o', asset_sym_+'c', asset_sym_+'hdy', asset_sym_+'ldy'] + asset_sym_time_lst
        df_grid = pd.DataFrame(0.0, index=df_es.index, columns=asset_sym_time_lst)

        file_path_src = os.path.join(pth_src, sym.upper() + '.txt')
        file_path_des = os.path.join(pth_src, sym + '.csv')

        print(f'Processing {num_sym}/{tot_sym}: {file_path_src}')
        df_file = pd.read_csv(file_path_src, dtype = {"Time" : "str"})
        dtimes = pd.to_datetime(df_file.Date + ' ' + df_file.Time, format= '%m/%d/%Y %H%M')
        df_file.set_index(dtimes, inplace=True)

        df_grid.drop(df_grid[ (df_grid.index > ts(str(df_file.index[-1])[:10])) | (df_grid.index < ts(str(df_file.index[0])[:10])) ].index, inplace=True)

        cont_dtimestamp_prev = ts((df_file.index[0] - datetime.timedelta(days=1)).date())
        num_row=0
        for row_file in df_file.index:
            num_row += 1
            cont_dtimestamp_cur = ts(row_file.date())
            if cont_dtimestamp_prev != cont_dtimestamp_cur:
                df_nodates = df_grid[(df_grid.index > cont_dtimestamp_prev) & (df_grid.index < cont_dtimestamp_cur)]
                if df_nodates.index.shape[0] > 0:
                    print(file_path_src, num_row, df_nodates.index)
                    df_grid.drop(df_nodates.index, inplace=True)

                # Clean + alias
                # for row_dtimestamp in df_grid.index:
                if num_row > 1 and 0 in df_grid.loc[cont_dtimestamp_prev].values:
                    # arr_nonzero = df_grid.loc[row_dtimestamp,beg_col:].to_numpy().nonzero()[0]
                    beg_col = asset_sym_ + o_time[0]
                    df_grid.loc[cont_dtimestamp_prev, beg_col:] = df_grid.loc[cont_dtimestamp_prev, beg_col:].replace(0, method='ffill')
                    df_grid.loc[cont_dtimestamp_prev, beg_col:] = df_grid.loc[cont_dtimestamp_prev, beg_col:].replace(0, method='bfill')
                    df_grid.loc[cont_dtimestamp_prev, asset_sym_ + o_time[1]] = df_grid.loc[cont_dtimestamp_prev, asset_sym_ + o_time[0]]
                    df_grid.loc[cont_dtimestamp_prev, asset_sym_ + c_time[1]] = df_grid.loc[cont_dtimestamp_prev, asset_sym_ + c_time[0]]

                # HILO
                # if num_row != 1:
                #     for k,v in hilo_specs.items():
                #         df_grid.loc[cont_dtimestamp_prev, asset_sym_ + k] = hilo_cur[k]
                #         df_grid.loc[cont_dtimestamp_prev, asset_sym_ + 'l' + k[1:]] = hilo_cur['l' + k[1:]]
                #
                # # reset
                # hilo_cur = {}
                # for k,v in hilo_specs.items():
                #     # if v[0][0] == 'd' or v[1][0] == 'd':
                #     #     print(v)
                #     hilo_cur[k] = -999999
                #     hilo_cur['l' + k[1:]] = 999999

                cont_dtimestamp_prev = cont_dtimestamp_cur

            if df_file.loc[row_file, 'Time'] == o_time[2]:
                df_grid.loc[cont_dtimestamp_cur, asset_sym_ + o_time[1]] = df_file.loc[row_file, o_time[3]]
                df_grid.loc[cont_dtimestamp_cur, asset_sym_ + o_time[0]] = df_file.loc[row_file, o_time[3]]
            elif df_file.loc[row_file, 'Time'] == c_time[2]:
                df_grid.loc[cont_dtimestamp_cur, asset_sym_ + c_time[1]] = df_file.loc[row_file, c_time[3]]
                df_grid.loc[cont_dtimestamp_cur, asset_sym_ + c_time[0]] = df_file.loc[row_file, c_time[3]]
                df_grid.loc[cont_dtimestamp_cur, asset_sym_ + c_time[2]] = df_file.loc[row_file, 'Open']
            elif df_file.loc[row_file, 'Time'] == c_time[0]:
                pass
            else:
                df_grid.loc[cont_dtimestamp_cur, asset_sym_ + df_file.loc[row_file, 'Time']] = df_file.loc[row_file, 'Open']

        # Clean + alias
        if 0 in df_grid.loc[cont_dtimestamp_cur].values:
            beg_col = asset_sym_ + o_time[0]
            df_grid.loc[cont_dtimestamp_cur, beg_col:] = df_grid.loc[cont_dtimestamp_cur, beg_col:].replace(0, method='ffill')
            df_grid.loc[cont_dtimestamp_cur, beg_col:] = df_grid.loc[cont_dtimestamp_cur, beg_col:].replace(0, method='bfill')
            df_grid.loc[cont_dtimestamp_cur, asset_sym_ + o_time[1]] = df_grid.loc[cont_dtimestamp_cur, asset_sym_ + o_time[0]]
            df_grid.loc[cont_dtimestamp_cur, asset_sym_ + c_time[1]] = df_grid.loc[cont_dtimestamp_cur, asset_sym_ + c_time[0]]


        # for k,v in hilo_specs.items():
        #     df_grid.loc[cont_dtimestamp_cur, asset_sym_ + k] = hilo_cur[k]
        #     df_grid.loc[cont_dtimestamp_cur, asset_sym_ + 'l' + k[1:]] = hilo_cur['l' + k[1:]]

        df_grid.drop(df_grid[ (df_grid.index > df_es.index[-1] ) | (df_grid.index < df_es.index[0]) ].index, inplace=True)
        df_grid.to_csv(file_path_des, index_label='Date')


def get_sym_lst(pth=pth_stk_sp500, file_suffix='.txt'):
    '''
    stk_sp500_lst = import_transform.get_sym_lst()
    stk_sp500_lst = import_transform.get_sym_lst('~/Agape/development/projects/fintech/data_in/stk/sp500_1min')
    '''
    # sp500_lst = [ f.split('.csv')[0].lower() for f in os.listdir(PATH_DATA_SP500) if os.path.isfile(os.path.join(PATH_DATA_SP500, f)) and 'table_' not in f ]
    # return sp500_lst

    if not pth:
        from apps.settings.constants_fin import SP500_LST
        # but prob easier if just import right above ...
        return SP500_LST
    # if src == 'pth_stk_sp500_eod':
    #    pth = os.path.abspath(os.path.join(PATH_PROJ, 'pth_stk_sp500_eod_1998_2013'))
    #    return [ f.split('.csv')[0].lower() for f in os.listdir(pth) if os.path.isfile(os.path.join(pth, f)) and 'table_' not in f ]
    # if src == 'STK_SP500_LST':
    #     l = []
    #     for l_row in csv.reader(open(path_file), delimiter='\t'):
    #         if len(l_row) > 0:
    #             l.append(l_row[0])
    #     # l2 = sorted(list(set(SP500_LST)-set(l)))
    #     return l

    elif pth[0] == '~' or pth[0] == '/':
        pth_src = os.path.expanduser(pth)
    else:
        pth_src = os.path.abspath(os.path.join(PATH_DATA_IN, pth))

    l = os.listdir(pth_src)
    return sorted([fname.strip(file_suffix) for fname in l if fname[-4:] == file_suffix], key=str.lower)

    # return [ f.split('.csv')[0].lower() for f in os.listdir(pth) if os.path.isfile(os.path.join(pth, f)) and f[-4:] == '.csv' ]


def import_hol(asset_group):
    ''' Use:
    df_hol_fut_use = import_hol('fut_use')
    df_hol = import_hol('stk_s500')
    '''
    asset, group = asset_group.split('_')
    hol_fname = INSTR_SPECS[asset][group]['hol'] + '.txt'
    df_hol = pd.read_csv(os.path.join(PATH_DATA_IN, 'econ/'+hol_fname), header=None, parse_dates=[0]) # index_col=0)
    df_hol.columns = ['date','exclude']
    return df_hol


def import_fut_Instr(src, sym_lst=['es'], bl_new=True):
    '''
    Instr = import_fut_Instr(src='pth_fut_use', sym_lst=['es'], bl_new=True)
            import_fut_Instr(src='~/Agape/development/projects/fintech/data_in/fut/use_1min', sym_lst=['es'], bl_new=True)

    Instr['fut_es'], Instr['stk_sp500_appl']
    Instr.fut_es.df.loc[pd.Timestamp('2002-09-11'),'fut_es_0914':'fut_es_0931']
    Instr.fut_es.df.columns
    Instr.fut_es.columns
    Instr.fut_es.specs['o_time']
    '''

    if src[:4] == 'pth_':
        tmp_asset_group = src.split('_')
        asset, group = tmp_asset_group[1], tmp_asset_group[2]
        pth_src = os.path.join(PATH_DATA_IN, globals()[src])
    else:
        if src == 'pwd':
            pth_src = os.getcwd()
        elif '/' in src:
            if src[-1] == '/':
                src = src[:-1]
            pth_src = os.path.join(PATH_DATA_IN, src)
        tmp_asset_group = src.split('/')
        asset, group = tmp_asset_group[-2], tmp_asset_group[-1].split('_')[0]

    l = os.listdir(pth_src)
    print(l)

    if not sym_lst:
        sym_fname_lst = [sym for sym in l if sym[-4:] == DES_EXT and sym[-8:-4] != 'zero']
    else:
        sym_fname_lst = [sym + DES_EXT for sym in sym_lst]

    if bl_new and ('Instr' in locals() or 'Instr' in globals()):
        del Instr
        # Instr.clear()  # note: still exists, just empty!

        # if 'Instr' in globals():
        #     del globals()['Instr']
        # for k in Instr.keys():
            # Instr.pop(k)
            # del globals()['Instr'][k]
    # Instr = InstrX(asset_sym, specs, df_grid)
    Instr = InstrX()

    hol = import_hol(asset+'_'+group)

    for sym_fname in sym_fname_lst:
        print("Importing:", sym_fname)
        file_path = os.path.join(pth_src, sym_fname)
        df_grid = None
        df_grid = pd.read_csv(file_path, parse_dates=['Date']).set_index('Date')

        sym = sym_fname[:-len(DES_EXT)]
        if asset == 'fut':
            asset_sym = asset + '_' + sym
            specs = INSTR_SPECS[asset][group][sym]
        elif asset == 'stk':
            asset_sym = asset + '_' + group + '_' + sym
            specs = INSTR_SPECS[asset][group]
        print('Attach:', asset_sym)

        Instr.attach(asset_sym, specs, df_grid, hol)

    print('All Instr.keys():', Instr.keys())

    # Symbolic/pointers: meta and other data pointed to Instr['fut_es']
    asset_sym_0 = asset_sym = asset + '_' + sym_lst[0]
    if 'hol' not in Instr[asset_sym_0]:
        Instr[asset_sym_0]['hol'] = hol
        Instr[asset_sym_0]['col_idx_first'] = COL_IDX_0000
        Instr[asset_sym_0]['col_idx_last'] = COL_IDX_2359

    for asset_sym_0 in Instr.keys():
       if 'hol' not in Instr[asset_sym_0]:
            # Instr[asset_sym_0] = Dict_dot(
            #   dict(hol = Instr['fut_es'].hol)
            # )
            Instr[asset_sym_0]['hol'] = Instr[asset_sym_0].hol
            Instr[asset_sym_0]['col_idx_first'] = Instr[asset_sym_0].col_idx_0000
            Instr[asset_sym_0]['col_idx_last'] = Instr[asset_sym_0].col_idx_2359

    print()
    print(Instr.keys())
    print(Instr[asset_sym_0].keys())
    print(Instr.fut_es.df_grid.index[0])
    print(Instr.fut_es.df_grid.index[-1])
    print(Instr.fut_es.df_grid.shape)

    return Instr


def import_fut_dct_df(src='pth_fut_use', sym_lst=['es'], bl_debug=True):
# def import_fut_dct_df(src='pth_fut', sym_lst=['es','us'], bl_debug=True):

    # asset='fut'
    # group=''
    # asset_group = asset '_' + group

    df_fut = {fut.lower():None for fut in sym_lst}

    # parser = lambda M_D_Y: pd.datetime.strptime(M_D_Y, '%m %d %Y')

    #for fut, fut_file in fut_files_dct.items():
    if not sym_lst:
        # todo
        sym_lst = ['es','us']

    cnt=0
    for sym in sym_lst:
        if bl_debug:
            cnt+=1
            print("Importing - " + str(cnt) + ": " + sym)

        file_path = os.path.join(PATH_DATA_IN, globals()[src], sym.lower() + '.csv')
        # file_path = os.path.join(PATH_DATA_IN, asset_group, sym.upper() + '.csv')
        # file_path = os.path.join(PATH_DATA_IN, INSTR_SPECS[asset]['path'], sym.upper() + '.csv')

        # #df_dct[sym] = pd.read_csv(join(PATH_DATA_FUT, + file_name), parse_dates=['Date']).set_index('Date')
        # df_fut[sym] = pd.read_csv(file_path, parse_dates=[[0,1,2]], date_parser=parser, index_col=0)
        #
        # df_fut[sym].rename(columns=lambda x: x.replace(':', ''), inplace=True)
        # #df_fut[fut].rename(columns=lambda x: FUT_TIME_PREFIX+x, inplace=True)
        # df_fut[sym].rename(columns=lambda x: asset+'_'+sym+'_'+x, inplace=True)
        # df_fut[sym].rename(columns={asset+'_'+sym+'_'+'HIGH':asset+'_'+sym+'_h', asset+'_'+sym+'_'+'LOW':asset+'_'+sym+'_l', asset+'_'+sym+'_'+'W':asset+'_'+sym+'_w'}, inplace=True)
        # #df_fut[fut].drop('w', axis=1, inplace=True)
        # df_fut[sym] = pd.read_csv(file_path, parse_dates=[[0,1,2]], date_parser=parser, index_col=0)
        df_fut[sym] = pd.read_csv(file_path, parse_dates=['Date']).set_index('Date')
        df_fut[sym].index.names = ['date']

    return df_fut


def import_stk(sym_lst, pth=pth_stk_sp500):
    '''
    sym_lst = STK_SP500_DRUG_LST
    dct_stk = import_transform.import_stk(sym_lst)

    dct_stk = import_transform.import_stk(['zbra','zion','zts'])

    dct_stk = {}
    sym = 'zion'
    dct_stk[sym] = import_transform.import_stk(sym)

    dct_stk[sym] = import_transform.import_stk(sym, '~/Agape/development/projects/fintech/data_in/stk/sp500_1min/')

    dct_stk = import_transform.import_stk(sym)

    dct_stk = pd.read_csv('~/Agape/development/projects/fintech/data_in/stk/sp500_1min/ZION.csv', parse_dates=['Date']).set_index('Date')
    '''
    strat = getattr(builtins, 'strat')
    Instr = strat['Instr']
    specs = INSTR_SPECS['stk']['sp500']
    hol = Instr.fut_es.hol  

    if pth[0] == '~' or pth[0] == '/':
        pth_src = os.path.expanduser(pth)
    else:
        pth_src = os.path.abspath(os.path.join(PATH_DATA_IN, pth))

    if type(sym_lst) == str:
        sym_lst = [sym.lower()]

    sym_lst = [sym.lower() for sym in sym_lst]
    dct_stk = {sym:None for sym in sym_lst}
    for sym in sym_lst:
        file_path_src = os.path.join(pth_src, sym + '.csv')
        print('Importing:', file_path_src)
        dct_stk[sym] = pd.read_csv(file_path_src, parse_dates=['Date']).set_index('Date')
        print(dct_stk[sym].shape)

        asset_sym = 'stk_' + sym
        if asset_sym in Instr:
            del Instr[asset_sym]
        Instr.attach(asset_sym, specs, dct_stk[sym], hol)

    print(Instr.keys())
    print(f"id(Instr.stk_{sym}.df_grid) == id(dct_stk['{sym}']) ==",
          id(Instr['stk_'+sym].df_grid) == id(dct_stk[sym]))

    return dct_stk


def import_crypto(crp_lst=['btc'], bl_debug=False):
    asset='crp'

    df_ = {sym.lower():None for sym in crp_lst}

    # parser = lambda M_D_Y: pd.datetime.strptime(M_D_Y, '%m %d %Y')

    cnt=0
    #for fut, fut_file in fut_files_dct.items():
    for sym in crp_lst:
        if bl_debug:
            cnt+=1
            print("Importing - " + str(cnt) + ": " + sym)

        # todo - fix
        file_path = os.path.join(PATH_CRYPTO, sym + DES_SUFFIX_EXT)
        #df_[fut] = pd.read_csv(file_path, parse_dates=[[0,1,2]], date_parser=parser, index_col=0)
        df_[sym] = pd.read_csv(file_path, parse_dates=['Date']).set_index('Date')

        df_[sym].rename(columns={'Open':asset + '_' + sym + '_o', 'High':asset + '_' + sym +'_h', 'Low':asset + '_' + sym +'_l', 'Adj Close':asset + '_' + sym +'_c', 'Volume':asset + '_' + sym +'_v'}, inplace=True)
        df_[sym].index.names = ['date']

    return df_

# ==============================================================================

# if __name__ == "__main__":

    # extract()

    # Instr = transform_grid_import(src='pth_fut_use', sym_lst=['es'])                      # prod
    # Instr = transform_grid_import(src='pth_fut_use', sym_lst=['es'], bl_out_zeros=False)
    # Instr = transform_grid_import(src='pth_fut_use', sym_lst=['es'], bl_no_clean=True)    # debug


    # DEBUG
    # transform_grid_import(src='fut/use_tmp/, sym_lst=['es3']')


''' Use:
] os.chdir(os.environ['PATH_APP_FINTECH'])
$ cd $PATH_APP_FINTECH


from apps.app_util.import_transform import *
Instr = import_fut_Instr(src='pth_fut_use', sym_lst=['es'], bl_new=True)


$ cd $PATH_APP
$ python -m apps.app_util.import_transform
] %run -m apps.app_util.import_transform
  %run -m apps.app_util.import_transform.import_transform_grid(src='pth_fut_us')


pd.options.display.max_rows = None
pd.options.display.max_columns = None


asset_sym = 'fut_es'
dtimestamp = Instr.fut_es.df_grid.index[-3]
Instr.fut_es.df_grid.loc[dtimestamp,'fut_es_0930':'fut_es_1000']
print(Instr.fut_es.df_grid.loc[dtimestamp,'fut_es_2340':])
print(Instr.fut_es.df_grid.loc[dtimestamp+pd.Timedelta(days=1),'fut_es_0000':'fut_es_0010'])
'''
