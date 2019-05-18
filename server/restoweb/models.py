from flask import url_for
from flask_login import UserMixin
from restoweb import db
import random
import string


def generate_api_token(size=32):
    return ''.join(
        random.SystemRandom().choice(string.ascii_letters + string.digits)
        for _ in range(size))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    apikey = db.Column(db.String(32), nullable=False, default=generate_api_token)
    ratings = db.relationship('Rating', backref='user', lazy=True)
    
    def get_info_url(self):
        return url_for('.user_info', user_id=self.id, _external=True)


class Resto(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(50), nullable=False)

    zip_code = db.Column(db.String(10), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    campus = db.Column(db.String(50))

    description = db.Column(db.Text)

    schedule = db.relationship('Schedule', backref='resto', lazy=True)
    menu = db.relationship('Menu', backref='resto', lazy=True)

    def get_info_url(self):
        return url_for('.restos_info', resto_id=self.id, _external=True)

    def get_menus_url(self):
        return url_for('.restos_menus', resto_id=self.id, _external=True)


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    time_open = db.Column(db.Time, nullable=False)
    time_closed = db.Column(db.Time, nullable=False)

    resto_id = db.Column(db.Integer, db.ForeignKey('resto.id'))


menu_contains_dish = db.Table('menu_contains_dish',
                              db.Column('menu_id', db.Integer, db.ForeignKey('menu.id'), primary_key=True),
                              db.Column('dish_id', db.Integer, db.ForeignKey('dish.id'), primary_key=True)
                              )


class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    date = db.Column(db.Date, nullable=False)

    resto_id = db.Column(db.Integer, db.ForeignKey('resto.id'))

    dishes = db.relationship('Dish', secondary=menu_contains_dish, lazy='subquery',
                             backref=db.backref('dishes', lazy=True))

    def get_info_url(self):
        return url_for('.menus_info', menu_id=self.id, _external=True)

    def get_dishes_url(self):
        return url_for('.menus_dishes', menu_id=self.id, _external=True)


class Dish(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float)
    diet = db.Column(db.String(50))
    ratings = db.relationship('Rating', backref='dish', lazy=True)

    type_id = db.Column(db.Integer, db.ForeignKey('dish_type.id'))
    type = db.relationship('DishType')

    def get_info_url(self):
        return url_for('.dishes_info', dish_id=self.id, _external=True)


class DishType(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(30), nullable=False, unique=True)

class Rating(db.Model):
    id = db.Column(db.Integer,primary_key=True)

    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    rating = db.Column(db.Integer, nullable=False)

    def get_rating_url(self):
        return url_for('.rating_info', rating_id=self.id, _external=True)
