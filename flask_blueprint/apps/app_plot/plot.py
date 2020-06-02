import os, sys, pathlib
from collections import OrderedDict
import datetime
# from dateutil.parser import parse as dateparse
from copy import deepcopy
import math, time

import numpy as np
import pandas as pd
from pandas.tseries.offsets import *
#from pandas.plotting import scatter_matrix
#import pandas.plotting as pdp

import colorlover as cl
# import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="ticks", color_codes=True)

import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.sandbox.regression.predstd import wls_prediction_std
import statsmodels.graphics.api as smg

from sklearn import linear_model, datasets
from scipy import stats as statsci

import torch
import torch.nn as nn
from torch.autograd import Variable

import plotly.graph_objs as go   # Layout, Figure
from plotly import tools
import plotly.figure_factory as ff

from bson.objectid import ObjectId
from apps.app_util import mongodb, col_coin_spec, col_coin_top, \
    col_coin_hist_daily, col_coin_hist_daily2, col_coin_hist_hour, col_coin_hist_min, \
    mongodb_geo, logger_flask

from apps.app_quant import stats
# from .stats import convert_pctcum_np, calc_pct_np

# ==============================================================================

def split_xy(xy) -> pd.core.series.Series:
    if type(xy) == list or type(xy) == tuple or type(xy) == np.ndarray:
        x = xy[0]
        y = xy[1]
        y = pd.Series(y, index=x)
    elif type(xy) == pd.core.frame.DataFrame or type(xy) == pd.core.series.Series:
        x = xy.index
        y = xy
    return x, y

#rgb(0, 127, 186) rgb(1, 126, 183) rgb(1, 126, 183)

def get_figure_obs_pred(xy_real=None,
                        xy_obs=None,
                        xy_train=None,
                        xy_pred=None):
    data_lst = []
    if xy_real:
        x_real, y_real = split_xy(xy_real)

        data_lst.append({
            'x': x_real,
            'y': y_real,
            'line':{'dash': 'dot',
                    'color':'rgba(3, 116, 193, 1.0)',
                    'width':1.5 },
            'name':'Real'
        })

    if xy_obs:
        x_obs, y_obs = split_xy(xy_obs)
        data_lst.append({
            'x': x_obs,
            'y': y_obs,
            #'mode': 'markers',
            #'marker':{'size':4, 'color': 'rgba(255, 127, 14, 0.8)'}, 'name':'trend_amp - observed' })
            'line':{'dash': 'dash',
                    'color': 'rgba(5, 162, 168, 1.0)',  #(9, 186, 198, 1.0)',
                    'width':1.5},
            'name':'Observed'
        })

    if xy_train:
        x_train, y_train = split_xy(xy_train)
        data_lst.append({
            'x': x_train,
            'y': y_train,
            'line':{'color': 'rgba(255, 127, 14, 1.0)',
                    'width':1.5},
            'name':'Train'
        })

    if xy_pred:
        x_pred, y_pred = split_xy(xy_pred)
        data_lst.append({
            'x': x_pred,
            'y': y_pred,
            'line':{'color': 'rgba(198, 55, 11, 1.0)',
                    'width':2},
            'name':'Prediction'
        })

    layout = dict(
        #title=title
        #width=700, height=500,
    )

    fig = go.Figure(data=data_lst, layout=layout)

    return fig


def get_figure_pred_err(xy_obs_real=None,
                        xy_train=None,
                        xy_pred=None):

    x_obs_real, y_obs_real = split_xy(xy_obs_real)
    y_train_err = None
    y_pred_err = None

    if xy_train:
        x_train, y_train = split_xy(xy_train)
        y_train_err = ((y_train - y_obs_real)/y_obs_real)[y_train.index]

    if xy_pred:
        x_pred, y_pred = split_xy(xy_pred)
        y_pred_err = ((y_pred - y_obs_real)/y_obs_real)[y_pred.index]

    data_lst = []
    data_lst.append({
        'x': x_obs_real,
        'y': y_obs_real,
        #'mode': 'markers',
        #'marker':{'size':4, 'color': 'rgba(255, 127, 14, 0.8)'}, 'name':'trend_amp - observed' })
        'line':{'dash': 'dash',
                'color': 'rgba(5, 162, 168, 1.0)',  #(9, 186, 198, 1.0)',
                'width':1.5},
        'name':'Observed'
    })

    if xy_train:
        data_lst.append({
            'x': x_train,
            'y': y_train_err,
            'line':{'color': 'rgba(255, 127, 14, 1.0)',
                    'width':1.5},
            'name':'Train Error'
        })

    if xy_pred:
        x_pred,y_pred = split_xy(xy_pred)
        data_lst.append({
            'x': x_pred,
            'y': y_pred_err,
            'line':{'color': 'rgba(198, 55, 11, 1.0)',
                    'width':1.5},
            'name':'Prediction Error'
        })

    layout = dict(
        #title=title
        #width=700,
        #height=500
    )

    fig = go.Figure(data=data_lst, layout=layout)

    return fig


