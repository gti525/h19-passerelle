from flask import jsonify
from flask_restplus import Resource, fields

from app import api
from app.schemas import TransactionSchema
from app.utils.decorators import parse_with, has_api_key

ns = api.namespace('transactions', description='Transaction operations')

credit_card_model = api.model('Credit Card',{
    'first_name': fields.String(required=True, example="John"),
    'last_name': fields.String(required=True, example="Doe"),
    'number': fields.Integer(required=True,example="356938035643809"),
    'cvv': fields.Integer(required=True,example="765"),
    'exp_month': fields.Integer(required=True,example=10),
    'exp_year': fields.Integer(required=True,example=22),
})

merchant_model = api.model("Merchant",{
    'name': fields.String(required=True,example="Simons"),
})

transaction_model = api.model('Transactions', {
    'amount': fields.Fixed(min=0.01, required=True, decimals=2, example=42.12),
    'purchase_desc': fields.String(required=True,example="PURCHASE/ Simons "),
    'credit_card': fields.Nested(credit_card_model),
    'merchant': fields.Nested(merchant_model),
})

API_KEY = "API_KEY"
api_parser = ns.parser()
api_parser.add_argument(API_KEY, location="headers")

@ns.route('/')
class TransactionScalar(Resource):
    """
    Endpoint for singular transaction
    """
    @has_api_key(api_parser)
    @ns.expect(transaction_model, envelope='resource')
    @ns.response(200, 'Success',headers={API_KEY:"Merchant API_KEY"})
    @ns.response(400, 'Validation Error')
    @ns.response(401, 'Unauthorized access')

    @parse_with(TransactionSchema(strict=True))
    def post(self,**kwargs):

        return jsonify({"result": "sucess"})


class TransactionCollection(Resource):
    pass
