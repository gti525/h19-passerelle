# GTI525 - Projet Passerelle (ExclaMoney)


* [Documentation API](https://h19-passerelle.herokuapp.com/api/doc)
* [API Base Url](https://h19-passerelle.herokuapp.com/api/v1)

## Installation
* [Python](https://www.python.org/downloads/)
* [Flask](http://flask.pocoo.org/docs/1.0/installation/)

## Requis
* python3
* Flask


## Resources
Python
* [Python](https://www.python.org)

## Database

````

# init the database
python manage.py db init
# apply the migration
python manage.py db migrate
# upgrade the db
python manage.py db upgrade

OR
#execute this
./setup.sh

````
## Run tests

```
#run ALL test
pytest

#run one test
pytest tests/filename

```

## Heroku

```
#run project heroku
git push heroku <branch-name>


#run local branch on heroku
git push heroku <branch-name>:master

```
