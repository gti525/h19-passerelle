from app import db
from app.models.base import TimestampMixin
from app.utils.aes import encrypt

PENDING = "Pending"
AUTHORIZED = "Authorized"
REFUSED = "Refused"
CANCELED = "Canceled"


class Transaction(TimestampMixin,db.Model):
    """
    Transaction table
    """
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    credit_card_number = db.Column(db.String(20), nullable=False)
    exp_month = db.Column(db.String, nullable=False)
    exp_year = db.Column(db.String, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    label = db.Column(db.String(50), nullable=False)
    merchant_id = db.Column(db.Integer, db.ForeignKey('merchant.id'),
                            nullable=False)
    status = db.Column(db.String(15), nullable=False, default=PENDING)
    bank_transaction_id = db.Column(db.Integer, nullable=False)

    def __init__(self, first_name=None, last_name=None, credit_card_number=None, exp_month=None, exp_year=None,
                 amount=None,
                 cvv=None, label=None):
        self.id = 123
        self.first_name = first_name
        self.last_name = last_name
        self.credit_card_number = 123
        self.exp_month = exp_month
        self.exp_year = exp_year
        self.amount = amount
        self.label = label
        self.cvv = cvv

    def set_merchant(self, merchant):
        self.merchant_id = merchant.id

    def set_bank_trans_id(self, id):
        self.bank_transaction_id = id

    def refuse(self):
        """Change status to refused"""
        self.status = REFUSED

    def authorize(self):
        """Change status to authorized"""
        self.status = AUTHORIZED

    def cancel(self):
        """Change status to canceled"""
        self.status = CANCELED

    def encrypt_data(self):
        self.credit_card_number = encrypt(self.credit_card_number)


class TransactionRepository:

    @staticmethod
    def create(**kwargs):
        t = Transaction(**kwargs)
        db.session.add(t)
        db.session.commit()

        return t

    @staticmethod
    def update(transaction):
        db.session.add(transaction)
        db.session.commit()

        return transaction
