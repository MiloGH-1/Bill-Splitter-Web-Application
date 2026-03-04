from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from routes.models import users
from routes.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


auth_bp = Blueprint("auth", __name__, url_prefix="/")



@auth_bp.route("/login", methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get("email") 
        password = request.form.get("pwd")
        hashed_password = generate_password_hash(password)

        found = users.query.filter_by(email=email).first()
        if found and check_password_hash(found.password, password):
                session["user"] = email
                session["user_id"] = found.id
                
                flash("Sucessfully logged in! Hello " + found.username, "green")
                return redirect(url_for("user.dashboard"))
        else:   
                flash("Incorrect Details", "red")
                return render_template("login.html")
    
    else:
        if "user" in session:    
            return redirect(url_for("user.dashboard"))
        
        return render_template("login.html")

@auth_bp.route('/register', methods = ["POST", "GET"])
def reg():
    if request.method == "POST":
        username = request.form.get("nm")
        password = request.form.get("pwd")
        email = request.form.get("email")

        hashed_password = generate_password_hash(password)

        foundEmail = users.query.filter_by(email = email).first()
        foundUser = users.query.filter_by(username = username).first()
        if foundEmail:
            flash("Email already in use!")
            return redirect(url_for("auth.reg"))
        
        
        elif foundUser:
            flash("Username already in use!", "red")
            return redirect(url_for("auth.reg"))

        else:
            usr = users(username, email, hashed_password)
            db.session.add(usr)
            db.session.commit()
            flash("Account Created!", "green")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("auth.login"))