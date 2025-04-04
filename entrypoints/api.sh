#!/bin/sh

while ! nc -z db 5432 ; do
    echo "Waiting for the PostgreSQL Server"
    sleep 3
done

python manage.py migrate
python manage.py loaddata stores categories products price_histories
python manage.py runserver 0.0.0.0:8000

