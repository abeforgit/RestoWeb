from restoweb import app, db
from restoweb.models import Resto, Schedule, Menu, Dish, DishType, Rating, User
from flask_login import current_user
from flask import render_template, request, jsonify, Response
from datetime import datetime
from restoweb.util import get_home_url, dish_from_url, inject_context
import math


@app.route('/')
def index():
    return render_template("index.html")


def check_admin():
    return current_user.is_authenticated and current_user.admin


@app.route('/restos', methods=['GET', 'POST'])
def restos():
    if request.method == 'GET':
        db_restos = Resto.query.all()

        resto_list = [{
            '@type': 'schema:Restaurant',
            'name': resto.name,
            'url': resto.get_info_url()
        } for resto in db_restos]

        return jsonify(inject_context({
            'restos': resto_list,
            'home': get_home_url()
        }, Resto.get_context()))

    elif request.method == 'POST':
        if not check_admin():
            return Response(status=401)
        if (not request.json):
            return Response(status=400)
        try:
            name = request.json['name']
            zip_code = request.json['location']['zip_code']
            city = request.json['location']['city']
            address = request.json['location']['address']
            campus = request.json['location']['campus']
            description = request.json['description']
        except:
            return Response(status=400)

        resto = Resto(
            name=name,
            zip_code=zip_code,
            city=city,
            address=address,
            campus=campus,
            description=description
        )

        db.session.add(resto)

        db.session.commit()

        return Response(status=201, headers={
            "Location": resto.get_info_url()
        })


@app.route('/restos/<int:resto_id>', methods=['GET', 'DELETE', 'PUT'])
def restos_info(resto_id):
    db_resto = Resto.query.get_or_404(resto_id)
    if request.method == 'GET':
        return jsonify(inject_context(db_resto.serialize_full(), Resto.get_context()))

    elif request.method == 'DELETE':
        if check_admin():
            db_schedules = Schedule.query.filter_by(resto_id=resto_id).all()
            db.session.delete(db_resto)
            for s in db_schedules:
                db.session.delete(s)
            db.session.commit()
            return Response(status=200)
        else:
            return Response(status=401)

    elif request.method == 'PUT':
        if check_admin():
            if (not request.json):
                return Response(status=400)
            try:
                db_resto.name = request.json['name']
                db_resto.zip_code = request.json['location']['zip_code']
                db_resto.city = request.json['location']['city']
                db_resto.address = request.json['location']['address']
                db_resto.campus = request.json['location']['campus']
                db_resto.description = request.json['description']
            except:
                return Response(status=400)
            db.session.commit()
            return Response(status=200)
        else:
            return Response(status=401)


@app.route('/restos/<int:resto_id>/menus', methods=['GET', 'POST'])
def restos_menus(resto_id):
    db_resto = Resto.query.get_or_404(resto_id)
    db_menus_query = Menu.query.filter_by(resto_id=db_resto.id)
    if request.method == 'GET':
        page = request.args.get('page', default=1, type=int)
        per_page = 10

        db_menus_paginate = db_menus_query.order_by(
            Menu.date.desc()).paginate(page, per_page, error_out=False).items

        menu_list = [{
            'url': menu.get_info_url(),
            '@type': 'schema:Menu'
        } for menu in db_menus_paginate]

        resto_key = {
            'url': db_resto.get_info_url()
        }

        menu_amount = db_menus_query.count()
        total_pages = math.ceil(menu_amount / per_page)
        meta = {
            'page': {
                'number': page,
                'limit': per_page,
                'total_pages': total_pages,
                'total_menus': menu_amount
            }
        }

        return jsonify(inject_context({
            'url': db_resto.get_menus_url(),

            'resto': resto_key,
            'menus': menu_list,

            'meta': meta
            }, Menu.get_context()))

    elif request.method == 'POST':
        if not check_admin():
            return Response(status=401)
        if (not request.json):
            return Response(status=400)

        try:
            dishes = request.json["dishes"]

            menu_date = request.json["date"]
            menu_date_datetime = datetime.strptime(
                menu_date, '%a, %d %b %Y %H:%M:%S %Z')
        except:
            return Response(status=400)
        menu = Menu(
            date=menu_date_datetime,
            resto_id=db_resto.id
        )

        for dish in dishes:
            menu.dishes.append(dish_from_url(dish["url"]))

        db.session.add(menu)
        db.session.commit()
        return Response(status=201, headers={
            "Location": menu.get_info_url()
        })


