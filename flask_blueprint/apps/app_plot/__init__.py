from flask import Blueprint
from flask.views import View, MethodView

# from apps import app

#from .a_basic_dash_graph import app_basic
from .a_basic_dash_fn import create_plot_basic2

from .app_plot_pair import app_pair
from .app_plot_scatter_histogram import app_scatter
from .app_plot_threed import app_threed
### from .streaming_wind.app_plot_stream_wind import app_stream_wind
from .ml_model_training.app_plot_training import app_stream_train


# ==============================================================================

app_plot = Blueprint('app_plot', __name__)

##from . import views_plot

# from apps import app_basic
#from apps.app_plot.a_basic_dash_graph import app_basic

# @app_plot.route('/dash', methods=['GET', 'POST'])
# def dash_basic():
#     return app_basic.index()

"""
app.add_url_rule('/',
                 view_func=Main.as_view('main'),
                 methods = ['GET'])

app.add_url_rule('/<page>/',
                 view_func=Main.as_view('page'),
                 methods = ['GET'])
"""
