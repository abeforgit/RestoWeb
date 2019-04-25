from restoweb import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)


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

    contains_dish = db.relationship('Dish', secondary=menu_contains_dish, lazy='subquery',
                                    backref=db.backref('menu', lazy=True))


class Dish(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Float)
    diet = db.Column(db.String(50))
