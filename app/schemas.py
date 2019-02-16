from datetime import datetime

import luhn
from flask_restplus import abort
from marshmallow import Schema
from marshmallow import fields, validates

from app.utils.http_codes import *


class BaseSchema(Schema):

    def handle_error(self, exc, data):
        """Log and raise our custom exception when (de)serialization fails."""
        raise abort(400, '{0} is required'.format(data))


class CreditCardSchema(BaseSchema):
    """
    Credit card attributes
    """
    first_name = fields.Str(required=True, error_messages={'required': 'First name is required.'})
    last_name = fields.Str(required=True, error_messages={'required': 'Last name is required.'})
    number = fields.Str(required=True, error_messages={'required': 'Credit Card Number is required.'})
    cvv = fields.Integer(required=True, error_messages={'required': 'CVV is required.'})
    exp = fields.String(required=True, error_messages={'required': 'Expiration month is required.'})

    @validates("exp")
    def validate_exp(self, value):
        if len(value) != 5:
            raise abort(400, INVALID)

        try:
            exp = value.split("/")
            month = int(exp[0])
            year = int(exp[1])
        except :
            raise abort(400, INVALID)

        year_invalid = year + 2000 < datetime.today().year
        same_year = year + 2000 == datetime.today().year
        month_invalid_same_year = month < datetime.today().month
        if year_invalid:
            raise abort(400, INVALID)
        elif same_year and month_invalid_same_year:
            raise abort(400, INVALID)

    @validates("number")
    def validate_credit_card_number(self, value):
        if not luhn.verify(str(value)) and len(value) == 16:
            print("1")
            raise abort(400, INVALID)


class MerchantSchema(BaseSchema):
    name = fields.Str(required=True, error_messages={'required': 'Name is required.'})
    id = fields.Str(required=True, error_messages={'required': 'ID is required.'})


class TransactionCreateSchema(BaseSchema):
    """
    Transaction attributes use during the creation of a transaction
    """
    amount = fields.Integer(required=True, error_messages={'required': 'Amount is required.'})
    purchase_desc = fields.Str(required=True, error_messages={'required': 'Purchase description is required.'})
    credit_card = fields.Nested(CreditCardSchema)
    merchant = fields.Nested(MerchantSchema)

    @validates("amount")
    def validate_amount(self, value):
        if value < 0:
            raise abort(400, INVALID)


class TransactionConfirmSchema(BaseSchema):
    """
    Transaction schemas for confirm a transaction
    """
    transaction_number = fields.Str(required=True, error_messages={"required": " Transaction is required"})


class TransactionCancelSchema(BaseSchema):
    """
    Transaction schemas for cancel  transaction
    """
    transaction_number = fields.Str(required=True, error_messages={"required": " Transaction is required"})
