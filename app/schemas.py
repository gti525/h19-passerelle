from datetime import datetime

import luhn
from flask_restplus import abort
from marshmallow import Schema
from marshmallow import fields, validates

INVALID_REQUEST = "Invalid request. Check the requirements"

class CreditCardSchema(Schema):

    number = fields.Integer(required=True,error_messages={'required': 'Credit Card Number is required.'})
    cvv = fields.Integer(required=True, error_messages={'required': 'CVV is required.'})
    exp_month = fields.Integer(required=True,error_messages={'required': 'Expiration month is required.'})
    exp_year = fields.Integer(required=True,error_messages={'required': 'Expiration year is required.'})

    @validates("exp_month")
    def validate_amount(self,value):
        if value > 2000 + datetime.today().year:
            raise abort(400,INVALID_REQUEST)

    @validates("exp_year")
    def validate_amount(self,value):
        if value > datetime.today().month:
            raise abort(400,INVALID_REQUEST)

    @validates("number")
    def validate_amount(self,value):
        if not luhn.verify(value):
            raise abort(400,INVALID_REQUEST)



class MerchantSchema(Schema):

    name = fields.Str(required=True,error_messages={'required': 'Name is required.'})



class TransactionSchema(Schema):
    """

    """
    first_name = fields.String(required=True, error_messages={'required': 'First name is required.'})
    last_name = fields.String(required=True,error_messages={'required': 'Last name is required.'})
    amount = fields.Integer(required=True,error_messages={'required': 'Amount is required.'})
    purchase_desc = fields.String(required=True,error_messages={'required': 'Purchase description is required.'})
    credit_card = fields.Nested(CreditCardSchema)
    merchant = fields.Nested(MerchantSchema)

    @validates("amount")
    def validate_amount(self,value):
        if value < 0:
            raise abort(400,INVALID_REQUEST)


class TransactionUpdateSchema(Schema):
    """
    Transaction attributes that will be returned
    after an update
    """
    pass


