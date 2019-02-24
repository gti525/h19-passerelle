from flask import render_template, Blueprint

login_bp = Blueprint('login', __name__, url_prefix='/login')


@login_bp.route("/")
def login():
    return render_template('login.html', title='Login')
