from flask import Flask, render_template
from routes.user import user_bp

app = Flask(__name__)

@app.route('/')
def loginReg():
    return render_template("login-or-reg.html")

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

app.register_blueprint(user_bp)