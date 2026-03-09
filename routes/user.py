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
        received_bills = payments.query.filter(payments.user_id == user_logged_in, payments.paid != True).all()

        all_usernames = [u.username for u in users.query.all()]

        all_sent_bills = bills.query.filter_by(user_id=user_logged_in).all()

        sent_bills = []
        for bill in all_sent_bills:
            unpaid_exists = payments.query.filter_by(bill_id=bill.id, paid=False).first()
            if unpaid_exists:
                sent_bills.append(bill)



        received_bills = payments.query.filter_by(user_id=user_logged_in, paid=False).all()

        return render_template("dashboard.html", sent=sent_bills, received = received_bills, USERNAMES = all_usernames)
    else:
        return redirect(url_for("auth.login"))


@user_bp.route("/history")
def history():
    if "user" in session:
        user_logged_in = session["user_id"]
        all_sent_bills = bills.query.filter_by(user_id=user_logged_in).all()
        paid_sent_bills = []

        received_debts = payments.query.filter_by(user_id=user_logged_in).all()

        paid_received_payments = []
        original_bill = []
        for payment in received_debts:
            if payment.paid == True:
                paid_received_payments.append(payment)
            
        for payment in paid_received_payments:
            billID = payment.bill_id
            bill = bills.query.filter_by(id = billID).first()
            original_bill.append(bill)


        for bill in all_sent_bills:
            unpaid_exists = payments.query.filter_by(bill_id=bill.id, paid=False).first()
            if not unpaid_exists:
                paid_sent_bills.append(bill)
    
        return render_template("history.html", collectedbills = paid_sent_bills, paidbills = original_bill) 

    else:
        return redirect(url_for("auth.login"))

@user_bp.route("/go_login", methods = ["POST"])
def go_login():
    return redirect(url_for("auth.login"))

@user_bp.route('/go_reg', methods = ["POST"])
def go_reg():
    return redirect(url_for("auth.reg"))
