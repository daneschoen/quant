
from flask import Blueprint
from flask.views import View, MethodView


app_analytic = Blueprint('app_analytic', __name__, template_folder='templates')


# Testing
@app_analytic.route('foo')
def foo():
    return "Module analytic is working!"


from apps import app


# Init app
from apps.app_analytic import init_app
init_app.go()


from apps.app_analytic import views
