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
# import seaborn as sns
# # sns.set(style="ticks", color_codes=True)

from scipy.spatial import Delaunay as sci_Delaunay

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

from apps.app_quant.strategy import *
from apps.app_quant.stats_regression import *
#import apps.app_plot.plot as plot
from . import plot


"""
# ==============================================================================
# Scatter + Histogram
# ==============================================================================
"""

app_threed = dash.Dash(server=app, url_base_pathname='/_' + PLOT_ROUTES['threed'])

#app_threed.server.config.from_pyfile('../settings/settings_pair.py')

app_threed.title = "QuantCypher - Data Visualization"
app_threed.config.supress_callback_exceptions = True
app_threed.css.config.serve_locally = True
app_threed.scripts.config.serve_locally = True

css_external = ["dash.css"] #,
                #"https://codepen.io/chriddyp/pen/bWLwgP.css",
                #"https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"]

js_external = []

for css in css_external:
   app_threed.css.append_css({"external_url": css})
#app.server.static_folder = 'static'  # if you run app.py from 'root-dir-name' you don't need to specify.

# @app.server.route('/static/<path:path>')

@app_threed.server.route('/static/<path:path>')
def static_file_threed(path):
    """
    static_folder = os.path.join(os.getcwd(), 'static')
    return send_from_directory(static_folder, path)

    -- app.py
    -- static/stylesheet.css
    """
    return app_threed.send_from_directory('/srv/', path)

for js in js_external:
    app_threed.scripts.append_script({"external_url": js})

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
app_threed.layout = html.Div(style={'marginTop':0, 'marginLeft':'45px','marginRight':'40px','paddingRight':'40px'}, children=[
    html.Link(
      rel='stylesheet',
      href='/static/css/dash.css'
    ),

    html.Div(style={'marginTop':-25, 'paddingTop':1, 'paddingRight':20, 'paddingBottom':7}, children=[
      html.H3(style={'textAlign': 'center', 'color':'rgba(67,67,67,1.0)'}, children='Reactive Data Visualization'),
      html.H4(style={'textAlign': 'center', 'marginBottom':2, 'paddingBottom':11, 'color':'rgba(78,78,78,1.0)'}, children='Scatter and Histogram'),
      #html.H5(style={'textAlign': 'center', 'marginTop':'-5.9', 'color':'rgba(78,78,78,1.0)', 'marginBottom':2, 'paddingBottom':11 }, children='Pairs Analysis for Intra- and Inter-Assets'),
    ]),

    html.Div(style={'backgroundColor': 'rgb(245, 245, 250)', 'color':'rgba(67,67,67,1.0)', 'marginBottom':20}, children=[
      html.P(style={'paddingTop':'8', 'paddingLeft':'8', 'paddingRight':'8'}, children='3-D charts convey much more powerful information than 2-D charts. Many more features can be visualized, and more clearly, from 3 to even 6 variables all at once.'),
      html.P(style={'marginTop':-7, 'paddingLeft':'8', 'paddingRight':'8'}, children='Metric distances between features, which can be difficult to visualize in 2D, can be more easily grasped in 3D.'),

      html.P(style={'paddingTop':'8', 'paddingLeft':'8'}, children='All 3-D graphs can be rotated by clicking and holding down. To zoom in, use scrolling.'),
      html.P(style={'paddingLeft':'8', 'marginTop':-7}, children='Double click on any legend item to show only that specific data series and hide all others.'),
      html.P(style={'paddingLeft':'8','paddingBottom':8, 'marginTop':-7}, children='Click once on any legend item to hide that data series.'),
    ]),

    html.Div(id='div_graph_3d_scatter', style={'border': 'thin lightgrey solid', 'marginBottom':4}, children=[
      dcc.Graph(id='graph_3d_scatter', config={'displayModeBar': False})
    ]),

    html.Div(id='div_graph_3d_ribbon', style={'border': 'thin lightgrey solid', 'marginBottom':4}, children=[
      html.Iframe(style={'height':750, 'width':'100%', 'paddingTop':-100, 'scrolling':'no', 'border':'none'},
                  src="//quantcypher.com/demo/dia/3d_ribbon_demo")
    ]),

    html.Div(id='div_graph_3d_scatter_size', style={'border': 'thin lightgrey solid', 'marginBottom':4}, children=[
      dcc.Graph(id='graph_3d_scatter_size', config={'displayModeBar': False})
    ]),

    html.Div(id='div_graph_3d_line', style={'border': 'thin lightgrey solid', 'marginBottom':4}, children=[
      dcc.Graph(id='graph_3d_line', config={'displayModeBar': False})
    ]),

    html.Div(id='div_graph_3d_line_mesh', style={'border': 'thin lightgrey solid', 'marginBottom':4}, children=[
      dcc.Graph(id='graph_3d_line_mesh', config={'displayModeBar': False})
    ]),

    html.Div(id='div_graph_3d_surface', style={'border': 'thin lightgrey solid', 'marginBottom':4}, children=[
      dcc.Graph(id='graph_3d_surface', config={'displayModeBar': False})
    ]),

    html.Div(id='div_graph_3d_surface_multiple', style={'border': 'thin lightgrey solid', 'marginBottom':4}, children=[
      dcc.Graph(id='graph_3d_surface_multiple', config={'displayModeBar': False})
    ]),

    html.Div(id='div_graph_3d_surface_projection', style={'border': 'thin lightgrey solid', 'marginBottom':4}, children=[
      dcc.Graph(id='graph_3d_surface_projection', config={'displayModeBar': False})
    ]),

    html.Div(id='div_graph_3d_surface_torus', style={'border': 'thin lightgrey solid', 'marginBottom':4}, children=[
      dcc.Graph(id='graph_3d_surface_torus', config={'displayModeBar': False})
    ]),

    html.Div(id='div_graph_3d_surface_mobius', style={'border': 'thin lightgrey solid', 'marginBottom':4}, children=[
      dcc.Graph(id='graph_3d_surface_mobius', config={'displayModeBar': False})
    ]),

])  # end page layout


