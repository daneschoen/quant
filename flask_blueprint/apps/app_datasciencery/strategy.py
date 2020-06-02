import os, sys, pathlib
from collections import OrderedDict
import re
import itertools
import csv

import numpy as np
import pandas as pd
#from pandas.plotting import scatter_matrix
#import pandas.plotting as pdp

# import matplotlib
# matplotlib.use("Agg")
# import matplotlib.pyplot as plt
# import seaborn as sns
# sns.set(style="ticks", color_codes=True)

import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.sandbox.regression.predstd import wls_prediction_std
import statsmodels.graphics.api as smg

from sklearn import linear_model

#from flask_apps.stats import *
#from flask_apps.globals import *

#from os import listdir
#from os.path import isfile, join
#import glob
#sp500 = glob.glob("/Users/acrosspond/Agape/development/projects/fintech/data_in/equity_future_com/sp500/*.csv")
#os.curdir, os.listdir()

#from . import stats_regression
from apps.app_quant import stats_regression

#from ..settings.settings import PATH_PROJ, PATH_APP
from apps.settings.settings import PATH_PROJ, PATH_APP
from apps.settings.constants_fin import *

# ==============================================================================
# pth_wrk = os.path.join(PATH_PROJ, "data_in")
# pth_equity = "data_in/equity/"
# pth_com_fx = "data_in/com_fx/"
# pth_econ = "data_in/econ/"
# pth_crypto = "data_in/crypto/"

# PATH_FUT = os.path.join(PATH_PROJ, pth_fut)
# PATH_DATA_SP500 = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../..', pth_sp500))
# PATH_EQUITY_SP500 = os.path.join(PATH_PROJ, pth_equity_sp500)
    # cur_path = os.getcwd()
    # if cur_path[:7] == '/Users/':
    #     PROJ_ROOT = cur_path.rsplit('/', 3)

pth_fut = "data_in/future/fut_1min"      # "fut_2018/"
pth_equity_sp500 = "data_in/equity/sp500_1min/"
pth_equity_nasdaq100 = "data_in/equity/nasdaq100_1min/"

# old
pth_equity_sp500_eod_1998_2013 = "data_in/equity/sp500_1min/"


PATH_CRYPTO = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../..', pth_crypto))


FNAME_SUFFIX = "_1min_col"   #  "_data1col.csv"
EXT = ".csv"
FNAME_SUFFIX_EXT = FNAME_SUFFIX + EXT

TIME_PREFIX = 'p'   # 't_'

# ------------------------------------------------------------------------------
''' Used by:
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


df_stk_sp500 = strategy.import_equity_sp500_dct_df()
df_stk_nasdaq100 = strategy.import_equity_nasdaq100_dct_df()

df_stk = strategy.import_equity_dct_df()
df_stk['sp500']
df_stk.keys())

df_stk['aapl'].head()
df_stk['goog'].tail()

df_stk_pctchg = {sym: df_.pct_change()[1:] for sym, df_ in df_stk.items()}
df_stk['aapl'].head()
df_stk_pctchg['aapl'].head()

df_stk_pctchg['aapl'].columns

df_stk_pctchg = {sym: df_.pct_change()[1:] for sym, df_ in df_stk.items()}

'''


def get_sym_lst(src='pth_equity_sp500'):
    # sp500_lst = [ f.split('.csv')[0].lower() for f in os.listdir(PATH_DATA_SP500) if os.path.isfile(os.path.join(PATH_DATA_SP500, f)) and 'table_' not in f ]
    # return sp500_lst

    if src=='const':
        from apps.settings.constants_fin import SP500_LST
        # but prob easier if just import right above ...
        return SP500_LST
    if src == 'pth_equity_sp500_eod':
        pth = os.path.abspath(os.path.join(PATH_PROJ, 'pth_equity_sp500_eod_1998_2013'))
        return [ f.split('.csv')[0].lower() for f in os.listdir(pth) if os.path.isfile(os.path.join(pth, f)) and 'table_' not in f ]
    # if src == 'lst_equity_sp500':
    #     l = []
    #     for l_row in csv.reader(open(path_file), delimiter='\t'):
    #         if len(l_row) > 0:
    #             l.append(l_row[0])
    #     # l2 = sorted(list(set(SP500_LST)-set(l)))
    #     return l
    # if src == 'pth_equity_sp500':
    pth = os.path.abspath(os.path.join(PATH_PROJ, globals()[src]))
    return [ f.split('.csv')[0].lower() for f in os.listdir(pth) if os.path.isfile(os.path.join(pth, f)) and f[-4:] == '.csv' ]


