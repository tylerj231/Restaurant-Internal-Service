# Restaurant-Internal-Service
Internal service for restaurant employees which helps them to make a decision at the lunch place.

****

## Installing using GitHub

**Install PostgresSQL and create db**
- git clone https://github.com/tylerj231/Restaurant-Internal-Service.git
- cd Restaurant-Service
- python -m venv venv
- source venv/bin/activate
- pip install requirements.txt
- SECRET_KEY = your secret key
- DB_PASSWORD = your password
- DB_USER = your db username
- DB_NAME = your db name
- DB_HOST= your db hostname
- python manage.py migrate
- python manage.py runserver

****

## Running API with docker
**Docker should be installed, and db properly configured.(see above)**

- docker-compose build
- docker-compose up
- Create admin user. First: "docker exec -it [container identifier hash] bash" then: "python manage.py createsuperuser"
- To run tests: python manage.py test. (You should be inside the container)
- ##### ! **Please note:** you might need to rerun docker container upon building it, as django app might finish to initialize faster, hence will try to connect to db, which has not been initialized yet.

****

## Getting access
****Make sure ModHeader or any other browser extension for authentication is installed****

- create user via api/user/register
- get access token via api/user/token
- put access token into Authorization header in ModHeader like so: Authorization | Bearer <your access token>

## Features

- JWT authentication
- Admin panel /admin/
- API documentation is at /api/doc/swagger/
- Create/Update/Delete for all endpoints (Admin only)
- Create/Delete vote for particular daily menu (Employees)
- Other endpoints only available for view (Employees)
- Filtering daily menu by particular date.

### Models diagram
![DB_Schema](/images/DB_Schema.png)
