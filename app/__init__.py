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
    from app.routes.api import tn

    api_V1.add_namespace(tn)
    api_V1.init_app(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(login_bp)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.errorhandler(404)
    def page_not_found(e):
        # note that we set the 404 status explicitly
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def page_not_found(e):
        # note that we set the 500 status explicitly
        return render_template('500.html'), 500

    return app