def import_stk_dct_df(src=None, bl_debug=True):  # src='pth_equity_sp500'
    # asset='stk'
    # group='sp500'
    # asset_group = asset +'_'+ group

    #sym_lst = lst_sp500
    #if not sym_lst:
        # sym_lst = ['aapl','goog']
    sym_lst = get_sym_lst(src=src)

    df_stk_ = {sym.lower():None for sym in sym_lst}

    cnt=0
    for sym in sym_lst:
        cnt+=1
        if bl_debug:
            # print(str(cnt) + ": " + sym)
            print("{0:10s}".format(str(cnt) + ": " + sym), end="")
            if cnt % 11 == 0:
                print()

        file_path = os.path.join(PATH_PROJ, globals()[src], sym.upper() + '.csv')
        df_stk_[sym] = pd.read_csv(file_path, parse_dates=['Date']).set_index('Date')
        df_stk_[sym].index.name = 'date'

        # df_stk[sym].rename(columns=lambda x: x.replace('Adj. Open', asset_group + '_' + sym + '_o'), inplace=True)
        # df_stk[sym].rename(columns=lambda x: x.replace('Adj. Close', asset_group+'_'+sym+'_c'), inplace=True)
        # df_stk[sym].rename(columns=lambda x: x.replace('Adj. High', asset_group+'_'+sym+'_h'), inplace=True)
        # df_stk[sym].rename(columns=lambda x: x.replace('Adj. Low', asset_group+'_'+sym+'_l'), inplace=True)
        # df_stk[sym].rename(columns=lambda x: x.replace('Adj. Volume', asset_group+'_'+sym+'_v'), inplace=True)
        #
        # df_stk[sym].rename(columns={'Adj_Open':asset_group+'_'+sym+'_o', 'Adj_Close':asset_group+'_'+sym+'_c', 'Adj_High':asset_group+'_'+sym+'_h', 'Adj_Low':asset_group+'_'+sym+'_l', 'Adj_Volume':asset_group+'_'+sym+'_v'}, inplace=True)

    return df_stk_


def import_stk_group(src_lst=['pth_equity_sp500','pth_equity_nasdaq100']):

    # df_stk_sp500 = import_stk_dct_df(sym_lst, src)
    # df_stk_nasdaq100 = import_stk_dct_df(sym_lst, src)

    stk = {}
    for src in src_lst:
        group = src.split('_')[2]
        stk[group] = import_stk_dct_df[src]
    return stk


def import_fut(src='pth_fut', sym_lst=['es','us'], bl_debug=True):

    # asset='fut'
    # group=''
    # asset_group = asset + '_' + group

    df_fut = {fut.lower():None for fut in fut_lst}

    # parser = lambda M_D_Y: pd.datetime.strptime(M_D_Y, '%m %d %Y')

    #for fut, fut_file in fut_files_dct.items():
    if sym_lst is None:
        # todo
        sym_lst = []

    cnt=0
    for sym in sym_lst:
        if bl_debug:
            cnt+=1
            print("Importing - " + str(cnt) + ": " + sym)

        file_path = os.path.join(PATH_PROJ, globals()[src], sym.upper() + '.csv')
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

        file_path = os.path.join(PATH_CRYPTO, sym + FNAME_SUFFIX_EXT)
        #df_[fut] = pd.read_csv(file_path, parse_dates=[[0,1,2]], date_parser=parser, index_col=0)
        df_[sym] = pd.read_csv(file_path, parse_dates=['Date']).set_index('Date')

        df_[sym].rename(columns={'Open':asset + '_' + sym + '_o', 'High':asset + '_' + sym +'_h', 'Low':asset + '_' + sym +'_l', 'Adj Close':asset + '_' + sym +'_c', 'Volume':asset + '_' + sym +'_v'}, inplace=True)
        df_[sym].index.names = ['date']

    return df_



def merge_df(*df_lst, columns=[]):
    ''' Use:

    df_stk_es = merge_df(df_stk[sym_stk], df_fut[sym_fut])
              = merge_df(*[df_stk[sym_stk], df_fut[sym_fut]])

    #df_a.join(df_b, how='inner')     # ==   ONLY on index and only pair
    #pd.merge(df_a, df_b, on='date')  # ==   NEED TO HAVE NAME FOR INDEX

    df_stk_es = merge_df(df_stk[sym_stk], df_fut[sym_fut])
              = merge_df(*[df_stk[sym_stk], df_fut[sym_fut]])


    # Merge-concat on dates, but only include certain cols
    cols_incl = ['Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Close', 'Adj. Volume']
    df_pair = pd.concat([df_stk[syms[0]].loc[:,cols_incl],
                         df_stk[syms[1]].loc[:,cols_incl]], axis=1, join='inner')

    #df_a.join(df_b, how='inner')     # ==   ONLY on index and not more than pair
    #pd.merge(df_a, df_b, on='date')  # ==   NEED TO HAVE NAME FOR INDEX

    #df_es_us_.drop(df_es_us_.index[0],inplace=True)
    '''
    #df_a.join(df_b, how='inner')     # ==   ONLY on index and only pair
    #pd.merge(df_a, df_b, on='date')  # ==   NEED TO HAVE NAME FOR INDEX

    df_ = pd.concat(df_lst, axis=1, join='inner')
    df_.dropna(inplace=True)
    if columns:
        df_.columns = columns
    return df_


def pctchg_df(df_asset):
    return {asset: df_.pct_change()[1:] for asset, df_ in df_asset.items()}


"""
# ------------------------------------------------------------------------------
# strategy tools
# ------------------------------------------------------------------------------
"""

