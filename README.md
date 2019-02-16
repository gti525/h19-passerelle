# GTI525 - Projet Passerelle

## Installation
* [Python](https://www.python.org/downloads/)
* [Flask](http://flask.pocoo.org/docs/1.0/installation/)

## Requis
* python3
* Flask


## Resources
Python
* [Python](https://www.python.org)

Flask
* [Flask MEGA Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
* [Flask By Example - Project Setup](https://realpython.com/flask-by-example-part-1-project-setup/)
* [Plusieurs exemples de projets flask](https://realpython.com/search?q=flask)

Git
* [Brève introduction a Git](http://rogerdudler.github.io/git-guide/)

## Database

````
# Create the db in the shell
python

# now you are in the shell
from app import db
db.create_all()

# exit the shell
exit()

# init the database
python manage.py init


# apply the migration
python manage.py migrate


#upgrade the db
python manage.py upgrade


````
## Run tests

```
#run ALL test
pytest

#run one test
pytest filename

```

## Heroku

```
#run project heroku
git push heroku master


#run local branch on heroku
git push heroku branchname:master

```