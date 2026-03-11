from flask import Blueprint, render_template, redirect, url_for, session
from routes.models import users, bills, payments, login_attempts

user_bp = Blueprint("user", __name__, url_prefix="/")

#Method which takes user to a page where they can choose to login or register
@user_bp.route("/")
def loginReg():
    #Checks if a user is already logged in
    if "user" in session:
        #If they are then it takes them straight to the dashboard
        return redirect(url_for("user.dashboard"))
    else:
        #If they aren't then takes them to the login or register page
        return render_template("login-or-reg.html")


#Method which takes user to dashboard page
@user_bp.route("/dashboard")
def dashboard():
    #Checks if there is a user in the session
    if "user" in session:
        #Gets the user id of the current logged user
        user_logged_in = session["user_id"]

        #Finds all the bills they have sent and received by checking where the user ID matches the id of the currently logged in user
        sent_bills = bills.query.filter_by(user_id = user_logged_in).all()
        received_bills = payments.query.filter(payments.user_id == user_logged_in, payments.paid != True).all()

        #Gets all the usernames on the database
        all_usernames = []
        for x in users.query.all():
            all_usernames.append(x.username)

        #Gets all bills which the user has sent
        all_sent_bills = bills.query.filter_by(user_id=user_logged_in).all()

        #Gets all bills which are not fully paid that the user has sent to others
        sent_bills = []
        for bill in all_sent_bills:
            unpaid_exists = payments.query.filter_by(bill_id=bill.id, paid=False).first()
            if unpaid_exists:
                sent_bills.append(bill)


        #Gets all bills which the user has received which they are yet to pay
        received_bills = payments.query.filter_by(user_id=user_logged_in, paid=False).all()
        
        #Returns the dashboard page with all the previosuly found info
        return render_template("dashboard.html", sent=sent_bills, received = received_bills, USERNAMES = all_usernames)
    else:
        return redirect(url_for("auth.login"))


#Method to return the history page
@user_bp.route("/history")
def history():
    #Checks if there is a user in the session
    if "user" in session:
        #Gets their ID
        user_logged_in = session["user_id"]

        #Queries the db to find all the bills which the user sent which are also not hidden by the creator
        all_sent_bills = bills.query.filter_by(user_id=user_logged_in, hidden_by_creator=False).all()
        paid_sent_bills = []

        #Queries the db to find all the bills which the user has recieved and that havent been hidden
        received_debts = payments.query.filter_by(user_id=user_logged_in, hidden_by_payer=False).all()


        paid_received_payments = []
        original_bill = []
        #Loops through the list of recieved bills and checks if they have been paid or not, if they have been then they are added to a list. 
        for payment in received_debts:
            if payment.paid == True:
                paid_received_payments.append(payment)
        
        #Loops through the received payments which the user has paid and finds the original bill of the payment
        for payment in paid_received_payments:
            billID = payment.bill_id
            bill = bills.query.filter_by(id = billID).first()
            original_bill.append(bill)

        #Loops through all the sent bills and checks if someone is yet to pay their portion
        for bill in all_sent_bills:
            unpaid_exists = payments.query.filter_by(bill_id=bill.id, paid=False).first()
            if not unpaid_exists:
                #If fully paid then the bill is added to a list of bills which have been fully paid
                paid_sent_bills.append(bill)

        #Queries DB to find payments which have been paid by the current logged in user
        user_completed_payments = payments.query.filter_by(user_id = user_logged_in, paid = True).all()
        total_out = 0
        #Loops through these payments and totals the amounts of them
        for x in user_completed_payments:
            total_out += x.amount_owed

        #Queries DB to find all the bills the current logged in user created
        my_bills = bills.query.filter_by(user_id = user_logged_in).all()
        bills_ids = []
        for x in my_bills:
            #Obtains the bill ids of all these bills
            bills_ids.append(x.id)

        total_in=0
        if bills_ids:
            #Totals the amounts of all these bills to get a total amount of money the user has collected
            collected = payments.query.filter(payments.bill_id.in_(bills_ids), payments.paid == True).all()
            for x in collected:
                total_in += x.amount_owed

        #Renders the template with all the important info
        return render_template("history.html", collectedbills = paid_sent_bills, 
                               paidbills = original_bill, 
                               total_out = total_out, 
                               total_in = total_in) 

    else:
        return redirect(url_for("auth.login"))

#Method to redirect to the login page
@user_bp.route("/go_login", methods = ["POST"])
def go_login():
    return redirect(url_for("auth.login"))

#Method to redirect to the register page
@user_bp.route('/go_reg', methods = ["POST"])
def go_reg():
    return redirect(url_for("auth.reg"))

#Method to go to the admin dashboard page
@user_bp.route("/admin")
def admin():
    #Checks if the current user logged in is an admin 
    if "user" not in session or not session.get("admin"):
        return ("user.dashboard")
    else:
        #Obtains all the users, bills and login attempts in the db
        all_logins = login_attempts.query.order_by(login_attempts.timestamp.desc()).limit(100).all()
        all_users = users.query.all()
        all_bills = bills.query.all()

        return render_template("admin.html", all_users = all_users, all_bills = all_bills, all_logins = all_logins)
    
#Method to redirect to the help page
@user_bp.route("/help")
def help():
    #Checks if there is a user in the session
    if "user" not in session:
        return redirect(url_for("auth.login"))
    else:
        return render_template("help.html")
    
