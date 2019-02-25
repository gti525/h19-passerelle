from flask import jsonify
from flask_restplus import Resource, fields, reqparse

from app import api_V1
from app import db
from app.models.trasactions import Transaction
from app.models.users import Merchant
from app.schemas import TransactionCreateSchema, TransactionConfirmSchema
from app.utils.decorators import parse_with, HasApiKey
from app.utils.genrators import random_with_N_digits
from app.utils.http_codes import *

MERCHANT_API_KEY = "Merchant API_KEY"
API_KEY = "API_KEY"

tn = api_V1.namespace('transaction', description='Transaction operations')

credit_card_model = tn.model('Credit Card', {
    'first_name': fields.String(required=True, example="John"),
    'last_name': fields.String(required=True, example="Doe"),
    'number': fields.Integer(required=True, example="1111222233334444"),
    'cvv': fields.Integer(required=True, example="765"),
    'exp': fields.String(required=True, example="10/22"),
})

merchant_model = tn.model("Merchant", {
    'name': fields.String(required=True, example="Simons"),
    'id': fields.String(required=True, example="D84D0C669C3C48779A217CD7C7EC00CC"),
})

transaction_model = tn.model('Transactions', {
    API_KEY: fields.String(required=True, example="1234567890"),
    'amount': fields.Integer(min=0, required=True, example=100),
    'purchase_desc': fields.String(required=True, example="PURCHASE/ Simons "),
    'credit_card': fields.Nested(credit_card_model),
    'merchant': fields.Nested(merchant_model),
})

# Model for transaction cancellation
cancellation_model = tn.model('Transaction cancellation', {
    'transaction_number': fields.String(required=True, example="1234567890"),
    API_KEY: fields.String(required=True, example="98765431235465"),
})

# Model for transaction confirmation
confirmation_model = tn.model('Transaction confirmation', {
    'transaction_number': fields.String(required=True, example="1234567890"),
    API_KEY: fields.String(required=True, example="98765431235465"),
})

#transactio success model
success_transaction_modal = tn.model('Sucessful transaction', {
    'transaction_number': fields.String(example="3330382145"),
    "result": fields.String(example=SUCCESS),
})
api_parser = reqparse.RequestParser()
api_parser.add_argument('API_KEY')


@tn.route("/create")
class TransactionResourceCreate(Resource):
    """
    Endpoint for singular transaction
    """

    @tn.expect(transaction_model)
    @tn.response(200, SUCCESS,success_transaction_modal)
    @tn.response(400, INVALID)
    @tn.response(401, UNAUTHORIZED_ACCESS)
    @HasApiKey(api_parser)
    @parse_with(TransactionCreateSchema(strict=True))
    def post(self, **kwargs):
        entity = kwargs["entity"]
        transaction = Transaction(
            id=random_with_N_digits(10),
            first_name=entity["credit_card"]["first_name"],
            last_name=entity["credit_card"]["last_name"],
            credit_card_number=entity["credit_card"]["number"],
            exp=entity["credit_card"]["exp"],
            cvv=entity["credit_card"]["cvv"],
            amount=entity["amount"],
            label=entity["purchase_desc"],
            merchant_id=entity["merchant"]["id"]
        )

        transaction_valid = True

        try:
            # Validate API KEY
            merchant = Merchant.query.filter_by(id=entity["API_KEY"]).first()

           # if merchant is None:
           #     transaction_valid = False



            if transaction_valid:
                db.session.add(transaction)
                db.session.commit()
                return jsonify({"result": SUCCESS, "transaction_number": transaction.id})
            else:
                return jsonify({"result": INVALID}),400
        except ValueError:
            return jsonify({"result": INVALID}), 400


@tn.route("/<string:trans_id>/confirm")
class TransactionResourceConfirmation(Resource):
    """
    Endpoint for transaction confirmation
    """

    @HasApiKey(api_parser)
    @tn.expect(confirmation_model)
    @tn.response(200, SUCCESS)
    @tn.response(400, INVALID)
    @tn.response(401, UNAUTHORIZED_ACCESS)
    @parse_with(TransactionConfirmSchema(strict=True))
    def post(self, **kwargs):
        return jsonify({"result": SUCCESS})


def processCreditCard():
    headers ={"X-API-KEY":"15489123311"}