def strip_eqn_y_x(eqn_model):
    eqn_model = eqn_model.lower()

    col_y = [eqn_model.split('~')[0].strip()]
    col_X = [ft_str.strip() for ft_str in eqn_model.split('~')[1].strip().split('+')]

    return col_y, col_X


def calc_feat(feat_str, method='diff'):
    ''' Usage:
    feat_df = calc_feat('fut_us_c_1p1615')
    feat_df = calc_feat('fut_us_1p1615')
    feat_df = calc_feat('fut_es_l')
    feat_df = calc_feat('fut_es_o')

    feat_df['fut_es_c_c1']  = es[c_es] - es[c_es].shift(1)
    feat_df['fut_es_c1_c2'] = es[c_es].shift(1) - es[c_es].shift(2)
    feat_df['fut_es_c2_c3'] = es[c_es].shift(2) - es[c_es].shift(3)
    feat_df['fut_es_c3_c4'] = es[c_es].shift(3) - es[c_es].shift(4)
    feat_df['fut_es_o_c1']  = es[o_es] - es[c_es].shift(1)
    feat_df['fut_es_c_o1']  = es[c_es] - es[o_es].shift(1)
    feat_df['fut_es_p1500_1p1500'] = es['fut_es_1500'] - es['fut_es_1500'].shift(1)

    feat_df['fut_us_c_c1']  = us[c_us] - us[c_us].shift(1)
    feat_df['fut_us_c_1p1615'] = us[c_us]- us['fut_us_1615'].shift(1)
    feat_df['fut_us_c1_c2'] = us[c_us].shift(1) - us[c_us].shift(2)
    feat_df['fut_us_c2_c3'] = us[c_us].shift(2) - us[c_us].shift(3)
    feat_df['fut_us_c3_c4'] = us[c_us].shift(3) - us[c_us].shift(4)
    feat_df['fut_us_o_c1']  = us[o_us] - us[c_us].shift(1)
    feat_df['fut_us_c_o1']  = us[c_us] - us[o_us].shift(1)
    feat_df['fut_us_1p1700_1p1615']  = us[c_us].shift(1) - us['fut_us_1615'].shift(1)
    '''

    feat_str_lst = feat_str.lower().split('_')
    asset = feat_str_lst[0]            # fut, stk
    sym = feat_str_lst[1]              # us, es
    dytime_lst = feat_str_lst[2:]      # c2, o, l, 1p1615, 800
    df=[]
    for dytime in dytime_lst:
        if 'c' in dytime or 'o' in dytime:
            time = dytime[0]
            dy = 0
            if len(dytime) > 1:
                dy = int(dytime[1:])
            if asset == 'fut':
                df.append(df_fut[sym][asset + '_' + sym + '_' + InstrX[asset + '_' + sym][time + '_timestamp']].shift(dy).copy())
                print(asset + '_' + sym + '_' + InstrX[asset + '_' + sym][time + '_timestamp'], dy)
            elif asset == 'stk':
                ## todo diff times for world stocks - exh - norm to ET time
                df.append(df_stk[sym][asset + '_' + sym + '_' + InstrX[asset + '_' + sym][time + '_timestamp']].shift(dy).copy())

        elif 'p' in dytime:
            dy = 0
            idx = dytime.index('p')
            if idx > 0:
                dy = int(dytime[0:idx])
            time = dytime[idx+1:]
            if len(time) < 4:
                time = '0' + time
            if asset == 'fut':
                df.append(df_fut[sym][asset + '_' + sym + '_' + time].shift(dy).copy())
                print(asset + '_' + sym + '_' + time, dy)
            elif asset == 'stk':
                df.append(df_stk[sym][asset + '_' + sym + '_' + InstrX[asset + '_' + sym][time + '_timestamp']].shift(dy).copy())

        else:   # numerical times: 0800 <= fut_us_0800  , usually used for intrady
            dy = 0
            time = dytime
            if len(time) < 4:
                time = '0' + time
            if asset == 'fut':
                df.append(df_fut[sym][asset + '_' + sym + '_' + time].shift(dy).copy())
                print(asset + '_' + sym + '_' + time, dy)
            elif asset == 'stk':
                df.append(df_stk[sym][asset + '_' + sym + '_' + InstrX[asset + '_' + sym][time + '_timestamp']].shift(dy).copy())

    #print(df[0].head())
    #print(df[1].head())
    _df = df[0]
    if method == 'diff':
        print('Stationarize Method:', method)
        if len(df) > 1:
            for __df in df[1:]:
                _df -= __df
    elif method == 'pct':
        print('Stationarize Method:', method)
        if len(df) > 1:
            for __df in df[1:]:
                _df = (_df - __df)/__df
        _df *= 1000
    _df.columns = feat_str
    #_df.dropna(inplace=True)
    _df = stats_regression.clean_nan_inf_pd(_df)

    return _df


