from flask import Blueprint, render_template, redirect, url_for, session, request, jsonify, flash
from routes.extensions import db
from routes.models import bills, users, payments
import base64
from routes.emails import send_bill_email, paid_bill_email

bills_bp = Blueprint("bills", __name__, url_prefix="/")


#Method to add a bill to the database
@bills_bp.route("/addBill", methods=["POST"])
def addBill():
    user_id = session.get("user_id")

    #Checks if a user is in the session
    if not user_id:
        return redirect(url_for("auth.login"))

    #Obtains values from the form in the HTML
    usernames = request.form.getlist("recipientList")
    amount = float(request.form.get("amount"))
    billTitle = request.form.get("name")
    bill_image = request.files.get("bill_image")
    image=None
    type=None

    #Checks if an image is present
    if bill_image and bill_image.filename != "":
        #Assigns a type and data to the image so it can be stored as a BLOB
        image=bill_image.read()
        type=bill_image.mimetype

    #Finds recipients by querying the user table and checking usernames
    recipients = users.query.filter(users.username.in_(usernames)).all()

    if not recipients:
        return redirect(url_for("user.dashboard"))

    #Instantiates new bill using the class from 'models.py'
    new_bill = bills(amount=amount, name=billTitle, user_id=user_id, image=image, type=type)

    #Adds to the db
    db.session.add(new_bill)
    db.session.flush()

    #Finds the amount each user will need to pay
    amount_pp = amount / (len(usernames)+1)

    #Loops through all the recipients and creates a new payment for each
    for x in recipients:
        payment = payments(bill_id = new_bill.id, user_id = x.id, amount_owed = amount_pp, name=billTitle)
        db.session.add(payment)

        #Sends an email to each recipient of the payment
        if x.email:
            send_bill_email(x.email, billTitle, amount_pp)

    
    db.session.commit()

    return redirect(url_for("user.dashboard"))
    

#Method to obtain info about a bill from the database
@bills_bp.route("/get_bill/<int:billID>", methods=["GET"])
def get_bill(billID):
    bill = bills.query.filter_by(id=billID).first()

    #Arrays to hold important info about the recipients
    recipientsIDs = []
    recipients = []

    #Obtains the payments which came from a bill ID
    usersIds = payments.query.filter_by(bill_id=billID).all()

    date = ""
    if bill.created_at:
        #Creates date for the bill and formats it nicely
        date = bill.created_at.strftime("%B %d, %Y at %I:%M %p")
    

    image_base = None
    if bill.image:
        #Encodes the image into binary so it can be stored in the DB
        image_base = base64.b64encode(bill.image).decode('utf-8')

    #Loops through all 
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
            #Turns image into binary 
            proof_base = base64.b64encode(x.proof_of_payment).decode('utf-8')

        user = users.query.get(x.user_id)
        recipient_paid.append({
            #Adds to the list the following info to be used in the website:
            'username': user.username,
            'paid': x.paid,
            'proof': proof_base
        })

    if bill:
        #Returns info back to the website about the bill so it can be used
        return jsonify({
            'name': bill.name,
            'amount': bill.amount,
            'recipients': recipient_paid,
            'image': image_base,
            'date': date
        })
    else:
        #Error message in case bill is unable to be found
        return jsonify({"error": "bill could not be found"}), 404


#Method to pay a bill
@bills_bp.route("/payBill", methods=["POST"])
def payBill():
    #Obtains the image and id of the payment to be paid
    pay_image = request.files.get("pay_img")
    payment_id = request.form.get("payment_id")

    #Finds the payment in the DB
    payment = payments.query.filter_by(id=payment_id).first()

    #Find the bill linked to this payment
    bill = bills.query.get(payment.bill_id)

    if payment and pay_image.filename != "":
        #Read the image file obtained from the form
        file = pay_image.read()
        payment.proof_of_payment=file
        payment.type=pay_image.mimetype

        #Set the 'paid' variable to true in the database to highlight its been paid
        payment.paid = True

        if bill:
            #Find who sent the bill and received the bill by matching the foreign key of the user ID between the 'users' and 'bills' table
            sender = users.query.get(bill.user_id)
            payer = users.query.get(payment.user_id)
            if sender and sender.email:
                #Send an email to the sender to alert them that it has been paid
                paid_bill_email(sender.email, bill.name, payer.username, payment.amount_owed)

        db.session.commit()

    #Flashes a message to alert user of payment
    flash("Sucessfully paid bill!", "green")
    return redirect(url_for("user.dashboard"))

