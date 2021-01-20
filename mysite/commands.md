### Create activate and deactivate a virtual environment

> py -m venv <venv name>

> .\<venv name>\Scripts\activate

> deactivate

### Install Django then check installation in python terminal

> pip install django

> import django
> django.get_version()
> quit()

### Create a django project

> django-admin startproject <project name>

### Make migrations and create database

> cd <directory name>
> python manage.py migrate

### Run a development server

> python manage.py runserver

### Create an application

> python manage.py startapp <application name>

### Create new migrations for the database then show the sql output

> python manage.py makemigrations <optional location>

> python manage.py sqlmigrate <directory name> <migration number>

### Create a database super user

> python manage.py createsuperuser

### Run a application specific python cli

> python manage.py shell