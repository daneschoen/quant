import os, sys

from flask import Flask, Blueprint, \
    render_template, request, redirect, url_for, \
    abort, session, \
    make_response, Response, \
    jsonify, send_from_directory, logging

from flask_wtf.csrf import CSRFProtect

from flask_session import Session
from flask_redis import FlaskRedis
import redis
#from flask_caching import Cache
from .cache import cache


# ==============================================================================
# Flask app creation
# ==============================================================================
app = Flask(__name__)
# app = Flask(__name__, host_matching=True, static_host='datasciencery.com')   # url_map.host_matching => True


class Blueprint_host(Blueprint):
    def __init__(self, *args, **kwargs):
        self.default_host = kwargs.pop('default_host', None)
        Blueprint.__init__(self, *args, **kwargs)

    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        options['host'] = options.pop('host', self.default_host)
        super().add_url_rule(self, rule, endpoint=None, view_func=None, **options)


# app.config.from_object('config')
# app.config.from_object(os.environ['APP_SETTINGS'])
# app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.config.from_pyfile('settings/settings.py')

# app.config['DEBUG'] = True
# app.debug = True
# app.config.update(
#    DEBUG=True,
#    SECRET_KEY='...'
# )

#CSRFProtect(app)
csrf_protect = CSRFProtect()
csrf_protect._exempt_views.add('dash.dash.dispatch')
csrf_protect.init_app(app)

#Session(app)
sess = Session()
sess.init_app(app)

# redis_store = FlaskRedis(app)
redis_store = FlaskRedis()
redis_store.init_app(app)

redis_db = redis.Redis()  #host='localhost', port=6379, db=0)
# redis_db = redis.StrictRedis(host="localhost", charset="utf-8", port=6379, db=0, decode_responses=True)

#cache = Cache(app, config=CACHE_CONFIG)
#cache = Cache(config=app.config['CACHE_CONFIG'])
cache.init_app(app) #, config=app.config['CACHE_CONFIG'])


# ==============================================================================
# Register the blueprints
# ==============================================================================

PLOT_ROUTES = dict(
  pair = 'datascience/',                     # <= @app_quant.route('/datascience/') bec of iframe
  scatter_histogram = 'scatter-histogram/',  # <= @app_laplacian.route('/scatter-histogram/')
  threed = 'threed/',                        # <= @app_laplacian.route('/3d/')
  stream_wind = 'stream-wind/',
  stream_model_training = 'stream-model-training/',
  machinelearning = 'machinelearning/'       # <= @app_quant.route('/machinelearning/')
)

from apps.app_auth import app_auth
from apps.app_admin import app_admin

from apps.app_geo import app_geo
from apps.app_fx import app_fx

from apps.app_datasciencery import app_datasciencery
from apps.app_quant import app_quant

#from apps.app_plot import app_pair
#from apps.app_plot import app_basic
#from apps.app_plot.a_basic_dash_graph import app_basic
#from apps.app_plot.a_basic_dash_fn import create_plot_basic2
#app_basic2 = create_plot_basic2(app)
#from apps.app_plot.a_basic_dash_graph import app_basic
from apps.app_plot import app_plot


# -----------------------------------------------------------
# DOMAINS - ML: www.quantcypher.com, www.datasciencery.com
# -----------------------------------------------------------
app.register_blueprint(app_auth, url_prefix='/account/')
app.register_blueprint(app_admin, url_prefix='/admin/')
app.register_blueprint(app_geo, url_prefix='/geo/')
app.register_blueprint(app_fx, url_prefix='/fx/')
app.register_blueprint(app_laplacian, url_prefix='/laplacian')
app.register_blueprint(app_datasciencery, url_prefix='/datasciencery')
app.register_blueprint(app_quant, url_prefix='/quant')
app.register_blueprint(app_plot, url_prefix='/plot/')
