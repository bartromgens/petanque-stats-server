!#/usr/bin/bash

rm dev.sqlite
python manage.py migrate
python manage.py import_scores
