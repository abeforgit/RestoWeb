from .restoweb import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.column(db.String(25), nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"User({self.id}, {self.username})"


class Resto(db.Model):
    name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Resto({self.name}, {self.location})"
