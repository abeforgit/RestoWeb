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
    # Find resto and schedules matching the given id
    # If no resto found, return 404
    resto = models.Resto.query.get_or_404(resto_id)
    schedules = models.Schedules.query.filter_by(resto_id=resto_id).all()
    return render_template("resto_info.html", resto=resto, schedules=schedules)


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/register')
def register():
    return render_template("register.html")
