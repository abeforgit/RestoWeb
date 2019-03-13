from restoweb import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)


class Resto(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(50), nullable=False)

    zip_code = db.Column(db.String(10))
    city = db.Column(db.String(30))
    address = db.Column(db.String(50))

    campus = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True)


class Schedules(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    time_open = db.Column(db.Time)
    working_time = db.Column(db.Integer)

    resto_id = db.Column(db.Integer, db.ForeignKey('resto.id'))


class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    date = db.Column(db.Date)

    resto_id = db.Column(db.Integer, db.ForeignKey('resto.id'))
