import os
import json
import tempfile

import pytest

from restoweb import restoweb, db

"""
-   GET /
-   GET /restos
-   POST /restos
-   GET /restos/<resto_id>
-   DELETE /restos/<resto_id>
-   GET /restos/<resto_id>/menus
-   POST /restos/<resto_id>/menus
-   GET /menus
-   GET /menus/<menu_id>
-   DELETE /menus/<menu_id>
-   GET /menus/<menu_id>/dishes
-   POST /menus/<menu_id>/dishes
-   GET /dishes
-   POST /dishes
-   GET /dishes/<dish_id>
-   DELETE /dishes/<dish_id>
"""

test_resto_example = {
            "name": "Resto Example",
            "description": "Discription Example",
            "location": {
                "zip_code": "0000",
                "city": "City Example",
                "address": "Address example",
                "campus": "Campus example"
            }
         }
test_resto_example_2 = {
            "name": "Resto Example 2",
            "description": "Discription Example 2",
            "location": {
                "zip_code": "0002",
                "city": "City Example 2",
                "address": "Address example 2",
                "campus": "Campus example 2"
            }
         }
test_menu_no_dishes = {
        "date": "Wed, 15 Sep 2017 00:00:00 GMT",
        "dishes": []
    }
test_menu_no_dishes_2 = {
        "date": "Wed, 16 Sep 2017 00:00:00 GMT",
        "dishes": []
    }
test_dish = {
        "name": "Test",
        "price": 1.5,
        "type": "Test",
        "diet": "555"
    }
test_dish_2 = {
        "name": "Test 2",
        "price": 1.52,
        "type": "Test 2",
        "diet": "552"
    }

@pytest.fixture
def client():
    db_fd, restoweb.app.config['DATABASE'] = tempfile.mkstemp()
    restoweb.app.config["TESTING"] = True
    client = restoweb.app.test_client()

    db.drop_all()
    db.create_all()

    yield client

    os.close(db_fd)
    os.unlink(restoweb.app.config["DATABASE"])



def test_root(client):
    rv = client.get('/')
    assert rv.status_code == 200

def test_endpoints(client):
    # Check resto count
    rv = client.get('/restos')
    assert rv.status_code == 200, "Invalid status code from GET /restos"
    assert rv.json["restos"] == [], "Restos aren't empty on start"

    # Add resto
    rv = client.post('/restos', json=test_resto_example)
    assert rv.status_code == 201, "Invalid status code from POST /restos"

    # Add resto
    rv = client.post('/restos', json=test_resto_example_2)
    assert rv.status_code == 201 , "Invalid status code from POST /restos"

    # Check resto count
    rv = client.get('/restos')
    assert rv.status_code == 200, "Invalid status code from GET /restos"
    restos = rv.json["restos"]
    assert len(restos) == 2, "Invalid amount of restos created"

    # Check individual resto
    for resto_entry in restos:
        rv = client.get(resto_entry["url"])
        assert rv.status_code == 200, "Invalid URL for resto"
        assert rv.json["name"] == resto_entry["name"], "Names do not match"
        # Maybe check rest of content too?

    # Delete resto
    rv = client.delete(restos[0]["url"])
    assert rv.status_code == 200, "Could not delete resto"

    # Check resto count
    rv = client.get('/restos')
    assert rv.status_code == 200, "Invalid status code from GET /restos"
    assert len(rv.json["restos"]) == 1, "Invalid amount of restos deleted"
    
    # Check menus for resto
    url = restos[1]["url"] + "/menus"
    rv = client.get(url)
    assert rv.status_code == 200, "Invalid status code from GET /restos/<id>/menus"
    assert rv.json["menus"] == [], "Menus aren't empty on start"

    # Add menu to resto
    rv = client.post(url, json=test_menu_no_dishes)
    assert rv.status_code == 201, "Invalid status code from POST /restos/<id>/menus"

    # Add menu to resto
    rv = client.post(url, json=test_menu_no_dishes_2)
    assert rv.status_code == 201, "Invalid status code from POST /restos/<id>/menus"

    # Check menu count for resto
    rv = client.get(url)
    assert rv.status_code == 200, "Invalid status code from GET /restos/<id>/menus"
    menus = rv.json["menus"]
    assert len(menus) == 2, "Invalid amount of menus created"

    # Check total menu count
    rv = client.get("/menus")
    assert rv.status_code == 200, "Invalid status code from GET /menus"
    menus = rv.json["menus"]
    assert len(menus) == 2, "Invalid amount of menus returned"

    # Check individual menus
    for menu_entry in menus:
        rv = client.get(menu_entry["url"])
        assert rv.status_code == 200, "Invalid status code from GET /menus/<id>"
        assert rv.json["dishes"] == [], "Dishes in menu aren't empty on start"

    # Delete menu
    menu_url_to_delete = menus[0]["url"]
    rv = client.delete(menu_url_to_delete)
    assert rv.status_code == 200, "Invalid status code from DELETE /menus"

    # Check menu count for resto
    rv = client.get(url)
    assert rv.status_code == 200, "Invalid status code from GET /restos/<id>/menus"
    menus = rv.json["menus"]
    assert len(menus) == 1, "Invalid amount of menus"

    # Check total menu count
    rv = client.get("/menus")
    assert rv.status_code == 200, "Invalid status code from GET /menus"
    menus = rv.json["menus"]
    assert len(menus) == 1, "Invalid amount of menus returned"
    
    # Check dish count
    rv = client.get('/dishes')
    assert rv.status_code == 200, "Invalid status code from GET /dishes"
    assert rv.json["dishes"] == [], "Dishes aren't empty on start"

    # Add dish
    rv = client.post('/dishes', json=test_dish)
    assert rv.status_code == 201, "Invalid status code from POST /dishes"

    # Add dish
    rv = client.post('/dishes', json=test_dish_2)
    assert rv.status_code == 201 , "Invalid status code from POST /dishes"

    # Check dish count
    rv = client.get('/dishes')
    assert rv.status_code == 200, "Invalid status code from GET /dishes"
    dishes = rv.json["dishes"]
    assert len(dishes) == 2, "Invalid amount of dishes created"

    # Check individual dish
    for dish_entry in dishes:
        rv = client.get(dish_entry["url"])
        assert rv.status_code == 200, "Invalid URL for dish"
        assert rv.json["name"] == dish_entry["name"], "Names do not match"
        # Maybe check rest of content too?

    # Delete dish
    rv = client.delete(dishes[0]["url"])
    assert rv.status_code == 200, "Could not delete dish"

    # Check dish count
    rv = client.get('/dishes')
    assert rv.status_code == 200, "Invalid status code from GET /dishes"
    assert len(rv.json["dishes"]) == 1, "Invalid amount of dishes deleted"

    # Add dish to menu
    menu_url = menus[0]['url'] + "/dishes"
    dish_url = dishes[1]['url']
    rv = client.post(menu_url, json={
        "dishes": [
            {
                "url": dish_url
            }
        ]
    })
    assert rv.status_code == 200, "Invalid status code from POST /menus/<id>/dishes"

    # Check dish count for menu
    rv = client.get(menu_url)
    assert rv.status_code == 200, "Invalid response from GET /menus/<id>/dishes"
    assert len(rv.json["dishes"]) == 1, "Dish not added to menu"
