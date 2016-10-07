from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

from werkzeug.security import check_password_hash, generate_password_hash

from app import db

from app.forms import LoginForm,RegisterForm

from app.models import User

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/signup',methods=['GET', 'POST'])
def signup():
    # form = RegisterForm(request.form)
    if request.method == 'POST':
        name =request.form['Username']
        email = request.form['Email']
        password = generate_password_hash(request.form['Password'])
        user = User(name,email, password)
        db.session.add(user)
        db.session.commit()
        session['logged_in'] = True
        flash('User Registration Successful. Login')
        return redirect(url_for('auth.signin'))
    return render_template('auth/signup.html')


@auth.route('/signin/', methods=['GET', 'POST'])
def signin():

    form = LoginForm(request.form)
    if request.method == 'POST':
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            session['user_name']=user.name
            # flash('Welcome %s' % user.name)
            return redirect(url_for('dashboard'))
            # redirect(url_for('index'),user=user)
        flash('Wrong email or password', 'error-message')

    return render_template("auth/signin.html", form=form)


@auth.route('/logout/', methods=['GET', 'POST'])
def signout():
    session.pop('logged_in', None)
    return redirect(url_for('auth.signin'))