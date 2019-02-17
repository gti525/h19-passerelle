from datetime import datetime

import luhn
from marshmallow import Schema
from marshmallow import fields, validates, ValidationError


class CreditCardSchema(Schema):
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
            raise ValidationError("Expiration date is invalid")

        try:
            exp = value.split("/")
            month = int(exp[0])
            year = int(exp[1])
        except:
            raise ValidationError("Expiration date is invalid")

        year_invalid = year + 2000 < datetime.today().year
        same_year = year + 2000 == datetime.today().year
        month_invalid_same_year = month < datetime.today().month
        if year_invalid:
            raise ValidationError("Expiration date is invalid")
        elif same_year and month_invalid_same_year:
            raise ValidationError("Expiration date is invalid")

    @validates("number")
    def validate_credit_card_number(self, value):
        if not luhn.verify(str(value)):
            raise ValidationError("CreditCard number is invalid")


class MerchantSchema(Schema):
    name = fields.Str(required=True, error_messages={'required': 'Name is required.'})
    id = fields.Str(required=True, error_messages={'required': 'ID is required.'})


class TransactionCreateSchema(Schema):
    """
    Transaction attributes use during the creation of a transaction
    """
    amount = fields.Number(required=True, error_messages={'required': 'Amount is required.'})
    purchase_desc = fields.Str(required=True, error_messages={'required': 'Purchase description is required.'})
    credit_card = fields.Nested(CreditCardSchema)
    merchant = fields.Nested(MerchantSchema)

    @validates("amount")
    def validate_amount(self, value):
        if value < 0:
            raise ValidationError("Amount is invalid")


class TransactionConfirmSchema(Schema):
    """
    Transaction schemas for confirm a transaction
    """
    transaction_number = fields.Str(required=True, error_messages={"required": " Transaction is required"})