def calc_model(eqn_model, strat, bl_recalc_model=True, method='diff'):
    '''
    features are re-used if cached
    but reg is calc-ed new even if cached W re-used features
    '''
    eqn_model = eqn_model.lower()

    col_y, col_X = strip_eqn_y_x(eqn_model)
    col_y_X = col_y + col_X

    #feat_df_model = [calc_feat(ft_str) for ft_str in col_y_X]   # never cache
    #feat_df_model = [feat_df[ft_str] for ft_str in col_y_X]     # assume always cached
    feat_df_model=[]
    for ft_str in col_y_X:
        feat_df_ = strat['feat_df'].get(ft_str)
        if feat_df_ is None or bl_recalc_model:
            feat_df_ = calc_feat(ft_str, method=method)
            strat['feat_df'][ft_str] = feat_df_    # cache
        feat_df_model.append(feat_df_)

    df_model = merge_df(*feat_df_model, columns=col_y_X)

    tot_len = len(df_model.index)
    if strat['train_pct'] <= 0:
        train_beg, train_end = strat['train_beg'], strat['train_end']
        test_beg, test_end = strat['test_beg'], strat['test_end']
        train_len = train_end - train_beg
        test_len = test_end - test_beg
        df_train, df_test = df_model[train_beg:train_end], df_model[test_beg:test_end]
    else:
        train_len = int(tot_len*strat['train_pct'])
        test_len = tot_len - train_len
        train_beg = 0
        train_end = train_len
        test_beg = train_len
        test_end = tot_len
        df_train, df_test = df_model[:train_len], df_model[train_len:]

    model_reg, reg_model = None, None
    if train_len >= 8 and test_len >= 1:
        model_reg, reg_model = stats_regression.reg_ols_sm(df_train[col_y],
                                                           df_train[col_X])

    strat[eqn_model] = {}
    strat[eqn_model]['type'] = 'model'
    strat[eqn_model]['tot_len'] = tot_len
    strat[eqn_model]['train_beg'] = train_beg
    strat[eqn_model]['train_end'] = train_end
    strat[eqn_model]['train_len'] = train_len
    strat[eqn_model]['test_beg'] = test_beg
    strat[eqn_model]['test_end'] = test_end
    strat[eqn_model]['test_len'] = test_len

    strat[eqn_model]['eqn_model'] = eqn_model   # superfluous, just to keep things consistent
    strat[eqn_model]['df_model'] = df_model
    strat[eqn_model]['df_train'] = df_train
    strat[eqn_model]['df_test'] = df_test
    strat[eqn_model]['reg_model'] = reg_model

    return strat


def parse_eqn_model_filter(eqn_model_filter):
    ''' Usage:
    eqn_model_filter = 'fut_es_c_o ~ fut_es_o_c1 < 0 + fut_es_c1_c2 < 0 + fut_es_c2_c3 < 0 + fut_es_c3_c4 < 0'  #*****!
    eqn_model_filter = 'fut_es_c_o ~ fut_es_o_c1 + fut_es_c1_c2 < 0 + fut_es_c2_c3 < 0 + fut_es_c3_c4 < 0'

    eqn_model = strategy.parse_eqn_model_filter(eqn_model_filter)
    '''

    y, X = eqn_model_filter.lower().split('~')
    eqn_model = y.strip() + ' ~ '

    X = X.split('+')
    for x in X:
        eqn_model += re.split("[>,>=,<,<=]+", x.strip())[0].strip() + ' + '
    eqn_model = eqn_model[:-3]
    return eqn_model


def calc_model_filter(eqn_model_filter, strat, eqn_model=None, bl_recalc_model=True, method='diff'):
    ''' DEFAULTS to re - calc_model '''
    eqn_model_filter = eqn_model_filter.lower()

    if not eqn_model:
        eqn_model = parse_eqn_model_filter(eqn_model_filter)
    else:
        eqn_model = eqn_model.lower()

    # bl_recalc = strat.get('bl_recalc', True)
    if bl_recalc_model or eqn_model not in strat:
        strat = calc_model(eqn_model, strat, bl_recalc_model=bl_recalc_model, method=method)

    df_model = strat[eqn_model]['df_model']   #strat[strat['eqn_model']]['df_model']
    #df_model[eqn_model_filter] = df_model[eqn_model].query('fut_es_c1_c2 < 0 and fut_es_c2_c3 < 0 and fut_es_c3_c4 < 0')

    col_y, col_X = strip_eqn_y_x(eqn_model_filter)
    col_X_query = []
    gtl_lst = ['>=', '<=', '=', '>', '<']   #! ORDER IS IMPORTANT
    for x in col_X:
        #if '>' in x or '<' in x or '=' in x:
        #    col_X_query.append(x)
        for gtl in gtl_lst:
            if gtl in x:
                sides = x.split(gtl)
                col_X_query.append(sides[0].strip() + ' ' + gtl + ' ' + sides[1].strip())
                break   #! important

    if len(col_X_query) > 1:
        df_model_filter = df_model.query(' and '.join(col_X_query))
    else:
        df_model_filter = df_model.query(col_X_query[0])

    df_model_filter.columns = col_y + col_X
    tot_len = len(df_model_filter.index)

    if strat['train_pct'] <= 0:
        train_beg, train_end = strat['train_beg'], strat['train_end']
        test_beg, test_end = strat['test_beg'], strat['test_end']
        train_len = train_end - train_beg
        test_len = test_end - test_beg
    else:
        train_len = int(tot_len*strat['train_pct'])
        test_len = tot_len - train_len
        train_beg = 0
        train_end = train_len
        test_beg = train_len
        test_end = tot_len

    df_train_filter, df_test_filter = df_model_filter[train_beg:train_end], df_model_filter[test_beg:test_end]

    model_reg, reg_model = None, None
    if train_len >= 7 and test_len >= 1:
        model_reg, reg_model = stats_regression.reg_ols_sm(df_train_filter[col_y],
                                                           df_train_filter[col_X])

    strat[eqn_model_filter] = {}
    strat[eqn_model_filter]['type'] = 'filter'

    strat[eqn_model_filter]['tot_len'] = tot_len
    strat[eqn_model_filter]['train_beg'] = train_beg
    strat[eqn_model_filter]['train_end'] = train_end
    strat[eqn_model_filter]['train_len'] = train_len
    strat[eqn_model_filter]['test_beg'] = test_beg
    strat[eqn_model_filter]['test_end'] = test_end
    strat[eqn_model_filter]['test_len'] = test_len

    strat[eqn_model_filter]['eqn_model'] = eqn_model   # link to model, old: = strat['eqn_model']
    strat[eqn_model_filter]['eqn_model_filter'] = eqn_model_filter
    strat[eqn_model_filter]['df_model_filter'] = df_model_filter
    strat[eqn_model_filter]['df_train_filter'] = df_train_filter
    strat[eqn_model_filter]['df_test_filter'] = df_test_filter
    strat[eqn_model_filter]['reg_model'] = reg_model

    return strat


