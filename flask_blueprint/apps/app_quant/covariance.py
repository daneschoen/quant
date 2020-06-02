import os, sys
import datetime
import pytz, time

import numpy as np
import pandas as pd
#import pandas.io.data
#from pandas.io import data, wb   < 0.17.0

from pandas_datareader import data as pd_webdata
from pandas_datareader import wb as pd_wb
# import pandas_datareader as pdr

import fix_yahoo_finance
fix_yahoo_finance.pdr_override()

# Must be in this order
#import matplotlib as mpl
#mpl.use('Agg')
#import matplotlib.pyplot as plt

##?  from .randomgen_gen import Random_gen

"""
>>> import matplotlib
>>> matplotlib.matplotlib_fname()
# This is the file location in Ubuntu
'/etc/matplotlibrc'

Ubuntu has X11, but the DISPLAY environment variable was not properly set. Try executing the following command and then rerunning your program:

export DISPLAY=localhost:0
"""

# ==============================================================================

WEBDATA_SOURCE = 'yahoo'  # 'google'

FNAME_PREFIX = 'pdweb_'
FNAME_SUFFIX_CSV = '_ohlc.csv'
# nm_json_suffix = '_ohlc.csv'
FNAME_MULTI_ = FNAME_PREFIX + 'multi_'     # _guest.csv'
CORR_ROLLING_ = FNAME_PREFIX + 'corr_rolling_'   # _guest.csv'

username = 'guest'

ABS_DIR = os.path.dirname(os.path.abspath(__file__))
# DIR_DATA = 'data'
# DIR_IMAGES = 'static/images'
DIR_IMAGES = '/static/images/'
DIR_DATA = '/static/data/'

# ------------------------------------------------------------------------------

def fetch_data(instr_lst, bl_save):
    """
    labels = ['a', 'b', 'c', 'd', 'e']
    s = Series([1, 2, 3, 4, 5], index=labels)

    mapping = s.to_dict()
    # {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
    Series(mapping)
    """

    if type(instr_lst) != list:
        instr_lst = [instr_lst]
    instr_lst = [i.upper() for i in instr_lst]

    dt_beg = datetime.datetime(2006,1,1)
    nw = datetime.datetime.now()
    dt_end = nw

    #goog = DataReader("GOOG", "yahoo", datetime(2000,1,1), datetime(2012,1,1))
    #print(goog["Adj Close"])

    df_instr_sym_={}
    for sym in instr_lst:
        """
        df.ix['2010-01-04']
        """
        df_instr_sym_[sym] = pd_webdata.DataReader(sym, WEBDATA_SOURCE, dt_beg, dt_end)['Adj Close']

        if bl_save:
            pathfname = os.path.join(DIR_DATA, FNAME_PREFIX + sym.lower() + FNAME_SUFFIX_CSV)
            df_instr_sym_[sym].to_csv(pathfname)

    return df_instr_sym_


def fetch_data_matrix(instr_lst, bl_save=True):

    sym_lst = [s.upper() for s in instr_lst]

    nw = datetime.datetime.now().date()
    dt_end = nw
    # dt_beg = datetime.datetime(2006,1,1)
    dt_beg = (dt_end - pd.DateOffset(years=10)).date()

    # dtstr_beg = dt_beg.strftime("%Y-%m-%d %H:%M:%S")

    try:
      # df = pd_webdata.DataReader(sym_lst, WEBDATA_SOURCE, dt_beg, dt_end)['Adj Close']
      """
      pnl = pd_webdata.DataReader(sym_lst, 'yahoo', dt_beg, dt_end)
      df = pnl.to_frame().unstack(level=1)
      df.columns = df.columns.swaplevel(0,1)
      """

      """
      Ex w fix_yahoo_finance
      df = pd_webdata.get_data_yahoo('AAPL', start='2017-04-23', end='2017-05-24')
      df = pd_webdata.get_data_yahoo(['AAPL','GOOG'], start='2017-04-23', end='2017-05-24')
      df = pd_webdata.get_data_yahoo('AAPL', dt_beg, dt_end)
      # Note the order of the last 2 data columns are 'Adj Close' and 'Volume' ie. not the previous format. To re-index:
      # cols = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']
      # data.reindex(columns=cols)
      """
      df = pd_webdata.get_data_yahoo(sym_lst, dt_beg, dt_end)['Adj Close']

    except:
      #print("Unexpected error:", sys.exc_info()[0])
      raise

    """
    df.loc['2010-01-04','Open']  ==  df.loc['2010-01-04']['Open']
    df.loc['2010-01-04','Open']['AAPL']  == df.loc['2010-01-04']['Open']['AAPL']
    df.loc['2010-01-04','AAPL']['Open']  == df.loc['2010-01-04']['AAPL']['Open']
    """

    if bl_save:
        # pathfname = os.path.abspath(os.path.join(ABS_DIR, DIR_DATA, fname))
        pathfname = os.path.join(DIR_DATA, FNAME_MULTI_ + username + '.csv')
        df.to_csv(pathfname)

    return df   # Panel df deprecated - use multiindex df.to_frame() or  df.to_xarray()


