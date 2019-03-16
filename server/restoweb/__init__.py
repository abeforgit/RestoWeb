from . import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from jinja2 import Environment, PackageLoader, select_autoescape


conf = {
    "development": config.DevelopmentConfig
}

app = Flask(__name__)
app.config.from_object(conf["development"])
app.config.update(dict(
    SECRET_KEY='development key',
    SQLALCHEMY_DATABASE_URI='sqlite:///resto.db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

db = SQLAlchemy(app)

env = Environment(
    loader=PackageLoader('restoweb', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

import restoweb.routes
import restoweb.models
