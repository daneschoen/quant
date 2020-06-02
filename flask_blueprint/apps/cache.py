import os
from flask_caching import Cache
from apps.settings.settings import CACHE_CONFIG

cache = Cache(config=CACHE_CONFIG)
