from flask import Blueprint, redirect

base_bp = Blueprint('base', __name__, url_prefix='/')


@base_bp.route("")
def base():
    return redirect("login")
