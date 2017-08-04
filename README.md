# HeadlineAPI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CircleCI](https://circleci.com/gh/BolajiOlajide/HeadlineAPI.svg?style=svg)](https://circleci.com/gh/BolajiOlajide/HeadlineAPI)

This repository contains an API for the mobile application: `HEADLINE`. `HEADLINE` is an iOS (should be coming to Android anytime soon) that helps you get relevant news and happenings from top nigerian websites.

## Development
This application was developed using [Flask](http://flask.pocoo.org/). Postgres was used for persisting data with [SQLAlchemy](https://www.sqlalchemy.org/) as [ORM](https://en.wikipedia.org/wiki/Object-relational_mapping).

### Development - Docker
Development with docker has been made simple. To get started make sure you have [docker](https://www.docker.com/) on your PC. You can download it [here](https://www.docker.com/).
Follow the following steps carefully to set the project up:
- Create a `.env` using the `.env.sample` file.
- Run the command `docker-compose up` to let the docker daemon start building the image and create the container.
- When you're done, use the command `docker-compose down` or `Ctrl + C` to stop the container.

## Application Features
###### User Authentication
Users are authenticated and validated using an `werkzeug` token. Generating tokens on login ensures each account is unique to a user and can't be accessed by an authenticated user.

## Installation
* Start up your terminal (or Command Prompt on Windows OS).
* Ensure that you've `python` installed on your PC.
* Clone the repository by entering the command `git clone https://github.com/BolajiOlajide/HeadLineAPI` in the terminal.
* Navigate to the project folder using `cd HeadLineAPI` on your terminal (or command prompt)
* After cloning, create a virtual environment then install the requirements with the command:
`pip install -r requirements.txt`.
* Create a `.env` file in your root directory as described in `.env.sample` file. Variables such as DATABASE_URL and config are defined in the .env file and it is essential you create this file before running the application.
```
FLASK_CONFIG='default'
DATABASE_URI='database connection to be used'
SECRET_KEY='random string used for generating token'
TEST_DB='database to be used for testing'
SERVER_NAME='server in which app is being tested: `localhost:5000` works.'

- Docker Variables
DB_USER=postgres
DB_PASS=postgres
DB_SERVICE=postgres
DB_PORT=5432
DB_NAME=postgres
```
* After this, you'll need to migrate data schema to the database using the command: `python manage.py create_db`.

## Usage
* A customized interactive python shell can be accessed by passing the command `python manage.py shell` on your terminal.
* Once this is done, the application can be started using `python manage.py runserver` and by default the application can be accessed at `http://127.0.0.1:5000` or `gunicorn manage:app` which starts the application using port `8000`. The application starts using the configuration settings defined in your .env file.

## Configuration
The API currently has 4 different configuration which can be defined in the .env file.
- `production`: this configuration starts the app ready for production to be deployed on any cloud application platform such as Heroku, AWS etc.
- `development`: this configuration starts the application in the development mode.
- `testing`: this configuration starts the application in a testing mode.
- `default`: this is the same as the development configuration.

## API Documentation
-----
The API has routes, each dedicated to a single task that uses HTTP response codes to indicate API status and errors.

### API Features

The following features make up the BucketList API:

#### Authentication
-   It uses itsdangerous-Serializer & werkzeug token for authentication.

-   It generates a token on successful login and returns it to the user.

-   It verifies the token to ensures a user is authenticated to access protected endpoints.

#### Users

-   It allows users to be created.

-   It allows users to login and obtain a token

-   It allows authenticated users to retrieve and update their information.

### API Resource Endpoints

URL Prefix = `http://sample_domain/` where sample domain is the root URL of the server HOST.


| EndPoint                                 | Functionality                 | Public Access|
| -----------------------------------------|:-----------------------------:|-------------:|
| **POST** /auth/register                  | Register a user               |    TRUE      |
| **POST** /auth/login                     | Logs a user in                |    TRUE      |


### Authentication
#### POST HTTP Request
-   `POST /auth/login`
INPUT:
```json
{
  "username":"username",
  "password":"password"
}
```

###### HTTP Response
-   HTTP Status: `200: OK`
JSON data
```json
{
  "token": "edasdnmdsakmkEcR4Ardmfsdamfkjdsjlasnfh)__QWEh"
}
```

#### POST HTTP Request
-   `POST /auth/register`
INPUT:
```json
{
  "username":"username",
  "password":"password"
}
```

###### HTTP Response
-   HTTP Status: `201: created`
JSON data
```json
{
  "username": "test_user"
}
```

### Author
- [Bolaji Olajide](https://twitter.com/Bolaji___)
