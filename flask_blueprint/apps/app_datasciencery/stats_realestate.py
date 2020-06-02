import os
import csv
import argparse

import pandas as pd

import requests
import quandl

import pickle
import matplotlib.pyplot as plt
# matplotlib.style.use('ggplot')
from matplotlib import style
style.use('fivethirtyeight')

# ==============================================================================

LIMIT = 20


pth = os.path.dirname(os.path.abspath(__file__))
PATH_OUT  = os.path.join(pth, '..', '..', '..', 'data_in/equity_future_com/sp500/')


# API_KEY_QUANDL = open('quandlapikey.txt','r').read()
API_KEY_QUANDL = "no72csj_VbQQmt7d_y63"
quandl.ApiConfig.api_key = API_KEY_QUANDL


API_QUANTL = "https://www.quandl.com/api/v3/datasets/"


"""
================================================================================


================================================================================
"""


def pd_read_html_ex():

    import matplotlib
    matplotlib.style.use('ggplot')

    url = 'https://myurl'

    df_table = pd.read_html(url, thousands=' ', header=0, index_col=0)[0]
    df_table["Folkmängd"].plot(color='k')
    plt.show()


def get_state_se():
    us_states = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states')
    return us_states[0][2][1:]


def get_hpi_benchmark():
    df = quandl.get("FMAC/HPI_USA")
    df["US"] = (df["Value"]-df["Value"][0]) / df["Value"][0] * 100.0
    return df


def initial_state_data():
    us_states = get_state_se()

    main_df = pd.DataFrame()

    for state in us_states:
        query = "FMAC/HPI_"+str(state)
        #df = quandl.get(query, authtoken=api_key)
        df = quandl.get(query)
        print(query)
        df[state] = (df[state]-df[state][0]) / df[state][0] * 100.0
        print(df.head())
        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df)

    pickle_out = open('us_states.pickle','wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()


def plot():
    fig = plt.figure()
    ax1 = plt.subplot2grid((1,1), (0,0))
    HPI_data = pd.read_pickle('us_states.pickle')
    plt.show()



# ==============================================================================


if __name__ == "__main__":
    plot()


"""
Usage:

p3 apps/app_util/data_quandl.py
p3 apps/app_util/data_quandl.py -m py
p3 apps/app_util/data_quandl.py -s AAPL GOOG
p3 apps/app_util/data_quandl.py -m py -s BCIW/_INX

OR

import apps.app_util.data_quandl as q
q.get_quandl_sp500()

"""
