import os
import csv
import argparse

import numpy as np
import pandas as pd

import requests
import quandl

from apps.settings.constants_fin import SP500_LST

# ==============================================================================

LIMIT = 20


pth = os.path.dirname(os.path.abspath(__file__))
PATH_OUT  = os.path.join(pth, '..', '..', '..', 'data_in/equity_future_com/sp500/')


# API_KEY_QUANDL = open('quandlapikey.txt','r').read()
API_KEY_QUANDL = "no72csj_VbQQmt7d_y63"

quandl.ApiConfig.api_key = API_KEY_QUANDL


API_QUANDL = "https://www.quandl.com/api/v3/datasets/"


"""
================================================================================
quandl.ApiConfig.api_version = '2015-04-09'

https://www.quandl.com/api/v3/datasets/EOD/GOOG.csv?api_key=no72csj_VbQQmt7d_y63&start_date=1970-01-01&end_date=2018-07-31&order=asc
https://www.quandl.com/api/v3/datasets/EOD/GOOG.csv?api_key=no72csj_VbQQmt7d_y63&start_date=1970-01-01&end_date=1970-01-01
quandl.get("EOD/AAPL", authtoken="no72csj_VbQQmt7d_y63", start_date="1970-01-01", end_date="1970-01-01")

------
rest :
------
?api_key=tEsTkEy123456789   ?api_key=no72csj_VbQQmt7d_y63
https://www.quandl.com/api/v3/datasets/WIKI/AAPL.csv
https://www.quandl.com/api/v3/datasets/WIKI/AAPL.csv?order=asc
https://www.quandl.com/api/v3/datasets/OPEC/ORB.csv
https://www.quandl.com/api/v3/datasets/OPEC/ORB.json
https://www.quandl.com/api/v3/datasets/OPEC/ORB.csv?start_date=2003-01-01&end_date=2019-03-06
?collapse=monthly
https://www.quandl.com/api/v3/datasets/OPEC/ORB.csv?rows=1  ?column=1  ?order=asc

quarterly pct change in AAPL stock between 1985 and 1997, closing prices only, in JSON format:
https://www.quandl.com/api/v3/datasets/WIKI/AAPL.json?start_date=1985-05-01&end_date=1997-07-01&order=asc&column_index=4&collapse=quarterly&transformation=rdiff
?transformation=normalize


----
py :
----
data = quandl.get("EIA/PET_RWTC_D", returns="numpy")
data = quandl.get("FRED/GDP", start_date="2001-12-31", end_date="2005-12-31")

data = quandl.get(["NSE/OIL.1", "WIKI/AAPL.4"])   # To request specific columns

data = quandl.get("WIKI/AAPL", rows=5)   # To request the last 5 rows

data = quandl.get("EIA/PET_RWTC_D", collapse="monthly")

data = quandl.get("FRED/GDP", transformation="rdiff")  # To perform elementary calculations on the data

quandl.bulkdownload("ZEA")

quandl.get_table('ZACKS/FC', ticker='AAPL')   # retrieves all rows for ZACKS/FC where ticker='AAPL'
quandl.get_table('ZACKS/FC', paginate=True)
quandl.get_table('ZACKS/FC', paginate=True, ticker='AAPL', qopts={'columns': ['ticker', 'per_end_date']})
quandl.get_table('ZACKS/FC', paginate=True, ticker=['AAPL', 'MSFT'], per_end_date={'gte': '2015-01-01'}, qopts={'columns':['ticker', 'per_end_date']})


================================================================================
"""


# 'BF.B','BRK.B' ==>

"""
['dataset'].keys():
dict_keys(['description', 'collapse', 'frequency', 'newest_available_date', 'database_code', 'database_id', 'name', 'transform', 'type', 'start_date', 'end_date', 'dataset_code', 'refreshed_at', 'limit', 'premium', 'column_names', 'data', 'oldest_available_date', 'order', 'id', 'column_index'])

res['dataset']['column_names']: ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Ex-Dividend', 'Split Ratio', 'Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Close', 'Adj. Volume']
res['dataset'][''data']
"""

# ------------------------------------------------------------------------------
# Get Meta-Data
# ------------------------------------------------------------------------------
def get_sp500_lst():
    res_lst = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    df_sp500_all = res_lst[0]
    se_sp500_sym = df_sp500_all[0][1:]
    # return list(se_sp500_sym)
    return [x.replace('.','_') for x in se_sp500_sym]

