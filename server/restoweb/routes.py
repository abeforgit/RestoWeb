from restoweb import app
from restoweb import models
from flask import render_template
from flask import request
from flask import jsonify
from flask import url_for


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/restos', methods=['GET', 'POST'])
def restos():
    if request.method == 'GET':
        resto_list = models.Resto.query.all()
        if request.content_type == 'application/json':
            result = []
            for resto in resto_list:
                result.append({
                    'name': resto.name,
                    'id': url_for('.restos_info', resto_id=resto.id, _external=True)
                })
            return jsonify(restos=result)
        else:
            return render_template("restos.html", resto_list=resto_list)

    elif request.method == 'POST':
        pass


@app.route('/restos/<int:resto_id>', methods=['GET', 'DELETE'])
def restos_info(resto_id):
    if request.method == 'GET':
        resto = models.Resto.query.get_or_404(resto_id)
        schedules = models.Schedule.query.filter_by(resto_id=resto_id).all()
        if request.content_type == 'application/json':
            schedule_result = []
            for schedule in schedules:
                schedule_result.append({
                    'time_open': schedule.time_open.isoformat(),
                    'time_closed': schedule.time_closed.isoformat()
                })

            location = {
                'zip_code': resto.zip_code,
                'city': resto.city,
                'address': resto.address,
                'campus': resto.campus
            }

            menus = {
                'id': url_for('.restos_menus', resto_id=resto.id, _external=True)
            }

            return jsonify(name=resto.name,
                           description=resto.description,
                           location=location,
                           menus=menus,
                           schedules=schedule_result)
        else:
            return render_template("restos_info.html", resto=resto, schedules=schedules)

    elif request.method == 'DELETE':
        pass


@app.route('/restos/<int:resto_id>/menus', methods=['GET', 'DELETE'])
def restos_menus(resto_id):
    if request.method == 'GET':
        menus_result = []

        menus = models.Menu.query.filter_by(resto_id=resto_id).all()
        for menu in menus:
            dishes = models.Dish.query.filter_by(menu_id=menu.id).all()
            for dish in dishes:
                pass

    elif request.method == 'DELETE':
        pass


@app.route('/menus', methods=['GET', 'POST'])
def menus():
    pass


@app.route('/menus/<int:menu_id>')
def menus_info(menu_id):
    pass


@app.route('/menus/<int:menu_id>/dishes', methods=['GET', 'POST'])
def menus_dishes(menu_id):
    pass


@app.route('/dishes', methods=['GET', 'POST'])
def dishes():
    pass


@app.route('/dishes/<int:dish_id>', methods=['GET', 'DELETE', 'PUT'])
def dishes_info(dish_id):
    if request.method == 'GET':
        dish = models.Dish.query.get_or_404(dish_id)
    pass
