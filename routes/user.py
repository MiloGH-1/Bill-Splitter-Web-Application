from flask import Blueprint, render_template, redirect, url_for, session
from routes.models import users, bills

user_bp = Blueprint("user", __name__, url_prefix="/")

@user_bp.route("/")
def loginReg():
    return render_template("login-or-reg.html")

@user_bp.route("/dashboard")
def dashboard():
    if "user" in session:
        user_logged_in = session["user_id"]
        sent_bills = bills.query.filter_by(user_id = user_logged_in).all()
        received_bills = bills.query.filter_by(recipient_id = user_logged_in).all()
        users_in_system = users.query.filter(users.id != user_logged_in).all()
        print(users_in_system)
        return render_template("dashboard.html", sent=sent_bills, received=received_bills, users_in_system = users_in_system)
    else:
        return redirect(url_for("auth.login"))


@user_bp.route("/history")
def history():
    return render_template("history.html") 


@user_bp.route("/go_login", methods = ["POST"])
def go_login():
    return redirect(url_for("auth.login"))

@user_bp.route('/go_reg', methods = ["POST"])
def go_reg():
    return redirect(url_for("auth.reg"))