import os
import csv
import argparse

import pandas as pd

import requests


# ==============================================================================



# ==============================================================================


def get_wiki(url):
    res_lst = pd.read_html(url)

    df_data_all = res_lst[0]

    heading = df_sp500_all.iloc[0][:5]
    #heading.append('sym')
    df_sp500 = df_sp500_all.iloc[1:,:5]
    df_sp500.columns = heading

    # df_sp500['Ticker symbol'] == df_sp500.loc[:,'Ticker symbol'] ==
    # df_sp500_all.iloc[1:,0] == df_sp500_all[0][1:]
    se_sp500_sym = df_sp500_all[0][1:]

    df_sp500['sym'] = [x.replace('.','_') for x in se_sp500_sym]

    return df_sp500


def get_wiki_schizophrenia():
    url = "https://en.wikipedia.org/wiki/Epidemiology_of_schizophrenia"
    res_lst = pd.read_html(url)
    df_data = pd.concat([ res_lst[1].iloc[1:], res_lst[2].iloc[1:], res_lst[3].iloc[1:] ], axis=0)

    heading = res_lst[1].iloc[0,:]
    df_data.columns = heading.str.lower().str.replace(' ', '_')   # ['Rank', 'Country', 'DALY rate']

    # pd.to_numeric(df_data, errors='ignore')
    # df_data[['Rank', 'DALY rate']] = df_data[['Rank', 'DALY rate']].astype(float)
    df_data['rank'] = df_data['rank'].astype(int)
    df_data['daly_rate'] = df_data['daly_rate'].astype(float)

    return df_data


# ==============================================================================


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    #parser.add_argument('css', nargs='*')
    parser.add_argument('-m', action="store", dest="m", nargs='*', default=['rest'])
    parser.add_argument('-s', action="store", dest="s", nargs='*')

    args = parser.parse_args()

    if args.m[0] == "py":
        if args.s is None:
            print("PY: SP500_LST\n")
            get_quandl_sp500_py()
        else:
            print("PY: " + str(args.s) + "\n")
            get_quandl_sp500_py(args.s)
    else:   # elif args.m[0] == "rest":
        if args.s is None:
            print("REST: SP500_LST\n")
            get_quandl_sp500_rest()
        else:
            print("REST: " + str(args.s) + "\n")
            get_quandl_sp500_rest(args.s)


"""
Usage:

p3 ../app_util/data_quandl.py
p3 apps/app_util/data_quandl.py
p3 apps/app_util/data_quandl.py -m py
p3 apps/app_util/data_quandl.py -s AAPL GOOG
p3 apps/app_util/data_quandl.py -m py -s BCIW/_INX

OR

import apps.app_util.data_quandl as q
q.get_quandl_sp500()

"""