def get_sp500_pd():
    res_lst = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    df_sp500_all = res_lst[0]

    heading = df_sp500_all.iloc[0][:5]
    #heading.append('sym')
    df_sp500 = df_sp500_all.iloc[1:,:5]
    df_sp500.columns = heading

    # df_sp500['Ticker symbol'] == df_sp500.loc[:,'Ticker symbol'] ==
    # df_sp500_all.iloc[1:,0] == df_sp500_all[0][1:]
    se_sp500_sym = df_sp500_all[0][1:]

    df_sp500['sym'] = [x.replace('.','_') for x in se_sp500_sym]

    return df_sp500

def process_sp500_file():
    sp500_lst=[]
    with open("sp500_list.txt") as f:
      for row in csv.reader(f, delimiter='\t'):
            sp500_lst.append(row[0])
    return sp500_lst


# ------------------------------------------------------------------------------
# Get quandl fundamental
# ------------------------------------------------------------------------------
def get_fundamental():
    fundamentalData = quandl.get_table('ZACKS/FC', ticker='AAPL')
    #fundamentalData[0:5]

# ------------------------------------------------------------------------------
# Get quandl data
# ------------------------------------------------------------------------------
def get_quandl_sp500_rest(sym_lst=SP500_LST, limit=LIMIT):
    n=0
    for sym in sym_lst:
        try:
          print("Get: " + sym)
          # res = requests.get("https://www.quandl.com/api/v3/datasets/WIKI/" + "ADBE" + "?order=asc")

          if "/" in sym:
              sym_csv = sym.split("/")[1] + ".csv"
              exch_sym = sym + ".json"
          else:
              sym_csv = sym + ".csv"
              exch_sym = "EOD/"+sym + ".json"

          res = requests.get(API_QUANDL + exch_sym + "&order=asc")
          if res.status_code != 200:
              print("ERROR - STATUS: " + str(res.status_code) + " : " + exch_sym)
              continue

          l_data = res.json()['dataset']['data']
          l_heading = res.json()['dataset']['column_names']
          print("Write: " + sym_csv)
          PATH_FILE_OUT  = os.path.join(PATH_OUT, sym_csv)
          with open(PATH_FILE_OUT, "w") as f:
            # writer = csv.writer(outcsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
            writer = csv.writer(f)

            writer.writerow(l_heading)
            writer.writerows(l_data)

          n+=1
          if n >= limit:
              break

        except Exception as e:
            print("ERROR - EXCEPT: " + str(e) + " : " + exch_sym)
            # break out since prob rest will fail
            break


def get_quandl_sp500_py(sym_lst=SP500_LST):
    n=0
    for sym in sym_lst:
        try:
          print(str(n) + ") Get: " + sym)
          if "/" in sym:
              sym_name = sym.split("/")[1]
              exch_sym = sym
          else:
              sym_name = sym
              exch_sym = "EOD/"+sym    # "WIKI/"+sym

          df_data = quandl.get(exch_sym)

          # df_data.sort_values(by='Split', ascending = 0)
          # df_data.sort_values(by='Split', ascending = 0)['Split'].head()
          # df_split = calculate_adjusted_prices(df_data, 'Close'):

          print("Write: " + sym_name + '.csv')
          file_path_out  = os.path.join(PATH_OUT, sym_name + '.csv')
          df_data.to_csv(file_path_out)

          n+=1
          if n >= LIMIT:
              break

        except Exception as e:
            print("ERROR - EXCEPT: " + str(e) + " : " + exch_sym)
            # break out since prob rest will fail
            break



# https://joshschertz.com/2016/08/27/Vectorizing-Adjusted-Close-with-Python/
def calculate_adjusted_prices(df, column):
    """ Vectorized approach for calculating the adjusted prices for the
    specified column in the provided DataFrame. This creates a new column
    called 'adj_<column name>' with the adjusted prices. This function requires
    that the DataFrame have columns with dividend and split_ratio values.

    :param df: DataFrame with raw prices along with dividend and split_ratio
        values
    :param column: String of which price column should have adjusted prices
        created for it
    :return: DataFrame with the addition of the adjusted price column
    """
    adj_column = 'Adj_' + column + '_Check'

    # Reverse the DataFrame order, sorting by date in descending order
    df.sort_index(ascending=False, inplace=True)

    price_col = df[column].values
    split_col = df['Split'].values
    dividend_col = df['Dividend'].values
    adj_price_col = np.zeros(len(df.index))
    adj_price_col[0] = price_col[0]

    for i in range(1, len(price_col)):
        adj_price_col[i] = round((adj_price_col[i - 1] + adj_price_col[i - 1] *
                   (((price_col[i] * split_col[i - 1]) -
                     price_col[i - 1] -
                     dividend_col[i - 1]) / price_col[i - 1])), 4)

    df[adj_column] = adj_price_col

    # Change the DataFrame order back to dates ascending
    df.sort_index(ascending=True, inplace=True)

    return df