## todo
def graph_pl():
    # residuals
    # hat vs real
    pass


def pl(df_test, reg_model, pred_thresh_pct=None, pred_thresh_pts=0.33):
    ''' Usage:
    - df_test
      - columns can ONLY contain relevant y, X: [y, x_1, x_2, ..., x_k]
      - can be test or valid
      - can be any length, >= 1
    - reg_model.params can be from model or filter
      - BUT DATES MUST MATCH ! test, valid dates > reg dates
        This fn does NOT CHECK if dates match !
    '''

    X = sm.add_constant(df_test.iloc[:, 1:])
    y_test_hat = np.dot(X, reg_model.params)

    y_test = df_test.iloc[:,0]
    y_test_err = (y_test_hat - y_test)/y_test
    max_y_test = np.max(np.abs(y_test))

    columns = ['win_sym', 'win_long', 'win_shrt', 'hat', 'real', 'pts', 'pct_err']
    df_pl = pd.DataFrame(index=df_test.index, columns=columns)

    strat_pl = OrderedDict([
      ('pct_win_tot',0),
      ('pct_win_long',0),
      ('pct_win_shrt',0),

      ('num_tot',0),
      ('num_long',0),
      ('num_short',0),

      ('pct_win_thresh',0), ('pct_win_thresh_long',0), ('pct_win_thresh_shrt',0),
      ('num_thresh',0), ('num_thresh_long',0), ('num_thresh_shrt',0),

      ('pct_win_nocoef_long',0), ('pct_win_nocoef_shrt',0),
      ('num_nocoef',0),

      ('df_pl', df_pl),
      ('len_train', int(reg_model.nobs)),
      ('len_test', len(y_test)),
      ('len_valid', 0)
    ])

    i=0
    #print(f"{'Win':>2} {'Pred':>10} {'Actual':>11} {'Pts':>11} {'Pct Err':>11}")
    #for _y_test_hat, _y_test, _y_test_err in zip(y_test_hat, y_test, y_test_err):
    for rec in df_test.itertuples(index=True, name='Pandas'):
        if np.sign(y_test_hat[i]) == np.sign(y_test[i]):
            strat_pl['pct_win_tot'] += 1
            df_pl.iloc[i]['win_sym'] = '+'
        else:
            df_pl.iloc[i]['win_sym'] = '-'

        df_pl.iloc[i]['hat']  = y_test_hat[i]
        df_pl.iloc[i]['real'] = y_test[i]

        strat_pl['num_tot'] += 1
        if y_test_hat[i] > 0:
            strat_pl['num_long'] += 1
            #df_pl.iloc[i]['pts']  = y_test_hat.iloc[i] - y_test.iloc[i]
            df_pl.iloc[i]['pct_err'] = y_test_err[i]
            if y_test[i] > 0:
                strat_pl['pct_win_long'] += 1
                df_pl.iloc[i]['win_long'] = '+'
            else:
                df_pl.iloc[i]['win_long'] = '-'
            df_pl.iloc[i]['win_shrt'] = ' '
        elif y_test_hat[i] < 0:
            strat_pl['num_short'] += 1
            #df_pl.iloc[i]['pts']  = y_test_hat.iloc[i] - y_test.iloc[i]
            df_pl.iloc[i]['pct_err'] = -y_test_err[i]
            if y_test[i] < 0:
                strat_pl['pct_win_shrt'] += 1
                df_pl.iloc[i]['win_shrt'] = '+'
            else:
                df_pl.iloc[i]['win_shrt'] = '-'
            df_pl.iloc[i]['win_long'] = ' '
        # --------------------------
        # thresh - skip near pred 0:
        # --------------------------
        if pred_thresh_pct:
            if np.abs(y_test_hat[i]) < pred_thresh_pct*max_y_test :
                pass   # dont trade
        elif np.abs(y_test_hat[i]) <= pred_thresh_pts :
                pass   # dont trade
        else:
            if np.sign(y_test_hat[i]) == np.sign(y_test[i]):
                strat_pl['pct_win_thresh'] += 1

            strat_pl['num_thresh'] += 1
            if y_test_hat[i] > 0:
                strat_pl['num_thresh_long'] += 1
                if y_test[i] > 0:
                   strat_pl['pct_win_thresh_long'] += 1
            elif y_test_hat[i] < 0:
                strat_pl['num_thresh_shrt'] += 1
                if y_test[i] < 0:
                    strat_pl['pct_win_thresh_shrt'] += 1

        # --------------------------
        # nocoef:
        # --------------------------
        strat_pl['num_nocoef'] += 1
        if y_test[i] > 0:
            strat_pl['pct_win_nocoef_long'] += 1
        elif y_test[i] < 0:
            strat_pl['pct_win_nocoef_shrt'] += 1

        i+=1

    #print(f'{sym:>2} {_y_test_hat:11.3f} {_y_test:11.3f} {pts:11.3f} {_y_test_err:11.3f}' )

    if strat_pl['num_tot'] == 0:
        strat_pl['pct_win_tot'] = np.nan
    else:
        strat_pl['pct_win_tot'] /= strat_pl['num_tot']
    if strat_pl['num_long'] == 0:
        strat_pl['pct_win_long'] = np.nan
    else:
        strat_pl['pct_win_long'] /= strat_pl['num_long']
    if strat_pl['num_short'] == 0:
        strat_pl['pct_win_shrt'] = np.nan
    else:
        strat_pl['pct_win_shrt'] /= strat_pl['num_short']

    if strat_pl['num_thresh'] == 0:
        strat_pl['pct_win_thresh'] = np.nan
    else:
        strat_pl['pct_win_thresh'] /= strat_pl['num_thresh']
    if strat_pl['num_thresh_long'] == 0:
        strat_pl['pct_win_thresh_long'] = np.nan
    else:
        strat_pl['pct_win_thresh_long'] /= strat_pl['num_thresh_long']
    if strat_pl['num_thresh_shrt'] == 0:
        strat_pl['pct_win_thresh_shrt'] = np.nan
    else:
        strat_pl['pct_win_thresh_shrt'] /= strat_pl['num_thresh_shrt']

    if strat_pl['num_nocoef'] == 0:
        strat_pl['pct_win_nocoef_long'] = np.nan
    else:
        strat_pl['pct_win_nocoef_long'] /= strat_pl['num_nocoef']
    if strat_pl['num_nocoef'] == 0:
        strat_pl['pct_win_nocoef_shrt'] = np.nan
    else:
        strat_pl['pct_win_nocoef_shrt'] /= strat_pl['num_nocoef']

    return strat_pl


