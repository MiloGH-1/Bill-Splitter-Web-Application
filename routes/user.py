from flask import Blueprint, render_template, redirect, url_for, session
from routes.models import users, bills, payments

user_bp = Blueprint("user", __name__, url_prefix="/")

@user_bp.route("/")
def loginReg():
    return render_template("login-or-reg.html")

@user_bp.route("/dashboard")
def dashboard():
    if "user" in session:
        user_logged_in = session["user_id"]
        sent_bills = bills.query.filter_by(user_id = user_logged_in).all()
        received_bills = payments.query.filter_by(user_id = user_logged_in).all()

        all_usernames = [u.username for u in users.query.all()]

        return render_template("dashboard.html", sent=sent_bills, received = received_bills, USERNAMES = all_usernames)
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
