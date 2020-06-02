import os, sys, pathlib
import argparse
from collections import OrderedDict
from copy import deepcopy
import uuid
from datetime import datetime
# from dateutil.parser import parse as dateparse
import time, math

import numpy as np
import pandas as pd
from pandas.tseries.offsets import *
#from pandas.plotting import scatter_matrix
#import pandas.plotting as pdp
#from pandas_datareader.data import DataReader
# import pandas_datareader.data as web
#from pandas_datareader import data, wb
# import quandl

import colorlover as cl
import matplotlib
matplotlib.use('Agg')
#import matplotlib.pyplot as plt
import seaborn as sns
# sns.set(style="ticks", color_codes=True)

import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.sandbox.regression.predstd import wls_prediction_std
import statsmodels.graphics.api as smg

from sklearn import linear_model

import json
import flask
from flask import send_from_directory, session

from flask_session import Session
# from flask_redis import FlaskRedis
from flask_caching import Cache

import plotly.graph_objs as go  # Layout,
from plotly import tools
import plotly.figure_factory as ff

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from textwrap import dedent

#sys.path.append("/home/sak/Agape/development/projects/fintech/flask_blueprint")
#from apps.app_quant.strategy import *
#sys.path.append("/home/sak/Agape/development/projects/fintech/flask_blueprint/apps/app_quant")
from .strategy import *
from .stats_regression import *
# from pair_state import Pairstate

from apps.settings.settings_pairs import *

"""
# ==============================================================================
# Pairs
# ==============================================================================
"""

# ==============================================================================
# app
# todo: __init__.py
#
#   put in run_server
#   session put pair state
#   pay
#   add regression, rolling corr
#       deep leanring
#   for singl: skew, hist, normality, autocorr
#   3d
#   upload files: c-o1, ...
#   full paid - more instruments, upload

# ==============================================================================
app = dash.Dash(__name__, url_base_pathname='/pair/')

app.server.config.from_pyfile('../settings/settings_pairs.py')

#sess = Session()
#sess.init_app(app)
Session(app.server)

# redis_store = FlaskRedis(app)
""" or:
redis_store = FlaskRedis()

def create_app():
    app = Flask(__name__)
    redis_store.init_app(app)
    return app
"""

CACHE_CONFIG = {
    # try 'filesystem' if you don't want to setup redis
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': os.environ.get('REDIS_URL', 'localhost:6379')
}
cache = Cache(config=CACHE_CONFIG)
cache.init_app(app.server)


app.config.supress_callback_exceptions = True

#app.config.requests_pathname_prefix = ''
#app.config.requests_pathname_prefix = app.config.routes_pathname_prefix.split('/')[-1]
#app.config.update({
    # remove the default of '/'
#   'routes_pathname_prefix': 'pair',

    # remove the default of '/'
#    'requests_pathname_prefix': 'pair'
#})

app.title = "QuantCypher - Pairs"
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

css_external = ["dash.css"] #,
                #"https://codepen.io/chriddyp/pen/bWLwgP.css",
                #"https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"]

js_external = []

#for css in css_external:
#    app.css.append_css({"external_url": css})
#app.server.static_folder = 'static'  # if you run app.py from 'root-dir-name' you don't need to specify.

# @app.server.route('/static/<path:path>')

@app.server.route('/static/<path:path>')
def static_file(path):
    """
    static_folder = os.path.join(os.getcwd(), 'static')
    return send_from_directory(static_folder, path)
    -- app.py
    -- static/stylesheet.css
    """
    return app.send_from_directory('/srv/', path)

for js in js_external:
    app.scripts.append_script({"external_url": js})

colors = {
    'background': '#f2f2da',
    'text': '#9ab8c4'
}

style_mb50 = {'marginBottom':'50'}

style_pre = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}


# ==============================================================================
# constants.py
# ==============================================================================

if DEBUG_PLOT:
    print("\n\ndash.__version__: " + dash.__version__ + "\n")


PER_CORR = 200

# ==============================================================================
# Data
# ==============================================================================

