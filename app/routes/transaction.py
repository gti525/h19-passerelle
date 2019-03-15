from flask_login import current_user
from flask import render_template, Blueprint, redirect
from app.models.trasactions import Transaction
from datetime import date, timedelta
from app.models.users import Merchant
import json

transaction_bp = Blueprint('transaction', __name__, url_prefix='/transaction')

vente01_id = 13
vente02_id = 15


@transaction_bp.route("/", methods=['GET', 'POST'])
def transaction():
    if current_user.is_authenticated:
        if current_user.type == 'admin':
            transactions = Transaction.query.all()
        else:
            transactions = Transaction.query.filter_by(merchant_id=current_user.id)

        recentTransactions = []
        for x in range(0, 4):
            d = date.today() - timedelta(x)
            recentTransactions.append(Transaction.query.filter_by(created=d).count())
        transactionsByMerchant = {}
        merchant01 = Merchant.query.get(vente01_id)
        merchant02 = Merchant.query.filter_by(id=vente02_id).first()
        transactionsByMerchant[merchant01.name] = Transaction.query.filter_by(merchant_id=vente01_id).count()
        transactionsByMerchant[merchant02.name] = Transaction.query.filter_by(merchant_id=vente02_id).count()

        transactionByStatus = []
        transactionByStatus.append(len([transaction for transaction in transactions if
                                        transaction.status in "Pending"]))
        transactionByStatus.append(len([transaction for transaction in transactions if
                                        transaction.status in "Authorized"]))
        transactionByStatus.append(len([transaction for transaction in transactions if
                                        transaction.status in "Refused"]))
        transactionByStatus.append(len([transaction for transaction in transactions if
                                        transaction.status in "Verified"]))

        return render_template("transaction.html", type=current_user.type, transactions=transactions,
                               recentTransactions=recentTransactions,
                               transactionsByMerchant=transactionsByMerchant, transactionByStatus=transactionByStatus)
    else:
        return redirect('login')