# ------------------------------------------------------------------------------
# called by api
# ------------------------------------------------------------------------------
def get_coin_names(l_sym):
    l_name = []
    for s in l_sym:
        d_res = col_coin_spec.find_one({'Symbol': s.upper()},{'_id':0})
        l_name.append(d_res['CoinName'])

    # l_name = [col_coin_spec.find_one({'Symbol': s.upper()},{'_id':0})['CoinName'] for s in l_sym]
    return l_name


def get_hist_daily(l_sym, _col_coin_hist_daily = col_coin_hist_daily):
    '''
    params: list of string
    return: numpy.ndarray
    '''
    ###todo try
    l_sym = [x.upper() for x in l_sym]
    l_data_s = _col_coin_hist_daily.find_one({'sym': l_sym[0]},{'hist':1, '_id':0})['hist']

    tot_sym = len(l_sym)
    # pre-allocate
    np_data = np.zeros((len(l_data_s), tot_sym+1))

    i=0
    for d_i in l_data_s:
        np_data[i,0] = d_i['time']  # d_i['dtime'].strftime('%Y-%m-%d')
        np_data[i,1] = d_i['close']
        i+=1

    for s in range(1, tot_sym):
        # try
        sym_s = l_sym[s]
        l_data_s = _col_coin_hist_daily.find_one({'sym': sym_s},{'hist':1, '_id':0})['hist']
        # {'time': 1523923200, 'volumeto': 4030842.13, 'high': 202.7, 'open': 195.27, 'dtime': datetime.datetime(2018, 4, 17, 0, 0), 'volumefrom': 20327.12, 'low': 194.93, 'close': 202.48}
        i=0
        for d_i in l_data_s:
            np_data[i,s+1] = d_i['close']
            i+=1

    return np_data


def get_data_2d_btcusd_sp() -> np.ndarray:
    """to do put in mongo"""
    '''
    ts,btcusd,es
    2010-07-16,0.04951,884.5
    '''
    # pt = '/srv/static/data/'
    path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..', '..', 'data_in'))
    path_file = os.path.abspath(os.path.join(path, 'df_btcusd_es.csv'))

    # f = open(path_file)
    # np_data = np.loadtxt(f, delimiter=',', skiprows=1, dtype={'names': ('ts', 'btcusd', 'es'),'formats': ('S1', 'f4', 'f4')})
    df = pd.read_csv(path_file)
    return df.query('ts>"2013"').values


