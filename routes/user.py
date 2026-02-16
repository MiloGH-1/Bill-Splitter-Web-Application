from flask import Blueprint, render_template

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/')
def loginReg():
    return render_template("login-or-reg.html")

@user_bp.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")