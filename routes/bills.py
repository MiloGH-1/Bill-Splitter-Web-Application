from flask import Blueprint, render_template, redirect, url_for, session, request, jsonify
from routes.extensions import db
from routes.models import bills, users, payments

bills_bp = Blueprint("bills", __name__, url_prefix="/")

@bills_bp.route("/addBill", methods=["POST"])
def addBill():
    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("auth.login"))

    usernames = request.form.getlist("recipientList")
    amount = float(request.form.get("amount"))
    billTitle = request.form.get("name")

    bill_image = request.files.get("bill_image")
    image=None
    type=None

    if bill_image and bill_image.filename != "":
        image=bill_image.read()
        type=bill_image.mimetype

    recipients = users.query.filter(users.username.in_(usernames)).all()

    if not recipients:
        return redirect(url_for("user.dashboard"))

    new_bill = bills(amount=amount, name=billTitle, user_id=user_id, image=image, type=type)
    db.session.add(new_bill)
    db.session.flush()

    amount_pp = amount / (len(usernames)+1)

    for x in recipients:
        payment = payments(bill_id = new_bill.id, user_id = x.id, amount_owed = amount_pp, name=billTitle)
        db.session.add(payment)

    
    db.session.commit()

    return redirect(url_for("user.dashboard"))
    

@bills_bp.route("/get_bill/<int:billID>", methods=["GET"])
def get_bill(billID):
    bill = bills.query.filter_by(id=billID).first()

    recipients = []
    users = payments.query.filter_by(bill_id=billID).all()
    for x in users:
        recipients.append(x.user_id)

    if bill:
        return jsonify({
            'name': bill.name,
            'amount': bill.amount,
            'recipients': recipients

        })
    else:
        return jsonify({"error": "bill could not be found"}), 404