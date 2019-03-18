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


class Schedules(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    time_open = db.Column(db.Time, nullable=False)
    time_closed = db.Column(db.Time, nullable=False)

    breakfast = db.Column(db.Boolean, nullable=False)
    lunch = db.Column(db.Boolean, nullable=False)
    dinner = db.Column(db.Boolean, nullable=False)

    resto_id = db.Column(db.Integer, db.ForeignKey('resto.id'))


class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    date = db.Column(db.Date, nullable=False)

    resto_id = db.Column(db.Integer, db.ForeignKey('resto.id'))