# @app_quant.route('api/plot/2d_btc_sp')
def get_plot_2d_btc_sp():
    '''
    -> jsonify(
    { 'div': 'div_plot_2d_btcusd_sp',
      'data': traces,
      'layout': layout,
      'config': config
    })
    '''
    np_data = get_data_2d_btcusd_sp()

    #per = 100+1
    #np_data = np_data[np_data.shape[0]-per:np_data.shape[0], :]

    #* np_data = stats.convert_pctcum_np(np_data[:,1:])  # 100x10
    #np_data = np.cumsum(np_data, axis=0)
    # len_data = np_data.shape[0]
    # y_timestamp = y_timestamp[1:]
    # y_num = y_num[1:]
    # y_dtstr = y_dtstr[1:]
    line0 = {
      'x': list(np_data[:, 0]),
      'y': list(np_data[:, 1]),
      'name': 'BTC',
      'type': 'scatter'
    }

    line1 = {
      'x': list(np_data[:, 0]),
      'y': list(np_data[:, 2]),
      'name': 'S&P',
      'yaxis': 'y2',
      'type': 'scatter'
    }

    data = [line0, line1]

    # tickfontsize = 11.5
    layout = {
      #'title':'',
      #showlegend: true,
      #'autosize': True,
      #'automargin': False,
      'margin': {'t':40, 'b': 0, 'l':48, 'r':48},
      #'height': 750,
      #'width': 1000,
      #'automargin': True,
      #'paper_bgcolor': 'rgba(11, 48, 105, 0.2)',  #'rgba(25,25,112, 0.2)','#d6ddf5'
      #'plot_bgcolor': '#2a408e', #'rgba(25,25,112, 0.5)',
      'showlegend': True,
      'legend': {'orientation': 'h'},
      'xaxis': {
        #'title': '',
        #'showticklabels': True,
        #'tickmode': 'array',
        #'tickvals': x_rib,
        #'ticktext': l_top_10_pop_name,
        #'tickfont': {'size':tickfontsize},
        #'ticklen':150,
        #'tickangle'
        #'ticks': 'outside',
        #'margin': {'b': 100, 'l':100, 'r':100, 't':100},
        #'autorange': True,
        #'range': [1, 22]
        'showspikes': True,
        'spikedash': 'solid',
        'spikemode': 'across',
        'spikethickness': 1.0,
      },
      'yaxis': {
        'title': 'BTC',
      },
      'yaxis2': {
         'title': 'S&P',
         #'tickfont': {'size':tickfontsize},
         'tickfont': {'color': 'rgb(250, 166, 6)'},
         'titlefont': {'color': 'rgb(228, 179, 29)'},
         'overlaying': 'y',
         'side': 'right'
         #'range':[min(y_num), max(y_num) + 5]
      }
    }

    config = {'displaylogo': False, 'displayModeBar': False, 'scrollZoom': False }

    d_res = { 'div': 'div_plot_2d_btcusd_sp',
              'data': data,
              'layout': layout,
              'config': config,
              'status_msg': 'ok'
            }

    return d_res
    # return jsonify(d_res)


