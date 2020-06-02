from flask import Blueprint
from flask.views import View, MethodView


app_geo = Blueprint('app_geo', __name__, template_folder='templates')


from . import views
