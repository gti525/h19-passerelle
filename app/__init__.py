import os

from dotenv import load_dotenv
from flask import Flask
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)
app.config.from_object(os.getenv('APP_SETTINGS'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app, version='1.0', title='PaymentGateway - API',
    description='Passerelle de paiement - GTI525:H19',
)
db = SQLAlchemy(app)

from app.routes import main
from app.routes import api


if __name__ == '__main__':
    app.run(debug=True)