"""
adjCloseCheck = calculate_adjusted_prices(priceData, "Close")
adjCloseCheck.loc["2015-01-23":"2015-02-06"]

ratioPlot = adjCloseCheck["Close"]/adjCloseCheck["adj_Close_Check"]
plt.figure(); ratioPlot.plot(); plt.legend(loc='best')
"""
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

$ cd ~/Agape/development/projects/fintech/flask_blueprint
  cd ~/projects/fintech/flask_blueprint

from apps.app_util.data_quandl import *
# import apps.app_util.data_quandl as q

get_quandl_sp500(SP500_LST[0:20])
get_quandl_sp500()

SP500_LST = ['A', 'AAL', 'AAP', 'AAPL', 'ABBV', 'ABC', 'ABMD', 'ABT', 'ACN', 'ADBE', 'ADI', 'ADM', 'ADP', 'ADS', 'ADSK', 'AEE', 'AEP', 'AES', 'AET', 'AFL', 'AGN', 'AIG', 'AIV', 'AIZ', 'AJG', 'AKAM', 'ALB', 'ALGN', 'ALK', 'ALL', 'ALLE', 'ALXN', 'AMAT', 'AMD', 'AME', 'AMG', 'AMGN', 'AMP', 'AMT', 'AMZN', 'ANDV', 'ANSS', 'ANTM', 'AON', 'AOS', 'APA', 'APC', 'APD', 'APH', 'APTV', 'ARE', 'ARNC', 'ATVI', 'AVB', 'AVGO', 'AVY', 'AWK', 'AXP', 'AZO', 'BA', 'BAC', 'BAX', 'BBT', 'BBY', 'BDX', 'BEN', 'BF_B', 'BHF', 'BHGE', 'BIIB', 'BK', 'BKNG', 'BLK', 'BLL', 'BMY', 'BR', 'BRK_B', 'BSX', 'BWA', 'BXP', 'C', 'CA', 'CAG', 'CAH', 'CAT', 'CB', 'CBOE', 'CBRE', 'CBS', 'CCI', 'CCL', 'CDNS', 'CELG', 'CERN', 'CF', 'CFG', 'CHD', 'CHRW', 'CHTR', 'CI', 'CINF', 'CL', 'CLX', 'CMA', 'CMCSA', 'CME', 'CMG', 'CMI', 'CMS', 'CNC', 'CNP', 'COF', 'COG', 'COL', 'COO', 'COP', 'COST', 'COTY', 'CPB', 'CPRT', 'CRM', 'CSCO', 'CSX', 'CTAS', 'CTL', 'CTSH', 'CTXS', 'CVS', 'CVX', 'CXO', 'D', 'DAL', 'DE', 'DFS', 'DG', 'DGX', 'DHI', 'DHR', 'DIS', 'DISCA', 'DISCK', 'DISH', 'DLR', 'DLTR', 'DOV', 'DRE', 'DRI', 'DTE', 'DUK', 'DVA', 'DVN', 'DWDP', 'DXC', 'EA', 'EBAY', 'ECL', 'ED', 'EFX', 'EIX', 'EL', 'EMN', 'EMR', 'EOG', 'EQIX', 'EQR', 'EQT', 'ES', 'ESRX', 'ESS', 'ETFC', 'ETN', 'ETR', 'EVHC', 'EVRG', 'EW', 'EXC', 'EXPD', 'EXPE', 'EXR', 'F', 'FAST', 'FB', 'FBHS', 'FCX', 'FDX', 'FE', 'FFIV', 'FIS', 'FISV', 'FITB', 'FL', 'FLIR', 'FLR', 'FLS', 'FLT', 'FMC', 'FOX', 'FOXA', 'FRT', 'FTI', 'FTV', 'GD', 'GE', 'GGP', 'GILD', 'GIS', 'GLW', 'GM', 'GOOG', 'GOOGL', 'GPC', 'GPN', 'GPS', 'GRMN', 'GS', 'GT', 'GWW', 'HAL', 'HAS', 'HBAN', 'HBI', 'HCA', 'HCP', 'HD', 'HES', 'HFC', 'HIG', 'HII', 'HLT', 'HOG', 'HOLX', 'HON', 'HP', 'HPE', 'HPQ', 'HRB', 'HRL', 'HRS', 'HSIC', 'HST', 'HSY', 'HUM', 'IBM', 'ICE', 'IDXX', 'IFF', 'ILMN', 'INCY', 'INFO', 'INTC', 'INTU', 'IP', 'IPG', 'IPGP', 'IQV', 'IR', 'IRM', 'ISRG', 'IT', 'ITW', 'IVZ', 'JBHT', 'JCI', 'JEC', 'JEF', 'JNJ', 'JNPR', 'JPM', 'JWN', 'K', 'KEY', 'KHC', 'KIM', 'KLAC', 'KMB', 'KMI', 'KMX', 'KO', 'KORS', 'KR', 'KSS', 'KSU', 'L', 'LB', 'LEG', 'LEN', 'LH', 'LKQ', 'LLL', 'LLY', 'LMT', 'LNC', 'LNT', 'LOW', 'LRCX', 'LUV', 'LYB', 'M', 'MA', 'MAA', 'MAC', 'MAR', 'MAS', 'MAT', 'MCD', 'MCHP', 'MCK', 'MCO', 'MDLZ', 'MDT', 'MET', 'MGM', 'MHK', 'MKC', 'MLM', 'MMC', 'MMM', 'MNST', 'MO', 'MOS', 'MPC', 'MRK', 'MRO', 'MS', 'MSCI', 'MSFT', 'MSI', 'MTB', 'MTD', 'MU', 'MYL', 'NBL', 'NCLH', 'NDAQ', 'NEE', 'NEM', 'NFLX', 'NFX', 'NI', 'NKE', 'NKTR', 'NLSN', 'NOC', 'NOV', 'NRG', 'NSC', 'NTAP', 'NTRS', 'NUE', 'NVDA', 'NWL', 'NWS', 'NWSA', 'O', 'OKE', 'OMC', 'ORCL', 'ORLY', 'OXY', 'PAYX', 'PBCT', 'PCAR', 'PCG', 'PEG', 'PEP', 'PFE', 'PFG', 'PG', 'PGR', 'PH', 'PHM', 'PKG', 'PKI', 'PLD', 'PM', 'PNC', 'PNR', 'PNW', 'PPG', 'PPL', 'PRGO', 'PRU', 'PSA', 'PSX', 'PVH', 'PWR', 'PX', 'PXD', 'PYPL', 'QCOM', 'QRVO', 'RCL', 'RE', 'REG', 'REGN', 'RF', 'RHI', 'RHT', 'RJF', 'RL', 'RMD', 'ROK', 'ROP', 'ROST', 'RSG', 'RTN', 'SBAC', 'SBUX', 'SCG', 'SCHW', 'SEE', 'SHW', 'SIVB', 'SJM', 'SLB', 'SLG', 'SNA', 'SNPS', 'SO', 'SPG', 'SPGI', 'SRCL', 'SRE', 'STI', 'STT', 'STX', 'STZ', 'SWK', 'SWKS', 'SYF', 'SYK', 'SYMC', 'SYY', 'T', 'TAP', 'TDG', 'TEL', 'TGT', 'TIF', 'TJX', 'TMK', 'TMO', 'TPR', 'TRIP', 'TROW', 'TRV', 'TSCO', 'TSN', 'TSS', 'TTWO', 'TWTR', 'TXN', 'TXT', 'UA', 'UAA', 'UAL', 'UDR', 'UHS', 'ULTA', 'UNH', 'UNM', 'UNP', 'UPS', 'URI', 'USB', 'UTX', 'V', 'VAR', 'VFC', 'VIAB', 'VLO', 'VMC', 'VNO', 'VRSK', 'VRSN', 'VRTX', 'VTR', 'VZ', 'WAT', 'WBA', 'WDC', 'WEC', 'WELL', 'WFC', 'WHR', 'WLTW', 'WM', 'WMB', 'WMT', 'WRK', 'WU', 'WY', 'WYNN', 'XEC', 'XEL', 'XL', 'XLNX', 'XOM', 'XRAY', 'XRX', 'XYL', 'YUM', 'ZBH', 'ZION', 'ZTS']
"""
