from app import db


class Transaction(db.Model):
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    credit_card_number = db.Column(db.String(80), nullable=False)
    exp_month = db.Column(db.Integer, nullable=False)
    exp_year = db.Column(db.Integer, nullable=False)
    cvv = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    is_valid = db.Column(db.Boolean, default=False)
