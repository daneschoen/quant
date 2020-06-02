import os
import datetime
import json
from pprint import pprint
import pprint
import requests

from apps.settings.constants import *



"""
--------------------------------------------------------------------------------
fx
--------------------------------------------------------------------------------

https://currencylayer.com/
https://fixer.io/quickstart
https://openexchangerates.org/

https://fixer.io/quickstart
1000x /month

http://data.fixer.io/api/latest

    ? access_key = YOUR_ACCESS_KEY
    & base = GBP
    & symbols = USD,AUD,CAD,PLN,MXN

http://data.fixer.io/api/latest?access_key=81ac3545eda48eafb15f349e9046536f
http://data.fixer.io/api/latest?access_key=81ac3545eda48eafb15f349e9046536f&base=USD&symbols=USD,AUD,CAD,EUR,MXN&format=1
http://data.fixer.io/api/latest?access_key=81ac3545eda48eafb15f349e9046536f&symbols=USD,AUD,CAD,PLN,MXN&format=1


http://data.fixer.io/api/convert

    ? access_key = YOUR_ACCESS_KEY
    & from = USD
    & to = EUR
    & amount = 25

http://data.fixer.io/api/convert?access_key=81ac3545eda48eafb15f349e9046536f&from=USD&to=KRW&amount=1

https://currencylayer.com/


European Central Bank Feed
Docs: http://www.ecb.int/stats/exchange/eurofxref/html/index.en.html#dev
Request: http://www.ecb.int/stats/eurofxref/eurofxref-daily.xml

XML Response:

<Cube>
  <Cube time="2015-07-07">
  <Cube currency="USD" rate="1.0931"/>
  <Cube currency="JPY" rate="133.88"/>
  <Cube currency="BGN" rate="1.9558"/>
  <Cube currency="CZK" rate="27.100"/>
</Cube>
--------------------------------------------------------------------------------
"""

"""
--------------------------------------------------------------------------------
equities
--------------------------------------------------------------------------------
https://blog.quandl.com/api-for-stock-data
https://www.quandl.com/api/v1/datasets/WIKI/AAPL.csv?column=4&sort_order=asc&collapse=quarterly&trim_start=2012-01-01&trim_end=2013-12-31

https://iextrading.com/developer/

https://www.alphavantage.co/
https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo


http://1forge.com/forex-data-api
http://www.financialcontent.com/support/documentation/json_quote_api.php


"""
