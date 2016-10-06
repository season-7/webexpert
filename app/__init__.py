from flask import Flask, render_template

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

from app.auth.controllers import auth as auth_module

app.register_blueprint(auth_module)
db.create_all()