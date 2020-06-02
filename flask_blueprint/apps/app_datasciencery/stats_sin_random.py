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
from scipy import stats

import plotly.graph_objs as go   # Layout, Figure
from plotly import tools
import plotly.figure_factory as ff


def gen_sin_increasing_noise(N=200, trend_sigma=0.2):
    """
    x_vals = np.random.rand(50)
    x_train = np.asarray(x_vals,dtype=np.float32).reshape(-1,1)
    m = 1
    alpha = np.random.rand(1)
    beta = np.random.rand(1)
    y_correct = np.asarray([2*i+m for i in x_vals], dtype=np.float32).reshape(-1,1)
    """
    # x = pd.Series()
    # x = pd.date_range('9/11/2001', periods=N)
    # x = pd.Series()
    # x = pd.date_range('9/11/2001', periods=N)
    x = np.linspace(0, (N/100)*np.pi, N)  # t = ...

    trend_lin = np.arange(N)/(N*.3)
    trend_slow = np.arange(N)/(N*.7)

    # y_sin_trend = np.sin(x*2) + trend_lin
    y_sin_trend_amp = trend_slow*np.sin(x*5) + trend_lin
    y_sin_trend_amp_noise = y_sin_trend_amp + np.random.normal(0, trend_sigma, y_sin_trend_amp.shape)*trend_lin

    df = pd.DataFrame({'x': x, 'y': y_sin_trend_amp, 'y_noise': y_sin_trend_amp_noise})

    return df


def gen_sin_inc_dec_noise(N=200, amp_sigma=1.0, trend_sigma=0.2):
    # x = pd.Series()
    # x = pd.date_range('9/11/2001', periods=N)
    x = np.linspace(0, 2*np.pi, N)  # t = ...

    trend_lin = np.arange(N)/(N*.3)

    # y_sin_trend = np.sin(x*10) + trend_lin
    y_sin_trend_amp = np.random.normal(1, amp_sigma, trend_lin.shape)*np.sin(x*5) + trend_lin
    y_sin_trend_amp_noise = y_sin_trend_amp + np.random.normal(0, trend_sigma, y_sin_trend_amp.shape)*trend_lin

    df = pd.DataFrame({'x': x, 'y': y_sin_trend_amp, 'y_noise': y_sin_trend_amp_noise})

    return df


def get_fig_sin_noise(df):
    ''' Use:
    fig = get_fig_sin_noise(df)

    fig.update(layout=dict(
        title='Sine increasing w noise',
        width=700, height=500
      )
    )
    '''
    data_lst = []
    #data_lst.append({'x': x, 'y': y_trend_lin, 'name':'trend_lin'})
    data_lst.append({'x': df.x, 'y': df.y, 'line':{'dash': 'dash', 'color':'rgba(3, 116, 193, 1.0)', 'width':1.5}, 'name':'y - real'})
    #data_lst.append({'x': x, 'y': y_trend_amp_noise, 'mode': 'markers', 'marker':{'size':4, 'color': 'rgba(255, 127, 14, 0.8)'}, 'name':'trend_amp - observed' })
    data_lst.append({'x': df.x, 'y': df.y_noise, 'line':{'dash': 'dot', 'color': 'rgba(255, 127, 14, 1.0)', 'width':1.5}, 'name':'y - observed' })

    # layout = dict(
    #   title='Sine increasing w noise',
    #   width=700,
    #   height=500
    # )

    fig = go.Figure(data=data_lst) #, layout=layout)
    return fig