# @app_quant.route('api/plot/3d_ribbon')
def get_plot_3d_ribbon():
    '''
    -> jsonify(
    { 'div': 'div_',
      'data': traces,
      'layout': layout,
      'config': config
    })

    d = json.load(open('3d-ribbon.json'))
    np.array(d['data']).shape => (7,1)
    d['data'][s].keys() =>
      ['colorscale', 'y', 'xsrc', 'cmax', 'showscale', 'x', 'name', 'z', 'ysrc', 'type', 'uid', 'cmin', 'zsrc']
    d['data'][s]['x'] ==> [[2, 3], [2, 3], ... 401 times]
    d['data'][s]['y'] ==> [[800, 800], [799, 799], ..., [400, 400]]
    d['data'][s]['z'] ==> [[0.891326202, 0.891326202], [0.888733027, 0.888733027], ..., [1.561837233, 1.561837233]]
    d['data'][s]['colorscale'] ==> [['0', 'rgb(31,31,255)'], ['0.1', 'rgb(31,31,255)'], ['0.2', 'rgb(31,31,255)'], ['0.3', 'rgb(31,31,255)'], ['0.4', 'rgb(31,31,255)'], ['0.5', 'rgb(31,31,255)'], ['0.6', 'rgb(31,31,255)'], ['0.7', 'rgb(31,31,255)'], ['0.8', 'rgb(31,31,255)'], ['0.9', 'rgb(31,31,255)'], ['1', 'rgb(31,31,255)']]

    f = open('/static/data/3d-ribbon.csv')
    np_data = np.loadtxt(f, delimiter=',')
    '''
    l_top_10_pop = col_coin_top.find_one({'top_10_pop': {'$exists': True}},{'_id':0})['top_10_pop']
    l_top_10_pop = l_top_10_pop[::-1]
    l_top_10_pop_name = get_coin_names(l_top_10_pop)
    l_top_10_pop_name = ['Bitcoin Cash' if x == 'Bitcoin Cash / BCC' else x for x in l_top_10_pop_name]

    np_data = get_hist_daily(l_top_10_pop)

    per = 100+1
    np_data = np_data[np_data.shape[0]-per:np_data.shape[0], :]

    tot_sym = np_data.shape[1]-1    # if np_data.shape[1]-1 => range(1, tot_sym+1)

    y_timestamp = np_data[:, 0]
    y_num = list(range(1,len(y_timestamp)+1))
    # list(map(lambda x: x**2, items))
    y_dtstr = list(map(lambda x: datetime.datetime.utcfromtimestamp(x).strftime('%Y-%m-%d'), y_timestamp))
    # x_rib = [[s*2+1, s*2+2] for s in range(0, tot_sym)]    # [[1,2], [3,4], ... ]
    # x_rib_mid = list(map(lambda x: (x[0]+x[1])/2, x_rib))
    x_rib = list(range(1,tot_sym*2, 2))

    np_data = stats.convert_pctcum_np(np_data[:,1:])  # 100x10
    #np_data = np.cumsum(np_data, axis=0)
    len_data = np_data.shape[0]

    y_timestamp = y_timestamp[1:]
    y_num = y_num[1:]
    y_dtstr = y_dtstr[1:]

    traces = []
    for s in range(0, tot_sym):
        z_raw_s = np_data[:, s]*100
        x_s = []
        y_s = []
        z_s = []

        for i in range(0, len_data):
            z_s.append([z_raw_s[i], z_raw_s[i]])
            #y_s.append([y_num[i], y_num[i]])
            y_s.append([y_dtstr[i], y_dtstr[i]])
            x_s.append([s*2, s*2+1])

        traces.append(dict(
            z=z_s,
            x=x_s,
            y=y_s,
            name = l_top_10_pop_name[s],
            #colorscale = PLOT_COLORSCALES_SOLID[s],
            #ci = int(255/tot_sym*s)  # ci = "color index"
            colorscale = [ [i, 'rgb(%d,%d, 255)'%(int(255/tot_sym*s),int(255/tot_sym*s))] for i in np.arange(0, 2, 0.1) ],
            showscale=False,
            type='surface',
            # opacity=0.7
            hoverinfo='text',
            text = [ [ l_top_10_pop_name[s]+'<br>' + _y_i + ': ' + '{:.2f}'.format(_z_i)+'%', l_top_10_pop_name[s]+'<br>' + _y_i + ': ' + '{:.2f}'.format(_z_i)+'%']
                     for _y_i, _z_i in zip(y_dtstr, z_raw_s) ]
            #text=[['{:.2f}'.format(x[j])+'<br>'+'{:.2f}'.format(y[i])+'<br>'+'{:.2f}'.format(z[i,j])
            #        for j in range(n_cols)] for i in range(n_rows)],
            # where x, y are lists or np.arrays of shape (n_cols,), (n_rows,)
            # and z is a list of lists or a np.array of shape (n_rows, n_cols)
        ))

    tickfontsize = 11.5
    layout = {
      'title':'Returns For Last 100 Days',
      #showlegend: true,
      'autosize': True,
      'margin': {'t':60, 'b': 40, 'l':0, 'r':0},
      'height': 750,
      #'width': 1000,
      #'automargin': True,
      #'paper_bgcolor': 'rgba(11, 48, 105, 0.2)',  #'rgba(25,25,112, 0.2)','#d6ddf5'
      #'plot_bgcolor': '#2a408e', #'rgba(25,25,112, 0.5)',
      'scene': {
        'aspectmode': "manual",
        'aspectratio': dict( x = 1.1, y = 1.1, z = 0.75),  #{'x':10, 'y':5, 'z':5},
        #'width': 500,
        'automargin': False,
        'xaxis': {
          'title': '',  #Top 10 Coins',
          'showticklabels': True,
          'tickmode': 'array',
          'tickvals': x_rib,
          'ticktext': l_top_10_pop_name,
          'tickfont': {'size':tickfontsize},
          #'ticklen':150,
          'ticks': 'outside',
          #'margin': {'b': 100, 'l':100, 'r':100, 't':100},
          #'autorange': True,
          'range': [1, 22]
        },
        'yaxis': {
          'title': '',
          'type': 'category',  #'date',
          #'tickangle': ,
          #'ticklen': 0,
          'tickfont': {'size':tickfontsize},
          'range':[min(y_num), max(y_num) + 5]
        },
        'zaxis': {
          'title': 'Return',
          'tickfont': {'size':tickfontsize},
          'ticksuffix': '%',
        }
      }
    }

    config = {'displaylogo': False, 'displayModeBar': False}

    d_res = { 'data': traces,
              'layout': layout,
              'config': config
            }

    return d_res
    #return jsonify(d_res)

