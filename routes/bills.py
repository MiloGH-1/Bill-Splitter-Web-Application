from flask import Blueprint, render_template, redirect, url_for, session, request, jsonify
from routes.extensions import db
from routes.models import bills, users, payments
import base64

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

    recipientsIDs = []
    recipients = []
    usersIds = payments.query.filter_by(bill_id=billID).all()
    
    image_base = None
    if bill.image:
        image_base = base64.b64encode(bill.image).decode('utf-8')

    for x in usersIds:
        recipientsIDs.append(x.user_id)

    for i in recipientsIDs:
        user = users.query.filter_by(id=i).first()
        recipients.append(user.username)

    payment_records = payments.query.filter_by(bill_id=billID).all()
    
    recipient_paid = []
    for x in payment_records:
        
        proof_base = None

        if x.proof_of_payment:
            proof_base = base64.b64encode(x.proof_of_payment).decode('utf-8')

        user = users.query.get(x.user_id)
        recipient_paid.append({
            'username': user.username,
            'paid': x.paid,
            'proof': proof_base
        })

    if bill:
        return jsonify({
            'name': bill.name,
            'amount': bill.amount,
            'recipients': recipient_paid,
            'image': image_base
        })
    else:
        return jsonify({"error": "bill could not be found"}), 404
    
@bills_bp.route("/payBill", methods=["POST"])
def payBill():
    pay_image = request.files.get("pay_img")
    payment_id = request.form.get("payment_id")

    payment = payments.query.get(payment_id)

    if payment and pay_image.filename != "":
        file = pay_image.read()
        payment.proof_of_payment=file
        payment.type=pay_image.mimetype

        payment.paid = True


        db.session.commit()

    return redirect(url_for("user.dashboard"))