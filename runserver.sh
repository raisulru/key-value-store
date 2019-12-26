#!/bin/bash
pipenv install
python manage.py migrate
python manage.py runserver