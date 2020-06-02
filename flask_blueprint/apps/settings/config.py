import os
from kombu import Queue, Exchange

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    SECRET_KEY = os.urandom(32)

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://earl-dbadmin:KkoakltNsxH07GBT@172.26.13.37/earl'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', SQLITE_DB)

    CELERY_TIMEZONE = 'US/Eastern'
    CELERY_BROKER_URL = 'amqp://localhost:5672'
    CELERY_RESULT_BACKEND = 'rpc://'

    # define the tasks queues
    CELERY_QUEUES = (
        Queue('default', Exchange('default'), routing_key='default'),
        Queue('get_visitors', Exchange('get_visitors'), routing_key='get_visitors'),
        Queue('append_visitors', Exchange('append_visitors'), routing_key='append_visitors'),
        Queue('create_leads', Exchange('create_leads'), routing_key='create_leads'),
        Queue('verify_leads', Exchange('verify_leads'), routing_key='verify_leads'),
        Queue('send_leads', Exchange('send_leads'), routing_key='send_leads'),
        Queue('send_adfs', Exchange('send_adfs'), routing_key='send_adfs'),
        Queue('send_followups', Exchange('send_followups'), routing_key='send_followups'),
        Queue('send_rvms', Exchange('send_rvsm'), routing_key='send_rvms'),
        Queue('reports', Exchange('reports'), routing_key='reports'),
        Queue('campaigns', Exchange('campaigns'), routing_key='campaigns'),
        Queue('stores', Exchange('stores'), routing_key='stores')
    )

    # define the task routes
    CELERY_ROUTES = {
        'get_new_visitors': {'queue': 'get_visitors', 'routing_key': 'get_visitors'},
        'append_visitor': {'queue': 'append_visitors', 'routing_key': 'append_visitors'},
        'create_lead': {'queue': 'create_leads', 'routing_key': 'create_lead'},
        'verify_lead': {'queue': 'verify_leads', 'routing_key': 'verify_lead'},
        'send_lead_to_dealer': {'queue': 'send_leads', 'routing_key': 'send_leads'},
        'send_auto_adf_lead': {'queue': 'send_adfs', 'routing_key': 'send_adfs'},
        'send_followup_email': {'queue': 'sends_followups', 'routing_key': 'send_followups'},
        'send_rvm': {'queue': 'send_rvms', 'routing_key': 'sends_rvms'},
        'reports': {'queue': 'reports', 'routing_key': 'reports'},
        'campaigns': {'queue': 'campaigns', 'routing_key': 'campaigns'},
        'stores': {'queue': 'stores', 'routing_key': 'stores'}
    }


class DevelopmentConfig(Config):
    DEBUG = True
    MONGO_SERVER = '172.26.13.37'
    MONGO_DB = 'earl-pixel-tracker'


class ProductionConfig(Config):
    DEBUG = False

# tests.py
# ...
import unittest
from settings import config
from apps import create_app

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

class ExampleTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        # See Grinberg's tutorial for the other essential bits

class TestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config.TEST_DATABASE_URI)
        self.client = self.app.test_client()


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