# ==============================================================================
# callbacks
# ==============================================================================

@app_threed.callback(Output('graph_3d_scatter', 'figure'),
    [ Input('graph_3d_scatter', 'children')
    ])
def graph_3d_scatter(foo):
    x, y, z = np.random.multivariate_normal(np.array([0,0,0]), np.eye(3), 400).transpose()

    trace1 = go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode='markers',
        marker=dict(
            size=5,
            color=z,                # set color to an array/list of desired values
            colorscale='Viridis',   # choose a colorscale
            opacity=0.8
        )
    )

    data = [trace1]
    layout = go.Layout(
        title='3D Scatter Plot of Different Classes of Data',
        margin=dict(
            t=90, l=0, r=0, b=0
        )
    )
    fig = go.Figure(data=data, layout=layout)

    #fig['layout'].update()
    return fig


@app_threed.callback(Output('graph_3d_scatter_size', 'figure'),
    [ Input('graph_3d_scatter_size', 'children')
    ])
def graph_3d_scatter_size(foo):

    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

    trace1 = go.Scatter3d(
        x=df['year'][750:1500],
        y=df['continent'][750:1500],
        z=df['pop'][750:1500],
        text=df['country'][750:1500],
        mode='markers',
        marker=dict(
            sizemode='diameter',
            sizeref=750,
            size=df['gdpPercap'][750:1500],
            color = df['lifeExp'][750:1500],
            colorscale = 'Viridis',
            colorbar = dict(title = 'Life<br>Expectancy'),
            line=dict(color='rgb(140, 140, 170)')
        )
    )

    data=[trace1]
    layout=dict(title='Examining Population and Life Expectancy Over Time')
    fig=dict(data=data, layout=layout)

    return fig


@app_threed.callback(Output('graph_3d_line', 'figure'),
    [ Input('graph_3d_line', 'children')
    ])
