from flask_login import current_user
from flask import render_template, Blueprint, redirect, request, flash
from app.models.users import Merchant, User
from app import db
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email

userModify_bp = Blueprint('userModify', __name__, url_prefix='/userModify')


@userModify_bp.route("/", methods=['GET', 'POST'])
def userModify():
    if current_user.is_authenticated:
        if current_user.type == 'admin':
            form = ModificationForm()
            merchandId = request.args.get('merchantId')
            merchant = Merchant.query.filter_by(id=merchandId).first()
            if request.method == 'GET':
                form.email.data = merchant.email
                form.name.data = merchant.name
                form.account_number.data = merchant.account_number
            elif request.method == 'POST':
                merchant.name = form.name.data
                merchant.account_number = form.account_number.data
                merchant.email = form.email.data
                db.session.commit()
                flash("Modification réussi!")
            return render_template('userModify.html', form=form, title='Modifier un usager')
        else:
            return redirect('dashboard')
    else:
        return redirect('login')


class ModificationForm(FlaskForm):
    name = StringField('Nom', validators=[DataRequired()], )
    account_number = StringField('Compte bancaire', validators=[DataRequired()])
    email = StringField('Courriel', validators=[DataRequired(), Email()])
    submit = SubmitField('Enregistrer')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Veuillez entrer une autre adresse courriel')
