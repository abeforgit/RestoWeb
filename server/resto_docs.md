# Documentation

## /restos

### GET

#### Response

- Body (200):

```json
{
  "restos": [
    {
      "name": String,
      "url": String,
    }
  ],
  "home": String
}
```

### POST

#### Request

- Header: `Content-Type: application/json`
- Body:

```json
{
    "name": String,
    "location": {
        "zip_code": String,
        "city": String,
        "address": String,
        "campus": String
    },
    "description": String
}
```

#### Response

- 400: if no json body is supplied (TODO or header is missing keys)
- 401: if not logged in or not authorized
- 201 (with `location` header): if Resto is created (at the url in the `location`-header)

## /restos/(id)

### GET

#### Response

- 404: if not found
- 200 (with body): if found

Body:
```json
{
    "url": String,
    "name": String,
    "description": String,
    "location": {
        "zip_code": String,
        "city": String,
        "address": String,
        "campus": String
    },
    "menus": {
        "url": String
    },
    "schedules": [
        {
            "time_open": String,
            "time_closed": String
        }
    ],
    "index": String
}
```

### DELETE

#### Response

- 404: if not found
- 401: if not logged in or not authorized
- 200: if succesfully deleted

### PUT

Identical to `POST /menus`, except 404 if not found

## /restos/(id)/menus

### GET

Add `?page=X` for page X

#### Response

- 404: if not found
- 200 (with body): if found

Body:

```json
{
    "url": String,
    "resto": {
        "url": String
    },
    "menus": [
        {
            "url": String
        }
    ],
    "meta": {
        "page": {
            "number": Integer,
            "limit": Integer,
            "total_pages": Integer,
            "total_menus": Integer
        }
    }
}
```

### POST

#### Request

- Header: `Content-Type: application/json`
- Body:

```json
{
    "date": String (Formatted like "Mon, 6 May 2019 00:00:00 GMT"),
    "dishes": [
        {
            "url": String
        }
    ]
}
```

#### Response

- 400: if no json body is supplied (TODO or header is missing keys)
- 401: if not logged in or not authorized
- 201 (with `location` header): if Resto is created (at the url in the `location`-header)

## /menus

### GET

Add `?page=X` for page X

#### Response

```json
{
    "menus": [
        {
            "url": String,
            "date": String
        }
    ],
    "home": String,
    "meta": {
        "page": {
            "number": Integer,
            "limit": Integer,
            "total_pages": Integer,
            "total_menus": Integer
        }
    }
}
```

## /menus/(id)

### GET

#### Response

- 404: if not found
- 200 (with body): if found

Body:

```json
{
    "url": String,
    "date": String (Formatted like "Mon, 6 May 2019 00:00:00 GMT"),
    "dishes": [
        {
            "url": String
        }
    ],
    "resto": {
      "url": String
    },
    "index": String
}
```

### DELETE

#### Response

- 400: if no json body is supplied (TODO or header is missing keys)
- 401: if not logged in or not authorized
- 200: if Menu is deleted

### PUT

Identical to `POST /menus`, except 404 if not found

## /menus/(id)/dishes

### GET

#### Response

- 404: if not found
- 200 (with body): if found

Body:

```json
{
    "url": String,
    "menu": {
        "url": String
    },
    "dishes": [{
        "url": String,
        "name": String,
        "price": String,
        "type": String,
        "diet": String
    }]
}
```

### POST

#### Request

- Header: `Content-Type: application/json`
- Body:

```json
{
    "dishes": [
        {
            "url": String
        }
    ]
}
```

#### Response

- 400: if no json body is supplied (TODO or header is missing keys)
- 401: if not logged in or not authorized
- 201 (with `location` header): if Resto is created (at the url in the `location`-header)

## /dishes

### GET

#### Response

```json
{
    "dishes": [
        {
            "url": String,
            "name": String,
            "price": Float,
            "type": String,
            "diet": String
        }
    ],
    "home": String
}
```

### POST

#### Request

- Header: `Content-Type: application/json`
- Body:

```json
{
    "name": String,
    "price": Float,
    "diet": String,
    "type": String
}
```

#### Response

- 400: if no json body is supplied (TODO or header is missing keys)
- 401: if not logged in or not authorized
- 201 (with `location` header): if Resto is created (at the url in the `location`-header)

## /dishes/(id)

### GET

#### Response

```json
{
    "url": String,
    "name": String,
    "type": String,
    "price": Float,
    "diet": String
}
```

### DELETE

#### Response

- 400: if no json body is supplied (TODO or header is missing keys)
- 401: if not logged in or not authorized
- 200: if Dish is deleted

### PUT

Identical to `POST /dishes`, except 404 if not found