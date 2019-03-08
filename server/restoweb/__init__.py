from . import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


conf = {
    "development": config.DevelopmentConfig
}

app = Flask(__name__)
app.config.from_object(conf["development"])
app.config.update(dict(
    SECRET_KEY='development key',
    SQLALCHEMY_DATABASE_URI='sqlite:///resto.db',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

db = SQLAlchemy(app)

import restoweb.routes
