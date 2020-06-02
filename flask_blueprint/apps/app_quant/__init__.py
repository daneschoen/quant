# from apps import Blueprint_host

from flask import Blueprint
from flask.views import View, MethodView


# app_quant = Blueprint_host('app_quant', __name__, template_folder='templates', default_host="quantcypher.com")
app_quant = Blueprint('app_quant', __name__, template_folder='templates')


from . import views_quant
