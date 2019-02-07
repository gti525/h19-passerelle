from app import db

class Status(db.Model):
    """
    Transaction status
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Sting(30))
