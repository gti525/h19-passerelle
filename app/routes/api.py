import logging
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

logger = logging.getLogger(__name__)

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
    'number': fields.Integer(required=True, example=4551464693977947),
    'cvv': fields.Integer(required=True, example="765"),
    'exp': fields.Nested(date_model),
})

merchant_model = tn.model("Merchant", {
    'name': fields.String(required=True, example="Simons"),
    'id': fields.String(required=True, example="D84D0C669C3C48779A217CD7C7EC00CC"),
})

transaction_model = tn.model('Transactions', {
    MERCHANT_API_KEY: fields.String(required=True, example="12345"),
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
                    "card_holder_name": "{} {} ".format(transaction.first_name, transaction.last_name),
                    "amount": transaction.amount,
                    "merchant": merchant,
                    "card_number": transaction.credit_card_number,
                    "cvv": transaction.cvv,
                    "month_exp": transaction.exp_month,
                    "year_exp": transaction.exp_year
                }

                if bank_id == BANKX_ID:
                    status_code, resp_data = call_fake_bank(action=PRE_AUTHORIZE_TRANS_ACTION, **trans_data)
                else:
                    status_code, resp_data = call_real_bank(bank_id, action=PRE_AUTHORIZE_TRANS_ACTION, **trans_data)

                if status_code == 200 and "transactionId" in resp_data is not None:
                    transaction.set_bank_trans_id(resp_data["transactionId"])
                    cancel_transaction_timer(transaction.id)
                    TransactionRepository.update(transaction)
                    return prepare_response(jsonify({"result": SUCCESS, "transaction_number": transaction.id}), 200)

            else:
                logger.info("Transaction invalid")
                return prepare_response(jsonify({"result": INVALID}), 400)
        except ValueError as e:
            logger.error("ValueError error occured. message={}".format(str(e)))
            return prepare_response(jsonify({"result": INVALID}), 400)

        except Exception as e:
            logger.error("Exception error occured. message={}".format(str(e)))
            return prepare_response(jsonify({"result": INVALID}), 400)

processed_transaction = "processed_transaction"
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
    @parse_with(TransactionProcessSchema(strict=True),arg_name=processed_transaction)
    def post(self, **kwargs):
        try:
            api_key = kwargs[processed_transaction][MERCHANT_API_KEY]
            transaction_number = kwargs[processed_transaction]["transaction_number"]
            action = kwargs[processed_transaction]["action"]

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

                    return prepare_response(jsonify({"result": SUCCESS}), 200)

            logger.error("Confirmation invalid")
            return prepare_response(jsonify({"result": INVALID}), 400)

        except ValueError as e:
            logger.error("ValueError error occured. message={}".format(str(e)))
            return prepare_response(jsonify({"result": INVALID}), 400)
        except Exception as e:
            logger.error("Exception error occured. message={}".format(str(e)))
            return prepare_response(jsonify({"result": INVALID}), 400)


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
                logger.error("Transaction {} cancelled".format(trans_num))

    t = Timer(RESERVATION_TIME, func, kwargs={"trans_num": trans_num})
    t.start()
    logger.error("Timer started for transaction {}".format(trans_num))


def prepare_response(data, code):
    response = data
    response.status_code = code
    return response
