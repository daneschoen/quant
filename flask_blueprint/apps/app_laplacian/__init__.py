from flask import Blueprint
from flask.views import View, MethodView


app_laplacian = Blueprint('app_laplacian', __name__, template_folder='templates')


from . import views_laplacian
