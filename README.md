# hh-repository
# wpp project 

This is a simple web page parser project has the fullowing features
1. You simply fill the form providing site's url, give it a name, set time limit, and number of pages to be parsed.
2. it will look the sites main page and find the urls related the page's of the site and parse the html content.
3. Then it will save it the database (postgresql database).
4. And some others.

for running this project you should have docker engine installed on your host machine
if you have that then follow the commands bellow

- docker compose up --build

And you will set up the environment on docker

list the running docker containers
- docker ps

By this command you will access to the cli of the wppdjango service container
- docker exec -it [name of server service container] bash

      There you can run django project commands like
      - python manage.py migrate
      - python manage.py makemigrations
      - python manage.py createsuperuser

To start the project simply copy and paste the url bellow on your browser
- http://127.0.0.1:8000

the project will show up 

To enter the cli of pgqldb service container
- docker exec -it [name of database service container] psql -U postgres

## if you dont have docker
I recommend using 'virtualenv' as follow
- virtualenv 'environment name'

if you are on windows
- .\'environment name'\Scripts\activate
- pip install -r requirements.txt

Chagen the database configuration on settings.py 
- python manage.py makemigrations
- python manage.py migrate
- python manage.py runserver

and you are ready to go
