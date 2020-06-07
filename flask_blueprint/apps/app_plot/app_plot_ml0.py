import os, sys, pathlib
import argparse
from collections import OrderedDict
from copy import deepcopy
import datetime

# from dateutil.parser import parse as dateparse
import json, pickle
import time, math
import uuid

import numpy as np
import pandas as pd
from pandas.tseries.offsets import *

import colorlover as cl
# import matplotlib
# matplotlib.use('Agg')
# #import matplotlib.pyplot as plt
import seaborn as sns
# # sns.set(style="ticks", color_codes=True)

import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.sandbox.regression.predstd import wls_prediction_std
import statsmodels.graphics.api as smg
from statsmodels.tsa.stattools import acf, pacf

from sklearn import linear_model

import flask
from flask import send_from_directory, session

import plotly.graph_objs as go  # Layout,
from plotly import tools
import plotly.figure_factory as ff

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
# X import .grasia_dash_components as gdc
#from . import grasia_dash_components as gdc
#import grasia_dash_components as gdc

from textwrap import dedent

from apps.app_auth import requires_auth

from apps.app_util import mongodb, col_coin_spec, col_coin_top, \
    col_coin_hist_daily, col_coin_hist_hour, col_coin_hist_min, \
    mongodb_geo, logger_flask

from apps import app, cache, redis_db, PLOT_ROUTES

from apps.settings.settings_server_plot import *

#from apps.app_quant import strategy
import apps.app_quant.strategy_utils as strategy_utils
import apps.app_quant.stats_regression as stats_regression

# from pair_state import Pairstate
# from apps.app_plot import df_asset


"""
# ==============================================================================
# Pairs - ML version
# ==============================================================================
"""

# ==============================================================================
# app
# todo: __init__.py
#
#   pay site:
#   add regression, rolling corr
#       deep leanring
#   for singl: skew, hist, normality, autocorr
#   3d
#   upload files: c-o1, ...
#   full paid - more instruments, upload

# ==============================================================================
app_pair = dash.Dash(server=app, url_base_pathname='/_' + PLOT_ROUTES['pair'])

#app_pair.server.config.from_pyfile('../settings/settings_pair.py')

app_pair.config.supress_callback_exceptions = True

#app.config.requests_pathname_prefix = ''
#app.config.requests_pathname_prefix = app.config.routes_pathname_prefix.split('/')[-1]
#app.config.update({
    # remove the default of '/'
#   'routes_pathname_prefix': 'pair',

    # remove the default of '/'
#    'requests_pathname_prefix': 'pair'
#})

app_pair.title = "QuantCypher - Data Science"
app_pair.css.config.serve_locally = True
app_pair.scripts.config.serve_locally = True

css_external = ["dash.css"] #,
                #"https://codepen.io/chriddyp/pen/bWLwgP.css",
                #"https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"]

js_external = []

#for css in css_external:
#    app.css.append_css({"external_url": css})
#app.server.static_folder = 'static'  # if you run app.py from 'root-dir-name' you don't need to specify.

# @app.server.route('/static/<path:path>')

@app_pair.server.route('/static/<path:path>')
def static_file_pair(path):
    """
    static_folder = os.path.join(os.getcwd(), 'static')
    return send_from_directory(static_folder, path)
    -- app.py
    -- static/stylesheet.css
    """
    return app_pair.send_from_directory('/srv/', path)

for js in js_external:
    app_pair.scripts.append_script({"external_url": js})

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

if app.config['DEBUG_PLOT']:
    print("\n\ndash.__version__: " + dash.__version__ + "\n")


PER_CORR = 200


# ==============================================================================
# Data
# ==============================================================================


TICKER_PATH = "~/projects/fintech/data_in/equity_future_com/tickers.csv"

# todo: or better yet, cache in mongodb
#       import full sp500_lst
def import_data():
    df_stk = strategy_utils.import_sp500_dct_df(sym_lst=['aapl','goog','nflx'])
    df_fut = strategy_utils.import_fut_dct_df()
    df_crp = strategy_utils.import_crypto_dct_df()

    df_sym = pd.read_csv(TICKER_PATH)
    print('X'*60 + ' import data')
    return df_stk, df_fut, df_crp, df_sym

