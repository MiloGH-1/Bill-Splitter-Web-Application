from flask import Blueprint, render_template, redirect, url_for, request, session

auth_bp = Blueprint("auth", __name__, url_prefix="/")

@auth_bp.route("/login", methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("nm")
        password = request.form.get("pwd")
        session["user"] = username
        return redirect(url_for("user.dashboard"))
    else:
        if "user" in session:    
            return redirect(url_for("user.dashboard"))
        
        return render_template("login.html")

@auth_bp.route('/register', methods = ["POST", "GET"])
def reg():
    if request.method == "POST":
        username = request.form.get("nm")
        password = request.form.get("pwd")
        return render_template("login.html")

    return render_template("register.html")


@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("auth.login"))