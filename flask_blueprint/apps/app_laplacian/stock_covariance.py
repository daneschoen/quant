
import os
import datetime

import pandas as pd
#import pandas.io.data
#from pandas.io import data, wb
#from pandas_datareader import data as pd_datareader
#from pandas_datareader import wb as pd_wb

from pandas import Series, DataFrame

# Must be in this order
#import matplotlib as mpl
#mpl.use('Agg')
#import matplotlib.pyplot as plt

"""
>>> import matplotlib
>>> matplotlib.matplotlib_fname()
# This is the file location in Ubuntu
'/etc/matplotlibrc'

Ubuntu has X11, but the DISPLAY environment variable was not properly set. Try executing the following command and then rerunning your program:

export DISPLAY=localhost:0
"""


nm_csv_suffix = '_ohlc.csv'
nm_json_suffix = '_ohlc.csv'

ABS_DIR = os.path.dirname(os.path.abspath(__file__))
DIR_DATA = 'data'
DIR_IMAGES = 'static/images'



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

    df_instr={}
    for sym in instr_lst:
        df_instr[sym] = pd.io.data.get_data_yahoo(sym,
                            start=dt_beg,
                            end=dt_end )
        if bl_save:
            dir_filename = os.path.join(DIR_DATA, sym.lower() + nm_csv_suffix)
            df_instr[sym].to_csv(dir_filename)

    #aapl.head()
    #aapl.to_csv('aapl_ohlc.csv')
    # !head data/aapl_ohlc.csv
    return df_instr


def fetch_data_matrix(instr_lst, bl_save):

    instr_lst = [i.upper() for i in instr_lst]

    dt_beg = datetime.datetime(2006,1,1)
    nw = datetime.datetime.now()
    dt_end = nw

    df_matrix = pd.io.data.get_data_yahoo(instr_lst,
                   start=dt_beg,
                   end=dt_end )['Adj Close']

    if bl_save:
        fname = 'multi_cls.csv'
        dir_filename = os.path.abspath(os.path.join(ABS_DIR, DIR_DATA, fname))
        df_matrix.to_csv(dir_filename)

    return df_matrix


def moving_avg(df):
    #
    # Moving Average
    #
    close_px = df['Adj Close']
    mavg = pd.rolling_mean(close_px, 40)

    #
    # Returns


def scatter_pair(df_matrix, corr_days):
    rets = df_matrix.pct_change()
    plt.scatter(rets[-100:].AAPL, rets[-100:].AMZN)
    plt.xlabel('Returns AAPL')
    plt.ylabel('Returns AMZN')


#def correlation_pair(instr_lst, days):
def correlation_pair(df_matrix, corr_days):
    #for sym in instr_lst:
    #    df = pd.read_csv(sym.lower() + nm_csv_suffix, index_col='Date', parse_dates=True)
    #ts = df['Close']

    rets = df_matrix.pct_change()
    corr = rets.corr()
    plt.scatter(rets[-100:].AAPL, rets[-100:].AMZN)
    plt.xlabel('Returns AAPL')
    plt.ylabel('Returns AMZN')

    corr = rets.corr()


def correlation_rolling(df_matrix, corr_days):

    #df_matrix= pd.read_csv('data/pair_cls.csv', index_col='Date', parse_dates=True)
    column_names = list(df_matrix.columns.values)

    # deprecated:
    correls = pd.rolling_corr_pairwise(df_matrix, corr_days)

    #covs = rolling_cov(df[['B','C','D']], df[['A','B','C']], 50, pairwise=True)
    #correls = pd.rolling_corr(df_multi, 30)

    correls.ix[:, column_names[0], column_names[1]].plot()
    dir_data_filename_png = os.path.abspath(os.path.join(ABS_DIR, DIR_DATA, 'corr_rolling.png'))
    dir_data_filename_svg = os.path.abspath(os.path.join(ABS_DIR, DIR_DATA, 'corr_rolling.svg'))
    dir_images_filename_png = os.path.abspath(os.path.join(ABS_DIR, DIR_IMAGES, 'corr_rolling.png'))
    dir_images_filename_svg = os.path.abspath(os.path.join(ABS_DIR, DIR_IMAGES, 'corr_rolling.svg'))
    plt.savefig(dir_data_filename_png)
    plt.savefig(dir_data_filename_svg)
    plt.savefig(dir_images_filename_png)
    plt.savefig(dir_images_filename_svg)


def correlation_matrix(df_matrix):

    ret_matrix = df_matrix.pct_change()

    pd.scatter_matrix(ret_matrix, diagonal='kde', figsize=(10, 10))

    #dir_data = os.path.join(ABS_DIR, DIR_DATA, fname)
    #dir_images = os.path.join(ABS_DIR, 'static/images')
    #os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'templates'))

    #plt.savefig(os.path.join(dir_data, 'corr_matrix_scatter.png'))
    plt.savefig(os.path.abspath(os.path.join(ABS_DIR, DIR_DATA, 'corr_matrix_scatter.png')))
    plt.savefig(os.path.abspath(os.path.join(ABS_DIR, DIR_IMAGES, 'corr_matrix_scatter.png')))
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



if __name__ == '__main__':

    instr_lst = ['aapl','goog','amzn','msft', 'yhoo']   # csco, orcl

    #fetch_data(instr_lst, save=True)

    df_matrix = fetch_data_matrix(instr_lst, save=True)
    corr_matrix = correlation_matrix(df_matrix)
    correlation_matrix_heat(corr_matrix)


    instr_lst = ['aapl','goog']
    df_matrix = fetch_data_matrix(instr_lst, save=True)
    correlation_rolling(df_matrix, days=30)