TICKER_PATH = "~/Agape/development/projects/fintech/data_in/equity_future_com/tickers.csv"

# todo: or better yet, cache in mongodb
#       import full sp500_lst
def import_data():
    df_stk = import_sp500(sym_lst=['aapl','goog','nflx'], bl_debug=DEBUG_PLOT)
    df_fut = import_fut()
    df_crp = import_crypto()

    df_sym = pd.read_csv(TICKER_PATH)

    return df_stk, df_fut, df_crp, df_sym

df_stk, df_fut, df_crp, df_symbol = import_data()
df_asset = {}
df_asset['stk'] = df_stk
df_asset['fut'] = df_fut
df_asset['crp'] = df_crp

df_cache = {}  # SHARED for ALL users !

session1 = { 'id_0':{
              'n_clicks':0
            }
          }

asset_lst = ['stk','fut','crp']

assets_meta = {'stk': {
                  'name': 'Stocks'
                },
               'fut': {
                 'es': {
                   'name': 'S&P 500 Index'
                 },
                 'us': {
                   'name': '30 Year US Bonds'
                 }
               },
               'crp': {
                  'name': 'Cryptocurrencies'
                 }
              }


def default_col_asset(asset, sym):
    if asset == 'stk':
        return asset + '-' + sym + '_c'
    elif asset == 'fut':
        return asset + '-' + sym + '_1615'
    elif asset == 'crp':
        return asset + '-' + sym + '_c'

def calc_sns_reg():
    sns_reg = sns.regplot(pd.DataFrame([1,2,3])[0],pd.DataFrame([1,2,3])[0])
    return sns_reg

# todo: dep on paid: disable instr
# ----------------
# dropdown options
# ----------------
opt_crp = [{'label': 'BTC', 'value': 'btc'}, {'label': 'ETH', 'value': 'eth'}]

opt_fut = [{'label': 'S&P 500 Index', 'value': 'es'}, {'label': 'US', 'value': 'us'}]

opt_stk = [{'label': 'AAPL', 'value': 'aapl'}, {'label': 'GOOG', 'value': 'goog'}, {'label': 'NFLX', 'value': 'nflx'}]

opt_comb = {'crp': opt_crp , 'fut': opt_fut, 'stk': opt_stk}

default_stk_idx = next((index for (index, d) in enumerate(opt_stk) if d["value"] == "aapl"), None)
default_stk_val = next(item for item in opt_stk if item["value"] == "aapl")['value']
default_option_val = {'crp': 'btc' , 'fut': 'es', 'stk': default_stk_val}
default_option_idx = {'crp': 0 , 'fut': 0, 'stk': default_stk_idx}


# ----------
# INIT STATE
# ----------

# todo: move to session and hidden div
#       full paid - more instruments, upload
#pair = Pairstate()

#sym_0 = 'aapl'
#sym_1 = 'es'

#pair.sym_0 = sym_0
#pair.sym_1 = sym_1
#pair.sym_0_col = 'c'
#pair.sym_1_col = 'p1615'

# todo cache:
#pair.df_mult = merge_df(*[df_stk[sym_0], df_fut[sym_1]])

#pair.dtrange_init = [str(pair.df_mult.iloc[-PER_CORR].name)[:10],
#                     str(pair.df_mult.iloc[-1].name)[:10]]


