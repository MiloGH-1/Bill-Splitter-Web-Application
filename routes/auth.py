from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from routes.models import users, login_attempts
from routes.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


auth_bp = Blueprint("auth", __name__, url_prefix="/")


#Method to log the user in
@auth_bp.route("/login", methods = ["POST", "GET"])
def login():
    #Checks if the form is a get or post request
    if request.method == "POST":
        #Obtains the info from the form
        email = request.form.get("email") 
        password = request.form.get("pwd")

        #Queries DB to see if a user is found with the email entered
        found = users.query.filter_by(email=email).first()
        if found and check_password_hash(found.password, password): #If email found and the passwords match
                #Logs the login attempt
                attempt = login_attempts(email_attempted=email, successful=True) 
                db.session.add(attempt)
                db.session.commit()

                #Creates session details
                session["user"] = email
                session["user_id"] = found.id
                session["user_name"] = found.username
                session["admin"] = found.admin

                #Flashes success message
                flash("Sucessfully logged in! Hello " + found.username, "green")
                return redirect(url_for("user.dashboard"))
        else:   
                #Logs a failed login attempt 
                attempt = login_attempts(email_attempted=email, successful=False)
                db.session.add(attempt)
                db.session.commit()
                flash("Incorrect Details", "red")
                return render_template("login.html")
    
    else:
        if "user" in session:    
            return redirect(url_for("user.dashboard"))
        
        return render_template("login.html")

#Method to reigster the user
@auth_bp.route('/register', methods = ["POST", "GET"])
def reg():
    if request.method == "POST":
        #Obtains info from the form
        username = request.form.get("nm")
        password = request.form.get("pwd")
        email = request.form.get("email")  

        #Hashes the password so it cant be viewed in the DB
        hashed_password = generate_password_hash(password)

        #Checks if the email or username they used is already in the database
        foundEmail = users.query.filter_by(email = email).first()
        foundUser = users.query.filter_by(username = username).first()

        #If email in use then dont allow the user to create an account
        if foundEmail:
            flash("Email already in use!")
            return redirect(url_for("auth.reg"))
        
        #If username in use then dont allow the user to create an account
        elif foundUser:
            flash("Username already in use!", "red")
            return redirect(url_for("auth.reg"))

        else:
            #Create new user and update DB
            usr = users(username, email, hashed_password)
            db.session.add(usr)
            db.session.commit()
            flash("Account Created!", "green")
        return redirect(url_for("auth.login"))

    return render_template("register.html")

#Method to loout the current user by clearing the session data
@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("auth.login"))