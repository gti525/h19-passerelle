from flask_login import current_user
from flask import render_template, Blueprint, redirect

userModify_bp = Blueprint('userModify', __name__, url_prefix='/userModify')


@userModify_bp.route("/", methods=['GET', 'POST'])
def userModify():
    if current_user.is_authenticated:
        return render_template("userModify.html")
    else:
        return redirect('login')