@app.route('/restos/<int:resto_id>/latestmenu')
def restos_latestmenu(resto_id):
    db_resto = Resto.query.get_or_404(resto_id)
    db_menu = Menu.query.filter_by(resto_id=db_resto.id).filter(Menu.date <= datetime.today()).order_by(Menu.date.desc()).first_or_404()

    return jsonify(inject_context(db_menu.serialize_full(), Menu.get_context()))


@app.route('/menus', methods=['GET'])
def menus():
    if request.method == 'GET':
        page = request.args.get('page', default=1, type=int)
        per_page = 10

        db_menu_query = Menu.query
        db_menus_paginate = db_menu_query.order_by(Menu.date.desc()).paginate(
            page, per_page, error_out=False).items

        menu_list = [{
            'url': menu.get_info_url(),
            'date': menu.date,
            '@type': 'schema:Menu'
        } for menu in db_menus_paginate]

        menu_amount = db_menu_query.count()
        total_pages = math.ceil(menu_amount / per_page)
        meta = {
            'page': {
                'number': page,
                'limit': per_page,
                'total_pages': total_pages,
                'total_menus': menu_amount
            }
        }

        return jsonify(inject_context({
            'menus': menu_list,
            'home': get_home_url(),
            'meta': meta
            }, Menu.get_context())
        )


@app.route('/menus/<int:menu_id>', methods=['GET', 'DELETE', 'PUT'])
def menus_info(menu_id):
    menu = Menu.query.get_or_404(menu_id)
    if request.method == "GET":
        return jsonify(inject_context(menu.serialize_full(), Menu.get_context()))
    elif request.method == "DELETE":
        if not check_admin():
            return Response(status=401)
        db.session.delete(menu)
        db.session.commit()
        return Response(status=200)

    elif request.method == "PUT":
        if check_admin():
            if (not request.json):
                return Response(status=400)

            try:
                dishes = request.json["dishes"]

                menu_date = request.json["date"]
                menu_date_datetime = datetime.strptime(
                    menu_date, '%a, %d %b %Y %H:%M:%S %Z')
            except:
                return Response(status=400)

            menu.date = menu_date_datetime

            for dish in dishes:
                if dish_from_url(dish["url"]) not in menu.dishes:
                    menu.dishes.append(dish_from_url(dish["url"]))

            return Response(status=200)
        else:
            return Response(status=401)


@app.route('/menus/<int:menu_id>/dishes', methods=['GET', 'POST'])
def menus_dishes(menu_id):
    menu = Menu.query.get_or_404(menu_id)
    if request.method == 'GET':
        dish_list = [dish.serialize() for dish in menu.dishes]

        menu_key = {
            'url': menu.get_info_url()
        }

        return jsonify(inject_context({
            'url': menu.get_dishes_url(),
            'menu': menu_key,
            'dishes': dish_list
            }, Dish.get_context())
        )

    elif request.method == 'POST':
        if not check_admin():
            return Response(status=401)
        if (not request.json):
            return Response(status=400)

        try:
            dishes = request.json["dishes"]
        except:
            return Response(status=400)

        for dish in dishes:
            menu.dishes.append(dish_from_url(dish["url"]))
        db.session.commit()
        return Response(status=200)


