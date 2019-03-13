from restoweb import app
from restoweb import models
from flask import render_template


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/restos')
def show_restos():
    resto_list = models.Resto.query.all()
    return render_template("restos.html", resto_list=resto_list)