def pl_output(strat_pl, bl_pl=True, bl_summary_long=False):
    print('Train len*:', strat_pl['len_train'], '  Test len:', strat_pl['len_test'])
    if bl_pl:
        # print(strat_pl['df_pl'])
        print(strat_pl['df_pl'].to_string(formatters={'win_shrt':'{:^8}'.format}))
    print()
    print(' '.join(strat_pl['df_pl']['win_sym']))
    print(' '.join(strat_pl['df_pl']['win_long']))
    print(' '.join(strat_pl['df_pl']['win_shrt']))
    print()

    if bl_summary_long:
        for k,v in strat_pl.items():
            if k != 'df_pl' and k[:3] != 'len':
                #print(f'{k:>10} : {v:5.2f}')
                if k[:3] == 'pct':
                    print("{0:<21s} {1:7.2f}".format(k,v))
                else:
                    print("{0:<21s} {1:7d}".format(k,v))

                if k == 'num_short' or k == 'num_thresh_shrt':
                    print()
    else:
        print("pct_win_tot            : {0:7.2f}".format(strat_pl['pct_win_tot']))
        print("pct_win_long, shrt     : {0:7.2f}   {1:7.2f}".format(strat_pl['pct_win_long'], strat_pl['pct_win_shrt']))
        print("num_tot                : {0:7d}".format(strat_pl['num_tot']))
        print("num_long, shrt         : {0:7d}   {1:7d}\n".format(strat_pl['num_long'], strat_pl['num_short']))

        print("pct_win_thresh         : {0:7.2f}".format(strat_pl['pct_win_thresh']))
        print("pct_win_thresh_long, s : {0:7.2f}   {1:7.2f}".format(strat_pl['pct_win_thresh_long'], strat_pl['pct_win_thresh_shrt']))
        print("num_thresh             : {0:7d}".format(strat_pl['num_thresh']))
        print("num_thresh_long, shrt  : {0:7d}   {1:7d}".format(strat_pl['num_thresh_long'], strat_pl['num_thresh_shrt']))

        print("pct_win_nocoef_long, s : {0:7.2f}   {1:7.2f}".format(strat_pl['pct_win_nocoef_long'], strat_pl['pct_win_nocoef_shrt']))
        print("num_nocoef             : {0:7d}".format(strat_pl['num_nocoef']))
        print()


