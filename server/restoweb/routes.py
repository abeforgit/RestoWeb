from restoweb import app
from restoweb import db
from restoweb.models import Resto, Schedule, Menu, Dish
from flask import render_template, url_for
from flask import request
from flask import jsonify


def get_home_url():
    return url_for('.index', _external=True)


def get_restos_url():
    return url_for('.restos', _external=True)


def get_menus_url():
    return url_for('.menus', _external=True)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/restos', methods=['GET', 'POST'])
def restos():
    if request.method == 'GET':
        db_restos = Resto.query.all()
        if request.content_type == 'application/json':
            resto_list = [{
                'name': resto.name,
                'url': resto.get_info_url()
            } for resto in db_restos]

            return jsonify(
                restos=resto_list,
                home=get_home_url()
            )
        else:
            return render_template("restos.html", resto_list=db_restos)

    elif request.method == 'POST':
        name = request.form['user']
        zip_code = request.form['zip_code']
        city = request.form['city']
        address = request.form['address']
        campus = request.form['campus']
        description = request.form['description']

        db.session.add(Resto(
            name=name,
            zip_code=zip_code,
            city=city,
            address=address,
            campus=campus,
            description=description
        ))

        db.session.commit()

        return f"{name} added"


@app.route('/restos/<int:resto_id>', methods=['GET', 'DELETE'])
def restos_info(resto_id):
    db_resto = Resto.query.get_or_404(resto_id)
    db_schedules = Schedule.query.filter_by(resto_id=resto_id).all()
    if request.method == 'GET':
        if request.content_type == 'application/json':
            schedule_result = [{
                'time_open': schedule.time_open.isoformat(),
                'time_closed': schedule.time_closed.isoformat()
            } for schedule in db_schedules]

            location = {
                'zip_code': db_resto.zip_code,
                'city': db_resto.city,
                'address': db_resto.address,
                'campus': db_resto.campus
            }

            menu_list = {
                'url': db_resto.get_menus_url()
            }

            return jsonify(
                url=db_resto.get_info_url(),

                name=db_resto.name,
                description=db_resto.description,
                location=location,
                menus=menu_list,
                schedules=schedule_result,

                index=get_restos_url()
            )
        else:
            return render_template("restos_info.html", resto=db_resto, schedules=db_schedules)

    elif request.method == 'DELETE':
        db.session.delete(db_resto)
        db.session.delete(db_schedules)
        db.session.commit()

        return f"{db_resto.name} deleted"


@app.route('/restos/<int:resto_id>/menus', methods=['GET', 'DELETE'])
def restos_menus(resto_id):
    db_resto = Resto.query.get_or_404(resto_id)
    db_menus_query = Menu.query.filter_by(resto_id=db_resto.id)
    if request.method == 'GET':
        page = request.args.get('page', default=1, type=int)
        per_page = 15

        db_menus_paginate = db_menus_query.order_by(Menu.date.desc()).paginate(page, per_page, error_out=False).items
        if request.content_type == 'application/json':
            menu_list = [{
                'url': menu.get_info_url(),
                'date': menu.date
            } for menu in db_menus_paginate]

            resto_key = {
                'url': db_resto.get_info_url()
            }

            return jsonify(
                url=db_resto.get_menus_url(),

                resto=resto_key,
                menus=menu_list
            )
    elif request.method == 'DELETE':
        db_menus = db_menus_query.all()
        db.session.delete(db_menus)
        db.session.commit()

        return f"All menus of {db_resto.name} deleted"


@app.route('/menus', methods=['GET', 'POST'])
def menus():
    if request.method == 'GET':
        page = request.args.get('page', default=1, type=int)
        per_page = 15

        db_menus_paginate = Menu.query.order_by(Menu.date.desc()).paginate(page, per_page, error_out=False).items
        if request.content_type == 'application/json':
            menu_list = [{
                'url': menu.get_info_url(),
                'date': menu.date
            } for menu in db_menus_paginate]

            return jsonify(
                menus=menu_list
            )
    elif request.method == 'POST':
        pass


@app.route('/menus/<int:menu_id>')
def menus_info(menu_id):
    menu = Menu.query.get_or_404(menu_id)
    if request.content_type == 'application/json':
        dish_list = [{
            'url': dish.get_info_url(),
            'name': dish.name,
            'price': dish.price,
            'type': dish.type.name,
            'diet': dish.diet
        } for dish in menu.dishes]

        return jsonify(
            url=menu.get_info_url(),

            date=menu.date,
            dishes=dish_list,

            index=get_menus_url()
        )


@app.route('/menus/<int:menu_id>/dishes', methods=['GET', 'POST'])
def menus_dishes(menu_id):
    if request.method == 'GET':
        menu = Menu.query.get_or_404(menu_id)
        if request.content_type == 'application/json':
            dish_list = [{
                'url': dish.get_info_url(),
                'name': dish.name,
                'price': dish.price,
                'type': dish.type.name,
                'diet': dish.diet
            } for dish in menu.dishes]

            menu_key = {
                'url': menu.get_info_url()
            }

            return jsonify(
                url=menu.get_dishes_url(),

                menu=menu_key,
                dishes=dish_list
            )
    elif request.method == 'POST':
        pass


@app.route('/dishes', methods=['GET', 'POST'])
def dishes():
    if request.method == 'GET':
        if request.content_type == 'application/json':
            db_dishes = Dish.query.all()
            dish_list = [{'name': dish.name,
                          'url': dish.get_info_url()} for dish in db_dishes]

            return jsonify(
                dishes=dish_list
            )
    elif request.method == 'POST':
        pass


@app.route('/dishes/<int:dish_id>', methods=['GET', 'DELETE', 'PUT'])
def dishes_info(dish_id):
    dish = Dish.query.get_or_404(dish_id)
    if request.method == 'GET':
        if request.content_type == 'application/json':
            return jsonify(
                name=dish.name,
                type=dish.type.name,
                price=dish.price,
                diet=dish.diet,

                url=dish.get_info_url()
            )
    elif request.method == 'DELETE':
        db.session.delete(dish)
    elif request.method == 'PUT':
        pass
    db.session.commit()

