# RESTO API DOCUMENTATION
https://groep22.webdev.ilabt.imec.be/

## /restos
### GET
Returns a list of all restos

**Header:** Content-Type: application/json  
**Response**:  
```
{
    restos: [
        { "name": "Resto Example",
          "url": "https://groep22.webdev.ilabt.imec.be/restos/1"
        }
    ]
    home: https://groep22.webdev.ilabt.imec.be/
}
```

### POST
Adds a new resto  
**Header:** Content-Type: application/json  
**Body**:  
```
{
    "name": "Resto Example",
    "description": "Description example"
    "location": {
        "zip_code": "0000",
        "city": "City example",
        "address": "Address example",
        "campus": "Campus example"
    }
}
```

## /restos/<int:resto_id>
### GET 
Returns all information of the resto belonging to resto_id

**Header:** Content-Type: application/json  
**Response:** 
```
{
    "url": "https://groep22.webdev.ilabt.imec.be/restos/1"
    "name": "Resto Example",
    "description": "Description example",
    "location": {
        "zip_code": "0000",
        "city": "City example",
        "address": "Address example",
        "campus": "Campus example"
    }
   "menus": {
        "url": "https://groep22.webdev.ilabt.imec.be/restos/1/menus"
    },
    "schedules": [
        {
            "time_open": "11:15:00",
            "time_closed": "14:00:00"
        }
    ],
    "index": "https://groep22.webdev.ilabt.imec.be/restos"
}
```

### DELETE
Deletes the resto belonging to resto_id

## /restos/<int:resto_id>/menus
### GET
Returns a list of menus of the resto belonging to resto_id

**Header:** Content-Type: application/json
**Parameters:**: 
- page (default=1)  

**Response:**
```
{
    "url": "https://groep22.webdev.ilabt.imec.be/1/menus",
    "resto": {
        "url": "https://groep22.webdev.ilabt.imec.be/restos/1"
    },
    "menus": [
        {
            "url": "https://groep22.webdev.ilabt.imec.be/menus/1",
            "date": "Tue, 31 Dec 2019 00:00:00 GMT"
        }
    ]
}
```

### POST
Add a new menu to this menu

**Header:** Content-Type: application/json
**Body:**
```
{
    "date": "Wed, 15 Sep 2017 00:00:00 GMT",
    "dishes": [
        {
            "url": "https://groep22.webdev.ilabt.imec.be/dishes/1"
        }
    ]
}
```

## /menus
### GET 
Returns a list of menus

**Header:** Content-Type: application/json  
**Parameters:**:  
- page (default=1)  

**Response:**
```
{
    "menus": [
        {
            "url": "https://groep22.webdev.ilabt.imec.be/menus/1",
            "date": "Tue, 31 Dec 2019 00:00:00 GMT"
        }
    ],
    "home": "https://groep22.webdev.ilabt.imec.be/"
}
```

## /menus/<int:menu_id>
### GET
Returns the menu belonging to menu_id

**Header:** Content-Type: application/json  
**Response:**
```
{
    "url": "https://groep22.webdev.ilabt.imec.be/menus/1",
    "date": "Sat, 12 May 2001 00:00:00 GMT",
    "dishes": [
        {
            "url": "https://groep22.webdev.ilabt.imec.be/dishes/1",
            "name": "Hamburger",
            "price": 1.5,
            "type": "Vlees",
            "diet": "75"
        }
    ],
    "index": "https://groep22.webdev.ilabt.imec.be/menus"
}
```

### DELETE
Delete the menu belonging to menu_id

## /menus/<int:menu_id>/dishes
### GET
Returns all dishes of the menu belonging to menu_id

**Header:** Content-Type: application/json  
**Response:**
```
{
    "url": "https://groep22.webdev.ilabt.imec.be/menus/1/dishes",
    "menu": {
        "url": "https://groep22.webdev.ilabt.imec.be/menus/1"
    },
    "dishes": [
        {
            "url": "https://groep22.webdev.ilabt.imec.be/dishes/1",
            "name": "Hamburger",
            "price": 1.5,
            "type": "Vlees",
            "diet": "75"
        }
    ]
}
```

### POST
Add dishes to menu belonging to menu_id

**Header:** Content-Type: application/json
**Body:**
```
{
    "dishes": [
        {
            "url": "https://groep22.webdev.ilabt.imec.be/dishes/1"
        }
    ]
}
```

### /dishes
### GET
Returns a list of all dishes  

**Header:** Content-Type: application/json  
**Response:**
```
{
     "dishes": [
        {
            "url": "https://groep22.webdev.ilabt.imec.be/dishes/1",
            "name": "Hamburger",
            "price": 1.5,
            "type": "Vlees",
            "diet": "75"
        }
    ],
    "home": "https://groep22.webdev.ilabt.imec.be/"
}
```

### POST
Add a dish

**Header:** Content-Type: application/json
**Body:**
```
{
    "name": "Hamburger",
    "price": 1.5,
    "type": "Vlees",
    "diet": "75"
}
```

## /dishes/<int:dish_id>
### GET
Returns information of dish belonging to dish_id

**Header:** Content-Type: application/json  
**Response:**
```
{
    "url": "https://groep22.webdev.ilabt.imec.be/dishes/1",
    "name": "Hamburger",
    "price": 1.5,
    "type": "Vlees",
    "diet": "75"  
}
```

### DELETE
Deletes the dish belonging to dish_id  
