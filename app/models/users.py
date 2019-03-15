from app import db
from app.models.base import TimestampMixin


ACTIVE = "active"
INACTIVE = "inactive"

class User(TimestampMixin,db.Model):
    """

    """
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(50))

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User %r>' % self.email

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }


class Admin(User):
    """

    """
    __tablename__ = 'admin'

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }


class Merchant(User):
    """

    """
    __tablename__ = 'merchant'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    api_key = db.Column(db.String(120), unique=True, nullable=False)
    account_number = db.Column(db.String(120), unique=True, nullable=False)
    status = db.Column(db.String(120), unique=False, nullable=False, default=ACTIVE)
    db.relationship('Transaction', backref='merchant', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity': 'merchant',
    }

    def __repr__(self):
        return (
            self.password,
            self.email,
            self.type,
            self.name,
            self.api_key
        )