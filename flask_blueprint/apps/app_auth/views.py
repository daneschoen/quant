from flask import render_template, request, redirect, url_for, g, \
    abort, session, flash, logging, \
    make_response, Response, \
    jsonify

from flask_login import login_user, logout_user, current_user, login_required, \
    confirm_login, fresh_login_required, \
    UserMixin, AnonymousUserMixin

from apps import app

from . import app_auth

from .models import User
from apps.app_util import col_user   #, logger

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# from bson.objectid import ObjectId

# ================================================================================
# Login - How flask-login manager works:
# 1) It registers current_user in request context
# 2) 'before_request' reads your session, gets user id, loads the user with 'user_loader'
#    and set it to current_user or AnonymousUser
# 3) When you visit a protected page, login_required checks current_user.is_authenticated()
#    else redirects to whatever you have set
# 4) On login, it adds user id to the session
# ================================================================================

# Ex 0/
@app_auth.route('mock/login0', methods = ['GET', 'POST'])
def login0():

    if request.method == 'GET':
        return '''
               <form action='login0' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'></input>
                <input type='password' name='pw' id='pw' placeholder='password'></input>
                <input type='submit' name='submit'></input>
               </form>
               '''
    if request.method == 'POST':
        logout_user()
        email = request.form['email']
        pwd = request.form['pw']
        #if email in users and pwd == users[email]['pw']:
        user_dic = col_user.find_one({ 'email': email })  #, 'pwd':pwd })
        if user_dic:
          #if user_dic['pwd'] == bcrypt.hashpw(pwd.encode(), user_dic['pwd']):
          if user_dic['pwd'] == bcrypt.check_password_hash(user_dic['pwd'], pwd):
            user_obj = User(user_dic)
            login_user(user_obj, remember=True)
            #user = User(email, pw)
            #user.id = email
            #login_user(user)
            return redirect(url_for('app_kiklearn.protected'))

        return 'Username/email and password could not be found'


# Ex 1/
@app_auth.route('mock/login1',methods = ['POST', 'GET'])
def login1():
    if request.method == 'POST':
        if request.form['username'] == 'admin':
            return redirect(url_for('success'))
        else:
            abort(401)

    return redirect(url_for('index'))

@app.route('/success')
def success():
   return 'logged in successfully'




@app_auth.route('login', methods = ['GET', 'POST'])
def login():
    """
    if request.method == "POST" and "username" in request.form:
        username = request.form["username"]
        if username in USER_NAMES:
            remember = request.form.get("remember", "no") == "yes"
            if login_user(USER_NAMES[username], remember=remember):
                flash("Logged in!")
                return redirect(request.args.get("next") or url_for("index"))
            else:
                flash("Sorry, but you could not log in.")
        else:
            flash(u"Invalid username.")
    return render_template("login.html")
    """

    if request.method == 'GET':
        return render_template('login.html', next=request.args.get('next'))
    elif request.method == 'POST':
        logout_user()
        username = request.form['txtUsername']
        pwd = request.form['txtPassword']

        #user = User.query.filter_by(username=username).filter_by(password=password)
        user_dic = col_user.find_one({ 'username': username })
        if user_dic:
          #if user_dic['pwd'] == bcrypt.hashpw(pwd.encode(), user_dic['pwd']):
          if bcrypt.check_password_hash(user_dic['pwd'], pwd):
            user_obj = User(user_dic)
            login_user(user_obj, remember=True)

            #return redirect(url_for('protected'))
            flash('Welcome back {0}'.format(username))
            #try:
            #    next = request.form['next']
            #    return redirect(next)
            #except:
            #    return redirect(url_for('index'))
            return redirect(request.args.get('next') or url_for("app_kiklearn.index"))
        flash('Invalid username and password combination')
        return redirect(url_for('app_auth.login'))
        # return redirect('/some-url')
        # return render_template('www.html')
    else:
        return abort(405)



    """
    #if current_user.is_authenticated():
    #     return render_template("/showcase/home.html")

    form = LoginForm()

    if (request.method == "POST" or request.method == "GET") and form.validate_on_submit():
        # user = Customer.query.filter_by(email=form.email.data).first()
        # if user is not None:
        #     if login_user(user):
        #         return redirect(request.args.get('next') or "showcase/account/receiver/profile")
        # else:
        #     user = User.query.filter_by(email=form.email.data).first()
        #     if user is not None:
        #         if login_user(user):
        #             return redirect(request.args.get('next') or "showcase/account/provider/profile")

        #remember = request.form.get("remember", "no") == "yes"
        email = form.email.data.strip().lower()   #request.form["username"]
        password = form.password.data.strip()     #request.form["password"]
        #remember = request.form.get("remember", "no") == "yes"
        remember = form.remember.data

        #user = col_user.find_one({"_id": ObjectId(id)})
        #user = col_user.find_one({ "email": email })
        user_dic = col_user.find_one({ "email": email })
        user_obj = User(user_dic)

        if login_user(user_obj, remember):

            if user_dic['role'] == "customer":
                return redirect(request.args.get("next") or url_for("receiver_profile"))
                #return redirect(request.args.get('next') or "showcase/account/receiver/profile")
            elif user_dic['role'] == "provider":
                return redirect(request.args.get('next') or url_for("provider_profile"))
                #return redirect(request.args.get('next') or "showcase/account/provider/profile")

        return render_template('showcase/static/404.html')

    return render_template('/login.html', form=form, next=next)
    """


