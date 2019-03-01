from flask_login import current_user
from flask import render_template, Blueprint, redirect

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_bp.route("/", methods=['GET', 'POST'])
def dashboard():
    if current_user.is_authenticated:
        return render_template("dashboard.html")
    else:
        return redirect('login')