# ==============================================================================
# Layout
# ==============================================================================
app.layout = html.Div(style={'marginTop':'70'} , children=[
    html.Link(
        rel='stylesheet',
        href='/static/css/dash.css'
    ),

    html.H3(style={'textAlign': 'center',}, children='Pairs Analysis: Statistics and Machine Learning'),
    html.H4(style={'textAlign': 'center', 'marginBottom':70}, children='Intra- and Inter-Assets'),

    html.Div(style={'marginBottom': '15'}, children ='Choose two instruments from any of these asset classes:'),

    html.Div(className="row", style={'marginBottom':'10'}, children=[
      html.Div(style={'width':'25%', 'marginRight':'20', 'display':'inline-block'}, children=[
        dcc.RadioItems(id='radio_0',
          options=[
            {'label': 'Stocks (S&P 500)', 'value': 'stk'},
            {'label': 'S&P 500 Index, Bonds', 'value': 'fut'},
            {'label': 'Crytpocurrencies', 'value': 'crp'}
          ], value='stk'
        )
      ]),
      html.Div(style={'width':'25%', 'display':'inline-block'}, children=[
        dcc.RadioItems(id='radio_1',
          options=[
            {'label': 'Stocks (S&P 500)', 'value': 'stk'},
            {'label': 'S&P 500 Index, Bonds', 'value': 'fut'},
            {'label': 'Crytpocurrencies', 'value': 'crp'}
          ], value='crp'
        )
      ])
    ]),

    html.Div(className="row", style={'marginBottom':'30'}, children=[

      html.Div(style={'width':'25%', 'marginRight':'20', 'display':'inline-block'}, children=[
        dcc.Dropdown(id='drop_0')
      ]),

      html.Div(style={'width':'25%', 'marginRight':'20', 'display':'inline-block'}, children=[
        dcc.Dropdown(id='drop_1')
      ]),

      html.Button(id='btn_reset', style={'display': 'inline-block','verticalAlign':'top','height':'35'},
          children = [html.Div(style={'marginTop':-3}, children=['Set to 200 Periods'])],
          n_clicks=0
      ),

    ]),


    html.Div(id='div_hidden_drop', style={'display':'none'}, children=[]),
    #'{"drop_0_asset": "None", "drop_0": "None", "drop_1": "None", "drop_1_asset": "None", }'),
    html.Div(id='div_hidden_reg', style={'display':'none'}, children=[]),


    dcc.Graph(id='graph_line_dual', config={'displayModeBar': False}),

    html.Div(id='div_graph_line_dual'),

    html.Div(className="row", style={'marginTop':'-70'}, children=[

      html.Div(className="six columns", children=[
        html.Div(dcc.Graph(id='graph_scatter', config={'displayModeBar': False}) #,
          # figure={
          # }
        )
      ]),

      html.Div(className="six columns", children=[
        html.Div(id='div_reg_summary', style={'fontSize':'11', 'fontFamily':'monospace', 'whiteSpace':'pre-wrap'})
      ]),

    ]),

])  # end page layout


# ==============================================================================
# callbacks
# ==============================================================================
# app.callback(Output('my-div', 'children'),
#                      [Input('my-input', 'value')],
#                      [State('my-div', 'children')])
# def update_div(value, existing_state):
#     if some_condition:
#          return existing_state

# ------------------------------------------------------------------------------
# radio  =>  drop, hidden
# ------------------------------------------------------------------------------
@app.callback(
    Output('drop_0', 'options'),
    [Input('radio_0', 'value')])
def radio_0_drop(asset):
    #return [{'label': i, 'value': i} for i in opt_comb[asset]]
    return opt_comb[asset]

@app.callback(
    Output('drop_1', 'options'),
    [Input('radio_1', 'value')])
def radio_1_drop(asset):
    return opt_comb[asset]


# @app.callback(
#     Output('drop_1', 'value'),
#     [Input('drop_1', 'options'),
#      Input('div_hidden_drop', 'children')])
# def set_default_value(available_options, state):
#     asset = json.loads(state)['drop_1_asset']
#     return available_options[default_option_idx[asset]]['value']


@app.callback(
    Output('drop_0', 'value'),
    [Input('drop_0', 'options')])
def set_drop_default_value_0(available_options):
    # asset = json.loads(state)['drop_1_asset']
    if available_options[0]['value'] == opt_stk[0]['value']:
        asset = 'stk'
    elif available_options[0]['value'] == opt_fut[0]['value']:
        asset = 'fut'
    else:
        asset = 'crp'
    return available_options[default_option_idx[asset]]['value']

@app.callback(
    Output('drop_1', 'value'),
    [Input('radio_1', 'value')])
