from flask_login import current_user
from flask import render_template, Blueprint, redirect

transaction_bp = Blueprint('transaction', __name__, url_prefix='/transaction')


@transaction_bp.route("/", methods=['GET', 'POST'])
def transaction():
    if current_user.is_authenticated:
        return render_template("transaction.html")
    else:
        return redirect('login')