def df_pl_output(df_pl):
    """
        win_sym += strat_pl['df_pl'].iloc[0, 0] + " "
        if strat_pl['df_pl'].iloc[0, 0] == '+':
            win_pct += 1
        num_all += 1

        if strat_pl['df_pl'].iloc[0]['hat'] > 0:
            num_long += 1
            if strat_pl['df_pl'].iloc[0]['real'] > 0:
                win_pct_long += 1

        elif strat_pl['df_pl'].iloc[0]['hat'] < 0:
            num_shrt += 1
            if strat_pl['df_pl'].iloc[0]['real'] < 0:
                win_pct_shrt += 1

        i += 1
    """
    pass


def calc_model_filter_rolling(eqn_model_filter, strat, eqn_model=None, train_test_pct=[0.75, 0.15], bl_model_coef=False):
    '''
    if bl_model_coef == True: y_hat = model_coef * model_filter
    '''
    eqn_model_filter = eqn_model_filter.lower()

    if not eqn_model:
        eqn_model = parse_eqn_model_filter(eqn_model_filter)
    else:
        eqn_model = eqn_model.lower()

    strat['train_pct'] = train_test_pct[0]
    if not bl_model_coef:
        strat = calc_model_filter(eqn_model_filter, strat)
        reg_model = strat[eqn_model_filter]['reg_model']
        df_model_filter = strat[eqn_model_filter]['df_model_filter']
        df_test_filter = strat[eqn_model_filter]['df_test_filter']

    else:
        strat = calc_model(eqn_model, strat)
        reg_model = strat[eqn_model]['reg_model']

        dt_last_model_train = strat[eqn_model]['df_train'].iloc[-1].name

        strat = calc_model_filter(eqn_model_filter, strat, bl_recalc_model=False)
        df_model_filter = strat[eqn_model_filter]['df_model_filter']
        df_test_filter = df_model_filter[df_model_filter.index > dt_last_model_train]

    strat_pl_noroll = pl(df_test_filter, reg_model)

    # Now start the rolling coef:
    tot_len = len(strat[eqn_model_filter]['df_model_filter'].index)

    train_len = int(tot_len * train_test_pct[0])
    test_len = int(tot_len * train_test_pct[1])
    strat['train_beg'] = 0 - 1
    strat['train_end'] = train_len - 1
    strat['test_beg'] = train_len - 1
    strat['test_end'] = train_len + test_len - 1

    win_sym = ""
    win_pct = 0
    win_pct_long = 0
    win_pct_shrt = 0
    num_all = 0
    num_long = 0
    num_shrt = 0
    i=0
    print()
    while strat['test_end'] < tot_len:
        strat['train_pct'] = -1

        strat['train_beg'] += 1
        strat['train_end'] += 1
        strat['test_beg'] += 1
        strat['test_end'] += 1

        if not bl_model_coef:
            strat = calc_model_filter(eqn_model_filter, strat)
            reg_model = strat[eqn_model_filter]['reg_model']
            df_test_filter = strat[eqn_model_filter]['df_test_filter']
        else:
            strat = calc_model(eqn_model, strat)
            reg_model = strat[eqn_model]['reg_model']

            dt_last_model_train = strat[eqn_model]['df_train'].iloc[-1].name

            strat = calc_model_filter(eqn_model_filter, strat, bl_recalc_model=False)
            df_model_filter = strat[eqn_model_filter]['df_model_filter']
            df_test_filter = df_model_filter[df_model_filter.index > dt_last_model_train]

        # print('\n\nMODEL:', eqn_model_filter, '\n')
        # print(strat[eqn_model_filter]['reg_model'].summary(), '\n\n')

        print('.'*10 + '\nMODEL:', eqn_model_filter)
        print('Roll - ' + str(i) + '   Train - ' + str(strat['train_beg']) + ':' + str(strat['train_end']) + '   Test - ' + str(strat['test_beg']) + ':' + str(strat['test_end']) )
        # print(strat[eqn_model_filter]['reg_model'].summary(), '\n\n')
        # strat_pl = pl(strat[eqn_model_filter]['df_test'], strat[eqn_model_filter]['reg_model'])
        strat_pl = pl(df_test_filter, reg_model)
        pl_output(strat_pl, bl_pl=False)

        win_sym += strat_pl['df_pl'].iloc[0, 0] + " "
        if strat_pl['df_pl'].iloc[0, 0] == '+':
            win_pct += 1
        num_all += 1

        if strat_pl['df_pl'].iloc[0]['hat'] > 0:
            num_long += 1
            if strat_pl['df_pl'].iloc[0]['real'] > 0:
                win_pct_long += 1

        elif strat_pl['df_pl'].iloc[0]['hat'] < 0:
            num_shrt += 1
            if strat_pl['df_pl'].iloc[0]['real'] < 0:
                win_pct_shrt += 1

        i += 1

    print()
    print(win_sym)

    win_pct = np.nan if num_all == 0 else win_pct/num_all
    win_pct_long = np.nan if num_long == 0 else win_pct_long/num_long
    win_pct_shrt = np.nan if num_shrt == 0 else win_pct_shrt/num_shrt

    print('win_pct_roll      : {0:6.2f}'.format(win_pct))
    print('win_pct_roll_long : {0:6.2f}'.format(win_pct_long))
    print('win_pct_roll_shrt : {0:6.2f}'.format(win_pct_shrt))
    print()

    pl_output(strat_pl_noroll)

