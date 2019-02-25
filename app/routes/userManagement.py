from flask_login import current_user
from flask import render_template, Blueprint, redirect

userManagement_bp = Blueprint('userManagement', __name__, url_prefix='/userManagement')


@userManagement_bp.route("/", methods=['GET', 'POST'])
def userManagement():
    if current_user.is_authenticated:
        return render_template("userManagement.html")
    else:
        return redirect('login')