# @app_quant.route('api/plot/3d_ribbon_demo')
def get_plot_3d_ribbon_demo():
    '''
    -> jsonify(
    { 'div': 'div_',
      'data': traces,
      'layout': layout,
      'config': config
    })
    '''
    l_top_10_pop = col_coin_top.find_one({'top_10_pop': {'$exists': True}},{'_id':0})['top_10_pop']
    l_top_10_pop = l_top_10_pop[::-1]
    l_top_10_pop_name = get_coin_names(l_top_10_pop)
    l_top_10_pop_name = ['Bitcoin Cash' if x == 'Bitcoin Cash / BCC' else x for x in l_top_10_pop_name]

    np_data = get_hist_daily(l_top_10_pop, _col_coin_hist_daily = col_coin_hist_daily2)

    per = 100+1
    np_data = np_data[np_data.shape[0]-per:np_data.shape[0], :]

    tot_sym = np_data.shape[1]-1    # if np_data.shape[1]-1 => range(1, tot_sym+1)

    y_timestamp = np_data[:, 0]
    y_num = list(range(1,len(y_timestamp)+1))
    # list(map(lambda x: x**2, items))
    y_dtstr = list(map(lambda x: datetime.datetime.utcfromtimestamp(x).strftime('%Y-%m-%d'), y_timestamp))
    # x_rib = [[s*2+1, s*2+2] for s in range(0, tot_sym)]    # [[1,2], [3,4], ... ]
    # x_rib_mid = list(map(lambda x: (x[0]+x[1])/2, x_rib))
    x_rib = list(range(1,tot_sym*2, 2))

    np_data = stats.convert_pctcum_np(np_data[:,1:])  # 100x10
    #np_data = np.cumsum(np_data, axis=0)
    len_data = np_data.shape[0]

    y_timestamp = y_timestamp[1:]
    y_num = y_num[1:]
    y_dtstr = y_dtstr[1:]

    traces = []
    for s in range(0, tot_sym):
        z_raw_s = np_data[:, s]*100
        x_s = []
        y_s = []
        z_s = []

        for i in range(0, len_data):
            z_s.append([z_raw_s[i], z_raw_s[i]])
            #y_s.append([y_num[i], y_num[i]])
            y_s.append([y_dtstr[i], y_dtstr[i]])
            x_s.append([s*2, s*2+1])

        traces.append(dict(
            z=z_s,
            x=x_s,
            y=y_s,
            name = l_top_10_pop_name[s],
            #colorscale = PLOT_COLORSCALES_SOLID[s],
            #ci = int(255/tot_sym*s)  # ci = "color index"
            colorscale = [ [i, 'rgb(%d,%d, 255)'%(int(255/tot_sym*s),int(255/tot_sym*s))] for i in np.arange(0, 2, 0.1) ],
            showscale=False,
            type='surface',
            # opacity=0.7
            hoverinfo='text',
            text = [ [ l_top_10_pop_name[s]+'<br>' + _y_i + ': ' + '{:.2f}'.format(_z_i)+'%', l_top_10_pop_name[s]+'<br>' + _y_i + ': ' + '{:.2f}'.format(_z_i)+'%']
                     for _y_i, _z_i in zip(y_dtstr, z_raw_s) ]
            #text=[['{:.2f}'.format(x[j])+'<br>'+'{:.2f}'.format(y[i])+'<br>'+'{:.2f}'.format(z[i,j])
            #        for j in range(n_cols)] for i in range(n_rows)],
            # where x, y are lists or np.arrays of shape (n_cols,), (n_rows,)
            # and z is a list of lists or a np.array of shape (n_rows, n_cols)
        ))

    tickfontsize = 11.5
    layout = {
      #'title':'Returns For Last 100 Days',
      #showlegend: true,
      'autosize': True,
      'margin': {'t':0, 'b': 10, 'l':5, 'r':5},
      'height': 700,
      #'width': 1000,
      #'automargin': True,
      #'paper_bgcolor': 'rgba(11, 48, 105, 0.2)',  #'rgba(25,25,112, 0.2)','#d6ddf5'
      #'plot_bgcolor': '#2a408e', #'rgba(25,25,112, 0.5)',
      'scene': {
        'aspectmode': "manual",
        'aspectratio': dict( x = 1.1, y = 1.1, z = 0.75),  #{'x':10, 'y':5, 'z':5},
        #'width': 500,
        'automargin': False,
        'xaxis': {
          'title': '',  #Top 10 Coins',
          'showticklabels': True,
          'tickmode': 'array',
          'tickvals': x_rib,
          'ticktext': l_top_10_pop_name,
          'tickfont': {'size':tickfontsize},
          #'ticklen':150,
          'ticks': 'outside',
          #'margin': {'b': 100, 'l':100, 'r':100, 't':100},
          #'autorange': True,
          'range': [1, 22]
        },
        'yaxis': {
          'title': '',
          'type': 'category',  #'date',
          #'tickangle': ,
          #'ticklen': 0,
          'tickfont': {'size':tickfontsize},
          'range':[min(y_num), max(y_num) + 5]
        },
        'zaxis': {
          'title': 'Return',
          'tickfont': {'size':tickfontsize},
          'ticksuffix': '%',
        }
      }
    }

    config = {'displaylogo': False, 'displayModeBar': False}

    d_res = { 'data': traces,
              'layout': layout,
              'config': config
            }

    return d_res
    # return jsonify(d_res)


