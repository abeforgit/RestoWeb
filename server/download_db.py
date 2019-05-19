import requests
from restoweb import db
from restoweb.models import Resto, Schedule, Menu, Dish, DishType, User
import datetime


def get_float_price(pricestring):
    p = ''.join(c for c in pricestring.replace(',', '.') if c.isdigit() or c == '.')
    return float(p)


def parse_time(s):
    hourstring, minutestring = s.split(':')
    return datetime.time(hour=int(hourstring), minute=int(minutestring))

db.drop_all()
db.create_all()

seen_dishes = {}

dish_types = {}

all_restos = requests.get('https://zeus.ugent.be/hydra/api/2.0/resto/meta.json').json()

for resto_description in all_restos['locations']:
    if 'endpoint' not in resto_description:
        continue
    resto = Resto(
        name=resto_description['name'],
        zip_code="9000",
        city="Gent",
        address=resto_description['address'],
        campus=None
    )
    print(resto_description['name'])
    db.session.add(resto)
    db.session.commit()
    for openinglist in resto_description['open']['resto']:
        s = Schedule(
            time_open=parse_time(openinglist[0]),
            time_closed=parse_time(openinglist[1]),
            resto_id=resto.id
        )
        db.session.add(s)
    url = f"https://zeus.ugent.be/hydra/api/2.0/resto/menu/{resto_description['endpoint']}/overview.json"
    overview = requests.get(url).json()
    for day in overview:
        if day['open']:
            menu = Menu(
                date=datetime.datetime.strptime(day['date'], '%Y-%m-%d').date(),
                resto_id=resto.id
            )
            db.session.add(menu)
            for meal in day['meals']:
                if meal['name'] not in seen_dishes:
                    if meal['type'] not in dish_types:
                        dish_types[meal['type']] = DishType(name=meal['type'])
                    seen_dishes[meal['name']] = Dish(
                        name=meal['name'],
                        type=dish_types[meal['type']],
                        price=get_float_price(meal['price']),
                        diet=meal['kind']
                    )
                menu.dishes.append(seen_dishes[meal['name']])

        for dish in seen_dishes.values():
            db.session.add(dish)
        for dish_type in dish_types.values():
            db.session.add(dish_type)

db.session.commit()
