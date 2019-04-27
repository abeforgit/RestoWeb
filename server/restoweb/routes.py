from restoweb import app
from restoweb.models import Resto, Schedule, Menu, Dish
from flask import render_template
from flask import request
from flask import jsonify


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/restos', methods=['GET', 'POST'])
def restos():
    if request.method == 'GET':
        resto_list = Resto.query.all()
        if request.content_type == 'application/json':
            result = [{'name': resto.name,
                       'id': resto.get_info_url()} for resto in resto_list]
            return jsonify(
                restos=result
            )
        else:
            return render_template("restos.html", resto_list=resto_list)

    elif request.method == 'POST':
        pass


@app.route('/restos/<int:resto_id>', methods=['GET', 'DELETE'])
def restos_info(resto_id):
    if request.method == 'GET':
        resto = Resto.query.get_or_404(resto_id)
        schedules = Schedule.query.filter_by(resto_id=resto_id).all()
        if request.content_type == 'application/json':
            schedule_result = [{
                'time_open': schedule.time_open.isoformat(),
                'time_closed': schedule.time_closed.isoformat()
                } for schedule in schedules]

            location = {
                'zip_code': resto.zip_code,
                'city': resto.city,
                'address': resto.address,
                'campus': resto.campus
            }

            menus = {
                'id': resto.get_menus_url()
            }

            return jsonify(
                id=resto.get_info_url(),

                name=resto.name,
                description=resto.description,
                location=location,
                menus=menus,
                schedules=schedule_result
            )
        else:
            return render_template("restos_info.html", resto=resto, schedules=schedules)

    elif request.method == 'DELETE':
        pass


@app.route('/restos/<int:resto_id>/menus', methods=['GET', 'DELETE'])
def restos_menus(resto_id):
    if request.method == 'GET':
        resto = Resto.query.get_or_404(resto_id)
        page = request.args.get('page', default=1, type=int)
        per_page = 15

        menus = Menu.query.filter_by(resto_id=resto.id)\
                    .order_by(Menu.date.desc()).paginate(page, per_page, error_out=False).items
        if request.content_type == 'application/json':
            menu_list = [{
                'id': menu.get_info_url(),
                'date': menu.date
            } for menu in menus]

            resto_key = {
                'id': resto.get_info_url()
            }

            return jsonify(
                id=resto.get_menus_url(),

                resto=resto_key,
                menus=menu_list
            )
    elif request.method == 'DELETE':
        pass


@app.route('/menus', methods=['GET', 'POST'])
def menus():
    if request.method == 'GET':
        page = request.args.get('page', default=1, type=int)
        per_page = 15

        menus = Menu.query.order_by(Menu.date.desc()).paginate(page, per_page, error_out=False).items
        if request.content_type == 'application/json':
            menu_list = [{
                'id': menu.get_info_url(),
                'date': menu.date
            } for menu in menus]

            return jsonify(
                menus=menu_list
            )
    pass


@app.route('/menus/<int:menu_id>')
def menus_info(menu_id):
    if request.method == 'GET':
        menu = Menu.query.get_or_404(menu_id)
        if request.content_type == 'application/json':
            dishes = {
                'id': menu.get_dishes_url()
            }

            return jsonify(
                id=menu.get_info_url(),

                dishes=dishes
            )
    pass


@app.route('/menus/<int:menu_id>/dishes', methods=['GET', 'POST'])
def menus_dishes(menu_id):
    if request.method == 'GET':
        menu = Menu.query.get_or_404(menu_id)
        if request.content_type == 'application/json':
            dish_list = [{
                'id': dish.get_info_url(),
                'name': dish.name
            } for dish in menu.dishes]

            menu_key = {
                'id': menu.get_info_url()
            }

            return jsonify(
                id=menu.get_dishes_url(),

                menu=menu_key,
                dishes=dish_list
            )
    pass


@app.route('/dishes', methods=['GET', 'POST'])
def dishes():
    if request.method == 'GET':
        dishes = Dish.query.all()

        if request.content_type == 'application/json':
            dish_list = [{'name': dish.name,
                       'id': dish.get_info_url()} for dish in dishes]

        return jsonify(
            dishes=dish_list
        )
    pass


@app.route('/dishes/<int:dish_id>', methods=['GET', 'DELETE', 'PUT'])
def dishes_info(dish_id):
    if request.method == 'GET':
        dish = Dish.query.get_or_404(dish_id)
        if request.content_type == 'application/json':
            return jsonify(
                name=dish.name,
                type=dish.type,
                price=dish.price,
                diet=dish.diet,

                id=dish.get_info_url()
            )
    else:
        pass
