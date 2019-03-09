from app import db

PENDING = "Pending"
AUTHORIZED = "Authorized"
REFUSED = "Refused"
CANCELED = "Canceled"


class Transaction(db.Model):
    """
    Transaction table
    """
    id = db.Column(db.String(30), primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    credit_card_number = db.Column(db.String(80), nullable=False)
    exp_month = db.Column(db.String, nullable=False)
    exp_year = db.Column(db.String, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    label = db.Column(db.String(100), nullable=False)
    merchant_id = db.Column(db.Integer, db.ForeignKey('merchant.id'),
                            nullable=False)
    status = db.Column(db.String(100), nullable=False, default=PENDING)
    bank_transaction_id = db.Column(db.Integer, nullable=False)

    def refuse(self):
        """Change status to refused"""
        self.status = REFUSED

    def authorize(self):
        """Change status to authorized"""
        self.status = AUTHORIZED

    def cancel(self):
        """Change status to canceled"""
        self.status = CANCELED


class TransactionRepository():

    @staticmethod
    def create(self, **kwargs):
        t = Transaction(**kwargs)
        db.session.add(t)
        db.session.commit()

        return t

    @staticmethod
    def update(self, transaction):
        db.session.add(transaction)
        db.session.commit()

        return transaction
