from flask import Blueprint, render_template, redirect, url_for, request


auth_bp = Blueprint('auth', __name__, url_prefix='/')

@auth_bp.route('/login', methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        return redirect(url_for("user.dashboard"))
    else:
        return render_template("login.html")

@auth_bp.route('/register', methods = ["POST", "GET"])
def reg():
    return render_template("register.html")