def graph_3d_line(foo):

    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/iris.csv')
    df.head()

    def brownian_motion(T = 1, N = 100, mu = 0.1, sigma = 0.01, S0 = 20):
        dt = float(T)/N
        t = np.linspace(0, T, N)
        W = np.random.standard_normal(size = N)
        W = np.cumsum(W)*np.sqrt(dt) # standard brownian motion
        X = (mu-0.5*sigma**2)*t + sigma*W
        S = S0*np.exp(X) # geometric brownian motion
        return S

    dates = pd.date_range('2012-01-01', '2013-02-22')
    T = (dates.max()-dates.min()).days / 365
    N = dates.size
    start_price = 100
    y = pd.Series(
        brownian_motion(T, N, sigma=0.1, S0=start_price), index=dates)
    z = pd.Series(
        brownian_motion(T, N, sigma=0.1, S0=start_price), index=dates)

    trace = go.Scatter3d(
        x=dates, y=y, z=z,
        marker=dict(
            size=4,
            color=z,
            colorscale='Viridis',
        ),
        line=dict(
            color='#1f77b4',
            width=1
        )
    )

    data = [trace]

    layout = dict(
        width=750,
        height=700,
        autosize=True,
        title='Path in 3 Feature Space',
        scene=dict(
            xaxis=dict(
                gridcolor='rgb(255, 255, 255)',
                zerolinecolor='rgb(255, 255, 255)',
                showbackground=True,
                backgroundcolor='rgb(230, 230,230)'
            ),
            yaxis=dict(
                gridcolor='rgb(255, 255, 255)',
                zerolinecolor='rgb(255, 255, 255)',
                showbackground=True,
                backgroundcolor='rgb(230, 230,230)'
            ),
            zaxis=dict(
                gridcolor='rgb(255, 255, 255)',
                zerolinecolor='rgb(255, 255, 255)',
                showbackground=True,
                backgroundcolor='rgb(230, 230,230)'
            ),
            camera=dict(
                up=dict(
                    x=0,
                    y=0,
                    z=1
                ),
                eye=dict(
                    x=-1.7428,
                    y=1.0707,
                    z=0.7100,
                )
            ),
            aspectratio = dict( x=1, y=1, z=0.7 ),
            aspectmode = 'manual'
        ),
    )

    fig = dict(data=data, layout=layout)
    return fig


@app_threed.callback(Output('graph_3d_line_mesh', 'figure'),
    [ Input('graph_3d_line_mesh', 'children')
    ])
def graph_3d_line_mesh(foo):
    # Cluster graph

    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/iris.csv')
    df.head()

    data = []
    clusters = []
    colors = ['rgb(228,26,28)','rgb(55,126,184)','rgb(77,175,74)']

    for i in range(len(df['Name'].unique())):
        name = df['Name'].unique()[i]
        color = colors[i]
        x = df[ df['Name'] == name ]['SepalLength']
        y = df[ df['Name'] == name ]['SepalWidth']
        z = df[ df['Name'] == name ]['PetalLength']

        trace = dict(
            name = name,
            x = x, y = y, z = z,
            type = "scatter3d",
            mode = 'markers',
            marker = dict( size=3, color=color, line=dict(width=0) ) )
        data.append( trace )

        cluster = dict(
            color = color,
            opacity = 0.3,
            type = "mesh3d",
            x = x, y = y, z = z )
        data.append( cluster )

    layout = dict(
        width=750,
        height=600,
        autosize=True,
        title='Cluster',
        scene=dict(
            xaxis=dict(
                gridcolor='rgb(255, 255, 255)',
                zerolinecolor='rgb(255, 255, 255)',
                showbackground=True,
                backgroundcolor='rgb(230, 230,230)'
            ),
            yaxis=dict(
                gridcolor='rgb(255, 255, 255)',
                zerolinecolor='rgb(255, 255, 255)',
                showbackground=True,
                backgroundcolor='rgb(230, 230, 230)'
            ),
            zaxis=dict(
                gridcolor='rgb(255, 255, 255)',
                zerolinecolor='rgb(255, 255, 255)',
                showbackground=True,
                backgroundcolor='rgb(230, 230, 230)'
            ),
            aspectratio = dict( x=1, y=1, z=0.7 ),
            aspectmode = 'manual'
        ),
    )

    fig = dict(data=data, layout=layout)
    return fig


@app_threed.callback(Output('graph_3d_surface', 'figure'),
    [ Input('graph_3d_surface', 'children')
    ])
def graph_3d_surface(foo):
    z_data = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/api_docs/mt_bruno_elevation.csv')

    data = [
      #go.Surface(
      #    z=z_data.values  #.as_matrix()
      #)
      { 'z': z_data.values,
        'type': 'surface'

      }
    ]

    layout = dict(    #go.Layout(
        title='Surface Plot',
        autosize=False,
        #width=500,
        height=600,
        margin=dict(
            l=65,
            r=50,
            b=65,
            t=90
        )
    )
    fig = go.Figure(data=data, layout=layout)
    return fig


