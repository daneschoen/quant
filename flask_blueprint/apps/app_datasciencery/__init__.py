from flask import Blueprint
from flask.views import View, MethodView


app_datasciencery = Blueprint('app_datasciencery', __name__, template_folder='templates')


from . import views_datasciencery
