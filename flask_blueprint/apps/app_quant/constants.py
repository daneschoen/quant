import os

PATH_PROJ_ROOT = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))

PATH_DATA_IN = os.path.join(PATH_PROJ_ROOT, 'data_in')

FILE_ES = 'esdata1col.csv'
PATH_FILE_ES = os.path.join(PATH_DATA_IN, FILE_ES)

FILE_BTC_USD = 'BTC-USD_yahoo.csv'
PATH_FILE_BTC_USD = os.path.join(PATH_DATA_IN, FILE_BTC_USD)

PATH_OUT_CHART = os.path.join(PATH_PROJ_ROOT, 'data_out_charts')
PATH_FILE_OUT_CHART_ROLLING_MEAN = os.path.join(PATH_PROJ_ROOT,
                                   'data_out_charts', 'rolling_mean.png')


# ==============================================================================
