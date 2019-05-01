from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
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
migrate = Migrate(app, db)
CORS(app)


env = Environment(
    loader=PackageLoader('restoweb', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

import restoweb.routes
import restoweb.error_routes
import restoweb.models
