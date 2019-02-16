from flask import render_template, Blueprint



main_bp = Blueprint('main', __name__, url_prefix='/main')


@main_bp.route("/index")
def index():
    return render_template('index.html', title='Home')