def set_drop_default_value_1(radio_value):
    # asset = json.loads(state)['drop_1_asset']
    return default_option_val[radio_value]

# ------------------------------------------------------------------------------
# radio, drop  =>  hidden - state
# ------------------------------------------------------------------------------
@app.callback(
    Output('div_hidden_drop', 'children'),
    [Input('radio_0', 'value'), Input('radio_1', 'value'),
     Input('drop_0', 'value'), Input('drop_1', 'value')])
def radio_drop_hidden(asset_0, asset_1, sym_0, sym_1):
    state = {}
    state['drop_0_asset'] = asset_0
    state['drop_1_asset'] = asset_1
    state['drop_0'] = sym_0
    state['drop_1'] = sym_1

    pair_name = asset_0 + '_' + sym_0 + '-' + asset_1 + '_' + sym_1
    # todo: redis : pair_name !
    if pair_name not in df_cache:
        df_pair = merge_df(*[df_asset[asset_0][sym_0], df_asset[asset_1][sym_1]])
        df_cache[pair_name] = df_pair

    return json.dumps(state)



# ------------------------------------------------------------------------------
# graphs
# ------------------------------------------------------------------------------

@app.callback(Output('graph_line_dual', 'figure'),
             [Input('btn_reset', 'n_clicks'),
              Input('div_hidden_drop', 'children')])
def graph_line_dual(n_clicks, state):
    if DEBUG_PLOT:
        print("============> " + str(state))
    state = json.loads(state)
    sym_0 = state['drop_0']
    sym_1 = state['drop_1']
    asset_0 = state['drop_0_asset']
    asset_1 = state['drop_1_asset']
    sym_0_col = default_col_asset(asset_0, sym_0)
    sym_1_col = default_col_asset(asset_1, sym_1)

    pair_name = asset_0 + '_' + sym_0 + '-' + asset_1 + '_' + sym_1
    df_pair = df_cache[pair_name]

    dtrange_init = [str(df_pair.iloc[-PER_CORR].name)[:10],
                    str(df_pair.iloc[-1].name)[:10]]

    # todo: redis : pair_name !
    # pair_name = asset_0 + '_' + sym_0 + '-' + asset_1 + '_' + sym_1
    # if pair_name in df_cache:
    #     df_pair = df_cache[pair_name]
    # else:
    #     df_pair = merge_df(*[df_asset[asset_0][sym_0], df_asset[asset_1][sym_1]])
    #     df_cache[pair_name] = df_pair

    data_lst = [go.Scatter(
        x = df_pair.index,
        y = df_pair[sym_0_col],
        name = sym_0.upper()
        #'type': 'scatter'  #'candlestick'
      ), go.Scatter(
        x = df_pair.index,
        y = df_pair[sym_1_col],
        name = sym_1.upper(),
        #'type': 'scatter'  #'candlestick'
        yaxis='y2'
      )
    ]

    layout = go.Layout(
        title = '{} vs {}'.format(sym_0.upper(), sym_1.upper()),
        xaxis=dict(
         rangeslider = dict(visible=True),
         range = dtrange_init,
         rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label='1m',
                     step='month',
                     stepmode='backward'),
                dict(count=6,
                     label='6m',
                     step='month',
                     stepmode='backward'),
                dict(count=1,
                    label='YTD',
                    step='year',
                    stepmode='todate'),
                dict(count=1,
                    label='1y',
                    step='year',
                    stepmode='backward'),
                dict(step='all')
            ])
          )
        ),
        yaxis=dict(
          title=sym_0.upper()
        ),
        yaxis2=dict(
          title=sym_1.upper(),
          titlefont=dict(
            color='orange'
          ),
          tickfont=dict(
            color='orange'
          ),
          overlaying='y',
          side='right'
        )
    )

    # config = {
    #   'displayModeBar': False,
    #   'displaylogo': False,
    #   'showLink': False
    # }

    #fig = go.Figure(data=data_lst, layout=layout)
    fig = {
        'data': data_lst,
        'layout': layout
    }
    return fig


