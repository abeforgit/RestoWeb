from restoweb import db
from restoweb.models import Resto, Dish
from flask import url_for

def get_home_url():
    return url_for('.index', _external=True)

def get_restos_url():
    return url_for('.restos', _external=True)

def get_menus_url():
    return url_for('.menus', _external=True)

def get_dishes_url():
    return url_for('.dishes', _external=True)

def resto_from_url(url):
    if (not url.startswith(get_restos_url())):
        print(f"{url} does not start with {get_restos_url()}");
        return None
    else:
        try:
            resto_id = int(url[len(get_restos_url())+1:])
            resto = Resto.query.get_or_404(resto_id)
            return resto
        except:
            return None

def dish_from_url(url):
    if (not url.startswith(get_dishes_url())):
        print(f"{url} does not start with {get_dishes_url()}");
        return None
    else:
        try:
            dish_id = int(url[len(get_dishes_url())+1:])
            dish = Dish.query.get_or_404(dish_id)
            return dish
        except:
            return None