def moving_avg(df, col_name, per):
    #
    # Moving Average
    #
    prc_col = df[col_name]     # eg 'Adj Close'
    mvgroll = pd.rolling_mean(prc_col, per)

    return mvgroll


def scatter_pair(df_matrix, corr_days):
    rets = df_matrix.pct_change()
    plt.scatter(rets[-100:].AAPL, rets[-100:].AMZN)
    plt.xlabel('Returns AAPL')
    plt.ylabel('Returns AMZN')


# def correlation_pair(instr_lst, days):
def correlation_pair(df_matrix, corr_dys):
    #for sym in instr_lst:
    #    df = pd.read_csv(sym.lower() + FNAME_SUFFIX_CSV, index_col='Date', parse_dates=True)
    #ts = df['Close']

    rets = df_matrix.pct_change()   # 1 - df / df.shift(1)  or  (df-df.shift(1))/df.shift(1)
    corr = rets.corr()
    plt.scatter(rets[-100:].AAPL, rets[-100:].AMZN)
    plt.xlabel('Returns AAPL')
    plt.ylabel('Returns AMZN')

    corr = rets.corr()


def correlation_rolling(df_matrix, corr_dys, bl_mat=False, bl_save=True):
    df_pctchg = df_matrix.pct_change()

    # df_matrix= pd.read_csv('data/pair_cls.csv', index_col='Date', parse_dates=True)
    col_names = list(df_matrix.columns.values)

    # rolling_corr = pd.rolling_corr(df_matrix, window=corr_dys)
    pnl_rollingcorr = pd.rolling_corr(df_pctchg, window=corr_dys)  #, pairwise=True)
    df_rollingcorr = pnl_rollingcorr.ix[:, col_names[0], col_names[1]]
    #covs = rolling_cov(df[['B','C','D']], df[['A','B','C']], 50, pairwise=True)
    #correls = pd.rolling_corr(df_multi, 30)

    if bl_mat:
        plt = df_rollingcorr.plot()
        fig = plt.get_figure()

        # dir_data_filename_png = os.path.abspath(os.path.join(ABS_DIR, DIR_DATA, 'quant_corr_rolling.png'))
        # dir_data_filename_svg = os.path.abspath(os.path.join(ABS_DIR, DIR_DATA, 'quant_corr_rolling.svg'))
        dir_images_fname_png = os.path.abspath(os.path.join(DIR_IMAGES, 'quant_corr_rolling.png'))
        dir_images_fname_svg = os.path.abspath(os.path.join(DIR_IMAGES, 'quant_corr_rolling.svg'))
        #plt.savefig(dir_data_filename_png)
        #plt.savefig(dir_data_filename_svg)
        fig.savefig(dir_images_fname_png)
        fig.savefig(dir_images_fname_svg)

    if bl_save:
        pathfname = os.path.join(DIR_DATA, CORR_ROLLING_ + username + '.csv')
        df_rollingcorr.to_csv(pathfname)

    return df_rollingcorr


def correlation_matrix(df_matrix):

    ret_matrix = df_matrix.pct_change()

    pd.scatter_matrix(ret_matrix, diagonal='kde', figsize=(10, 10))

    #dir_data = os.path.join(ABS_DIR, DIR_DATA, fname)
    #dir_images = os.path.join(ABS_DIR, 'static/images')
    #os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'templates'))

    #plt.savefig(os.path.join(dir_data, 'corr_matrix_scatter.png'))
    #plt.savefig(os.path.abspath(os.path.join(ABS_DIR, DIR_DATA, 'corr_matrix_scatter.png')))
    plt.savefig(os.path.abspath(os.path.join(DIR_IMAGES, 'quant_corr_matrix_scatter.png')))
    plt.close()

    return ret_matrix.corr()


