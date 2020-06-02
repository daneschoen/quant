from flask import render_template, request, redirect, url_for, g, \
    abort, session, flash, logging, \
    make_response, Response, \
    jsonify
from flask import Blueprint

from functools import wraps


from flask.views import View, MethodView

from apps import app


app_auth = Blueprint('app_auth', __name__, template_folder='templates')


from bson.objectid import ObjectId

###to do: from apps.app_util import col_user
#??? from apps.app_kiklearn.models import User

from flask_login import LoginManager, AnonymousUserMixin

#oid = OpenID(app,os.path.join(basedir,'tmp'))

# ==============================================================================
# Basic Authentication
# ==============================================================================
def check_auth(username, password):
    return username == 'sak' and password == app.config['SECRET_KEY']


def authenticate_fail():
    msg = {'message': "Authenticate"}
    resp = jsonify(msg)
    resp = jsonify('.')

    resp.status_code = 403   # 401
    resp.headers['WWW-Authenticate'] = 'Basic realm="Forbidden"'

    return resp

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return authenticate_fail()

        elif not check_auth(auth.username, auth.password):
            return authenticate_fail()
        return f(*args, **kwargs)

    return decorated



"""
curl -v -u "admin:secret" http://127.0.0.1:5000/secret
curl http://127.0.0.1:5000/zdorovye/parbaudit/mongo
curl -u admin:secretd 127.0.0.1:5000/izmeginat/foo

curl -v -H "Authorization: Basic YWRtaW46c2VjcmV0" 127.0.0.1:5000/izmeginat/foo

$ echo -n admin:secret | base64      <==>  >>> base64.b64encode(u.encode()).decode()
$ echo YWRtaW46c2VjcmV0 | base64 -d  <==>  >>> base64.b64decode(v.encode()).decode()
                                               base64.b64decode(v).decode()

Authenticated RESPONSE:
GET /secrets Authorization: Basic YWRtaW46c2VjcmV0
Shhh this is top secret spy stuff!

Unauthenticated REQUEST:
GET /secrets
HTTP/1.0 401 UNAUTHORIZED
WWW-Authenticate: Basic realm="Example"
{
  "message": "Authenticate."
}

Flask uses a MultiDict to store the headers. To present clients with multiple possible authentication schemes it is possible to simply add more WWW-Authenticate lines to the header

resp.headers['WWW-Authenticate'] = 'Basic realm="Example"'
resp.headers.add('WWW-Authenticate', 'Bearer realm="Example"')

or use a single line with multiple schemes (the standard allows both).
"""



# ==============================================================================
# Login
# ==============================================================================
class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.username = 'guest'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'app_auth.login'
login_manager.login_message = "Please log in to access this page."
login_manager.refresh_view = 'reauth' #'login_refresh'
login_manager.anonymous_user = Anonymous

# Required callback for flask.ext.login
# Take a user ID (a unicode) and return a user object or None if the user does
# not exist.
@login_manager.user_loader
def load_user(_id):
    """
    # Mock version/ _id is email:
    if _id not in users:
        return
    user = User(_id, users[_id]['pw'])
    #user.id = _id  .id attribute does not necessarily exists
    return user
    """
    """
    u = User.get(_id)
    if not u:
      return None
    return User(u[0], u[1])
    """
    # SQL version/
    #return User.query.get(id)
    #return User.query.filter(User.id == int(user_id)).first()

    #user = Customer.query.get(id)
    #if user is None:
    #    user = User.query.get(id)
    #return user

    # Mongo version/
    user_dic = col_user.find_one({'_id': ObjectId(_id)})
    if not user_dic:
      return None
    user_obj = User(user_dic)
    return user_obj


# ------------------------------------------------------------------------------
# Login users wo using cookies, instead use:
# - header values or
# - an api key passed as a query argument.
# This callback should behave the same as your user_loader callback, except
# that it accepts the Flask request instead of a user_id.
# ------------------------------------------------------------------------------
@login_manager.request_loader
def request_loader(request):
    # Mock 0/
    """
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['pw'] == users[email]['pw']

    return user
    """

    # Mock 1/
    # to use this:
    # http://localhost:5000/protected/?token=JohnDoe:John
    #
    # from itsdangerous import JSONWebSignatureSerializer
    # s = JSONWebSignatureSerializer('secret-key')
    # token = s.dumps({'username': JaneDoe, 'password' : 'secret'})
    # The token in the above code can be used to pass from the server side.
    # Validate the token and check against db:
    # s = JSONWebSignatureSerializer('secret-key')
    # credential = s.loads(token)

    token = request.headers.get('Authorization')
    if token is None:
        token = request.args.get('token')

    if token is not None:
        username,password = token.split(":") # naive token
        user_entry = User.get(username)
        if (user_entry is not None):
            ###user = User(user_entry[0],user_entry[1])
            if (user.password == password):
                return user

    return None


from apps.app_auth import views
