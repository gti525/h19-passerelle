from flask_login import current_user
from flask import render_template, Blueprint, redirect
from app.models.trasactions import Transaction

transaction_bp = Blueprint('transaction', __name__, url_prefix='/transaction')


@transaction_bp.route("/", methods=['GET', 'POST'])
def transaction():
    if current_user.is_authenticated:
        if current_user.type == 'admin':
            transactions = Transaction.query.all()
        else:
            transactions = Transaction.query.filter_by(merchant_id=current_user.id)

        return render_template("transaction.html", transactions=transactions)
    else:
        return redirect('login')