@app_threed.callback(Output('graph_3d_surface_multiple', 'figure'),
    [ Input('graph_3d_surface_multiple', 'children')
    ])
def graph_3d_surface_multiple(foo):
    z1 = [
        [8.83,8.89,8.81,8.87,8.9,8.87],
        [8.89,8.94,8.85,8.94,8.96,8.92],
        [8.84,8.9,8.82,8.92,8.93,8.91],
        [8.79,8.85,8.79,8.9,8.94,8.92],
        [8.79,8.88,8.81,8.9,8.95,8.92],
        [8.8,8.82,8.78,8.91,8.94,8.92],
        [8.75,8.78,8.77,8.91,8.95,8.92],
        [8.8,8.8,8.77,8.91,8.95,8.94],
        [8.74,8.81,8.76,8.93,8.98,8.99],
        [8.89,8.99,8.92,9.1,9.13,9.11],
        [8.97,8.97,8.91,9.09,9.11,9.11],
        [9.04,9.08,9.05,9.25,9.28,9.27],
        [9,9.01,9,9.2,9.23,9.2],
        [8.99,8.99,8.98,9.18,9.2,9.19],
        [8.93,8.97,8.97,9.18,9.2,9.18]
    ]

    z2 = [[zij+1 for zij in zi] for zi in z1]
    z3 = [[zij-1 for zij in zi] for zi in z1]

    data = [
        go.Surface(z=z1),
        go.Surface(z=z2, showscale=False, opacity=0.9),
        go.Surface(z=z3, showscale=False, opacity=0.9)
    ]

    fig = go.Figure(data=data)
    fig.update(layout=dict(title="Multiple Surface Plot", height=700))
    return fig


@app_threed.callback(Output('graph_3d_surface_projection', 'figure'),
    [ Input('graph_3d_surface_projection', 'children')
    ])