def correlation_matrix_heat(corr_matrix):
    plt.imshow(corr_matrix, cmap='hot', interpolation='none')
    plt.colorbar()
    plt.xticks(range(len(corr_matrix)), corr_matrix.columns)
    plt.yticks(range(len(corr_matrix)), corr_matrix.columns)

    #plt.savefig(os.path.join(DIR_DATA, 'corr_matrix_heat.png'))
    #plt.savefig(os.path.join(DIR_DATA, 'corr_matrix_heat.svg'))
    plt.savefig(os.path.abspath(os.path.join(ABS_DIR, DIR_DATA, 'corr_matrix_heat.png')))
    plt.savefig(os.path.abspath(os.path.join(ABS_DIR, DIR_IMAGES, 'corr_matrix_heat.png')))
    plt.savefig(os.path.abspath(os.path.join(ABS_DIR, DIR_DATA, 'corr_matrix_heat.svg')))
    plt.savefig(os.path.abspath(os.path.join(ABS_DIR, DIR_IMAGES, 'corr_matrix_heat.svg')))

    plt.close()


def quant_distributions(dist, mu, sigma, size):
    # mu, sigma, size = 0, 0.1, 1000
    # mu, sigma, size = 3, 1.0, 1000

    if dist == 'normal':
        # abs(mu - np.mean(s)) < 0.01
        # abs(sigma - np.std(s, ddof=1)) < 0.0
        s = np.random.normal(mu, sigma, size)

    elif dist == 'lognormal':
        s = np.random.lognormal(mu, sigma, size)

    elif dist == 'custom':
        randomgen = Random_gen()
        s = randomgen.get_sample(size)

    """
    ------
    Bucket
    ------
    min(s), max(s)
    -0.31221440921772381, 0.29052879950320193
    s = np.random.normal(3, .5, size)
    min(s), max(s)
    (1.585037466426426, 4.5513383256128579)
    s = np.random.normal(-2, 2, size)
    min(s), max(s)
    (-8.8859611101434428, 4.1076323914819381)

    """
    if dist == 'custom':
        """
        randomgen.probabilities
        [0.01, 0.3, 0.58, 0.1, 0.01]
        randomgen.samplespace_omega
        [-1, 0, 1, 2, 3]
        """
        bin_tot = len(randomgen.samplespace_omega) - 1
        bin_edges = randomgen.samplespace_omega
        freq_bins, bins = np.histogram(s, bins=bin_edges)
        bucket_lst = []
        for bin_edge, freq_bin in zip(bin_edges, freq_bins):
            bucket_lst.append([bin_edge, int(freq_bin)])
    else:
        NORMALIZE_AMT = 1

        bin_tot = 30
        if dist == 'lognormal':
            bin_tot = 100

        bin_edges_tot = bin_tot + 1
        #bin_edges = np.linspace(min(s)-np.finfo(float).eps, max(s)+np.finfo(float).eps, 23)
        bin_edges = np.linspace(np.floor(min(s)), np.ceil(max(s)), bin_edges_tot)
        bin_edges[-1] += 1e-06

        freq_bins, bins = np.histogram(s, bins=bin_edges)

        idxs = np.digitize(s, bin_edges)
        bin_means = [s[idxs == i].mean() for i in range(1, len(bin_edges))]
        #else:
        #    bin_means = hist[1][:-1]

        normalize_ratio = max(freq_bins)/NORMALIZE_AMT
        bucket_lst = []
        for bin_edge, freq_bin in zip(bin_edges, freq_bins):
            #if np.isnan(bin_mean):
            #    bin_mean = 0.0
            bucket_lst.append([bin_edge, freq_bin/normalize_ratio])
        # np.nan_to_num(bucket_lst)
    return bucket_lst


# ==============================================================================

if __name__ == '__main__':

    instr_lst = ['aapl','goog','amzn','msft', 'yhoo']   # csco, orcl

    #fetch_data(instr_lst, save=True)

    df_matrix = fetch_data_matrix(instr_lst, save=True)
    corr_matrix = correlation_matrix(df_matrix)
    correlation_matrix_heat(corr_matrix)


    instr_lst = ['aapl','goog']
    df_matrix = fetch_data_matrix(instr_lst, save=True)
    correlation_rolling(df_matrix, days=30)
