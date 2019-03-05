import os

from dotenv import load_dotenv
from flask import Flask
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from flask_login import LoginManager

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
    from app.routes.login import  login_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.settings import settings_bp
    from app.routes.userManagement import userManagement_bp
    from app.routes.userModify import userModify_bp
    from app.routes.register import register_bp
    from app.routes.transaction import transaction_bp
    from app.routes.errors import page_not_found, page_error

    from app.routes.api import tn

    api_V1.add_namespace(tn)
    api_V1.init_app(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(userManagement_bp)
    app.register_blueprint(userModify_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(transaction_bp)

    app.register_error_handler(500,page_error)
    app.register_error_handler(404,page_not_found)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)



    return app
