import os

# http://flask.pocoo.org/docs/0.12/config/

# -----
# PATH
# -----
pth_settings = os.path.dirname(os.path.realpath(__file__))

PATH_PROJ = os.path.abspath(os.path.join(pth_settings, '../../..'))
PATH_APP = os.path.abspath(os.path.join(pth_settings, '../..'))
PATH_DATA_IN = os.path.abspath(os.path.join(pth_settings, '../../../data_in/'))

"""
pth_wrk = os.getcwd()  ==

PROJ_PATH = os.path.abspath(os.path.dirname( __file__ ))
if PROJ_PATH[:6] == "/Users":
    PROJ_PATH = PROJ_PATH[:36] + "projects/fintech/"
else:
    PROJ_PATH = PROJ_PATH[:10] + "projects/fintech/"

APP_PATH = PROJ_PATH + "flask_blueprint/"
"""


# Changed in settings_local.py
DEBUG = False
TESTING = False
TEMPLATES_AUTO_RELOAD = True

CSRF_ENABLED = True

ADMINS = ['admin@visuably.com']

USER_ID = 0

# Application threads. A common general assumption is using 2 per available
# processor cores - to handle incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

###toddo SERVER_NAME

"""
app.config['DEBUG'] = True
For built-in configuration values - forwarded to the Flask object so you can read and write them from there:
app.debug = True


hostname = socket.gethostname().replace('.','_').replace('-','_')

if not hostname.startswith('kiklearn'):
    try:
        from flask_blueprint.settings.DEV_local import *
        hostname = "DEV_local"
    except ImportError as e:
        raise e
else:
    #hstr = "import settings.{0} as local_settings".format(hostname)
    hstr = "from flask_blueprint.settings.{0} import *".format(hostname)
    exec(hstr)

print("Loaded settings from {0}.py".format(hostname))
HOSTNAME = hostname
REMEMBER_COOKIE_NAME = 'sessionid'
"""


# ==============================================================================
# Mongodb
# ==============================================================================
MONGO_HOSTNAME_FINTECH = 'localhost'  #'172.31.24.58'
MONGO_PORT_FINTECH = 27017
MONGO_DBNAME_FINTECH = 'fintech'

MONGO_HOSTNAME_ = MONGO_HOSTNAME_FINTECH
MONGO_PORT_ = MONGO_PORT_FINTECH
MONGO_DBNAME_ = MONGO_DBNAME_FINTECH

MONGO_DBNAME_GEO = 'geo'           #'rivercast'
MONGO_HOSTNAME_GEO = 'localhost'
MONGO_PORT_GEO = 27017

MONGO_DBNAME_TRIBAL = 'blog_tribal'           #'rivercast'
MONGO_HOSTNAME_TRIBAL = 'localhost'
MONGO_PORT_TRIBAL = 27017


# ==============================================================================
# EMAIL
# ==============================================================================
EMAIL_FINTECH_ADMIN  = 'admin@quantcypher.com'
EMAIL_FINTECH_ME     = 'daniel@quantcypher.com'
EMAIL_COINTIUS_ADMIN = 'admin@cointius.com'
EMAIL_COINTIUS_ME    = 'daniel@cointius.com'

EMAIL_TRIBAL_ADMIN = ''
EMAIL_TRIBAL_ME = ''
EMAIL_SCIENCE_ADMIN = 'daniel@scienceismeta.com'
EMAIL_SCIENCE_ME = 'daniel@cointius.com'

EMAIL_SERVER_PORT_GMAIL = ('smtp.gmail.com', 587)
EMAIL_SERVER_PORT_ZOHO = ("smtp.zoho.com", 587) # 465)   SSl


# ==============================================================================
# Log
# ==============================================================================
#LOG_DIR = './log'
#LOG_DIR = os.path.join(os.path.dirname(__file__), 'log')
LOG_UWSGI_PATH_NAME = '/var/log/uwsgi/uwsgi.log'
LOG_FLASK_PATH_NAME = '/var/log/uwsgi/flask.log'
LOG_USER_PATH_NAME = '/var/log/uwsgi/user.log'
LOG_UWSGI = 'log_uwsgi'
LOG_FLASK = 'log_flask'
LOG_USER = 'log_user'
# '%(asctime)s - %(levelname)s - %(message)s'
#LOG_FLASK_FORMATTER = "[%(asctime)s] {%(pathname)s:%(lineno)d} - %(levelname)s : %(message)s"
LOG_FLASK_FORMATTER = "[%(asctime)s] <%(filename)s:%(lineno)d> - %(levelname)s : %(message)s"
LOG_UWSGI_FORMATTER = "FLASK > [%(asctime)s] <%(filename)s:%(lineno)d> - %(levelname)s : %(message)s"


# ==============================================================================
# KEYS
# ==============================================================================
"""
#app.config['SECRET_KEY'] = 'super-secret'

import uuid
uuid.uuid4()


In python 3, if you prefer a plain string (to store in a JSON file, for example),
you can convert to a hex string:
import os
os.urandom(24).encode('hex')


$ python -c 'import os; print(os.urandom(16))'
b'_5#y2L"F4Q8z\n\xec]/'

import binascii
binascii.hexlify(os.urandom(24))
"""


# for s3 and ses
#AWS_ACCESS_KEY = 'foobar'
#AWS_SECRET_ACCESS_KEY = 'foobar'

#EMAIL_HOST = 'email-smtp.us-west-2.amazonaws.com'
#EMAIL_HOST_USER = 'foobar'
#EMAIL_HOST_PASSWORD = 'foobar'
#EMAIL_PORT = 587


#BALANCED_KEY = 'foobar'
#BALANCED_KEY_TEST = 'foobar'
#BALANCED_MARKETPLACE_TEST = 'TEST-foobar'

CACHE_CONFIG = {
    # try 'filesystem' if you don't want to setup redis
    #'CACHE_TYPE': 'redis',
    #'CACHE_REDIS_URL': os.environ.get('REDIS_URL', 'localhost:6379')
}

# ==============================================================================
# Import other files into config namespace: settings and constants
# ==============================================================================
# import constants as CONST

try:
  from apps.settings.settings_server import *
except ImportError:
    try:
      from apps.settings.settings_local import *
    except ImportError:
        pass

# try:
#   from apps.settings.settings_pair import *
# except ImportError:
#     pass
