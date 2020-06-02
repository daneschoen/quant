from flask import Blueprint
from flask.views import View, MethodView


app_laplacian = Blueprint('app_laplacian', __name__, template_folder='templates')


# from apps import app

# ------------
# Init the app
# ------------
#from apps.app_tribal import init_app
#init_app.go()

from . import views_laplacian
