import os

from dotenv import load_dotenv
from flask import Flask
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy

load_dotenv()


db = SQLAlchemy()

api = Api(version='1.0',
          title='PaymentGateway - API',
          description='Passerelle de paiement - GTI525:H19',
          )

def create_app(config=None):
    app = Flask(__name__)
    if config is None:
        config = os.getenv('APP_SETTINGS')  # config_name = "development"

    app.config.from_object(config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    api.init_app(app)
    db.init_app(app)

    from app.models.users import Admin, Merchant, User
    from app.models.trasactions import Transaction

    from app.routes import main
    from app.routes import api as apis

    return app