df_stk, df_fut, df_crp, df_symbol = import_data()
df_asset = {}
df_asset['stk'] = df_stk
df_asset['fut'] = df_fut
df_asset['crp'] = df_crp

# ==============================================================================

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
        return asset + '_' + sym + '_c'
    elif asset == 'fut':
        return asset + '_' + sym + '_1615'
    elif asset == 'crp':
        return asset + '_' + sym + '_c'

def default_sym_title(asset, sym):
    if asset == 'fut':
        if sym == 'es':
            return 'S&P 500 Index'
        if sym == 'us':
          return 'US 30 Year Bond'

    return sym.upper()


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
#logger_flask.info('yabbadababa')

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
app_pair.layout = html.Div(style={'marginTop':'15'}, children=[
    html.Link(
        rel='stylesheet',
        href='/static/css/dash.css'
    ),

    html.Div(style={'backgroundColor': 'rgb(250, 250, 255)', 'marginTop':'-13', 'paddingTop':1, 'paddingBottom':7}, children=[
      html.H3(style={'textAlign': 'center', 'color':'rgba(67,67,67,1.0)'}, children='Data Science & Data Visualization'),
      html.H4(style={'textAlign': 'center', 'marginTop':'-9', 'color':'rgba(78,78,78,1.0)'}, children='Machine Learning, Statistics, and Reactive Graphs'),
      html.H5(style={'textAlign': 'center', 'marginTop':'-5.9', 'color':'rgba(78,78,78,1.0)', 'marginBottom':2, 'paddingBottom':11 }, children='Pairs Analysis for Intra- and Inter-Assets'),
    ]),

    html.Div(className="row", style={'marginBottom':'7', 'paddingLeft':'10','paddingRight':'10',
      'backgroundColor': 'rgb(247, 247, 250)', 'border': 'thin lightgrey solid'}, children=[
      html.Div(style={'paddingTop':'10', 'marginBottom': '15'}, children ='Choose two instruments from any of these asset classes:'),

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
      ]),

      html.Div(className="row", style={'marginTop':'10', 'marginBottom':'10'}, children=[

        html.Div(style={'width':'25%', 'marginRight':'20', 'display':'inline-block'}, children=[
          dcc.Dropdown(id='drop_0')
        ]),

        html.Div(style={'width':'25%', 'marginRight':'20', 'display':'inline-block'}, children=[
          dcc.Dropdown(id='drop_1')
        ]),

        html.Button(id='btn_reset', style={'display': 'inline-block', 'verticalAlign':'top', 'paddingLeft':'6', 'paddingRight':'6', 'height':'35', 'backgroundColor':'rgb(245,245,245)'},
          children = [html.Div(style={'marginTop':-3}, children=['Reset to 200 Periods'])],
          n_clicks=0
        ),

      ]),

    ]),


    html.Div(id='div_hidden_drop', style={'display':'none'}, children=[]),
    #'{"drop_0_asset": "None", "drop_0": "None", "drop_1": "None", "drop_1_asset": "None", }'),
    html.Div(id='div_hidden_reg', style={'display':'none'}, children=[]),


    html.Div(id='div_graph_line_dual', style={'border': 'thin lightgrey solid', 'marginBottom':4}, children=[
      dcc.Graph(id='graph_line_dual', config={'displayModeBar': False})
    ]),


    html.Div(className="row", style={'border': 'thin lightgrey solid', 'marginBottom':4}, children=[

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

    html.Div(className="row", style={'border': 'thin lightgrey solid', 'marginBottom':4}, children=[
        html.Div(className="six columns", children=[dcc.Graph(id='graph_3d_surface_reg')]),
        html.Div(className="six columns", children=[dcc.Graph(id='graph_corr_rolling')]),
    ]),

    html.Div(className="row", style={'border': 'thin lightgrey solid', 'marginBottom':4}, children=[
        html.Div(className="six columns", children=[dcc.Graph(id='graph_acf_pacf_0')]),
        html.Div(className="six columns", children=[dcc.Graph(id='graph_acf_pacf_1')]),
    ]),

    # html.Div(className="row", children=[
    #     html.Div(className="six columns", children=[dcc.Graph(id='qq')]),
    #     html.Div(className="six columns", children=[dcc.Graph(id='qq2')]),
    # ])

    # html.Div(className="row", children=[
    #     html.Div(children=[dcc.Graph(id='deeplearning')]),
    # ])

    #gdc.Import()
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
@app_pair.callback(
    Output('drop_0', 'options'),
    [Input('radio_0', 'value')])
def radio_0_drop(asset):
    #return [{'label': i, 'value': i} for i in opt_comb[asset]]
    return opt_comb[asset]

@app_pair.callback(
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


@app_pair.callback(
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

@app_pair.callback(
    Output('drop_1', 'value'),
    [Input('radio_1', 'value')])
def set_drop_default_value_1(radio_value):
    # asset = json.loads(state)['drop_1_asset']
    return default_option_val[radio_value]

# ------------------------------------------------------------------------------
# radio, drop  =>  hidden - state
# ------------------------------------------------------------------------------
# @app_pair.callback(
#     Output('div_hidden_drop', 'children'),
#     [Input('radio_0', 'value'), Input('radio_1', 'value'),
#      Input('drop_0', 'value'), Input('drop_1', 'value')])
# def radio_drop_hidden(asset_0, asset_1, sym_0, sym_1):
#     state_selection = {}
#     state_selection['asset_0'] = asset_0
#     state_selection['asset_1'] = asset_1
#     state_selection['sym_0'] = sym_0
#     state_selection['sym_1'] = sym_1
#     # eg, 'stk_aapl-crp_btc'
#     pair_name = asset_0 + '_' + sym_0 + '-' + asset_1 + '_' + sym_1
#     state_selection['pair_name'] = pair_name
#     df_pair = get_pair_merged(pair_name)
#
#     return json.dumps(state_selection)



# ------------------------------------------------------------------------------
# graphs
# ------------------------------------------------------------------------------

@app_pair.callback(Output('graph_line_dual', 'figure'),
    [ Input('radio_0', 'value'), Input('radio_1', 'value'),
      Input('drop_0', 'value'), Input('drop_1', 'value'),
      Input('btn_reset', 'n_clicks'),
      Input('div_hidden_drop', 'children')
    ])
def graph_line_dual(asset_0, asset_1, sym_0, sym_1, n_clicks, state):
    pair_name = asset_0 + '_' + sym_0 + '-' + asset_1 + '_' + sym_1
    df_pair_raw = get_pair_merged(pair_name)

    # state = json.loads(state)
    # sym_0 = state['drop_0']
    # sym_1 = state['drop_1']
    # asset_0 = state['drop_0_asset']
    # asset_1 = state['drop_1_asset']

    sym_0_col = default_col_asset(asset_0, sym_0)
    sym_1_col = default_col_asset(asset_1, sym_1)

    dtrange_init = [str(df_pair_raw.iloc[-PER_CORR].name)[:10],
                    str(df_pair_raw.iloc[-1].name)[:10]]

    data_lst = [go.Scatter(
        x = df_pair_raw.index,
        y = df_pair_raw[sym_0_col],
        name = default_sym_title(asset_0, sym_0)
        #'type': 'scatter'  #'candlestick'
      ), go.Scatter(
        x = df_pair_raw.index,
        y = df_pair_raw[sym_1_col],
        name = default_sym_title(asset_1, sym_1),
        #'type': 'scatter'  #'candlestick'
        yaxis='y2'
      )
    ]

    layout = go.Layout(
        title = '{} vs {}'.format(default_sym_title(asset_0, sym_0), default_sym_title(asset_1, sym_1)),
        paper_bgcolor = '#F5F6F9',
        plot_bgcolor = '#F5F6F9',
        margin=dict(b=20),
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
          ),
          type='date'
          # color = '#444',  #'white'
          # gridcolor='#E1E5ED',
          #calendar='gregorian',
          #showline=False,
          #zerolinewidth=True,
          #zerolinewidth=1,
        ),
        yaxis=dict(
          title=default_sym_title(asset_0, sym_0),
          autorange=True,
          # gridcolor = '#444'
          #showline=False
          zeroline=False
        ),
        yaxis2=dict(
          title=default_sym_title(asset_1, sym_1),
          titlefont=dict(
            color='orange'
          ),
          tickfont=dict(
            color='orange'
          ),
          overlaying='y',
          side='right',
          autorange=True,
          #showline=False
          zeroline=False
          # gridcolor = '#444',
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


@app_pair.callback(Output('graph_scatter', 'figure'),
    [ Input('radio_0', 'value'), Input('radio_1', 'value'),
      Input('drop_0', 'value'), Input('drop_1', 'value'),
      Input('graph_line_dual', 'relayoutData'),
      Input('btn_reset', 'n_clicks'),
      Input('div_hidden_drop', 'children')
    ])
def graph_scatter(asset_0, asset_1, sym_0, sym_1, relayoutData, n_clicks, state):
    pair_name = asset_0 + '_' + sym_0 + '-' + asset_1 + '_' + sym_1
    df_pair_raw = get_pair_merged(pair_name)

    sym_0_col = default_col_asset(asset_0, sym_0)
    sym_1_col = default_col_asset(asset_1, sym_1)

    dtrange_init = [str(df_pair_raw.iloc[-PER_CORR].name)[:10],
                    str(df_pair_raw.iloc[-1].name)[:10]]
    dtrange = deepcopy(dtrange_init)

    # Since relayoutData = {'xaxis.autorange': True} even when button clicked:
    if n_clicks != session1['id_0']['n_clicks']:
        session1['id_0']['n_clicks'] = n_clicks
        print('----------------- n_click')
    elif ((relayoutData is None) or
          ('xaxis.autorange' in relayoutData and relayoutData['xaxis.autorange'] == True)): # or
          # ('xaxis.range' not in relayoutData and 'xaxis.range[0]' not in relayoutData)):
        dtrange = [str(df_pair_raw.index[0])[:10], str(df_pair_raw.index[-1])[:10]]
    elif ('autosize' in relayoutData and relayoutData['autosize'] == True):
        pass
    else:
        if 'xaxis.range' in relayoutData:
            if pd.Timestamp(relayoutData['xaxis.range'][0][:10]) >= df_pair_raw.index[0]:
                dtrange[0] = relayoutData['xaxis.range'][0][:10]
            if pd.Timestamp(relayoutData['xaxis.range'][1][:10]) <= df_pair_raw.index[-1]:
                dtrange[1] = relayoutData['xaxis.range'][1][:10]
        else:
            if pd.Timestamp(relayoutData['xaxis.range[0]'][:10]) >= df_pair_raw.index[0]:
                dtrange[0] = relayoutData['xaxis.range[0]'][:10]
            if pd.Timestamp(relayoutData['xaxis.range[1]'][:10]) <= df_pair_raw.index[-1]:
                dtrange[1] = relayoutData['xaxis.range[1]'][:10]

    if dtrange[0] not in df_pair_raw.index:
        # todo: pd.Timestamp('2010-07-19').dayofweek
        # roll fwd
        tmp_dtime = pd.Timestamp(dtrange[0]) + pd.Timedelta(days=1)
        while tmp_dtime not in df_pair_raw.index:
            tmp_dtime += pd.Timedelta(days=1)
        dtrange[0] = str(tmp_dtime)[:10]

    if dtrange[1] not in df_pair_raw.index:
        tmp_dtime = pd.Timestamp(dtrange[1]) - pd.Timedelta(days=1)
        while tmp_dtime not in df_pair_raw.index:
            tmp_dtime -= pd.Timedelta(days=1)
        dtrange[1] = str(tmp_dtime)[:10]

    print(dtrange)

    # slightly different from expected due to weekends
    per = df_pair_raw.index.get_loc(dtrange[1]) - df_pair_raw.index.get_loc(dtrange[0]) + 1

    x_all_raw = df_pair_raw[sym_0_col]
    y_all_raw = df_pair_raw[sym_1_col]

    x_all, y_all, x_per, y_per = stats_regression.transform_pctchange_clean_standardize_sample_pd(x_all_raw, y_all_raw, dtrange[0], dtrange[1])

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

    model, reg_model = stats_regression.reg_ols_sm(y_per, x_per)
    x_reg = x_per
    y_reg = reg_model.predict()

    session_data = dict(
      reg_model = reg_model,
      dtime = datetime.datetime.utcnow()
    )
    redis_db.set(session.sid, pickle.dumps(session_data))

    return get_figure_scatter_reg(x_all, y_all, x_per, y_per, x_reg, y_reg, asset_0, sym_0, asset_1, sym_1, per)


@app_pair.callback(
    Output('div_reg_summary', 'children'),
    [Input('graph_scatter', 'figure')])
def gen_reg(_):
    session_data = pickle.loads(redis_db.get(session.sid))

    reg_model = session_data.get('reg_model', 'no reg_model')

    s = str(reg_model.summary())
    ss = s.split('Warnings')[0]
    ss = ss.split('='*78, 4)
    return '\n\n\n\n' + ''.join(ss[:-1])


@app_pair.callback(Output('graph_3d_surface_reg', 'figure'),
    [ Input('radio_0', 'value'), Input('radio_1', 'value'),
      Input('drop_0', 'value'), Input('drop_1', 'value'),
    ])
def graph_3d_surface_reg(asset_0, asset_1, sym_0, sym_1):
    pair_name = asset_0 + '_' + sym_0 + '-' + asset_1 + '_' + sym_1
    df_pair_raw = get_pair_merged(pair_name)

    sym_0_col = default_col_asset(asset_0, sym_0)
    sym_1_col = default_col_asset(asset_1, sym_1)

    x_all_raw = df_pair_raw[sym_0_col]
    y_all_raw = df_pair_raw[sym_1_col]

    x_all = stats_regression.transform_pctchange_clean_standardize_pd(x_all_raw)
    y_all = stats_regression.transform_pctchange_clean_standardize_pd(y_all_raw)

    x, y, z = stats_regression.calc_matrix_reg(x_all, y_all, PER_CORR)

    return get_figure_3d_surface_reg(x, y, z, 'Regression Plane - Rolling ' + str(PER_CORR) + ' period')


@app_pair.callback(Output('graph_corr_rolling', 'figure'),
    [ Input('radio_0', 'value'), Input('radio_1', 'value'),
      Input('drop_0', 'value'), Input('drop_1', 'value'),
    ])
def graph_corr_rolling(asset_0, asset_1, sym_0, sym_1):
    pair_0,  pair_1 = asset_0 + '_' + sym_0, asset_1 + '_' + sym_1
    pair_name = pair_0 + '-' + pair_1
    df_pair_standard = get_pair_standard(pair_name)

    sym_0_col = default_col_asset(asset_0, sym_0)
    sym_1_col = default_col_asset(asset_1, sym_1)

    se_corr_rolling = df_pair_standard[sym_0_col].rolling(window=PER_CORR).corr(df_pair_standard[sym_1_col])

    return get_figure_line_dt(y_ = se_corr_rolling[PER_CORR:], x_dt = se_corr_rolling.index,
                              title = 'Rolling Correlation: {} - {}'.format(default_sym_title(asset_0, sym_0), default_sym_title(asset_1, sym_1)),
                              yaxis_dtick=0.2)


@app_pair.callback(Output('graph_acf_pacf_0', 'figure'),
    [ Input('radio_0', 'value'), Input('radio_1', 'value'),
      Input('drop_0', 'value'), Input('drop_1', 'value'),
    ])
def graph_acf_pacf_0(asset_0, asset_1, sym_0, sym_1):
    pair_0,  pair_1 = asset_0 + '_' + sym_0, asset_1 + '_' + sym_1
    pair_name = pair_0 + '-' + pair_1
    df_pair_standard = get_pair_standard(pair_name)

    sym_0_col = default_col_asset(asset_0, sym_0)
    # sym_1_col = default_col_asset(asset_1, sym_1)

    acf_x = acf(df_pair_standard[sym_0_col])  # acf(x_all, unbiased=True, nlags=nlags-1)
    pacf_x = pacf(df_pair_standard[sym_0_col])

    #display(data_lst[0]['y'])
    #display(data_lst[1]['y'])

    fig = get_figure_acf_pacf(acf_x=acf_x, pacf_x=pacf_x, title='Autocorrelation: ' + default_sym_title(asset_0, sym_0))
    return fig


@app_pair.callback(Output('graph_acf_pacf_1', 'figure'),
    [ Input('radio_0', 'value'), Input('radio_1', 'value'),
      Input('drop_0', 'value'), Input('drop_1', 'value'),
    ])
def graph_acf_pacf_1(asset_0, asset_1, sym_0, sym_1):
    pair_0,  pair_1 = asset_0 + '_' + sym_0, asset_1 + '_' + sym_1
    pair_name = pair_0 + '-' + pair_1
    df_pair_standard = get_pair_standard(pair_name)

    # sym_0_col = default_col_asset(asset_0, sym_0)
    sym_1_col = default_col_asset(asset_1, sym_1)

    acf_x = acf(df_pair_standard[sym_1_col])  # acf(x_all, unbiased=True, nlags=nlags-1)
    pacf_x = pacf(df_pair_standard[sym_1_col])

    fig = get_figure_acf_pacf(acf_x=acf_x, pacf_x=pacf_x, title='Autocorrelation: ' + default_sym_title(asset_1, sym_1))
    return fig



# ==============================================================================
# Functions
# ==============================================================================
# @app.cache.memoize(timeout=None)
# @cache.memoize(timeout=None)
# def get_session_data(session_id):
#     return datetime.utcnow()


@cache.memoize(timeout=None)
def get_pair_merged(pair_name):
    """
    df_cache['stk_aapl-crp_btc'] = merge_df
    """
    # if pair_name not in df_cache:
    (asset_0, sym_0), (asset_1, sym_1)  = [asset_sym.split('_') for asset_sym in pair_name.split('-')]
    print('&'*40 + pair_name + time.ctime())

    df_pair_raw = merge_df(*[df_asset[asset_0][sym_0], df_asset[asset_1][sym_1]])

    return df_pair_raw


@cache.memoize(timeout=None)
def get_pair_standard(pair_name):
    # if pair_name not in df_cache:
    (asset_0, sym_0), (asset_1, sym_1)  = [asset_sym.split('_') for asset_sym in pair_name.split('-')]
    df_pair_raw = get_pair_merged(pair_name)

    sym_0_col = default_col_asset(asset_0, sym_0)
    sym_1_col = default_col_asset(asset_1, sym_1)

    x_all_raw = df_pair_raw[sym_0_col]
    y_all_raw = df_pair_raw[sym_1_col]

    x_all = stats_regression.transform_pctchange_clean_standardize_pd(x_all_raw)
    y_all = stats_regression.transform_pctchange_clean_standardize_pd(y_all_raw)

    df_pair_standard = pd.concat([x_all, y_all], axis=1)

    return df_pair_standard


# -------------------------    get_figure's     --------------------------------

def get_figure_line_dt(*, y_, x_dt, title, yaxis_dtick=None):
    data_lst = [ go.Scatter(
        y = y_,
        x = x_dt,
        # name =
        #type = 'scatter'  #'candlestick'
      )
    ]

    layout = go.Layout(
        title = title,
        # paper_bgcolor = '#F5F6F9',
        # plot_bgcolor = '#F5F6F9',
        #margin=dict(b=20),
        xaxis=dict(
          type='date'
          # color = '#444',  #'white'
          # gridcolor='#E1E5ED',
          #calendar='gregorian',
          #showline=False,
          #zerolinewidth=True,
          #zerolinewidth=1,
        ),
        yaxis=dict(
          #title=,
          # autorange=True,
          range=[-1, 1]
          # gridcolor = '#444'
          #showline=False
          #zeroline=False
        )
    )

    if yaxis_dtick:
        # layout['yaxis'].update(dict(dtick=yaxis_dtick))
        layout['yaxis']['dtick']=yaxis_dtick

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



def get_figure_scatter_reg(x_all, y_all, x_per, y_per, x_reg, y_reg, asset_0, sym_0, asset_1, sym_1, per):
    data_lst = []
    if x_all is not None:
        data_lst.append({
          'x': x_all,
          'y': y_all,
          #'text': ['a', 'b', 'c', 'd'],
          #'customdata': ['c.a', 'c.b', 'c.c', 'c.d'],
          'name': 'All Data',
          'mode': 'markers',
          'marker': {
            'size': 3,
            'color': 'rgba(190, 190, 190, 0.9)' #'rgba(186, 203, 209, 0.7)'   # #dbd4c9
          }
        })

    if x_per is not None:
        data_lst.append({
          'x': x_per,
          'y': y_per,
          'name': str(per) + ' Period',
          'mode': 'markers',
          'marker': {
            'size': 4,
            'color': 'rgba(227, 176, 90, 1.0)'
          }
        })

    if x_reg is not None:
        data_lst.append({
          'x': x_reg,
          'y': y_reg,
          'name': 'Regression Line',
          'type': 'scatter',
          'mode': 'lines',
          'line': {
             'color': 'rgb(68, 122, 219)',
             'width': 1.0
          }
        })

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
        "title": default_sym_title(asset_0, sym_0),
        #"zeroline": False
      },
      "yaxis": {
        "gridcolor": "rgb(255,255,255)",
        "mirror": True,
        #"range": [-11.6745548881, 54.4383879616],
        "showline": True,
        "ticklen": 4,
        "title": default_sym_title(asset_1, sym_1),
        #"zeroline": False
      }
    }

    #fig = go.Figure(data=data_lst, layout=layout)
    fig = {
        'data': data_lst,
        'layout': layout
    }
    return fig


def get_figure_3d_surface_reg(_x, _y, _z, _title):
    data_lst=[]

    trace = dict(
        x = _x,
        y = _y,
        z = _z,
        type = 'surface',
        colorscale = 'Viridis'
    )

    data_lst.append(trace)

    layout = dict(
        title=_title,
        #autosize=False,
        #width=500,
        #height=500,
        #margin=dict(
        #    l=65, r=50, b=65, t=90
        #)
        # xaxis=dict(
        #   autorange='reversed'
        # )
    )
    fig = dict(data=data_lst, layout=layout)

    return fig


def get_figure_acf_pacf(acf_x, pacf_x, title):
    fig = tools.make_subplots(rows=2, cols=1)

    data_lst=[]
    data_lst.append(dict(
        y = acf_x,
        type = 'bar',
        name = 'ACF',
        width=0.4,
        marker = dict(
            color = 'rgba(170, 39, 100, 0.8)',  # 'rgba(170, 39, 40, 0.8)', 'rgba(140, 39, 40, 0.8)',
            #tickfont=dict(
            #    size=14,
            line = dict(
                color = 'rgba(170, 39, 100, 1)',
                width = 1)
        )
    ))

    data_lst.append(dict(
        y = pacf_x,
        type = 'bar',
        name = 'PACF',
        width=0.4,
        marker = dict(
            color = 'rgba(100, 39, 100, 0.8)',
            #tickfont=dict(
            #    size=14,
            line = dict(
                color = 'rgba(100, 39, 100, 1)',
                width = 1)
        )
    ))

    fig.append_trace(data_lst[0], 1, 1)
    fig.append_trace(data_lst[1], 2, 1)
    #fig['layout'].update(height=600, width=800, title='i <3 annotations and subplots')
    fig['layout'].update(title=title)
    fig['layout'].update(yaxis=dict(dtick=0.25))

    return fig

# ==============================================================================

# if __name__ == '__main__':
#     parser = argparse.ArgumentParser()
#     parser.add_argument('-p', action="store", dest="p", nargs=1, default=[PORT])
#     args = parser.parse_args()
#
#     port = int(args.p[0])
#
#     # app.run(host='0.0.0.0', port=80)
#     app.run_server(debug=DEBUG_PLOT, port=port)
