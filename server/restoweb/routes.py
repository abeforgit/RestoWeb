from restoweb import app
from restoweb import db
from restoweb.models import Resto, Schedule, Menu, Dish, DishType
from flask import render_template, url_for, request, jsonify, Response
from datetime import datetime
from restoweb.util import get_home_url, get_menus_url, get_restos_url, resto_from_url, dish_from_url

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/restos', methods=['GET', 'POST'])
def restos():
    if request.method == 'GET':
        db_restos = Resto.query.all()

        resto_list = [{
            'name': resto.name,
            'url': resto.get_info_url()
        } for resto in db_restos]

        return jsonify(
            restos=resto_list,
            home=get_home_url()
        )

    elif request.method == 'POST':
        name = request.json['name']
        zip_code = request.json['location']['zip_code']
        city = request.json['location']['city']
        address = request.json['location']['address']
        campus = request.json['location']['campus']
        description = request.json['description']

        db.session.add(Resto(
            name=name,
            zip_code=zip_code,
            city=city,
            address=address,
            campus=campus,
            description=description
        ))

        db.session.commit()

        return Response(status=201)


@app.route('/restos/<int:resto_id>', methods=['GET', 'DELETE'])
def restos_info(resto_id):
    db_resto = Resto.query.get_or_404(resto_id)
    db_schedules = Schedule.query.filter_by(resto_id=resto_id).all()
    if request.method == 'GET':
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

    elif request.method == 'DELETE':
        db.session.delete(db_resto)
        db.session.commit()

        return Response(status=200)


@app.route('/restos/<int:resto_id>/menus', methods=['GET', 'POST'])
def restos_menus(resto_id):
    db_resto = Resto.query.get_or_404(resto_id)
    db_menus_query = Menu.query.filter_by(resto_id=db_resto.id)
    if request.method == 'GET':
        page = request.args.get('page', default=1, type=int)
        per_page = 15

        db_menus_paginate = db_menus_query.order_by(Menu.date.desc()).paginate(page, per_page, error_out=False).items
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

    elif request.method == 'POST':
        dishes = request.json["dishes"]

        menu_date = request.json["date"]
        menu_date_datetime = datetime.strptime(menu_date, '%a, %d %b %Y %H:%M:%S %Z')

        menu = Menu(
            date=menu_date_datetime,
            resto_id=db_resto.id
        )

        for dish in dishes:
            menu.dishes.append(dish_from_url(dish["url"]))

        db.session.add(menu)
        db.session.commit()
        return Response(status=201)


@app.route('/menus', methods=['GET'])
def menus():
    if request.method == 'GET':
        page = request.args.get('page', default=1, type=int)
        per_page = 15

        db_menus_paginate = Menu.query.order_by(Menu.date.desc()).paginate(page, per_page, error_out=False).items

        menu_list = [{
            'url': menu.get_info_url(),
            'date': menu.date
        } for menu in db_menus_paginate]

        return jsonify(
            menus=menu_list,
            home=get_home_url()
        )

@app.route('/menus/<int:menu_id>', methods=['GET', 'DELETE'])
def menus_info(menu_id):
    menu = Menu.query.get_or_404(menu_id)
    if request.method == "GET":
        dish_list = [{
            'url': dish.get_info_url(),
            'name': dish.name,
            'price': dish.price,
            'type': dish.type.name,
            'diet': dish.diet
        } for dish in menu.dishes]

        resto = Resto.query.get_or_404(menu.resto_id)

        return jsonify(
            url=menu.get_info_url(),

            date=menu.date,
            dishes=dish_list,
            resto=resto.get_info_url(),

            index=get_menus_url()
        )
    elif request.method == "DELETE":
        db.session.delete(menu)
        db.session.commit()
        return Response(status=200)

@app.route('/menus/<int:menu_id>/dishes', methods=['GET', 'POST'])
def menus_dishes(menu_id):
    menu = Menu.query.get_or_404(menu_id)
    if request.method == 'GET':
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
        for dish in request.json["dishes"]:
            menu.dishes.append(dish_from_url(dish["url"]))
        db.session.commit()
        return Response(status=200)


@app.route('/dishes', methods=['GET', 'POST'])
def dishes():
    if request.method == 'GET':
        db_dishes = Dish.query.all()

        dish_list = [{
            'url': dish.get_info_url(),
            'name': dish.name,
            'price': dish.price,
            'type': dish.type.name,
            'diet': dish.diet
        } for dish in db_dishes]

        return jsonify(
            dishes=dish_list,
            home=get_home_url()
        )

    elif request.method == 'POST':
        dish_name = request.json["name"]
        dish_price = float(request.json["price"])
        dish_diet = request.json["diet"]
        dish_type_str = request.json["type"]

        dish_type = DishType.query.filter_by(name = dish_type_str).first()
        if dish_type == None:
            dish_type = DishType(name=dish_type_str)
            db.session.add(dish_type)

        dish = Dish(name=dish_name, price=dish_price, diet=dish_diet, type=dish_type)
        db.session.add(dish)
        db.session.commit()
        return Response(status=201)

@app.route('/dishes/<int:dish_id>', methods=['GET', 'DELETE'])
def dishes_info(dish_id):
    dish = Dish.query.get_or_404(dish_id)
    if request.method == 'GET':
        return jsonify(
            url=dish.get_info_url(),

            name=dish.name,
            type=dish.type.name,
            price=dish.price,
            diet=dish.diet
        )

    elif request.method == 'DELETE':
        db.session.delete(dish)
        db.session.commit()
        return Response(status=200)
