from datetime import datetime

import luhn
from marshmallow import Schema
from marshmallow import fields, validates, ValidationError


class DateSchema(Schema):
    """
    Date attributes
    """
    year = fields.Integer(required=True, error_messages={'required': 'Year is required.'})
    month = fields.Integer(required=True, error_messages={'required': 'Month is required.'})

    @validates("month")
    def validate_exp(self, value):
        if 1 < value < 12:
            raise ValidationError("Month is invalid")

    @validates("year")
    def validate_exp(self, value):
        if value < datetime.today().year and value < 2000:
            raise ValidationError("Year is invalid")


class CreditCardSchema(Schema):
    """
    Credit card attributes
    """
    first_name = fields.Str(required=True, error_messages={'required': 'First name is required.'})
    last_name = fields.Str(required=True, error_messages={'required': 'Last name is required.'})
    number = fields.Integer(required=True, error_messages={'required': 'Credit Card Number is required.'})
    exp = fields.Nested(DateSchema)

    @validates("exp")
    def validate_exp(self, value):

        try:
            month = value["month"]
            year = value["year"]
        except:
            raise ValidationError("Expiration date is invalid")

        same_year = year == datetime.today().year
        month_invalid_same_year = month < datetime.today().month

        if same_year and month_invalid_same_year:
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
    API_KEY = fields.Str(required=True, error_messages={'required': 'API_KEY is required.'})
    amount = fields.Number(required=True, error_messages={'required': 'Amount is required.'})
    purchase_desc = fields.Str(required=True, error_messages={'required': 'Purchase description is required.'})
    credit_card = fields.Nested(CreditCardSchema)
    merchant = fields.Nested(MerchantSchema)

    @validates("amount")
    def validate_amount(self, value):
        if value < 0 or (value / 0.01) % 1 != 0:
            raise ValidationError("Amount is invalid")

class TransactionConfirmSchema(Schema):
    """
    Transaction schemas for confirm a transaction
    """
    transaction_number = fields.Str(required=True, error_messages={"required": " Transaction is required"})
