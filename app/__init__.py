import os

from dotenv import load_dotenv
from flask import Flask
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

db = SQLAlchemy()
api_V1 = Api(version='1.0', title='PaymentGateway - API',
             description='Passerelle de paiement - GTI525:H19',
             )


def create_app(config=None):
    app = Flask(__name__)
    # app.wsgi_app = ProxyFix(app.wsgi_app)

    if config is None:
        config = os.getenv('APP_SETTINGS')  # config_name = "development"

    app.config.from_object(config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.SWAGGER_UI_DOC_EXPANSION = 'list'

    db.init_app(app)

    from app.models.users import Admin, Merchant, User
    from app.models.trasactions import Transaction

    from app.routes.main import main_bp
    from app.routes.errors import error_bp
    from app.routes.api import tn

    api_V1.add_namespace(tn)
    api_V1.init_app(app)

    app.register_blueprint(error_bp)
    app.register_blueprint(main_bp)
    return app