@app_auth.route('register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        username = request.form['txtUsername']
        password = request.form['txtPassword']
        #
        # MUST CHECK FOR UNIQUE USERNAME AND/OR EMAIL
        #
        ###user = User.query.filter_by(username=username)
        if user.count() == 0:
            ###user = User(username=username, password=password)
            ###db.session.add(user)
            ###db.session.commit()

            flash('You have registered the username {0}. Please login'.format(username))
            return redirect(url_for('app_auth.login'))
        else:
            flash('The username {0} is already in use.  Please try a new username.'.format(username))
            return redirect(url_for('app_auth.register'))
    else:
        abort(405)


@app_auth.route("reauth", methods=["GET", "POST"])
@login_required
def reauth():
    if request.method == "POST":
        confirm_login()
        flash(u"Reauthenticated.")
        return redirect(request.args.get("next") or url_for("app_kiklearn.index"))
    return render_template("reauth.html")


@app_auth.route('logout')   #, methods = ['GET', 'POST'])
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for("app_kiklearn.index"))
    #return redirect(request.args.get('next') or "showcase")


#@login_manager.unauthorized_handler
#def unauthorized_callback():
#def unauthorized_handler():
#    return 'Unauthorized'
#
#    session['next_url'] = request.path
#    return redirect('/login/')
#and then in login view:
#
#def login():
#    # ... if success
#    next_url = session.get('next_url', '/')
#    session.clear()
#    return redirect(next_url)

# ---------------------------------------------------------
# CHANGE PASSWORD
# ---------------------------------------------------------
"""
@app_auth.route('password_forgot', methods=['GET', 'POST'])
def password_forgot():
    form = ForgotPasswordForm()

    if request.method == 'POST' and form.validate_on_submit():
        mailconn.send_email('megan@carebooker.com',
            'aws test subject!!!',
            '<p>hi</p>',
            form.email.data,
            format="html")
        return render_template('/showcase/forgot-password-notice.html', email=form.email)

    return render_template('password_forgot.html', form=form)
"""

"""
# RESET PASSWORD PAGE (AFTER FOLLOWING EMAIL LINK)
@app_auth.route('password_reset', methods=['GET', 'POST'])
def password_reset():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        return redirect('/showcase')

    return render_template('/password_reset.html', form=form)
"""


"""
@app_auth.route('password_change', methods=['GET', 'POST'])
@login_required
def password_change():
    user = col_user.find_one({ "_id": ObjectId(current_user.get_id()) })
    form = PasswordChange_Form()

    if request.method == 'POST' and form.form_id.data == "form_password_change" and form.validate_on_submit():
        password_hash = generate_password_hash(form.password_new.data.strip())
        #user['password_hash'] = password_hash
        col_user.update(
          { "_id": ObjectId(current_user.get_id()) },
          { "$set": {
              "password_hash": password_hash
            }
          }
        )
        user = col_user.find_one({ "_id": ObjectId(current_user.get_id()) })
        user_obj = User(user)
        if login_user(user_obj):

            if user['role'] == "customer":
                return redirect(request.args.get("next") or url_for("receiver_profile"))
                #return redirect(request.args.get('next') or "showcase/account/receiver/profile")
            elif user['role'] == "provider":
                return redirect(request.args.get('next') or url_for("provider_profile"))
                #return redirect(request.args.get('next') or "showcase/account/provider/profile")

    return render_template( '/password_change.html',
      form=form,
      user=user )
"""

"""
@app_auth.route('email_change', methods=['GET', 'POST'])
@login_required
def email_change():
    user = col_user.find_one({ "_id": ObjectId(current_user.get_id()) })
    form = EmailChange_Form()

    if request.method == 'POST' and form.form_id.data == "form_email_change" and form.validate_on_submit():
        email = form.password.data.strip().lower()
        col_user.update(
          { "_id": user['_id'] },
          { "$set": {
              "email": email
            }
          }
        )
        user = col_user.find_one({ "_id": ObjectId(current_user.get_id()) })
        user_obj = User(user)
        if login_user(user_obj):

            if user['role'] == "customer":
                return redirect(request.args.get("next") or url_for("receiver_profile"))
                #return redirect(request.args.get('next') or "showcase/account/receiver/profile")
            elif user['role'] == "provider":
                return redirect(request.args.get('next') or url_for("provider_profile"))

    return render_template( '/showcase/email_change.html',
      form=form,
      user=user )

"""
