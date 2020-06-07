import os, sys, pathlib
from collections import OrderedDict
from datetime import datetime
# from dateutil.parser import parse as dateparse
import time, math

import numpy as np
import pandas as pd
from pandas.tseries.offsets import *

# import statsmodels.api as sm
# import statsmodels.formula.api as smf
# from statsmodels.sandbox.regression.predstd import wls_prediction_std
# import statsmodels.graphics.api as smg
#
# from sklearn import linear_model

import colorlover as cl

import plotly.graph_objs as go  # Layout,
from plotly import tools
import plotly.figure_factory as ff

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
# X import .grasia_dash_components as gdc
# from . import grasia_dash_components as gdc
#import grasia_dash_components as gdc

from textwrap import dedent

# from apps import app

"""
# ==============================================================================
# Basic Dash: graph
# ==============================================================================
"""

def create_plot_basic2(app):
    # ==============================================================================
    # todo: __init__.py and constants.py
    # ==============================================================================
    # app_basic2 = dash.Dash(server=app)
    app_basic2 = dash.Dash(__name__, server=app, crsf_protect=False, url_base_pathname='/basic2/')
    # app_basic2 = dash.Dash(__name__)
    app_basic2.config.supress_callback_exceptions = True

    #app_basic2.css.config.serve_locally = True
    #app_basic2.scripts.config.serve_locally = True

    app_basic2.css.append_css({
        "external_url": "/static/css/dash.css"  #"https://codepen.io/chriddyp/pen/bWLwgP.css"
    })
    # app_basic2.server.static_folder = 'static'  # if you run app_basic2.py from 'root-dir-name' you don't need to specify.


    colors = {
        'background': '#f2f2da',
        'text': '#9ab8c4'
    }

    DEBUG=True

    if DEBUG:
        print("\n\ndash.__version__: " + dash.__version__ + "\n")


    # ==============================================================================
    # Data
    # ==============================================================================


    header_names =['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'class']
    df_iris = pd.read_csv('/srv/static/data/iris_data.csv', names=header_names)


    # ==============================================================================
    # Layout
    # ==============================================================================

    app_basic2.layout = html.Div(style={'width': '600'}, children=[
        html.Div(id='content'),
        dcc.Location(id='location', refresh=False),

        html.H3(id='hola',
            children='Hello Dash',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),
        # Section Reactive 'Excel' Example
        html.Label('Hours per Day'),
        dcc.Slider(id='hours', value=5, min=0, max=24, step=1),

        html.Label('Rate'),
        dcc.Input(id='rate', value=2, type='number'),

        html.Label('Amount per Day'),
        html.Div(id='amount'),

        html.Label('Amount per Week'),
        html.Div(id='amount-per-week'),

        html.Div(style={'height': '50'}),

        dcc.Dropdown(
            id='dropdown_ticker',
            options=[
                #{'label': 'Poxel', 'value': 'EURONEXT/POXEL'},
                #{'label': 'Orange', 'value': 'EURONEXT/ORA'},
                #{'label': 'TechnipFMC', 'value': 'EURONEXT/FTI'},

                {'label': 'AAPL', 'value': 'AAPL'},
                {'label': 'GOOG', 'value': 'GOOG'},
                {'label': 'Netflix', 'value': 'NFLX'}
            ],
            value='NFLX'

        ),

        #dcc.Graph(id='graph_0_0', config={'displayModeBar': False}),

        html.Div(id='graph_2_0', children=dcc.Graph(id="dummy")),

        #gdc.Import()

      ]
    )

    # -------------------------------- callbacks -----------------------------------

    @app_basic2.callback(Output('amount', 'children'),
                  [Input('hours', 'value'), Input('rate', 'value')])
    def compute_amount(hours, rate):
        return float(hours) * float(rate)

    @app_basic2.callback(Output('amount-per-week', 'children'),
                  [Input('amount', 'children')])
    def compute_week(amount):
        return float(amount) * 7


    @app_basic2.callback(Output('graph_2_0', 'children'),
                 [Input('dropdown_ticker', 'value')])
    def foo(_):
        dcc_graph = dcc.Graph(id='foo',
            figure={
                'data': [
                    {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'scatter', 'mode':'markers' ,'name': 'SF'},
                    {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'scatter', 'mode':'markers', 'name': u'Montréal'},
                ],
                'layout': {
                    'plot_bgcolor': colors['background'],
                    'paper_bgcolor': colors['background'],
                    'font': {
                        'color': colors['text']
                    }
                }
            }
        )
        return dcc_graph


    return app_basic2
# ==============================================================================

# if __name__ == '__main__':
#     app.run_server(debug=DEBUG)
