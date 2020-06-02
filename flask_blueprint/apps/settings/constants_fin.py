"""
# ------------------------------------------------------------------------------
# EQUITIES - SP
# https://en.wikipedia.org/wiki/List_of_S%26P_500_companies
# ------------------------------------------------------------------------------
"""
# 'AEP', 'AES', 'AET'
STK_SP500_LST = ['A', 'AAL', 'AAP', 'AAPL', 'ABBV', 'ABC', 'ABMD', 'ABT', 'ACN', 'ADBE', 'ADI', 'ADM', 'ADP', 'ADS', 'ADSK', 'AEE', 'AEP', 'AES', 'AET', 'AFL', 'AGN', 'AIG', 'AIV', 'AIZ', 'AJG', 'AKAM', 'ALB', 'ALGN', 'ALK', 'ALL', 'ALLE', 'ALXN', 'AMAT', 'AMD', 'AME', 'AMG', 'AMGN', 'AMP', 'AMT', 'AMZN', 'ANDV', 'ANSS', 'ANTM', 'AON', 'AOS', 'APA', 'APC', 'APD', 'APH', 'APTV', 'ARE', 'ARNC', 'ATVI', 'AVB', 'AVGO', 'AVY', 'AWK', 'AXP', 'AZO', 'BA', 'BAC', 'BAX', 'BBT', 'BBY', 'BDX', 'BEN', 'BF_B', 'BHF', 'BHGE', 'BIIB', 'BK', 'BKNG', 'BLK', 'BLL', 'BMY', 'BR', 'BRK_B', 'BSX', 'BWA', 'BXP', 'C', 'CA', 'CAG', 'CAH', 'CAT', 'CB', 'CBOE', 'CBRE', 'CBS', 'CCI', 'CCL', 'CDNS', 'CELG', 'CERN', 'CF', 'CFG', 'CHD', 'CHRW', 'CHTR', 'CI', 'CINF', 'CL', 'CLX', 'CMA', 'CMCSA', 'CME', 'CMG', 'CMI', 'CMS', 'CNC', 'CNP', 'COF', 'COG', 'COL', 'COO', 'COP', 'COST', 'COTY', 'CPB', 'CPRT', 'CRM', 'CSCO', 'CSX', 'CTAS', 'CTL', 'CTSH', 'CTXS', 'CVS', 'CVX', 'CXO', 'D', 'DAL', 'DE', 'DFS', 'DG', 'DGX', 'DHI', 'DHR', 'DIS', 'DISCA', 'DISCK', 'DISH', 'DLR', 'DLTR', 'DOV', 'DRE', 'DRI', 'DTE', 'DUK', 'DVA', 'DVN', 'DWDP', 'DXC', 'EA', 'EBAY', 'ECL', 'ED', 'EFX', 'EIX', 'EL', 'EMN', 'EMR', 'EOG', 'EQIX', 'EQR', 'EQT', 'ES', 'ESRX', 'ESS', 'ETFC', 'ETN', 'ETR', 'EVHC', 'EVRG', 'EW', 'EXC', 'EXPD', 'EXPE', 'EXR', 'F', 'FAST', 'FB', 'FBHS', 'FCX', 'FDX', 'FE', 'FFIV', 'FIS', 'FISV', 'FITB', 'FL', 'FLIR', 'FLR', 'FLS', 'FLT', 'FMC', 'FOX', 'FOXA', 'FRT', 'FTI', 'FTV', 'GD', 'GE', 'GGP', 'GILD', 'GIS', 'GLW', 'GM', 'GOOG', 'GOOGL', 'GPC', 'GPN', 'GPS', 'GRMN', 'GS', 'GT', 'GWW', 'HAL', 'HAS', 'HBAN', 'HBI', 'HCA', 'HCP', 'HD', 'HES', 'HFC', 'HIG', 'HII', 'HLT', 'HOG', 'HOLX', 'HON', 'HP', 'HPE', 'HPQ', 'HRB', 'HRL', 'HRS', 'HSIC', 'HST', 'HSY', 'HUM', 'IBM', 'ICE', 'IDXX', 'IFF', 'ILMN', 'INCY', 'INFO', 'INTC', 'INTU', 'IP', 'IPG', 'IPGP', 'IQV', 'IR', 'IRM', 'ISRG', 'IT', 'ITW', 'IVZ', 'JBHT', 'JCI', 'JEC', 'JEF', 'JNJ', 'JNPR', 'JPM', 'JWN', 'K', 'KEY', 'KHC', 'KIM', 'KLAC', 'KMB', 'KMI', 'KMX', 'KO', 'KORS', 'KR', 'KSS', 'KSU', 'L', 'LB', 'LEG', 'LEN', 'LH', 'LKQ', 'LLL', 'LLY', 'LMT', 'LNC', 'LNT', 'LOW', 'LRCX', 'LUV', 'LYB', 'M', 'MA', 'MAA', 'MAC', 'MAR', 'MAS', 'MAT', 'MCD', 'MCHP', 'MCK', 'MCO', 'MDLZ', 'MDT', 'MET', 'MGM', 'MHK', 'MKC', 'MLM', 'MMC', 'MMM', 'MNST', 'MO', 'MOS', 'MPC', 'MRK', 'MRO', 'MS', 'MSCI', 'MSFT', 'MSI', 'MTB', 'MTD', 'MU', 'MYL', 'NBL', 'NCLH', 'NDAQ', 'NEE', 'NEM', 'NFLX', 'NFX', 'NI', 'NKE', 'NKTR', 'NLSN', 'NOC', 'NOV', 'NRG', 'NSC', 'NTAP', 'NTRS', 'NUE', 'NVDA', 'NWL', 'NWS', 'NWSA', 'O', 'OKE', 'OMC', 'ORCL', 'ORLY', 'OXY', 'PAYX', 'PBCT', 'PCAR', 'PCG', 'PEG', 'PEP', 'PFE', 'PFG', 'PG', 'PGR', 'PH', 'PHM', 'PKG', 'PKI', 'PLD', 'PM', 'PNC', 'PNR', 'PNW', 'PPG', 'PPL', 'PRGO', 'PRU', 'PSA', 'PSX', 'PVH', 'PWR', 'PX', 'PXD', 'PYPL', 'QCOM', 'QRVO', 'RCL', 'RE', 'REG', 'REGN', 'RF', 'RHI', 'RHT', 'RJF', 'RL', 'RMD', 'ROK', 'ROP', 'ROST', 'RSG', 'RTN', 'SBAC', 'SBUX', 'SCG', 'SCHW', 'SEE', 'SHW', 'SIVB', 'SJM', 'SLB', 'SLG', 'SNA', 'SNPS', 'SO', 'SPG', 'SPGI', 'SRCL', 'SRE', 'STI', 'STT', 'STX', 'STZ', 'SWK', 'SWKS', 'SYF', 'SYK', 'SYMC', 'SYY', 'T', 'TAP', 'TDG', 'TEL', 'TGT', 'TIF', 'TJX', 'TMK', 'TMO', 'TPR', 'TRIP', 'TROW', 'TRV', 'TSCO', 'TSN', 'TSS', 'TTWO', 'TWTR', 'TXN', 'TXT', 'UA', 'UAA', 'UAL', 'UDR', 'UHS', 'ULTA', 'UNH', 'UNM', 'UNP', 'UPS', 'URI', 'USB', 'UTX', 'V', 'VAR', 'VFC', 'VIAB', 'VLO', 'VMC', 'VNO', 'VRSK', 'VRSN', 'VRTX', 'VTR', 'VZ', 'WAT', 'WBA', 'WDC', 'WEC', 'WELL', 'WFC', 'WHR', 'WLTW', 'WM', 'WMB', 'WMT', 'WRK', 'WU', 'WY', 'WYNN', 'XEC', 'XEL', 'XL', 'XLNX', 'XOM', 'XRAY', 'XRX', 'XYL', 'YUM', 'ZBH', 'ZION', 'ZTS']

