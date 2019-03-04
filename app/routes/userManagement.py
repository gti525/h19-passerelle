from flask_login import current_user
from flask import render_template, Blueprint, redirect, request, flash
from app.models.users import Merchant
from app import db

userManagement_bp = Blueprint('userManagement', __name__, url_prefix='/userManagement')


@userManagement_bp.route("/", methods=['GET', 'POST'])
def userManagement():
    if current_user.is_authenticated:
        if current_user.type == 'admin':
            merchants = Merchant.query.filter_by(status='active')
        else:
            redirect("dashboard.html")

        return render_template("userManagement.html", merchants=merchants)
    else:
        return redirect('login')


@userManagement_bp.route("/delete", methods=['GET'])
def userDelete():
    if current_user.is_authenticated:
        if current_user.type == 'admin':
            merchantId = request.args.get('merchantId')
            merchant = Merchant.query.filter_by(id=merchantId).first()
            merchant.status = 'inactive'
            db.session.commit()
            flash("Marchand supprimer")
        else:
            redirect("dashboard")

        return redirect('userManagement')
    else:
        return redirect('login')
