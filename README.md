# key-value-store
Its a test project for key store with TTL.

# Features
- This app has three APIs.
  - `GET api/values`
    - Response will be `{key1: value1, key2: value2, key3: value3...}`
  - `GET api/values?keys=key1,key2...`
    - Response will be `{key1: value1, key2: value2}`
  - `POST api/values`
    - Post body `{key1: value1, key2: value2..}`
  - `PATCH api/values`
    - Patch body will be `{key1: value1}`

# Technology I use here
- python 3.7.4
- Django 2.2
- DRF 3.11
- redis (For cache database)
- Faker (Fake data for test)

# How to run in local
- Install redis in your system and run
- Clone this repo
- Create virtualenv (I used pipenv)
- Run `pipenv shell` and `pipenv install`
- Run in your console `./runserver`
- For running test run command `python manage.py test`
