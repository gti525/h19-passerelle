from flask import render_template, Blueprint, redirect, flash
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import EqualTo

from app import db
from app.utils.aes import encrypt

settings_bp = Blueprint('settings', __name__, url_prefix='/settings')


@settings_bp.route("/", methods=['GET', 'POST'])
def settings():
    if current_user.is_authenticated:
        form = RegistrationForm()
        if form.validate_on_submit():
            if not form.username == None:
                current_user.name = form.username.data
            if not form.password.data == "":
                current_user.password = encrypt(form.password.data)
            db.session.commit()
            flash("Modification enregister")
            return redirect('settings')
        return render_template('settings.html', title='Settings', form=form, user=current_user)
    else:
        return redirect('login')


class RegistrationForm(FlaskForm):
    username = StringField('Nom d\'usager')
    password = PasswordField('Nouveau mot de passe')
    password2 = PasswordField('Validation du mot de passe', validators=[EqualTo('password')])
    submit = SubmitField('Modifier')
