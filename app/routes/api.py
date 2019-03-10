from threading import Timer

from flask import jsonify
from flask_restplus import Resource, fields, reqparse

from app import api_V1
from app.banks import *
from app.consts import *
from app.models.trasactions import Transaction, PENDING, TransactionRepository
from app.models.users import Merchant
from app.schemas import TransactionCreateSchema, TransactionProcessSchema
from app.utils.aes import decrypt
from app.utils.decorators import parse_with, HasApiKey
from app.utils.genrators import random_with_N_digits

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
    'number': fields.Integer(required=True, example=1111222233334444),
    'cvv': fields.Integer(required=True, example=765),
    'exp': fields.Nested(date_model),
})

merchant_model = tn.model("Merchant", {
    'name': fields.String(required=True, example="Simons"),
    'id': fields.String(required=True, example="D84D0C669C3C48779A217CD7C7EC00CC"),
})

transaction_model = tn.model('Transactions', {
    MERCHANT_API_KEY: fields.String(required=True, example="1234567890"),
    'amount': fields.Integer(min=0, required=True, example=100),
    'purchase_desc': fields.String(required=True, example="PURCHASE/ Simons "),
    'credit_card': fields.Nested(credit_card_model),
})

# Model for transaction cancellation
cancellation_model = tn.model('Transaction cancellation', {
    'transaction_number': fields.String(required=True, example="1234567890"),
    MERCHANT_API_KEY: fields.String(required=True, example="98765431235465"),
})

# Model for transaction confirmation
ProcessTransaction = tn.model('Transaction process', {
    'transaction_number': fields.String(required=True, example="1234567890"),
    "action": fields.String(description='Action', enum=[CONFIRM_TRANS, CANCEL_TRANS]),
    MERCHANT_API_KEY: fields.String(required=True, example="98765431235465"),
})

# transaction success model
success_transaction_modal = tn.model('Sucessful transaction', {
    'transaction_number': fields.String(example="3330382145"),
    "result": fields.String(example=SUCCESS),
})

api_parser = reqparse.RequestParser()
api_parser.add_argument(MERCHANT_API_KEY)


@tn.route("/create")
class TransactionResourceCreate(Resource):
    """
    Endpoint for singular transaction
    """

    @tn.expect(transaction_model)
    @tn.response(200, SUCCESS, success_transaction_modal)
    @tn.response(400, INVALID)
    @tn.response(403, UNAUTHORIZED_ACCESS)
    @HasApiKey(api_parser)
    @parse_with(TransactionCreateSchema(strict=True))
    def post(self, **kwargs):
        trans = kwargs["entity"]

        transaction_valid = True

        try:
            # Validate API KEY
            merchant = Merchant.query.filter_by(api_key=trans[MERCHANT_API_KEY]).first()

            if merchant is None:
                transaction_valid = False

            if transaction_valid:

                bank_id = get_bank_id(trans["credit_card"]["number"])
                trans_data = {
                    "card_holder_name": "{} {} ".format(trans["credit_card"]["first_name"],
                                                        trans["credit_card"]["last_name"]),
                    "amount": trans["amount"],
                    "merchant": merchant,
                    "card_number": trans["credit_card"]["number"],
                    "cvv": trans["credit_card"]["cvv"],
                    "month_exp": trans["credit_card"]["exp"]["month"],
                    "year_exp": trans["credit_card"]["exp"]["year"]
                }

                if bank_id == BANKX_ID:
                    status_code, resp_data = call_fake_bank(action=PRE_AUTHORIZE_TRANS_ACTION, **trans_data)

                else:
                    status_code, resp_data = call_real_bank(bank_id, action=PRE_AUTHORIZE_TRANS_ACTION, **trans_data)

                if status_code == 200 and "transactionId" in resp_data is not None:
                    t = TransactionRepository.create({
                        "id": random_with_N_digits(10),
                        "first_name": trans["credit_card"]["first_name"],
                        "last_name": trans["credit_card"]["last_name"],
                        "credit_card_number": trans["credit_card"]["number"],
                        "exp_month": trans["credit_card"]["exp"]["month"],
                        "exp_year": trans["credit_card"]["exp"]["year"],
                        "cvv": trans["credit_card"]["cvv"],
                        "amount": trans["amount"],
                        "label": trans["purchase_desc"],
                        "merchant_id": trans["merchant"]["id"],
                        "bank_transaction_id": resp_data["transactionId"]
                    })

                    cancel_transaction_timer(t.id)
                    return jsonify({"result": SUCCESS, "transaction_number": t.id}), 200

            else:
                return jsonify({"result": INVALID}), 400
        except ValueError:
            return jsonify({"result": INVALID}), 400


@tn.route("/process")
class TransactionResourceConfirmation(Resource):
    """
    Endpoint for transaction confirmation
    """

    @HasApiKey(api_parser)
    @tn.expect(ProcessTransaction)
    @tn.response(200, SUCCESS)
    @tn.response(400, INVALID)
    @tn.response(403, UNAUTHORIZED_ACCESS)
    @parse_with(TransactionProcessSchema(strict=True))
    def post(self, **kwargs):
        try:
            api_key = kwargs["entity"][MERCHANT_API_KEY]
            transaction_number = kwargs["entity"]["transaction_number"]
            action = kwargs["entity"]["action"]

            transaction = Transaction.query.get(transaction_number)
            merchant = Merchant.query.filter_by(api_key=api_key).first()

            if transaction is not None and merchant is not None:
                card_number = decrypt(transaction.credit_card_number)
                bank_id = get_bank_id(card_number)
                trans_data = {"bank_transaction_id": transaction_number, "action": action}

                if bank_id == BANKX_ID:
                    status_code, resp_data = call_fake_bank(action=PROCESS_TRANS_ACTION, **trans_data)

                else:
                    status_code, resp_data = call_real_bank(bank_id, action=PROCESS_TRANS_ACTION, **trans_data)

                if status_code == 200 or status_code == 201:

                    if action == CANCEL_TRANS:
                        transaction.cancel()
                    elif action == CONFIRM_TRANS:
                        transaction.authorize()

                    TransactionRepository.update(transaction)

                    return jsonify({"result": SUCCESS}), 200
            return jsonify({"result": INVALID}), 400

        except ValueError:
            return jsonify({"result": INVALID}), 400


def cancel_transaction_timer(trans_num):
    """
    Change transaction status to REFUSED after 15 minutes
    if still PENDING
    """

    def func(id):
        if id:
            trans = Transaction.query.get(id)

            if trans is not None and trans.status == PENDING:
                trans.refuse()
                TransactionRepository.update(trans)

    t = Timer(RESERVATION_TIME, func, kwargs={"trans_num": trans_num})
    t.start()
