#!/bin/bash

# Running dokku commands for django manage.py

python manage.py makemigrations && python manage.py migrate && python manage.py update_countries_plus

# Processes has ended
