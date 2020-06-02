import os, sys
import datetime
import pytz, time

import numpy as np
import pandas as pd
#import pandas.io.data
#from pandas.io import data, wb   < 0.17.0
from pandas_datareader import data as pd_webdata
from pandas_datareader import wb as pd_wb
from pandas.plotting import autocorrelation_plot as pd_autocorr_plot

import fix_yahoo_finance
fix_yahoo_finance.pdr_override()

# Must be in this order
#import matplotlib as mpl
#mpl.use('Agg')
#import matplotlib.pyplot as plt
#import matplotlib.dates as mdates

# import seaborn as sns

from .constants import *

"""
vol
which time of day volume
intraday
rolling correlation:
- pairwise
- crypto vs es during us times? what happens night
  vs bonds vs dax during euro time

"""

# ==============================================================================
# datetime.datetime.fromtimestamp(1435968000.0)

# ==============================================================================


df_es = None
df_btcusd = None


def import_csv(path_file):   # path_file=PATH_FILE
    return pd.read_csv(path_file)


def get_common_dates(df0, df1):
    # df_es.loc[3385,'ts'] == df_btcusd.loc[2756,'ts']
    pass



def run_stats(df_matrix):
    """
    df = pd.DataFrame(np.random.randn(1000, 4),
                     index=pd.date_range('1/1/2000', periods=1000),
                      columns=['A', 'B', 'C', 'D'])
    """
    # Rolling mean
    # ax = df_es_com.loc[:,'23:59'].rolling(30).mean().plot()
    # roll_mean = df_es_com.loc[:,'23:59'].rolling(30).mean()

    # Rolling sum
    #ax = df.rolling(3, win_type='triang').sum()


    # -------------------
    # Rolling correlation
    # -------------------
    ROLLING_CORR_PER = 90
    df_matrix_pctchg = df_matrix.pct_change()

    # df_rollcorr_mat = df_pctchg.rolling(window=ROLLING_CORR_PER).corr(pairwise=True)
    df_rollcorr_mat = df_matrix_pctchg.rolling(window=ROLLING_CORR_PER).corr()
    s_rollcorr = df_rollcorr_mat.unstack(1)[('btcusd', 'es')]
    #s_rollcorr = pd.Series(s_rollcorr, index = s_rollcorr)

    fig = plt.figure()
    s_rollcorr.plot()

    fig.savefig(os.path.join(PATH_OUT_CHART, "rolling_corr_btcusd_es.png"))


    # -------------------
    # Scatter
    # -------------------
    mplot = plt.scatter(df_pctchg[-200:].btcusd, df_pctchg[-200:].es)
    plt.xlabel('Returns BTC-USD')
    plt.ylabel('Returns S&P Futures')

    fig = mplot.get_figure()
    fig.savefig(os.path.join(PATH_OUT_CHART, "scatter_btcusd_es.png"))


    # --------------------
    # Autocorrelation, ACF
    # --------------------
    LAGS = 10
    # results["autocorr"] = [pd.Series(x).autocorr(lag) for lag in range(LAGS)]
    autocorr = [df_pctchg['btcusd'].autocorr(lag) for lag in range(LAGS)]
    fig = plt.figure()
    plt.plot(autocorr)  #kind="bar", figsize=(10,5), grid=True)
    fig.savefig(os.path.join(PATH_OUT_CHART, "scatter_btcusd_autocorr.png"))

    fig = plt.figure()
    pd_autocorr_plot(df_pctchg.loc[:,'btcusd'])
    fig.savefig(os.path.join(PATH_OUT_CHART, "scatter_btcusd_autocorr0.png"))

    fig = plt.figure()
    pd_autocorr_plot(df_pctchg.loc[:,'es'])
    fig.savefig(os.path.join(PATH_OUT_CHART, "scatter_es_autocorr0.png"))


def save_data(df_es, df_btcusd, df_matrix):

    df_btcusd.to_csv(os.path.join(PATH_DATA_IN, 'df_btcusd.csv'), encoding='utf-8', index=False)
    df_es.to_csv(os.path.join(PATH_DATA_IN, 'df_es.csv'), encoding='utf-8', index=False)
    df_matrix.to_csv(os.path.join(PATH_DATA_IN, 'df_matrix.csv'), encoding='utf-8')


    """
    for k, v in list(locals().items()):
         if v is df_btcusd:
             as_str = k
             print(as_str)

    blah = 1
    blah_name = [ k for k,v in locals().items() if v is blah][0]

    df_btcusd_name = [ k for k,v in locals().items() if v is df_btcusd][0]
    """


def clean_data():
    df = df.replace(np.nan, 0)

def import_data():
    df_es = import_csv(PATH_FILE_ES)
    df_btcusd = import_csv(PATH_FILE_BTC_USD)
    df_es.rename(columns={"Y": "year", "D": "day", "M": "month"}, inplace=True)

    s_ts_es = pd.to_datetime(df_es.loc[:, :'year'])
    s_ts_btcusd = pd.to_datetime(df_btcusd.loc[:, 'Date'])

    df_es['ts'] = s_ts_es
    df_btcusd['ts'] = s_ts_btcusd

    df_es_com = df_es[df_es['ts'].isin(df_btcusd['ts'])]
    df_btcusd_com = df_btcusd[df_btcusd['ts'].isin(df_es['ts'])]

    ES_TIME = "19:00"
    #s_es = pd.Series(df_es_com.loc[:,'23:59'], index=df_es_com.loc[:,'ts'])
    s_es = pd.Series(df_es_com.loc[:,ES_TIME])
    s_es.index = df_es_com.loc[:,'ts']
    s_es_1615 = pd.Series(df_es_com.loc[:,'16:15'])
    s_es_1615.index = df_es_com.loc[:,'ts']
    s_btcusd = pd.Series(df_btcusd_com.loc[:,'Adj Close'])
    s_btcusd.index = df_btcusd_com.loc[:,'ts']

    df_matrix = pd.concat([s_btcusd, s_es], axis=1)
    df_matrix.rename(columns={"Adj Close": "btcusd", ES_TIME: "es"}, inplace=True)
    df_matrix_1615 = pd.concat([s_btcusd, s_es_1615], axis=1)
    df_matrix_1615.rename(columns={"Adj Close": "btcusd", "16:15": "es"}, inplace=True)

    # df_ = s_btcusd.to_frame()
    # df_['es'] = s_es
    # df_.rename(columns={"Adj Close": "btcusd"}, inplace=True)

    # a.to_frame().join(b.to_frame())
    #df_es_pctchg = df_es.pct_change()
    #df_btcusd_pctchg = df_btcusd.pct_change()
    #df_matrix_pctchg = df_matrix.pct_change()

    #return df_es, df_es_pctchg, df_btcusd, df_btcusd_pctchg, df_matrix, df_matrix_pctchg
    return df_es, df_btcusd, df_matrix

"""
# ==============================================================================
from quant.stats_crypto import *

df_es, df_btcusd, df_matrix = import_data()

df_es_1615_pctchg = df_es.loc[:,'16:15'].pct_change()
df_btcusd_2359_pctchg = df_btcusd.loc[:,'Adj Close'].pct_change()
df_matrix_pctchg = df_matrix.pct_change()


save_data(df_es, df_btcusd, df_matrix)

# ==============================================================================
"""

if __name__ == '__main__':
    """
    run()

    get_common_dates(df0, df1)

    s = df.loc[:, '23:59']
    print(s)
    """