STK_SP500_DRUG_LST  = ['ABBV','AMGN','GILD','PFE','LLY','AGN']
STK_SP500_DRUG_LST2 = ['ABBV','AMGN','GILD', 'GSK', 'PFE', 'NVS', 'SNY', 'LLY', 'AGN','RLMD', 'TAK']

"""
# ------------------------------------------------------------------------------
# FX
# ------------------------------------------------------------------------------
"""
FX_PAIR_TOP = \
['EUR/USD',
'GBP/USD',
'USD/CAD',
'USD/CHF',
'USD/JPY',
'EUR/GBP',
'AUD/USD',
'EUR/AUD',
'EUR/CHF',
'EUR/JPY',
'GBP/CHF',
'GBP/JPY',
'AUD/JPY',
'NZD/USD'
]

FX_PAIR = \
['AUD/CAD',
'AUD/CHF',
'AUD/HKD',
'AUD/NZD',
'AUD/SGD',
'CAD/CHF',
'CAD/HKD',
'CAD/JPY',
'CAD/SGD',
'CHF/HKD',
'CHF/JPY',
'CHF/ZAR',
'EUR/CAD',
'EUR/CZK',
'EUR/DKK',
'EUR/HKD',
'EUR/HUF',
'EUR/NOK',
'EUR/NZD',
'EUR/PLN',
'EUR/SEK',
'EUR/SGD',
'EUR/TRY',
'EUR/ZAR',
'GBP/AUD',
'GBP/CAD',
'GBP/HKD',
'GBP/NZD',
'GBP/PLN'
]