def graph_3d_surface_projection(foo):
    xx=np.linspace(-3.5, 3.5, 100)
    yy=np.linspace(-3.5, 3.5, 100)
    x,y=np.meshgrid(xx, yy)
    z=np.exp(-(x-1)**2-y**2)-10*(x**3+y**4-x/5)*np.exp(-(x**2+y**2))

    colorscale=[[0.0, 'rgb(20,29,67)'],
               [0.1, 'rgb(28,76,96)'],
               [0.2, 'rgb(16,125,121)'],
               [0.3, 'rgb(92,166,133)'],
               [0.4, 'rgb(182,202,175)'],
               [0.5, 'rgb(253,245,243)'],
               [0.6, 'rgb(230,183,162)'],
               [0.7, 'rgb(211,118,105)'],
               [0.8, 'rgb(174,63,95)'],
               [0.9, 'rgb(116,25,93)'],
               [1.0, 'rgb(51,13,53)']]

    textz=[['x: '+'{:0.5f}'.format(x[i][j])+'<br>y: '+'{:0.5f}'.format(y[i][j])+
            '<br>z: '+'{:0.5f}'.format(z[i][j]) for j in range(z.shape[1])] for i in range(z.shape[0])]

    trace1= go.Surface(z=z,
                    x=x,
                    y=y,
                    colorscale=colorscale,
                    text=textz,
                    hoverinfo='text',
                    )

    axis = dict(
      showbackground=True,
      backgroundcolor="rgb(230, 230,230)",
      showgrid=False,
      zeroline=False,
      showline=False)

    ztickvals=range(-6,4)
    layout = go.Layout(title="Projections of a surface onto coordinate planes" ,
                    autosize=False,
                    width=700,
                    height=600,
                    #scene=dict(xaxis=dict(axis, range=[-3.5, 3.5]),
                    #            yaxis=dict(axis, range=[-3.5, 3.5]),
                    #            zaxis=dict(axis , tickvals=ztickvals),
                                #aspectratio=dict(x=1,
                                #                 y=1,
                                #                 z=0.95)
                    #           )
    )

    # Discretization of each Plane
    # The surface projections will be plotted in the planes of equations Z=np.min(z)-2, X=np.min(xx),
    # respectively Y=np.min(yy).

    z_offset=(np.min(z)-2)*np.ones(z.shape)#
    x_offset=np.min(xx)*np.ones(z.shape)
    y_offset=np.min(yy)*np.ones(z.shape)

    # Define the color functions and the color numpy arrays, C_z, C_x, C_y, corresponding to each plane:
    # Define the 3-tuples of coordinates to be displayed at hovering the mouse over the projections.
    # The first two coordinates give the position in the projection plane, whereas the third one is used for
    # assigning the color, just in the same way the coordinate z is used for the z-direction projection.

    proj_z=lambda x, y, z: z   #projection in the z-direction
    colorsurfz=proj_z(x,y,z)
    proj_x=lambda x, y, z: x
    colorsurfx=proj_z(x,y,z)
    proj_y=lambda x, y, z: y
    colorsurfy=proj_z(x,y,z)

    textx=[['y: '+'{:0.5f}'.format(y[i][j])+'<br>z: '+'{:0.5f}'.format(z[i][j])+
            '<br>x: '+'{:0.5f}'.format(x[i][j]) for j in range(z.shape[1])]  for i in range(z.shape[0])]
    texty=[['x: '+'{:0.5f}'.format(x[i][j])+'<br>z: '+'{:0.5f}'.format(z[i][j]) +
            '<br>y: '+'{:0.5f}'.format(y[i][j]) for j in range(z.shape[1])] for i in range(z.shape[0])]

    tracex = go.Surface(z=z,
                    x=x_offset,
                    y=y,
                    colorscale=colorscale,
                    showlegend=False,
                    showscale=False,
                    surfacecolor=colorsurfx,
                    text=textx,
                    hoverinfo='text'
                   )
    tracey = go.Surface(z=z,
                    x=x,
                    y=y_offset,
                    colorscale=colorscale,
                    showlegend=False,
                    showscale=False,
                    surfacecolor=colorsurfy,
                    text=texty,
                    hoverinfo='text'
                   )
    tracez = go.Surface(z=z_offset,
                    x=x,
                    y=y,
                    colorscale=colorscale,
                    showlegend=False,
                    showscale=False,
                    surfacecolor=colorsurfx,
                    text=textz,
                    hoverinfo='text'
                   )

    data=[trace1, tracex, tracey, tracez]
    fig = go.Figure(data=data, layout=layout)
    return fig


@app_threed.callback(Output('graph_3d_surface_torus', 'figure'),
    [ Input('graph_3d_surface_torus', 'children')
    ])
def graph_3d_surface_torus(foo):
    # Torus

    u = np.linspace(0, 2*np.pi, 20)
    v = np.linspace(0, 2*np.pi, 20)
    u,v = np.meshgrid(u,v)
    u = u.flatten()
    v = v.flatten()

    x = (3 + (np.cos(v)))*np.cos(u)
    y = (3 + (np.cos(v)))*np.sin(u)
    z = np.sin(v)

    points2D = np.vstack([u,v]).T
    tri = sci_Delaunay(points2D)
    simplices = tri.simplices

    fig = ff.create_trisurf(x=x, y=y, z=z,
                             simplices=simplices,
                             title="Torus", aspectratio=dict(x=1, y=1, z=0.3))

    fig.update(layout=dict(width=750))
    return fig


@app_threed.callback(Output('graph_3d_surface_mobius', 'figure'),
    [ Input('graph_3d_surface_mobius', 'children')
    ])
def graph_3d_surface_mobius(foo):
    u = np.linspace(0, 2*np.pi, 24)
    v = np.linspace(-1, 1, 8)
    u,v = np.meshgrid(u,v)
    u = u.flatten()
    v = v.flatten()

    tp = 1 + 0.5*v*np.cos(u/2.)
    x = tp*np.cos(u)
    y = tp*np.sin(u)
    z = 0.5*v*np.sin(u/2.)

    points2D = np.vstack([u,v]).T
    tri = sci_Delaunay(points2D)
    simplices = tri.simplices

    fig = ff.create_trisurf(x=x, y=y, z=z,
                            colormap="Portland",
                            simplices=simplices,
                            title="Mobius Band")

    fig.update(layout=dict(width=750))
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