# @app_quant.route('api/plot/3d_volatility')
def get_plot_3d_volatility():
    '''
    -> jsonify(
      { 'div': 'div_plot_2d_btcusd_sp',
        'data': traces,
        'layout': layout,
        'config': config
      })
    '''
    l_top_10_pop = col_coin_top.find_one({'top_10_pop': {'$exists': True}},{'_id':0})['top_10_pop']
    l_top_10_pop = l_top_10_pop[::-1]
    l_top_10_pop_name = get_coin_names(l_top_10_pop)
    l_top_10_pop_name = ['Bitcoin Cash' if x == 'Bitcoin Cash / BCC' else x for x in l_top_10_pop_name]

    np_data = get_hist_daily(l_top_10_pop)

    per = 100+1
    np_data = np_data[np_data.shape[0]-per:np_data.shape[0], :]

    tot_sym = np_data.shape[1]-1    # if np_data.shape[1]-1 => range(1, tot_sym+1)

    y_timestamp = np_data[:, 0]
    y_num = list(range(1,len(y_timestamp)+1))
    # list(map(lambda x: x**2, items))
    y_dtstr = list(map(lambda x: datetime.datetime.utcfromtimestamp(x).strftime('%Y-%m-%d'), y_timestamp))
    # x_rib = [[s*2+1, s*2+2] for s in range(0, tot_sym)]    # [[1,2], [3,4], ... ]
    # x_rib_mid = list(map(lambda x: (x[0]+x[1])/2, x_rib))
    x_rib = list(range(1,tot_sym*2, 2))

    np_data = stats.calc_pct_np(np_data[:,1:])  # 100x10
    # np_data = np.cumsum(np_data, axis=0)
    len_data = np_data.shape[0]

    y_timestamp = y_timestamp[1:]
    y_num = y_num[1:]
    y_dtstr = y_dtstr[1:]

    traces = []
    for s in range(0, tot_sym):
        z_raw_s = np_data[:, s]*100
        x_s = []
        y_s = []
        z_s = []

        for i in range(0, len_data):
            z_s.append([z_raw_s[i], z_raw_s[i]])
            #y_s.append([y_num[i], y_num[i]])
            y_s.append([y_dtstr[i], y_dtstr[i]])
            x_s.append([s*2, s*2+1])

        traces.append(dict(
            z=z_s,
            x=x_s,
            y=y_s,
            name = l_top_10_pop_name[s],
            #colorscale = PLOT_COLORSCALES_SOLID[s],
            #ci = int(255/tot_sym*s)  # ci = "color index"
            colorscale = [ [i, 'rgb(%d,%d, 255)'%(int(255/tot_sym*s),int(255/tot_sym*s))] for i in np.arange(0, 2, 0.1) ],
            showscale=False,
            type='surface',
            # opacity=0.7
            hoverinfo='text',
            text = [ [ l_top_10_pop_name[s]+'<br>' + _y_i + ': ' + '{:.2f}'.format(_z_i)+'%', l_top_10_pop_name[s]+'<br>' + _y_i + ': ' + '{:.2f}'.format(_z_i)+'%']
                     for _y_i, _z_i in zip(y_dtstr, z_raw_s) ]
            #text=[['{:.2f}'.format(x[j])+'<br>'+'{:.2f}'.format(y[i])+'<br>'+'{:.2f}'.format(z[i,j])
            #        for j in range(n_cols)] for i in range(n_rows)],
            # where x, y are lists or np.arrays of shape (n_cols,), (n_rows,)
            # and z is a list of lists or a np.array of shape (n_rows, n_cols)
        ))

    tickfontsize = 11.5
    layout = {
      'title':'Volatility - Last 100 Days',
      #showlegend: true,
      'autosize': True,
      'height': 700,
      #'width': 1000,
      'margin': {'t':60, 'b': 40, 'l':0, 'r':0},
      'automargin': False,
      'scene': {
        'aspectmode': "manual",
        'aspectratio': dict( x = 1.3, y = 1.1, z = 0.7),  #{'x':10, 'y':5, 'z':5},

        'xaxis': {
          'title': '',  #Top 10 Coins',
          'showticklabels': True,
          'tickmode': 'array',
          'tickvals': x_rib,
          'ticktext': l_top_10_pop_name,
          'tickfont': {'size':tickfontsize},
          #'ticklen':150,
          #'autorange': True,
          'ticks': 'outside',
          #'margin': {'b': 100, 'l':100, 'r':100, 't':100},
          'range': [1, 23]
        },
        'yaxis': {
          'title': '',
          'type': 'category',  #'date',
          #'tickangle': ,
          'tickfont': {'size':tickfontsize},
          'range':[min(y_num), max(y_num) + 5]
        },
        'zaxis': {
          'title': 'Return',
          'tickfont': {'size':tickfontsize},
          'ticksuffix': '%',
        }
      }
    }

    config = {'displaylogo': False, 'displayModeBar': False}

    d_res = { 'div': 'div_plot_3d_volatility',
              'data': traces,
              'layout': layout,
              'config': config
            }

    return d_res
    # return jsonify(d_res)


