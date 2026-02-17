from flask import Blueprint, render_template, redirect, url_for

user_bp = Blueprint('user', __name__, url_prefix='/')

@user_bp.route('/')
def loginReg():
    return render_template("login-or-reg.html")

@user_bp.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

@user_bp.route('/go_login', methods = ["POST"])
def go_login():
    return redirect(url_for("auth.login"))

@user_bp.route('/go_reg', methods = ["POST"])
def go_reg():
    return redirect(url_for("auth.reg"))