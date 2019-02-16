from flask import jsonify
from flask_restplus import Resource, fields, reqparse

from app import api_V1
from app.schemas import TransactionCreateSchema, TransactionConfirmCancelSchema
from app.utils.decorators import parse_with, HasApiKey
from app.utils.http_codes import *

MERCHANT_API_KEY = "Merchant API_KEY"

tn = api_V1.namespace('transaction', description='Transaction operations')

credit_card_model = tn.model('Credit Card', {
    'number': fields.Integer(required=True, example="356938035643809"),
    'cvv': fields.Integer(required=True, example="765"),
    'exp_month': fields.Integer(required=True, example=10),
    'exp_year': fields.Integer(required=True, example=22),
})

merchant_model = tn.model("Merchant", {
    'name': fields.String(required=True, example="Simons"),
    'id': fields.String(required=True, example="D84D0C669C3C48779A217CD7C7EC00CC"),
})

transaction_model = tn.model('Transactions', {
    'first_name': fields.String(required=True, example="John"),
    'last_name': fields.String(required=True, example="Doe"),
    'amount': fields.Integer(min=0, required=True, example=100),
    'purchase_desc': fields.String(required=True, example="PURCHASE/ Simons "),
    'credit_card': fields.Nested(credit_card_model),
    'merchant': fields.Nested(merchant_model),
})

API_KEY = "API_KEY"
# api_parser = tn.parser()
# api_parser.add_argument(API_KEY, location="headers")

api_parser = reqparse.RequestParser()
api_parser.add_argument('API_KEY')

@tn.route("/create")
class TransactionResourceCreate(Resource):
    """
    Endpoint for singular transaction
    """

    @tn.expect(transaction_model)
    @tn.response(200, SUCCESS, headers={API_KEY: MERCHANT_API_KEY})
    @tn.response(400, INVALID)
    @tn.response(401, UNAUTHORIZED_ACCESS)
    @HasApiKey(api_parser)
    @parse_with(TransactionCreateSchema(strict=True))
    def post(self, **kwargs):
        return jsonify({"result": SUCCESS})


@tn.route("/<int:trans_id>/confirm")
class TransactionResourceConfirmation(Resource):
    """
    Endpoint for transaction confirmation
    """

    @HasApiKey(api_parser)
    @tn.expect(transaction_model)
    @tn.response(200, SUCCESS, headers={API_KEY: MERCHANT_API_KEY})
    @tn.response(400, INVALID)
    @tn.response(401, UNAUTHORIZED_ACCESS)
    @parse_with(TransactionConfirmCancelSchema(strict=True))
    def post(self, **kwargs):
        return jsonify({"result": SUCCESS})


@tn.route("/<int:trans_id>/cancel")
class TransactionResourceCancel(Resource):
    """
    Endpoint for transaction cancel
    """

    @HasApiKey(api_parser)
    @tn.expect(transaction_model, envelope='resource')
    @tn.response(200, SUCCESS, headers={API_KEY: MERCHANT_API_KEY})
    @tn.response(400, INVALID)
    @tn.response(401, UNAUTHORIZED_ACCESS)
    @parse_with(TransactionConfirmCancelSchema(strict=True))
    def post(self, **kwargs):
        return jsonify({"result": SUCCESS})



