from flask_login import current_user
from flask import render_template, Blueprint, redirect

settings_bp = Blueprint('settings', __name__, url_prefix='/settings')


@settings_bp.route("/", methods=['GET', 'POST'])
def settings():
    if current_user.is_authenticated:
        return render_template("settings.html")
    else:
        return redirect('login')