# ------------------------------------------------------------------------------

def strat_scanner(strat, freq='30min', num_coef=3):
    '''
    Every M min increments

    eqn_model  = "fut_es_0015_0010 ~ fut_es_0010_0005 + fut_es_0005_0000"
    eqn_model  = "fut_es_1000_0930 ~ fut_es_0930_0900 + fut_es_0900_0830"
    eqn_model_filter = "fut_es_1000_0930 ~ fut_es_0930_0900 > 0 + fut_es_0900_0830 > 0"

    '''
    freq_lst = ['1min','2min','3min','4min','5min','10min','15min','30min','H']
    if freq:
        freq = freq
    time_inc_lst = [ x[11:16].replace(':','') for x in pd.date_range('2019-01-01', '2019-01-02', freq=freq, tz='UTC').astype(str) ][:-1]

    asset_sym = 'fut_es_'
    eqn_model_lst = []
    beg = num_coef + 1
    for i in range(beg, len(time_inc_lst)):
        """
        eqn_model_lst.append( asset_sym + time_inc_lst[i] + '_' + time_inc_lst[i-1] +
                              ' ~ ' + asset_sym + time_inc_lst[i-1] + '_' + time_inc_lst[i-2] +
                              ' + ' + asset_sym + time_inc_lst[i-2] + '_' + time_inc_lst[i-3] +
                              ' + ' + asset_sym + time_inc_lst[i-3] + '_' + time_inc_lst[i-4] )
        """
        eqn_model = asset_sym + time_inc_lst[i] + '_'  + time_inc_lst[i-1] + ' ~ '
        for k in range(num_coef):
            eqn_model += asset_sym + time_inc_lst[i-k-1] + '_' + time_inc_lst[i-k-2] + ' + '

        eqn_model_lst.append(eqn_model[:-3])

    strat_scan = {k: None for k in eqn_model_lst}

    for eqn_model in eqn_model_lst:
        print(eqn_model)
        strat['train_pct'] = strat['TRAIN_PCT']
        strat_scan[eqn_model] = {}
        strat_scan[eqn_model]['reg_model'] = calc_model(eqn_model, strat)[eqn_model]['reg_model']
        strat_scan[eqn_model]['max_coef'] = max(abs(strat_scan[eqn_model]['reg_model'].params[1:]))

        # strat = strategy.calc_model_filter(eqn_model_filter, eqn_model, strat)
        # strat_pl = strategy.pl(strat[eqn_model_filter]['df_test'], strat[eqn_model_filter]['reg_model'])

        # abs(strat[eqn_model]['reg_model'].params[1:])  rsquared_adj   pvalues[1:]
        # t_test   f_test   f_pvalue

    return sorted(strat_scan.items(), key=lambda x: x[1]['max_coef'])  # , reverse=True)  # easier to see not reversed


def permute_eqn_model_filter(eqn_model, product_sym_lst = ['>','<'], bl_print=True):
    ''' Step #1a:
        permute >< for eqn_model_filter  <=  eqn_model = most promising from scan
    '''
    y, X = strip_eqn_y_x(eqn_model.lower())
    num_coef = len(X)
    permute_gtl = itertools.product(product_sym_lst, repeat=num_coef)
    eqn_model_filter_lst = []
    for filter in permute_gtl:
        eqn_model_filter = y[0] + ' ~ '
        for x, gtl in zip(X, filter):
            eqn_model_filter += x + ' ' + gtl + " 0 + "

        eqn_model_filter_lst.append(eqn_model_filter[:-3])

    if bl_print:
        for eqn_model_filter in eqn_model_filter_lst:
            print(eqn_model_filter)

    return eqn_model_filter_lst


def calc_permute_eqn_model_filter(eqn_model_filter_lst, strat):
    ''' Step #1b:
        calc_model_filter for product permutation lst
    '''
    i=1
    num_tot_permute = len(eqn_model_filter_lst)
    for eqn_model_filter in eqn_model_filter_lst:
        strat['train_pct'] = strat['TRAIN_PCT']
        strat = calc_model_filter(eqn_model_filter, strat)
        print('\n' + '.'*80 + '\nMODEL', str(i) + '/' + str(num_tot_permute) + ':', eqn_model_filter, '\n')
        if strat[eqn_model_filter]['reg_model']:
            print(strat[eqn_model_filter]['reg_model'].summary(), '\n\n')
            strat_pl = pl(strat[eqn_model_filter]['df_test_filter'], strat[eqn_model_filter]['reg_model'])
            pl_output(strat_pl, bl_pl=False, bl_summary_long=False)
        else:
            print('*train_len, test_len:', strat[eqn_model_filter]['train_len'], strat[eqn_model_filter]['test_len'], '\n\n')

        i+=1


# ==============================================================================
# ==============================================================================
