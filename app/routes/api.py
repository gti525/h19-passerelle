import logging
from threading import Timer

from flask import jsonify
from flask_restplus import Resource, fields, reqparse

import tasks
from app import api_V1
from app.banks import *
from app.consts import *
from app.models.transactions import Transaction, PENDING, TransactionRepository
from app.models.users import Merchant
from app.schemas import TransactionCreateSchema, TransactionProcessSchema
from app.utils.aes import decrypt
from app.utils.decorators import parse_with, HasApiKey
from app.utils.genrators import add_leading_zero

logger = logging.getLogger(__name__)

RESERVATION_TIME = 915  # 15 minutes and 15 seconds

tn = api_V1.namespace('transaction', description='Transaction operations')

ExpirationDate = tn.model('ExpirationDate', {
    'month': fields.Integer(example=10),
    "year": fields.Integer(example=2023),
})

CreditCard = tn.model('CreditCard', {
    'first_name': fields.String(required=True, example="John"),
    'last_name': fields.String(required=True, example="Doe"),
    'number': fields.Integer(required=True, example=4551464693977947),
    'cvv': fields.String(required=True, example="765"),
    'exp': fields.Nested(ExpirationDate),
})

CreateTransactionRequest = tn.model('CreateTransactionRequest', {
    MERCHANT_API_KEY: fields.String(required=True, example="12345"),
    'amount': fields.Float(min=0, required=True, example=100.42),
    'purchase_desc': fields.String(required=True, example="PURCHASE/ Simons "),
    'credit_card': fields.Nested(CreditCard),
})

CreateTransactionReply = tn.model('CreateTransactionReply', {
    'transaction_number': fields.String(example="3330382145"),
    "result": fields.String(example=ACCEPTED, enum=[ACCEPTED, DECLINED]),
})

ProcessTransactionRequest = tn.model('ProcessTransactionRequest', {
    'transaction_number': fields.String(required=True, example="1234567890"),
    "action": fields.String(description='Action', enum=[COMMIT, CANCEL]),
    MERCHANT_API_KEY: fields.String(required=True, example="98765431235465"),
})
ProcessTransactionReply = tn.model('ProcessTransactionReply', {
    "result": fields.String(example=COMMITTED, enum=[COMMITTED, CANCELLED]),
})

api_parser = reqparse.RequestParser()
api_parser.add_argument(MERCHANT_API_KEY)


@tn.route("/create")
class TransactionResourceCreate(Resource):
    """
    Endpoint for singular transaction
    """

    @tn.expect(CreateTransactionRequest)
    @tn.response(200, SUCCESS, CreateTransactionReply)
    @tn.response(400, INVALID_PAYLOAD)
    @tn.response(403, UNAUTHORIZED_ACCESS)
    @tn.response(500, FAILURE)
    @HasApiKey(api_parser)
    @parse_with(TransactionCreateSchema(strict=True), arg_name="transaction")
    def post(self, **kwargs):
        credit_card = kwargs["transaction"]["credit_card"]
        label = kwargs["transaction"]["purchase_desc"]
        amount = kwargs["transaction"]["amount"]
        transaction = Transaction(credit_card=credit_card, label=label, amount=amount)
        merchant_api_key = kwargs[MERCHANT_API_KEY]
        transaction_valid = True

        try:
            # Validate API KEY
            merchant = Merchant.query.filter_by(api_key=merchant_api_key).first()

            if merchant is None:
                transaction_valid = False
                logger.info("Merchant doesnt exist")

            if transaction_valid:

                transaction.set_merchant(merchant)
                bank_id = get_bank_id(transaction.credit_card_number)
                trans_data = {
                    "card_holder_name": "{} {}".format(transaction.first_name, transaction.last_name),
                    "amount": transaction.amount,
                    "merchant": merchant,
                    "card_number": transaction.credit_card_number,
                    "cvv": transaction.cvv,
                    "month_exp": add_leading_zero(transaction.exp_month),
                    "year_exp": transaction.exp_year
                }

                if bank_id == BANKX_ID:
                    status_code, resp_data = call_fake_bank(act=PRE_AUTHORIZE_TRANS_ACTION, **trans_data)
                else:
                    status_code, resp_data = call_real_bank(bank_id, act=PRE_AUTHORIZE_TRANS_ACTION, **trans_data)

                if status_code == 200:
                    if resp_data["result"] == ACCEPTED:
                        transaction.encrypt_data()
                        transaction.set_bank_trans_id(resp_data["transactionId"])
                        TransactionRepository.create(transaction=transaction)
                        cancel_transaction_timer(transaction.id)
                        logger.info("Transaction {} was accepted".format(transaction.id))

                        return prepare_response(jsonify({"result": ACCEPTED, "transaction_number": transaction.id}),
                                                200)
                    elif resp_data["result"] == DECLINED or resp_data["result"] == DECLINED_NO_FUNDS:
                        logger.info("Transaction {} was declined".format(transaction.id))

                        return prepare_response(jsonify({"result": DECLINED, "transaction_number": None}), 200)


            else:
                logger.info("Transaction invalid")
                return prepare_response(jsonify({"result": FAILURE}), 500)
        except ValueError as e:
            logger.error("ValueError error occured. {}".format(str(e)))
            return prepare_response(jsonify({"result": FAILURE}), 500)

        except Exception as e:
            logger.error("Exception error occured. {}".format(str(e)))
            return prepare_response(jsonify({"result": FAILURE}), 500)

        return prepare_response(jsonify({"result": FAILURE}), 500)


