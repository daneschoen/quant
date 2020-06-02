
# ==============================================================================
# This is settings.py, settings_server.py, settings_local.py
# ==============================================================================
import os
import logging

# ===========================
# Mongodb
# ===========================
# Gets overriden by settings_local.py
MONGO_HOSTNAME = 'localhost'  #'172.31.24.58'
MONGO_PORT = 27017
MONGO_DBNAME = 'kiklearn'
COLL_ENTITY = 'entity'

COL_GEO = 'geo'


# ===========================
# Log
# ===========================
#LOG_DIR = './log'
LOG_DIR = os.path.join(os.path.dirname(__file__), 'log')

LOG_CRAWL_site_NAMEPATH = os.path.join(LOG_DIR, "crawl_site")
LOG_QUEUE_site_NAMEPATH = os.path.join(LOG_DIR, "queue_site")
LOG_PROCESS_TASKS_NAMEPATH = os.path.join(LOG_DIR, "queue_process_tasks")

LOG_CRAWL_site_LEVEL = logging.INFO  #"DEBUG"
LOG_QUEUE_site_LEVEL = logging.INFO  #"DEBUG"
LOG_PROCESS_TASKS_LEVEL  = logging.INFO  #"DEBUG"
LOG_BYTES = 1024*2000


# ===========================
# EMAIL
# ===========================
#EMAIL_LOG_TIMES = [12,0]
EMAIL_SMTP_HOST = "localhost"
EMAIL_LOG_FROM = "donotreply@kiklearn.com"
EMAIL_LOG_TO = ['danschoe@gmail.com']


# ===========================
# Crawl
# ===========================
CRAWL_site_URL_RSS = 'http://foobar'
CRAWL_site_FILEROOTNAME = 'site'
# DIR_CRAWL_site = '/data/crawler/scripts/crawl/site'
DIR_CRAWL_site = os.path.join(os.path.dirname(__file__), 'crawled/site')
# DIR_CRAWL_site_ARCHIVE = '/data/crawler/scripts/crawl/archive/site'
DIR_CRAWL_site_ARCHIVE = os.path.join(os.path.dirname(__file__), 'crawled/archive/site')


# ===========================
# Queue
# ===========================
EXCHANGE_NAME = ''
QUEUE_site1_NAME = "queue_site1"
QUEUE_site2_NAME = "queue_site2"

QUEUE_PROCESS_A = "queue_process_a"
QUEUE_PROCESS_B = "queue_process_b"

