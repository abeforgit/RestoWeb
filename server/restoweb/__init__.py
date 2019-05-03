from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import LoginManager
from jinja2 import Environment, PackageLoader, select_autoescape
from . import config
from flask_cors import CORS
import os

conf = {
    "development": config.DevelopmentConfig
}

app = Flask(__name__)
app.config.from_object(conf["development"])
app.config.update(dict(
    SECRET_KEY='development key',
    SQLALCHEMY_DATABASE_URI=f"sqlite:///{os.path.join(app.root_path, 'resto.db')}",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    USERNAME='admin',
    PASSWORD='default',
    JSON_SORT_KEYS=False
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db, render_as_batch=True)
CORS(app)



env = Environment(
    loader=PackageLoader('restoweb', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

import restoweb.routes
import restoweb.error_routes
import restoweb.models

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return restoweb.models.User.query.get(int(user_id))

import restoweb.auth
