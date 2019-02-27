from flask import render_template, Blueprint, redirect, flash
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from app import db
from app.models.users import User

register_bp = Blueprint('register', __name__, url_prefix='/register')


@register_bp.route("/", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated and current_user.type == 'admin':

        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(form.email.data, form.password.data,form.type.data)

            db.session.add(user)
            db.session.commit()
            flash('User has been created!')
            return redirect('dashboard')
        return render_template('register.html', title='Register', form=form)
    else:
        return redirect('login')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    type = SelectField(u'User Type', choices=[(User.type == 'admin', "Admin"), (User.type == 'merchant', "Merchant")])

    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
