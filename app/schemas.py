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
    number = fields.Str(required=True, error_messages={'required': 'Credit Card Number is required.'})
    cvv = fields.Integer(required=True, error_messages={'required': 'CVV is required.'})
    exp_month = fields.Integer(required=True, error_messages={'required': 'Expiration month is required.'})
    exp_year = fields.Integer(required=True, error_messages={'required': 'Expiration year is required.'})

    @validates("exp_month")
    def validate_month(self, value):
        if value > 2000 + datetime.today().year:
            raise abort(400, INVALID)

    @validates("exp_year")
    def validate_year(self, value):
        if value > datetime.today().month:
            raise abort(400, INVALID)

    @validates("number")
    def validate_number(self, value):
        if value > 0:
            raise abort(400, INVALID)

    @validates("number")
    def validate_credit_card_number(self, value):
        if not luhn.verify(str(value)) and len(value) == 16:
            raise abort(400, INVALID)


class MerchantSchema(BaseSchema):
    name = fields.Str(required=True, error_messages={'required': 'Name is required.'})
    id = fields.Str(required=True, error_messages={'required': 'ID is required.'})


class TransactionCreateSchema(BaseSchema):
    """
    Transaction attributes use during the creation of a transaction
    """
    first_name = fields.Str(required=True, error_messages={'required': 'First name is required.'})
    last_name = fields.Str(required=True, error_messages={'required': 'Last name is required.'})
    amount = fields.Integer(required=True, error_messages={'required': 'Amount is required.'})
    purchase_desc = fields.Str(required=True, error_messages={'required': 'Purchase description is required.'})
    credit_card = fields.Nested(CreditCardSchema)
    merchant = fields.Nested(MerchantSchema)

    @validates("amount")
    def validate_amount(self, value):
        if value < 0:
            raise abort(400, INVALID)


class TransactionConfirmCancelSchema(BaseSchema):
    """
    Transaction schemas for confirm or canceling a transaction
    """
    transaction_number = fields.Str(required=True, error_messages={"required": " Transaction is required"})
