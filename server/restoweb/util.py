from restoweb import db
from restoweb.models import Resto, User, Dish, get_dishes_url, get_restos_url
from flask import url_for
from rdflib import Graph, Literal, BNode, Namespace, RDF

def get_home_url():
    return url_for('.index', _external=True)


def resto_from_url(url):
    if (not url.startswith(get_restos_url())):
        print(f"{url} does not start with {get_restos_url()}")
        return None
    else:
        try:
            resto_id = int(url[len(get_restos_url()) + 1:])
            resto = Resto.query.get_or_404(resto_id)
            return resto
        except:
            return None


def dish_from_url(url):
    if (not url.startswith(get_dishes_url())):
        print(f"{url} does not start with {get_dishes_url()}")
        return None
    else:
        try:
            dish_id = int(url[len(get_dishes_url()) + 1:])
            dish = Dish.query.get_or_404(dish_id)
            return dish
        except:
            return None


def inject_context(d, context):
    d['@context'] = context
    return d

def build_rdfgraph():
    schemaorg = Namespace("https://schema.org/")
    ret = Graph()

    person_mapping = {}

    for user in User.query.all():
        person = BNode()

        ret.add( (person, RDF.type, schemaorg.Person) )
        ret.add( (person, schemaorg.name, Literal(user.username)) )
        ret.add( (person, schemaorg.url, Literal(user.get_info_url())) )
        person_mapping[user.username] = person

    for resto in Resto.query.all():
        resto_node = BNode()
        ret.add( (resto_node, RDF.type, schemaorg.Restaurant) )
        ret.add( (resto_node, schemaorg.name, Literal(resto.name)) )
        ret.add( (resto_node, schemaorg.description, Literal(resto.description)) )
        ret.add( (resto_node, schemaorg.url, Literal(resto.get_info_url())) )
        opening_hours = ""
        for schedule in resto.schedule:
            opening_hours += schedule.time_open.strftime("%H:%M")
            opening_hours += " - "
            opening_hours += schedule.time_closed.strftime("%H:%M")
        ret.add( (resto_node, schemaorg.openingHours, Literal(opening_hours)) )

        postal_address = BNode()
        ret.add( (postal_address, RDF.type, schemaorg.PostalAddress) )
        ret.add( (postal_address, schemaorg.postalCode, Literal(resto.zip_code)) )
        ret.add( (postal_address, schemaorg.addressLocality, Literal(resto.city)) )
        ret.add( (postal_address, schemaorg.streetAddress, Literal(resto.address)) )
        for menu in resto.menu:
            menu_node = BNode()
            ret.add( (menu_node, RDF.type, schemaorg.Menu) ) 
            ret.add( (menu_node, schemaorg.expires, Literal(menu.date.isoformat())) )
            ret.add( (menu_node, schemaorg.url, Literal(menu.get_info_url())) )

            for dish in menu.dishes:
                menu_item = BNode()
                ret.add( (menu_item, RDF.type, schemaorg.MenuItem) )
                ret.add( (menu_item, schemaorg.name, Literal(dish.name)) )
                ret.add( (menu_item, schemaorg.url, Literal(dish.get_info_url())) )
                if dish.diet == "vegan":
                    ret.add( (menu_item, schemaorg.suitableForDiet, schemaorg.VegetarianDiet) )
                    ret.add( (menu_item, schemaorg.suitableForDiet, schemaorg.VeganDiet) )
                if dish.diet == "vegetarian":
                    ret.add( (menu_item, schemaorg.suitableForDiet, schemaorg.VegetarianDiet) )

                offer = BNode()
                ret.add( (offer, RDF.type, schemaorg.Offer) )
                ret.add( (offer, schemaorg.price, Literal(dish.price)) )
                ret.add( (offer, schemaorg.priceCurrency, Literal("EUR")) )
                
                ret.add( (menu_item, schemaorg.offers, offer) )

                for db_rating in dish.ratings:
                    review = BNode()
                    ret.add( (review, RDF.type, schemaorg.Review) )
                    rating = BNode()
                    ret.add( (rating, RDF.type, schemaorg.Rating) )
                    ret.add( (rating, schemaorg.author, person_mapping[db_rating.user.username]) )
                    ret.add( (rating, schemaorg.ratingValue, Literal(db_rating.rating)) )
                    ret.add( (rating, schemaorg.url, Literal(db_rating.get_rating_url())) )

                    ret.add( (review, schemaorg.reviewRating, rating) )

                    ret.add( (offer, schemaorg.review, review) )


                ret.add( (menu_node, schemaorg.hasMenuItem, menu_item) )
                ret.add( (menu_node, schemaorg.hasMenuSection, Literal(dish.type.name)) )
            ret.add( (resto_node, schemaorg.hasMenu, menu_node) )
    return ret
