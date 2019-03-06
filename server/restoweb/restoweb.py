import os
from . import config
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash

conf = {
    "development": config.DevelopmentConfig
}

app = Flask(__name__)
app.config.from_object(conf["development"])
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'restoweb.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


@app.route('/')
def hello():
    return "hello world"
