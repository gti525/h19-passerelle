import os

from flask import Flask, Blueprint, url_for
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.getenv('APP_SETTINGS'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)
db = SQLAlchemy(app)

from app.routes import main

if __name__ == '__main__':
    app.run(debug=True)
