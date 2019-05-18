from restoweb import db, bcrypt
from restoweb.models import Resto, Schedule, Menu, Dish, DishType, User
import datetime

db.drop_all()
db.create_all()

restos = [
    Resto(
        name="Resto De Brug",
        zip_code="9000",
        city="Gent",
        address="Sint-Pietersnieuwstraat 45",
        campus="Campus Ufo"
    ),
    Resto(
        name="Resto Campus Sterre",
        zip_code="9000",
        city="Gent",
        address="Krijgslaan 281",
        campus="Campus Sterre",
        description="De resto bevindt zich in gebouw S5."
    ),
    Resto(
        name="Resto Kantienberg",
        zip_code="9000",
        city="Gent",
        address="Stalhof 45",
        description="De resto bevindt zich op het gelijkvloers van Home Canterbury."
    )
]

schedules = [
    Schedule(
        time_open=datetime.time(hour=11, minute=15),
        time_closed=datetime.time(hour=14, minute=0),

        resto_id=1
    ),
    Schedule(
        time_open=datetime.time(hour=17, minute=30),
        time_closed=datetime.time(hour=21, minute=0),

        resto_id=1
    ),

    Schedule(
        time_open=datetime.time(hour=8, minute=0),
        time_closed=datetime.time(hour=14, minute=0),

        resto_id=2
    ),
    Schedule(
        time_open=datetime.time(hour=11, minute=15),
        time_closed=datetime.time(hour=14, minute=0),

        resto_id=2
    ),

    Schedule(
        time_open=datetime.time(hour=11, minute=15),
        time_closed=datetime.time(hour=14, minute=0),

        resto_id=3
    ),
]

menus = [
    Menu(
        date=datetime.date(2001, 5, 12),
        resto_id=1
    ),

    Menu(
        date=datetime.date(2019, 12, 31),
        resto_id=1
    )
]

dish_type = DishType(
    name="Vlees"
)


menus[0].dishes.append(Dish(
    name="Hamburger",
    type=dish_type,
    price=1.50,
    diet="150+"
))

menus[0].dishes.append(Dish(
    name="Eend",
    type=dish_type,
    price=17.95
))


for resto in restos:
    db.session.add(resto)

for schedule in schedules:
    db.session.add(schedule)

for menu in menus:
    db.session.add(menu)

user = User(username='test', password_hash=bcrypt.generate_password_hash("test").decode('utf-8'))
db.session.add(user)
db.session.commit()
print("API KEY:")
print(user.apikey)