@app.route('/dishes', methods=['GET', 'POST'])
def dishes():
    if request.method == 'GET':
        db_dishes = Dish.query.all()

        dish_list = [dish.serialize() for dish in db_dishes]

        return jsonify(inject_context({
            'dishes': dish_list,
            'home': get_home_url()
        }, Dish.get_context()))

    elif request.method == 'POST':
        if not check_admin():
            return Response(status=401)
        if (not request.json):
            return Response(status=400)

        try:
            dish_name = request.json["name"]
            dish_price = float(request.json["price"])
            dish_diet = request.json["diet"]
            dish_type_str = request.json["type"]
        except:
            return Response(status=400)

        dish_type = DishType.query.filter_by(name=dish_type_str).first()
        if dish_type == None:
            dish_type = DishType(name=dish_type_str)
            db.session.add(dish_type)

        dish = Dish(name=dish_name, price=dish_price,
                    diet=dish_diet, type=dish_type)
        db.session.add(dish)
        db.session.commit()
        return Response(status=201, headers={
            "Location": dish.get_info_url()
        })


@app.route('/dishes/<int:dish_id>', methods=['GET', 'DELETE', 'PUT'])
def dishes_info(dish_id):
    dish = Dish.query.get_or_404(dish_id)
    if request.method == 'GET':
        return jsonify(
            inject_context(dish.serialize(), Dish.get_context())
        )

    elif request.method == 'DELETE':
        if check_admin():
            db.session.delete(dish)
            db.session.commit()
            return Response(status=200)
        else:
            return Response(status=401)

    elif request.method == "PUT":
        if check_admin():
            if (not request.json):
                return Response(status=400)

            try:
                dish_name = request.json["name"]
                dish_price = float(request.json["price"])
                dish_diet = request.json["diet"]
                dish_type_str = request.json["type"]
            except:
                return Response(status=400)

            dish_type = DishType.query.filter_by(name=dish_type_str).first()
            if dish_type == None:
                dish_type = DishType(name=dish_type_str)
                db.session.add(dish_type)

            dish.name = dish_name
            dish.price = dish_price
            dish.diet = dish_diet
            dish.type = dish_type
            db.session.commit()
            return Response(status=200)
        else:
            return Response(status=401)

@app.route('/dishes/<int:dish_id>/ratings', methods=['GET', 'POST'])
def ratings_info(dish_id):
    dish = Dish.query.get_or_404(dish_id)
    if request.method == 'GET':
        return jsonify(
           ratings=[{
                "rating": rating.rating,
                "user": rating.user.get_info_url(),
                "url": rating.get_rating_url()

            } for rating in dish.ratings]
        )
    elif request.method == 'POST':
        if not request.json:
            return Response(status=400)

        try:
            rating = int(request.json['rating'])
        except:
            return Response(status=400)

        if rating > 5 or rating < 1 or Rating.query.filter_by(user=current_user, dish=dish).count():
            return Response(status=400)

        rating = Rating(
                rating=rating
            )
        dish.ratings.append(rating)
        current_user.ratings.append(rating)
        db.session.add(rating)
        db.session.commit()
        return Response(status=201, headers={
            "Location": rating.get_rating_url()
        })

@app.route('/users/<int:user_id>', methods=['GET'])
def user_info(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(inject_context({
            'username': user.username,
            'ratings': [rating.serialize() for rating in user.ratings]
            }, Rating.get_context()))

@app.route('/ratings', methods=['GET'])
def ratings():
    return jsonify(inject_context(
            {'ratings': [rating.serialize() for rating in Rating.query.all()]},
            Rating.get_context()
        ))

@app.route('/ratings/<int:rating_id>', methods=['GET', 'DELETE', 'PUT'])
def rating_info(rating_id):
    rating = Rating.query.get_or_404(rating_id)
    if request.method == 'GET':
        return jsonify(inject_context(rating.serialize(), Rating.get_context()))
    elif request.method == 'DELETE':
        db.session.delete(rating)
        db.session.commit()
        return Response(status=200)
    elif request.method == 'PUT':
        if not request.json:
            return Response(status=400)

        try:
            new_rating = request.json["rating"]
        except:
            return Response(status=400)

        rating.rating = new_rating
        db.session.commit()
        return Response(status=200)
