from flask import Blueprint
from flask.views import View, MethodView


app_admin = Blueprint('app_admin', __name__, template_folder='templates')


from . import views
