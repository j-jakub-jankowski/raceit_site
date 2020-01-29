## RaceIT
Site to show information about race and competitors results. Used in LAN in the place of race office.


## Technologies
Project is created with:
* Django 3.0.1
* channels 2.4.1
* Bootstrap 4
* SQLite


## Setup
* Clone the project:
git clone <...>
* Create and start a a virtual environment:
virtualenv env --no-site-packages
source env/bin/activate
* Install the project dependencies:
pip install -r requirements.txt
* To start the development server:
python manage.py runserver


The database contains sample data and superuser:
login: test
password: test

Folder chrono_files contains sample chronotrack file and could be use to test live results.


## Features
* Creating race, adding info about them, rules and routes,
* Showing start list and results,
* Loading result data from chronotrack file,
* Display live results - based on websocket so no need to refresh page.

#TODO:
* sorting data in admin panel
