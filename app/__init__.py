import os
import sqlite3
from flask import Flask, render_template,g,session,url_for,abort,flash,redirect,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard',methods=['POST', 'GET'])
def dashboard():
    if request.method == 'POST':
        if not session.get('logged_in'):
            abort(401)
        db = get_db()
        db.execute('insert into entries (title, text) values (?, ?)',
                   [request.form['title'], request.form['text']])
        db.commit()
        flash('New entry was successfully posted')
        return redirect(url_for('show_entries'))

    elif request.method == 'GET':
        db = get_db()
        cur = db.execute('select title, text from entries order by id desc')
        entries = cur.fetchall()
        return render_template('dashboard.html', entries=entries)
    return render_template('dashboard.html')

"""""
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

from app.auth.controllers import auth as auth_module

app.register_blueprint(auth_module)
"""""
db.create_all()