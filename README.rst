=====================
TicTacToe Game (python-django)
=====================

TicTacToe is written in Python (Django Web Framework), Bootstrap CSS Framework and HTML5.

This repository includes a standard patterns used by Django such as ORM, views and Django Template mix with Bootstrap framework.

Installation
------------

Clone this repository using GIT CLONE 'WEB-URL'

You must be inside the Virtual Environment to run this dependencies::

    cd <path_to_code>
    pip install -r requirements.txt

Create a admin user and run the server::

    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver

Note: If there is a migration error. Kindly delete the migrations folder and db.sqlite3
and run::

    python manage.py makemigrations game
    python manage.py migrate
    and run the server again
    
Requirements
------------

Django version 3.1.6

