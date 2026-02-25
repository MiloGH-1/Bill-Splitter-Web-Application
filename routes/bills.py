from flask import Blueprint, render_template, redirect, url_for, session, request
from routes.extensions import db
from routes.models import bills, users

bills_bp = Blueprint("bills", __name__, url_prefix="/")

@bills_bp.route("/addBill", methods=["POST"])
def addBill():
    user_id = session.get("user_id")

    if not user_id:
        print("test")
        return redirect(url_for("auth.login"))

    username = request.form.get("recipient_user")
    amount = request.form.get("amount")
    recipient = users.query.filter_by(username=username).first()

    if not recipient or recipient.id == user_id:   
        return redirect(url_for("user.dashboard"))

    new_bill = bills(amount=amount, user_id=user_id, recipient_id=recipient.id)

    db.session.add(new_bill)
    db.session.commit()
    print("NEW BILL SAVED WITH ID:", new_bill.id)
    return redirect(url_for("user.dashboard"))
    
