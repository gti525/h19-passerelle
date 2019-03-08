from flask import render_template, Blueprint, redirect, flash
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.utils.aes import encrypt
from app.utils.genrators import random_with_N_digits

from app import db
from app.models.users import Admin, Merchant, User

register_bp = Blueprint('register', __name__, url_prefix='/register')


@register_bp.route("/", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated and current_user.type == 'admin':

        form = RegistrationForm()
        if form.validate_on_submit():
            if form.userType.data == 'admin':
                user = Admin(email=form.email.data, password=encrypt(form.password.data), type=form.userType.data)
            else:
                user = Merchant( email=form.email.data, password=encrypt(form.password.data), type=form.userType.data, name=form.username.data, api_key=encrypt(str(random_with_N_digits(2))+form.email.data +form.username.data))

            db.session.add(user)
            db.session.commit()
            flash("Utilisateur créé")
            return redirect('dashboard')
        return render_template('register.html', title='Register', form=form)
    else:
        return redirect('login')


class RegistrationForm(FlaskForm):
    username = StringField('Nom', validators=[DataRequired()], )
    email = StringField('Courriel', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    password2 = PasswordField('Validation Mot de passe', validators=[DataRequired(), EqualTo('password')])
    userType = SelectField(u'Type', choices=[('admin', 'Administrateur'), ('merchant', 'Marchand')])
    submit = SubmitField('Enregistrer')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Veuillez entrer une autre adresse courriel')
