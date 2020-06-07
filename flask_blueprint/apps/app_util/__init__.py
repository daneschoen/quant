# ==============================================================================
# mongodb
# logging
# ==============================================================================
from pymongo import MongoClient

# from flask import logging
import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter

from apps import app
from apps.settings.constants import *

from .util_email import email_smtp


def get_mongodb(hostname, port, dbname):
    client = MongoClient(hostname, port)
    mongodb = client[dbname]
    return client, mongodb


mongoclient_fintech, mongodb_fintech = get_mongodb(app.config['MONGO_HOSTNAME_FINTECH'], app.config['MONGO_PORT_FINTECH'], app.config['MONGO_DBNAME_FINTECH'])
mongoclient_geo, mongodb_geo = get_mongodb(app.config['MONGO_HOSTNAME_GEO'], app.config['MONGO_PORT_GEO'], app.config['MONGO_DBNAME_GEO'])

mongoclient, mongodb = mongoclient_fintech, mongodb_fintech

col_coin_spec = mongodb[COL_COIN_SPEC]
col_coin_top = mongodb[COL_COIN_TOP]
col_coin_hist_daily = mongodb[COL_COIN_HIST_DAILY]
col_coin_hist_daily2 = mongodb[COL_COIN_HIST_DAILY2]
col_coin_hist_hour = mongodb[COL_COIN_HIST_HOUR]
col_coin_hist_min = mongodb[COL_COIN_HIST_MIN]

col_user = mongodb[COL_USER]
col_contact = mongodb[COL_CONTACT]

col_geo_city = mongodb_geo[COL_GEO_CITY]
col_geo_cnty = mongodb_geo[COL_GEO_CNTY]

col_fx = mongodb_geo[COL_FX]


logger_flask = logging.getLogger(app.config['LOG_FLASK'])   # 'LOG_UWSGI_PATH_NAME'
logger_user = logging.getLogger(app.config['LOG_USER'])

log_level = logging.DEBUG
log_formatter = Formatter(app.config['LOG_FLASK_FORMATTER'])
#log_handler_stream = logging.StreamHandler()
log_handler_flask = RotatingFileHandler(app.config['LOG_FLASK_PATH_NAME'], maxBytes=1024*1024*10, backupCount=10)
log_handler_flask.setFormatter(log_formatter)
log_handler_flask.setLevel(log_level)
#logger = logging.getLogger(__name__)
log_handler_user = RotatingFileHandler(app.config['LOG_USER_PATH_NAME'], maxBytes=1024*1024*10, backupCount=10)
log_handler_user.setFormatter(log_formatter)
log_handler_user.setLevel(log_level)

logger_flask.setLevel(log_level)
logger_flask.addHandler(log_handler_flask)

logger_user.setLevel(log_level)
logger_user.addHandler(log_handler_user)
