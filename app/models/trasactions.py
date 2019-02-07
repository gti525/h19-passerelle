from sqlalchemy_utils import UUIDType

from app import db


class Transaction(db.Model):
    """
    Transaction table
    """
    id = db.Column(UUIDType(binary=False),primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    credit_card_number = db.Column(db.String(80), nullable=False)
    exp_month = db.Column(db.Integer, nullable=False)
    exp_year = db.Column(db.Integer, nullable=False)
    cvv = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    label = db.Column(db.String(100), nullable=False)#
    merchant_id = db.Column(db.Integer, db.ForeignKey('merchant.id'),
                          nullable=False)