@app.callback(Output('graph_scatter', 'figure'),
                     [Input('graph_line_dual', 'relayoutData'),
                      Input('btn_reset', 'n_clicks'),
                      Input('div_hidden_drop', 'children')])
def graph_scatter(relayoutData, n_clicks, state):
    state = json.loads(state)
    sym_0 = state['drop_0']
    sym_1 = state['drop_1']
    asset_0 = state['drop_0_asset']
    asset_1 = state['drop_1_asset']
    sym_0_col = default_col_asset(asset_0, sym_0)
    sym_1_col = default_col_asset(asset_1, sym_1)

    pair_name = asset_0 + '_' + sym_0 + '-' + asset_1 + '_' + sym_1
    df_pair = df_cache[pair_name]

    dtrange_init = [str(df_pair.iloc[-PER_CORR].name)[:10],
                    str(df_pair.iloc[-1].name)[:10]]
    dtrange = deepcopy(dtrange_init)

    # Since relayoutData = {'xaxis.autorange': True} even when button clicked:
    if n_clicks != session1['id_0']['n_clicks']:
        session1['id_0']['n_clicks'] = n_clicks
    elif ((relayoutData is None) or
          ('xaxis.autorange' in relayoutData and relayoutData['xaxis.autorange'] == True)): # or
          # ('xaxis.range' not in relayoutData and 'xaxis.range[0]' not in relayoutData)):
        dtrange = [str(df_pair.index[0])[:10], str(df_pair.index[-1])[:10]]
    elif ('autosize' in relayoutData and relayoutData['autosize'] == True):
        pass
    else:
        if 'xaxis.range' in relayoutData:
            if pd.Timestamp(relayoutData['xaxis.range'][0][:10]) >= df_pair.index[0]:
                dtrange[0] = relayoutData['xaxis.range'][0][:10]
            if pd.Timestamp(relayoutData['xaxis.range'][1][:10]) <= df_pair.index[-1]:
                dtrange[1] = relayoutData['xaxis.range'][1][:10]
        else:
            if pd.Timestamp(relayoutData['xaxis.range[0]'][:10]) >= df_pair.index[0]:
                dtrange[0] = relayoutData['xaxis.range[0]'][:10]
            if pd.Timestamp(relayoutData['xaxis.range[1]'][:10]) <= df_pair.index[-1]:
                dtrange[1] = relayoutData['xaxis.range[1]'][:10]

    if dtrange[0] not in df_pair.index:
        # todo: pd.Timestamp('2010-07-19').dayofweek
        # roll fwd
        tmp_dtime = pd.Timestamp(dtrange[0]) + pd.Timedelta(days=1)
        while tmp_dtime not in df_pair.index:
            tmp_dtime += pd.Timedelta(days=1)
        dtrange[0] = str(tmp_dtime)[:10]

    if dtrange[1] not in df_pair.index:
        tmp_dtime = pd.Timestamp(dtrange[1]) - pd.Timedelta(days=1)
        while tmp_dtime not in df_pair.index:
            tmp_dtime -= pd.Timedelta(days=1)
        dtrange[1] = str(tmp_dtime)[:10]

    if DEBUG_PLOT: print(dtrange)

    # slightly different from expected due to weekends
    per = df_pair.index.get_loc(dtrange[1]) - df_pair.index.get_loc(dtrange[0]) + 1

    x_all = df_pair[sym_0_col].pct_change()
    y_all = df_pair[sym_1_col].pct_change()
    x_per = df_pair.loc[dtrange[0]:dtrange[1],sym_0_col].pct_change()#[1:]
    y_per = df_pair.loc[dtrange[0]:dtrange[1],sym_1_col].pct_change()#[1:]
    x_per, y_per = clean_nan_inf(x_per, y_per)

    # # get regression line and confidence from sns
    # sns_reg = sns.regplot(x_per, y_per)
    # X_reg = sns_reg.get_lines()[0].get_xdata()  # regression x-coordinates
    # y_reg = sns_reg.get_lines()[0].get_ydata()  # regression y-coordinate
    # P = sns_reg.get_children()[1].get_paths()   # the list of Path(s) bounding the shape of 95% confidence interval-transparent
    # # To get the transparent confidence interval band along the regression line, extract the path describing the boundary of that band
    # p_codes={1:'M', 2: 'L', 79: 'Z'}   # to get the Plotly codes for commands to define the svg path
    # path=''
    # for s in P[0].iter_segments():
    #     c=p_codes[s[1]]
    #     xx, yy=s[0]
    #     path+=c+str('{:.5f}'.format(xx))+' '+str('{:.5f}'.format(yy))
    # # #display(path)

    model, reg_model = reg_ols_sm(x_per, y_per)
    x_reg = x_per
    y_reg = reg_model.predict()
    uid = uuid.uuid4()
    session['uid'] = uid
    session['sid'] = session.sid
    session['dtime'] = datetime.datetime.utcnow()
    session['reg_model'] = reg_model
    print(reg_model.summary())
    print("*"*20)
    print(uid)
    print(session['sid'])

    data_lst = [{
        'x': x_all,
        'y': y_all,
        #'text': ['a', 'b', 'c', 'd'],
        #'customdata': ['c.a', 'c.b', 'c.c', 'c.d'],
        'name': 'All Data',
        'mode': 'markers',
        'marker': {
          'size': 3,
          'color': '#dbd4c9' #'rgba(186, 203, 209, 0.7)'   # #dbd4c9
        }
      },{
        'x': x_per,
        'y': y_per,
        'name': str(per) + ' Period',
        'mode': 'markers',
        'marker': {
          'size': 4,
          'color': 'rgba(227, 176, 90, 1.0)'
        }
      },{
        'x': x_reg,
        'y': y_reg,
        'name': 'Regression Line',
        'type': 'scatter',
        'mode': 'lines',
        'line': {
           'color': 'rgb(68, 122, 219)',
           'width': 1.0
        }
      }
    ]

    layout = {
      #"autosize": False,
      #"font": {"family": "Balto"},
      #"height": 500,
      "hovermode": "closest",
      #"margin": {"t": 120},
      "plot_bgcolor": "rgba(240,240,240,0.9)",
      # "shapes": [
      #   {
      #     "fillcolor": "rgba(68, 122, 219, 0.25)",
      #     "line": {
      #       "color": "rgba(68, 122, 219, 0.25)",
      #       "width": 0.1
      #     },
      #     "path": path,
      #     "type": "path"
      #   }
      # ],
      "title": "Linear Regression",
      # "width": 700,
      "xaxis": {
        "gridcolor": "rgb(255,255,255)",
        "mirror": True,
        #"range": [3.29408776285, 9.04691223715],
        "showline": True,
        "ticklen": 4,
        "title": sym_0.upper(),
        #"zeroline": False
      },
      "yaxis": {
        "gridcolor": "rgb(255,255,255)",
        "mirror": True,
        #"range": [-11.6745548881, 54.4383879616],
        "showline": True,
        "ticklen": 4,
        "title": sym_1.upper(),
        #"zeroline": False
      }
    }

    #fig = go.Figure(data=data_lst, layout=layout)
    fig = {
        'data': data_lst,
        'layout': layout
    }
    return fig


@app.callback(
    Output('div_reg_summary', 'children'),
    [Input('graph_scatter', 'figure')])
def get_reg(_):
    reg_model = session.get('reg_model', '')
    s = str(reg_model.summary())
    ss = s.split('Warnings')[0]
    ss = ss.split('='*78, 4)
    print(s)
    print(session.sid)
    print(session.get('dtime', None))
    return '\n\n\n\n' + ''.join(ss[:-1])



# ==============================================================================

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', action="store", dest="p", nargs=1, default=[PORT])
    args = parser.parse_args()

    port = int(args.p[0])

    # app.run(host='0.0.0.0', port=80)
    app.run_server(debug=DEBUG_PLOT, port=port)
