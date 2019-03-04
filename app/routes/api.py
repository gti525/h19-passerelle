from threading import Timer

from flask import jsonify
from flask_restplus import Resource, fields, reqparse
import requests
from app import api_V1
from app import db
from app.models.trasactions import Transaction, PENDING, REFUSED
from app.models.users import Merchant
from app.schemas import TransactionCreateSchema, TransactionConfirmSchema
from app.utils.decorators import parse_with, HasApiKey
from app.utils.genrators import random_with_N_digits
from app.utils.http_codes import *
from app.utils.aes import encrypt, decrypt

MERCHANT_API_KEY = "Merchant API_KEY"
API_KEY = "API_KEY"
RESERVATION_TIME = 900  # 15 minutes in seconds

tn = api_V1.namespace('transaction', description='Transaction operations')

# date  model
date_model = tn.model('Expiration date', {
    'month': fields.Integer(example=10),
    "year": fields.Integer(example=2023),
})

credit_card_model = tn.model('Credit Card', {
    'first_name': fields.String(required=True, example="John"),
    'last_name': fields.String(required=True, example="Doe"),
    'number': fields.Integer(required=True, example="1111222233334444"),
    'cvv': fields.Integer(required=True, example="765"),
    'exp': fields.Nested(date_model),
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

# transaction success model
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
    @tn.response(200, SUCCESS, success_transaction_modal)
    @tn.response(400, INVALID)
    @tn.response(401, UNAUTHORIZED_ACCESS)
    @HasApiKey(api_parser)
    @parse_with(TransactionCreateSchema(strict=True))
    def post(self, **kwargs):
        trans = kwargs["entity"]

        transaction_valid = True

        try:
            # Validate API KEY
            merchant = Merchant.query.filter_by(api_key=trans["API_KEY"]).first()

            if merchant is None:
                transaction_valid = False

            if transaction_valid:

                r = process_credit_card(trans["amount"],
                                        merchant.name,
                                        trans["credit_card"]["number"],
                                        trans["credit_card"]["cvv"],
                                        trans["credit_card"]["exp"]["month"],
                                        trans["credit_card"]["exp"]["year"],
                                        )

                if r.status_code == 200:
                    t = Transaction(
                        id=random_with_N_digits(10),
                        first_name=trans["credit_card"]["first_name"],
                        last_name=trans["credit_card"]["last_name"],
                        credit_card_number=trans["credit_card"]["number"],
                        exp=trans["credit_card"]["exp"],
                        cvv=trans["credit_card"]["cvv"],
                        amount=trans["amount"],
                        label=trans["purchase_desc"],
                        merchant_id=trans["merchant"]["id"]
                    )
                    t.authorize()
                    db.session.add(t)
                    db.session.commit()

                    cancel_transaction_timer(t.id)
                    return jsonify({"result": SUCCESS, "transaction_number": t.id}), 200
            else:
                return jsonify({"result": INVALID}), 400
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


def process_credit_card(amount, merchant_name, card_number, cvv, month_exp, year_exp):
    url = "http://banque2-h19-dev.herokuapp.com/api/paymentGateway"
    headers = {"X-API-KEY": "15489123311"}
    data = {
        "bankId": "9bb9426e-f176-4a76-9be5-68709325e43c",
        "amount": amount,
        "merchant": merchant_name,
        "account": {
            "number": encrypt(card_number),
            "monthExp": month_exp,
            "yearExp": year_exp,
            "cvv": encrypt(cvv)
        }
    }
    r = requests.post(url, headers=headers, data=data)

    return r


def cancel_transaction_timer(trans_num):
    """
    Change transaction statuts to REFUSED after 15 minutes
    if still PENDING
    """
    def func(trans_num):
        if trans_num:
            trans = Transaction.r.query.get(trans_num)

            if trans is not None and trans.status == PENDING:
                trans.refuse()

                db.session.add(trans)
                db.session.commit()

    t = Timer(RESERVATION_TIME, func, kwargs={"trans_num": trans_num})
    t.start()
