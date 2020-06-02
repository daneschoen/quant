
from flask import g, flash
#from babel.support import LazyProxy

import os, sys
import logging, logging.handlers
import subprocess

from pymongo import MongoClient

#from flask.ext.sqlalchemy import Pagination
from math import ceil

###from flask_apps.constants import *

# ================================================================================
# VIEWS helpers
# ================================================================================

def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')

"""
def get_pagination(self, page, per_page=PER_PAGE, error_out=True):
    Returns 'per_page' items from page 'page'.  By default it will
    abort with 404 if no items were found and the page was larger than
    1.  This behavor can be disabled by setting 'error_out' to False
    Returns an :class: Pagination object.

    #if error_out and page < 1:
    #    abort(404)

    #items = self.limit(per_page).offset((page - 1) * per_page).all()
    # ---------------------------------------------------------------
    #items = users.limit(20).offset((0) * 20).all()
    #items = users.all()[0:15]
    #items = self.all()[per_page*(page-1):per_page*(page)]

    items = self[(page-1)*PER_PAGE: (page-1)*PER_PAGE + PER_PAGE]

    #if not items and page != 1 and error_out:
    #    abort(404)

    return Pagination(self, page, per_page, self.count(), items)
"""

class PaginationMongo(object):

    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num



"""
    if request.method == 'POST' and form.form_id.data == "form_provider_profile_edit" and not form.validate_on_submit():
        #flash_errors(form)
        x=""
        for field, errors in form.errors.items():
            for error in errors:
                x = x + " >>>  "   +  str(getattr(form, field).label.text) + "  " +str(error)
        return x
"""



"""
----------
REDIRECT
----------
"""
""" worst way: using jquery
var url = "http://stackoverflow.com";    
$(location).attr('href',url);

better pure html:
// similar behavior as an HTTP redirect
window.location.replace("http://stackoverflow.com");

It is better than using window.location.href =, because replace() does not put the originating page in the session
history, meaning the user won't get stuck in a never-ending back-button fiasco. If you want to simulate someone
clicking on a link, use location.href. If you want to simulate an HTTP redirect, use location.replace.

// similar behavior as clicking on a link
window.location.href = "http://stackoverflow.com";

"""

def redirect_url(default='homepage'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)

""" To use:
def some_view():
    # some action
    return redirect(redirect_url())
    
Without any parameters it will redirect the user back to where he came from (request.referrer).
You can add the get parameter next to specify a url. This is useful for oauth for example.

instagram.authorize(callback=url_for(".oauth_authorized",
                                    next=redirect_url(),
                                    _external=True))
I also added a default view if there should be no referrer for some reason

redirect_url('.another_view')


More securely by ensuring you cannot get redirected to a malicious attacker's page on another host:

Secure redirect
---------------
from urlparse import urlparse, urljoin
from flask import request, url_for, redirect
"""    

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

"""A simple way to to use it is by writing a get_redirect_target function that looks at various hints to find the
redirect target:
"""
def get_redirect_target():
    for target in request.values.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target

"""Since we don't want to redirect to the same page we have to make sure that the actual back redirect is slightly
different (only use the submitted data, not the referrer). Also we can have a fallback there:

def redirect_back(endpoint, **values):
    target = request.form['next']
    if not target or not is_safe_url(target):
        target = url_for(endpoint, **values)
    return redirect(target)
"""

"""It will tried to use next and the referrer first and fall back to a given endpoint.
You can then use it like this in the views:

@app.route('/login', methods=['GET', 'POST'])
def login_example():
    next = get_redirect_target()
    if request.method == 'POST':
        # login code here
        return redirect_back('index')
    return render_template('index.html', next=next)
"""

"""
The or is important so that we have a redirect target if all hints fail (in this case the index page).

In the template you have to make sure to relay the redirect target:

<form action="" method=post>
  <dl>
    <dt>Username:
    <dd><input type=text name=username>
    <dt>Password:
    <dd><input type=password name=password>
  </dl>
  <p>
    <input type=submit value=Login>
    <input type=hidden value="{{ next or '' }}" name=next>
</form>

The or here is just here to make None become an empty string.
"""
"""
Example form and view:

class RedirectForm(Form):
    next = HiddenField()

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        if not self.next.data:
            self.next.data = get_redirect_target() or ''

    def redirect(self, endpoint='index', **values):
        if is_safe_url(self.next.data):
            return redirect(self.next.data)
        target = get_redirect_target()
        return redirect(target or url_for(endpoint, **values))

class LoginForm(RedirectForm):
    username = TextField('Username')
    password = TextField('Password')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # do something with the form data here
        return form.redirect('index')
    return render_template('login.html', form=form)
    
"""    
# ================================================================================
# INTERNATIIONALIZATION
# ================================================================================
"""
def ugettext(s):
    # we assume a before_request function assigns the correct user-specific translations
    return g.translations.ugettext(s)

ugettext_lazy = LazyProxy(ugettext)

from speaklater import make_lazy_gettext
ugettext_lazy = make_lazy_gettext(lambda: g.translations.get)
"""

# ================================================================================
# Set env variables if needed
# ================================================================================
def setenv():
    script = os.getenv("HOME") + "setenv.sh"
    pipe = subprocess.Popen(". %s; env" % script, stdout=subprocess.PIPE, shell=True)
    data = pipe.communicate()[0]
    env = dict((line.split("=", 1) for line in data.splitlines()))
    os.environ.update(env)


def getDtStr(dtime):
    dt_yr = str(dtime.year)
    dt_mt = str(dtime.month)
    dt_dy = str(dtime.day)
    if len(dt_mt) < 2:
        dt_mt = "0" + dt_mt
    if len(dt_dy) < 2:
        dt_dy = "0" + dt_dy
    return (dt_yr, dt_mt, dt_dy)
    #return dt_yr + dt_mt + dt_dy



# ================================================================================
# Logging routines
# ================================================================================
LEVELS = { 'debug':logging.DEBUG,
           'info':logging.INFO,
           'warning':logging.WARNING,
           'error':logging.ERROR,
           'critical':logging.CRITICAL,
         }

def getLoggerInst(log_name, *args):
    log_filename = log_name + ".log"

    logger = logging.getLogger(log_name)

    #hdlr = logging.FileHandler(log_filename)
    hdlr = logging.handlers.RotatingFileHandler(log_filename, maxBytes=LOG_BYTES, backupCount=5)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)

    #lvl = LEVELS.get(level_name, logging.NOTSET)

    if args:
        logger.setLevel(args[0])
    else:
        logger.setLevel(logging.INFO)
    return logger


def getLoggerInstance(log_name, log_filename):
    logger = logging.getLogger(log_name)

    hdlr = logging.FileHandler(log_filename)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)
    return logger


def getLogger(log_name):
    #LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) ' '-35s %(lineno) -5d: %(message)s')
    #LOGGER = logging.getLogger(__name__)
    #logging.getLogger('pika').setLevel(logging.DEBUG)
    logging.basicConfig(level = logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    logformat=('%(asctime)s %(levelname)s %(name)s %(message)s')
    logging.basicConfig(format=logformat, level=logging.CRITICAL)



# ================================================================================
# Database routines
# ================================================================================
def get_mongodb(hostname, port, dbname):
    #client = MongoClient('localhost', 27017)
    client = MongoClient(hostname, port)
    mongodb = client[dbname]
    return mongodb



