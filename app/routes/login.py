from flask import render_template, Blueprint, redirect, request, flash
from flask_login import login_user
from app.models.users import User

login_bp = Blueprint('login', __name__, url_prefix='/login')


@login_bp.route("/", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'GET':
        return render_template('login.html', title='Connexion')
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        registered_user = User.query.filter_by(email=email, password=password).first()
        # registered_user = User('papa', email, password, 'admin')
        if registered_user is None:
            return render_template('login.html', error="Courriel ou mot de passe invalide")
        login_user(registered_user)
        return render_template('index.html', title="Accueil")