#@app_quant.route('api/plot/3d_scatter_crypto_sp_')
def get_plot_3d_scatter_crypto_sp_():
#@app_quant.route('api/plot/3d_scatter_crypto_sp_time')
#def api_plot_3d_scatter_crypto_sp_time():
    '''
    Need to get into shape:
    { 'div':
      'data':
      'layout':
      'config';
    }

    d = json.load(open('3d-ribbon.json'))
    np.array(d['data']).shape => (7,1)
    d['data'][s].keys() =>
      ['colorscale', 'y', 'xsrc', 'cmax', 'showscale', 'x', 'name', 'z', 'ysrc', 'type', 'uid', 'cmin', 'zsrc']
    d['data'][s]['x'] ==> [[2, 3], [2, 3], ... 401 times]
    d['data'][s]['y'] ==> [[800, 800], [799, 799], ..., [400, 400]]
    d['data'][s]['z'] ==> [[0.891326202, 0.891326202], [0.888733027, 0.888733027], ..., [1.561837233, 1.561837233]]
    d['data'][s]['colorscale'] ==> [['0', 'rgb(31,31,255)'], ['0.1', 'rgb(31,31,255)'], ['0.2', 'rgb(31,31,255)'], ['0.3', 'rgb(31,31,255)'], ['0.4', 'rgb(31,31,255)'], ['0.5', 'rgb(31,31,255)'], ['0.6', 'rgb(31,31,255)'], ['0.7', 'rgb(31,31,255)'], ['0.8', 'rgb(31,31,255)'], ['0.9', 'rgb(31,31,255)'], ['1', 'rgb(31,31,255)']]

    '''
    l_top_10_pop = col_coin_top.find_one({'top_10_pop': {'$exists': True}},{'_id':0})['top_10_pop']
    l_top_10_pop = l_top_10_pop[::-1]
    l_top_10_pop_name = get_coin_names(l_top_10_pop)
    l_top_10_pop_name = ['Bitcoin Cash' if x == 'Bitcoin Cash / BCC' else x for x in l_top_10_pop_name]

    np_data = get_hist_daily(l_top_10_pop)

    per = 100+1
    np_data = np_data[np_data.shape[0]-per:np_data.shape[0], :]

    tot_sym = np_data.shape[1]-1    # if np_data.shape[1]-1 => range(1, tot_sym+1)

    y_timestamp = np_data[:, 0]
    y_num = list(range(1,len(y_timestamp)+1))
    # list(map(lambda x: x**2, items))
    y_dtstr = list(map(lambda x: datetime.datetime.utcfromtimestamp(x).strftime('%Y-%m-%d'), y_timestamp))
    # x_rib = [[s*2+1, s*2+2] for s in range(0, tot_sym)]    # [[1,2], [3,4], ... ]
    # x_rib_mid = list(map(lambda x: (x[0]+x[1])/2, x_rib))
    x_rib = list(range(1,tot_sym*2, 2))

    np_data = stats.calc_pct_np(np_data[:,1:])  # 100x10
    # np_data = np.cumsum(np_data, axis=0)
    len_data = np_data.shape[0]

    y_timestamp = y_timestamp[1:]
    y_num = y_num[1:]
    y_dtstr = y_dtstr[1:]

    traces = []
    for s in range(0, tot_sym):
        z_raw_s = np_data[:, s]*100
        x_s = []
        y_s = []
        z_s = []

        for i in range(0, len_data):
            z_s.append([z_raw_s[i], z_raw_s[i]])
            #y_s.append([y_num[i], y_num[i]])
            y_s.append([y_dtstr[i], y_dtstr[i]])
            x_s.append([s*2, s*2+1])

        traces.append(dict(
            z=z_s,
            x=x_s,
            y=y_s,
            name = l_top_10_pop_name[s],
            #colorscale = PLOT_COLORSCALES_SOLID[s],
            #ci = int(255/tot_sym*s)  # ci = "color index"
            colorscale = [ [i, 'rgb(%d,%d, 255)'%(int(255/tot_sym*s),int(255/tot_sym*s))] for i in np.arange(0, 2, 0.1) ],
            showscale=False,
            type='surface',
            # opacity=0.7
            hoverinfo='text',
            text = [ [ l_top_10_pop_name[s]+'<br>' + _y_i + ': ' + '{:.2f}'.format(_z_i)+'%', l_top_10_pop_name[s]+'<br>' + _y_i + ': ' + '{:.2f}'.format(_z_i)+'%']
                     for _y_i, _z_i in zip(y_dtstr, z_raw_s) ]
            #text=[['{:.2f}'.format(x[j])+'<br>'+'{:.2f}'.format(y[i])+'<br>'+'{:.2f}'.format(z[i,j])
            #        for j in range(n_cols)] for i in range(n_rows)],
            # where x, y are lists or np.arrays of shape (n_cols,), (n_rows,)
            # and z is a list of lists or a np.array of shape (n_rows, n_cols)
        ))

    tickfontsize = 11.5
    layout = {
      'title':'Volatility For Last 100 Days',
      #showlegend: true,
      'autosize': True,
      'height': 700,
      #'width': 1000,
      'margin': {'t':60, 'b': 40, 'l':0, 'r':0},
      'automargin': False,
      'scene': {
        'aspectmode': "manual",
        'aspectratio': dict( x = 1.3, y = 1.1, z = 0.7),  #{'x':10, 'y':5, 'z':5},

        'xaxis': {
          'title': '',  #Top 10 Coins',
          'showticklabels': True,
          'tickmode': 'array',
          'tickvals': x_rib,
          'ticktext': l_top_10_pop_name,
          'tickfont': {'size':tickfontsize},
          #'ticklen':150,
          #'autorange': True,
          'ticks': 'outside',
          #'margin': {'b': 100, 'l':100, 'r':100, 't':100},
          'range': [1, 23]
        },
        'yaxis': {
          'title': '',
          'type': 'category',  #'date',
          #'tickangle': ,
          'tickfont': {'size':tickfontsize},
          'range':[min(y_num), max(y_num) + 5]
        },
        'zaxis': {
          'title': 'Return',
          'tickfont': {'size':tickfontsize},
          'ticksuffix': '%',
        }
      }
    }

    config = {'displaylogo': False, 'displayModeBar': False}

    d_res = { 'div': 'div_plot_3d_volatility',
              'data': traces,
              'layout': layout,
              'config': config
            }

    return d_res
    #return jsonify(d_res)


# ==============================================================================
# ==============================================================================
# ==============================================================================
