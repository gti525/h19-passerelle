from flask_login import current_user
from flask import render_template, Blueprint, redirect

register_bp = Blueprint('register', __name__, url_prefix='/register')


@register_bp.route("/", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return render_template("register.html")
    else:
        return redirect('login')
