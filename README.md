# Superheroes API

A Flask RESTful API for managing superheroes and their powers, with proper many-to-many relationships and validations.

## Features

- RESTful endpoints for heroes, powers, and hero-power associations
- Proper many-to-many relationships between heroes and powers
- Data validation for power descriptions and hero-power strengths
- Error handling with appropriate HTTP status codes
- SQLite database with Flask-SQLAlchemy ORM

## Database Schema

![ER Diagram](https://example.com/er-diagram.png) 

- **Heroes**: Store superhero information
- **Powers**: Store superpower information
- **HeroPowers**: Association table with strength attribute

## API Endpoints

### Heroes

| Endpoint | Method | Description | Response Format |
|----------|--------|-------------|-----------------|
| `/heroes` | GET | Get all heroes | Array of hero objects |
| `/heroes/<int:id>` | GET | Get a specific hero | Hero object with powers |

### Powers

| Endpoint | Method | Description | Response Format |
|----------|--------|-------------|-----------------|
| `/powers` | GET | Get all powers | Array of power objects |
| `/powers/<int:id>` | GET | Get a specific power | Power object |
| `/powers/<int:id>` | PATCH | Update a power's description | Updated power object |

### HeroPowers

| Endpoint | Method | Description | Response Format |
|----------|--------|-------------|-----------------|
| `/hero_powers` | POST | Create a hero-power association | Created association with hero and power details |

## Request/Response Examples

### GET /heroes
**Response:**
```json
[
  {
    "id": 1,
    "name": "Kamala Khan",
    "super_name": "Ms. Marvel"
  }
]

```


### GET /heroes/1
**Response:**
```json
{
  "id": 1,
  "name": "Kamala Khan",
  "super_name": "Ms. Marvel",
  "hero_powers": [
    {
      "hero_id": 1,
      "id": 1,
      "power": {
        "description": "gives the wielder the ability to fly...",
        "id": 2,
        "name": "flight"
      },
      "power_id": 2,
      "strength": "Strong"
    }
  ]
}
```



### POST /hero_powers
**Response:**
```json
{
  "id": 11,
  "hero_id": 3,
  "power_id": 1,
  "strength": "Average",
  "hero": {
    "id": 3,
    "name": "Gwen Stacy",
    "super_name": "Spider-Gwen"
  },
  "power": {
    "description": "gives the wielder super-human strengths",
    "id": 1,
    "name": "super strength"
  }
}
```


### Error Responses
**Response:**
```json
{
  "error": "Hero not found"
}
```

### Validation errors
**Response:**
```json
{
  "errors": ["Description must be at least 20 characters long"]
}
```

## Setup

1.clone the repo.
`git clone git@github.com:Elizabeth-NN/superheroes.git`

2.Create and activate a virtual environment:

Run `pipenv install` to install the dependencies and `pipenv shell` to enter
your virtual environment before running the code.

```console
$ pipenv install
$ pipenv shell
```
3.Initialize the database:

```console
$ cd server
$ flask db init
$ flask db migrate -m "initial migration"
$ flask db upgrade
```

4.Seed the database:
```
python3 seed.py
```

5.Run the application

```
flask run
```

## Tech Stack:
Python 3

Flask

Flask-SQLAlchemy

Flask-Migrate

## License

MIT license