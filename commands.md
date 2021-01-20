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