from app import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    type = db.Column(db.String(50))

    def __repr__(self):
        return '<User %r>' % self.email

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }


class Admin(User):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }


class Merchant(User):
    __tablename__ = 'merchant'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    api_key = db.Column(db.String(120), unique=True, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'merchant',
    }
