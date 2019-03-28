import logging

from app import db
from app.models.base import TimestampMixin
from app.utils.aes import encrypt
from app.utils.genrators import random_with_N_digits

logger = logging.getLogger(__name__)

PENDING = "Pending"
AUTHORIZED = "Authorized"
REFUSED = "Refused"
CANCELED = "Canceled"


class Transaction(TimestampMixin,db.Model):
    """
    Transaction table
    """
    id = db.Column(db.BigInteger, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    credit_card_number = db.Column(db.String(20), nullable=False)
    exp_month = db.Column(db.String, nullable=False)
    exp_year = db.Column(db.String, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    label = db.Column(db.String(50), nullable=False)
    merchant_id = db.Column(db.BigInteger, db.ForeignKey('merchant.id'),
                            nullable=False)
    status = db.Column(db.String(15), nullable=False, default=PENDING)
    bank_transaction_id = db.Column(db.BigInteger, nullable=True)

    def __init__(self, credit_card=None, amount=None, label=None):
        self.id = random_with_N_digits(8)
        self.amount = amount
        self.label = label

        if credit_card:
            self.first_name = credit_card["first_name"]
            self.last_name = credit_card["last_name"]
            self.credit_card_number = credit_card["number"]
            self.cvv = credit_card["cvv"]

            if credit_card["exp"]:
                self.exp_month = credit_card["exp"]["month"]
                self.exp_year = credit_card["exp"]["year"]

    def __repr__(self):
        return '<Transaction amount={}, created={}, updated={},  />'.format(self.amount, self.created, self.updated)

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
    def create(transaction=None, **kwargs):
        if transaction is None:
            transaction = Transaction(**kwargs)

        db.session.add(transaction)
        db.session.commit()
        logger.info("Transaction created")
        return transaction

    @staticmethod
    def update(transaction):
        db.session.add(transaction)
        db.session.commit()
        logger.info("Transaction updated")


        return transaction
