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


@app.route('/resto/<int:resto_id>')
def resto_info(resto_id):
    resto = models.Resto.query.filter_by(id=resto_id).first()
    return render_template("resto_info.html", resto=resto)