'''
London Stock Exchange opens at 8 a.m. and closes at 4:30 p.m. local time with no lunch period.
Euronext Paris opens at 9 a.m. and closes at 5:30 p.m. local time with no lunch period.
Swiss Exchange opens at 9:00 a.m., closes at 5:30 p.m. local time and has no lunch period.

Shanghai Stock Exchange opens at 9:30 a.m. and closes at 3 p.m. local time, and it has a lunch period from 11:30 a.m. to 1 p.m. Japans Tokyo Stock Exchange opens at 9:00 a.m. and closes at 3 p.m. local time, with a lunch period from 11:30 a.m. to 12:30 p.m. The Hong Kong Stock Exchange opens at 9:30 a.m. and closes at 4 p.m. local time, and it has a lunch period from 12 p.m. to 1 p.m.'

df_ASSET_GROUP
df_fut['es']
df_stk_sp500['aapl']
df_stk_dow
df_stk_russel
df_stk_lon

'''

INSTR_SPECS = dict(
  fut = {
    'use': {
      #'path': 'fut/us_1min',
      'hol': 'hol_es',
      'es': {
        'o_time' : ('0930','o', '0930','Open'),
        'ob_time': ('1800','ob', '1800','Open'),
        'c_time' : ('1600','c', '1559','Close'),  # 1600, C <= 1559 Close
        'cb_time': ('1615','cb', '1614','Close'),
        'cc_time': ('1700','cc', '1659','Close'),

        'beg_time': '0000',

        'hilo': {
            'hdy': ('o','c'),
            'hdyb': ('o','cb'),
            'hdyc': ('o','cc'),
            'hdyd': ('o','0935'),
            'hdye': ('o','0945'),
            'hdyf': ('o','1000'),
            'hdyg': ('o','1030'),
            'hdyh': ('o','1100'),
            'hdyi': ('o','1200'),
            'hdyj': ('o','1300'),
            #'h':('ob1','c'),
            'ha': ('0000','cc'),
            'hb': ('ob','2359'),
            'hc': ('0000','0929'), # delta(o,0d1)
        },

        'beg_date': '2000-01-04'
        # Rollover: Thursday before the 3rd Friday of contract month;
        # Last trading day: 8:30 a.m. on the third Friday of the contract month
      },
      'us': {
        'o_time' : ('0800','o', '0800','Open', '0759'),
        'c_time' : ('1700','c', '1659','Close'),
        'cb_time': ('1500','cb', '1459','Close'),
        'cc_time': ('1500','cc', '1459','Close'),
        'beg_date': '2000-01-04'
      },
      'nq': {
        # nasdaq100 emini
        'o_time' : ('0800','o', '0800','Open', '0759'),
        'c_time' : ('1700','c', '1659','Close'),
        'cb_time': ('1500','cb', '1459','Close'),
        'cc_time': ('1500','cc', '1459','Close'),
        'beg_date': '2000-01-04'
      },
      'ym': {
        # dow jones emini
        'o_time' : ('0800','o', '0800','Open', '0759'),
        'c_time' : ('1700','c', '1659','Close'),
        'cb_time': ('1500','cb', '1459','Close'),
        'cc_time': ('1500','cc', '1459','Close'),
        'beg_date': '2000-01-04'
      },
      'rty': {
        # russell 2000 emini
        'o_time' : ('0800','o', '0800','Open', '0759'),
        'c_time' : ('1700','c', '1659','Close'),
        'cb_time': ('1500','cb', '1459','Close'),
        'cc_time': ('1500','cc', '1459','Close'),
        'beg_date': '2000-01-04'
      },
      'emd': {
        # sp midcap 400 emini
        'o_time' : ('0800','o', '0800','Open', '0759'),
        'c_time' : ('1700','c', '1659','Close'),
        'cb_time': ('1500','cb', '1459','Close'),
        'cc_time': ('1500','cc', '1459','Close'),
        'beg_date': '2000-01-04'
      },
      'qm': {
        # crude oil emini
        'o_time' : ('0800','o', '0800','Open', '0759'),
        'c_time' : ('1700','c', '1659','Close'),
        'cb_time': ('1500','cb', '1459','Close'),
        'cc_time': ('1500','cc', '1459','Close'),
        'beg_date': '2000-01-04'
      },
    }
  },

  stk = {
    'sp500': {
      'o_time': ('0930','o', '0930','Open'),
      'c_time': ('1600','c', '1559','Close'),

      'beg_time': '0930',

      'beg_date': '2000-01-04',
      'hol': 'hol_es',
      # 'path': 'stk/sp500/sp500_1min/'
    },

    'nasdaq100': {
      'o_time': ('0930','o', '0930','Open'),
      'c_time': ('1600','c', '1559','Close'),
      'cb_time': ('1600','cb', '1559','Close'),
      'cc_time': ('1600','cc', '1559','Close'),

      'beg_year': 2002,
      'hol': 'hol_es',
      #'path': 'stk/sp500/nasdaq100_1min/'
    }

  },

  fx = {

  },

  econ = {

  }

)