processed_transaction = "processed_transaction"


@tn.route("/process")
class TransactionResourceConfirmation(Resource):
    """
    Endpoint for transaction confirmation
    """

    @HasApiKey(api_parser)
    @tn.expect(ProcessTransactionRequest)
    @tn.response(200, SUCCESS, ProcessTransactionReply)
    @tn.response(400, INVALID_PAYLOAD)
    @tn.response(403, UNAUTHORIZED_ACCESS)
    @tn.response(500, FAILURE)
    @parse_with(TransactionProcessSchema(strict=True), arg_name=processed_transaction)
    def post(self, **kwargs):
        try:
            api_key = kwargs[MERCHANT_API_KEY]
            transaction_number = kwargs[processed_transaction]["transaction_number"]
            action = kwargs[processed_transaction]["action"]

            transaction = Transaction.query.get(transaction_number)
            merchant = Merchant.query.filter_by(api_key=api_key).first()

            if transaction is not None and \
                    merchant is not None and \
                    transaction.status == PENDING and \
                    merchant.status == "active":

                card_number = decrypt(transaction.credit_card_number)
                bank_id = get_bank_id(card_number)
                trans_data = {"bank_transaction_id": transaction.bank_transaction_id, "action": action}

                if bank_id == BANKX_ID:
                    status_code, resp_data = call_fake_bank(act=PROCESS_TRANS_ACTION, **trans_data)

                else:
                    status_code, resp_data = call_real_bank(bank_id, act=PROCESS_TRANS_ACTION, **trans_data)

                if status_code == 200 or status_code == 201:

                    if action == CANCEL and resp_data["result"] == CANCELLED:
                        transaction.cancel()
                        logger.info("Transaction {} was canceled".format(transaction.id))
                        resp_result = CANCELLED
                    elif action == COMMIT and resp_data["result"] == COMMITTED:
                        transaction.authorize()
                        logger.info("Transaction {} was authorized".format(transaction.id))
                        resp_result = COMMITTED

                    TransactionRepository.update(transaction)

                    return prepare_response(jsonify({"result": resp_result}), 200)

            logger.error("Process failed")
            return prepare_response(jsonify({"result": FAILURE}), 500)

        except ValueError as e:
            logger.error("ValueError error occured. message={}".format(str(e)))
            return prepare_response(jsonify({"result": FAILURE}), 500)
        except Exception as e:
            logger.error("Exception error occured. message={}".format(str(e)))
            return prepare_response(jsonify({"result": FAILURE}), 500)


def cancel_transaction_timer(trans_num):
    """
    Change transaction status to REFUSED after 15 minutes
    if still PENDING
    """

    def func(**kwargs):
        if kwargs["trans_num"]:
            logger.info("Canceling transaction {}".format(trans_num))

            tasks.cancel_transaction(kwargs["trans_num"])

    t = Timer(RESERVATION_TIME, func, kwargs={"trans_num": trans_num})
    t.start()
    logger.info("Timer started for transaction {}".format(trans_num))


def prepare_response(data, code):
    response = data
    response.status_code = code
    return response
