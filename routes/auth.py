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
                return redirect(url_for("user.dashboard"))
        else:   
                
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

        found = users.query.filter_by(email = email).first()
        if found:
            return redirect(url_for("auth.login"))

        else:
            usr = users(username, email, hashed_password)
            db.session.add(usr)
            db.session.commit()
        return redirect(url_for("auth.login"))

    return redirect(url_for("auth.register"))


@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("auth.login"))