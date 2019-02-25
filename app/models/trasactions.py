from app import db


class Transaction(db.Model):
    """
    Transaction table
    """
    id = db.Column(db.String(30) ,primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    credit_card_number = db.Column(db.String(80), nullable=False)
    exp = db.Column(db.String, nullable=False)
    cvv = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    label = db.Column(db.String(100), nullable=False)
    merchant_id = db.Column(db.Integer, db.ForeignKey('merchant.id'),
                          nullable=False)

