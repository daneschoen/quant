from flask_login import UserMixin, AnonymousUserMixin
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)

class User(UserMixin):

    def __init__(self, dic):
        self.dic = dic

    #
    # used by current_user.get_id(), ...
    #
    def is_authenticated(self):
        """ Returns True if user is logged in - ie, they have provided valid credentials.
        """
        return True

    def is_active(self):
        """ In addition to being authenticated, they also have activated their account,
        not been suspended, or any condition your application has for rejecting an
        account. Inactive accounts may not log in.
        """
        return self.dic['active']

    def get_id(self):
        """
        Returns unique identification for this user, must be unicode not int
        Used to load the user from the user_loader callback.
        """
        return str(self.dic['_id'])

    @property
    def role(self):
        return self.dic['role']

    @property
    def classification(self):
        return self.dic['classification']

    @property
    def username(self):
        #return self.username
        return self.dic['username']

    @property
    def email(self):
        return self.dic['email']

    @property
    def id(self):
        return str(self.dic['_id'])