@bills_bp.route("/delete_bill", methods = ["POST"])
def delete_bill():
    bill_id = request.form.get("bill_id")

    if bill_id:
        bill_to_delete = bills.query.get(bill_id)

        if bill_to_delete:
            no_payments = True
            query = payments.query.filter_by(bill_id=bill_id).all()

            for x in query:
                if x.paid == True:
                    no_payments = False

            if no_payments:
                payments.query.filter_by(bill_id=bill_id).delete()
                db.session.delete(bill_to_delete)
                db.session.commit()
            else:
                flash("Cannot delete bill if atleast one recipient has already paid!")

    return redirect(url_for("user.dashboard"))

@bills_bp.route("/delete_saved_bill", methods = ["POST"])
def delete_saved_bill():
    user_id = session.get("user_id")
    bill_id = request.form.get("bill_id")

    if bill_id:
        bill = bills.query.filter_by(id=bill_id, user_id=user_id).first()
        if bill:
            bill.hidden_by_creator = True

        payment = payments.query.filter_by(bill_id=bill_id, user_id=user_id).first()
        if payment:
            payment.hidden_by_payer = True

        if bill or payment:
            db.session.commit()
    return redirect(url_for("user.history"))

@bills_bp.route("/admin_bill_delete", methods = ["POST"])
def admin_bill_delete():
    if not session.get("admin"):
        return redirect(url_for("user.dashboard"))
    
    else:
        bill_id = request.form.get("bill_id")

        if bill_id:
            bill_to_delete = bills.query.get(bill_id)

            if bill_to_delete:
                payments.query.filter_by(bill_id=bill_id).delete()
                db.session.delete(bill_to_delete)
                db.session.commit()
                flash("Bill deleted sucessfully from entire database", "green")
    return redirect(url_for("user.admin"))

@bills_bp.route("/account_delete", methods = ["POST"])
def account_delete():
    if not session.get("admin"):
        return redirect(url_for("user.dashboard"))
    
    else:
        user_id = request.form.get("user_id")

        if user_id:
            account_to_delete = users.query.get(user_id)

            if account_to_delete and account_to_delete.username != "admin":
                payments.query.filter_by(user_id=account_to_delete.id).delete()

                user_bills = bills.query.filter_by(user_id=account_to_delete.id).all()
                
                for b in user_bills:
                    payments.query.filter_by(bill_id=b.id).delete()

                bills.query.filter_by(user_id=account_to_delete.id).delete()

                db.session.delete(account_to_delete)
                db.session.commit()
                flash("Sucessfully deleted account forever, it is not recoverable", "green")
            else:
                flash("Cannot delete admin account", "red")

    return redirect(url_for("user.admin"))

@bills_bp.route("/edit_bill", methods=["POST"])
def edit_bill():
    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("auth.login"))
    
    else:
        bill_id = request.form.get("bill_id")
        new_name = request.form.get("new_name")
        new_amount = request.form.get("new_amount")

        if bill_id and new_name and new_amount:
            bill_to_edit = bills.query.get(bill_id)

            if bill_to_edit:
                bill_to_edit.name = new_name
                bill_to_edit.amount = float(new_amount)
                

                payments_list = payments.query.filter_by(bill_id=bill_id).all()
                
                if payments_list:

                    amount_pp = float(new_amount) / (len(payments_list) + 1)
                    
                    for x in payments_list:
                        x.amount_owed = amount_pp
                        x.name = new_name
                
                db.session.commit()
                flash("Bill updated successfully!", "green")

    return redirect(url_for("user.dashboard"))

@bills_bp.route("/admin_edit_bill", methods=["POST"])
def admin_edit_bill():
    if not session.get("admin"):
        return redirect(url_for("auth.login"))
    
    else:
        bill_id = request.form.get("bill_id")
        new_name = request.form.get("new_name")
        new_amount = request.form.get("new_amount")

        if bill_id and new_name and new_amount:
            bill_to_edit = bills.query.get(bill_id)

            if bill_to_edit:
                bill_to_edit.name = new_name
                bill_to_edit.amount = float(new_amount)
                

                payments_list = payments.query.filter_by(bill_id=bill_id).all()
                
                if payments_list:

                    amount_pp = float(new_amount) / (len(payments_list) + 1)
                    
                    for x in payments_list:
                        x.amount_owed = amount_pp
                        x.name = new_name
                
                db.session.commit()
                flash("Bill updated successfully!", "green")

    return redirect(url_for("user.admin"))