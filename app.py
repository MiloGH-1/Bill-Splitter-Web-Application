from flask import Flask, render_template, session
from flask_sqlalchemy import SQLAlchemy
from routes.user import user_bp
from routes.auth import auth_bp
from routes.extensions import db, mail
from routes.models import users
from routes.bills import bills_bp

app = Flask(__name__)
app.secret_key = "secretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['MAIL_SUPPRESS_SEND'] = True
app.config['MAIL_DEBUG'] = True

db.init_app(app)
mail.init_app(app)

app.register_blueprint(user_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(bills_bp)

with app.app_context():
    db.create_all()

from flask_mail import email_dispatched

# This function catches the email right before it gets suppressed and prints it!
def log_message(app, message):
    print("\n" + "="*30)
    print("📧 EMAIL INTERCEPTED (SUPPRESSED)")
    print("="*30)
    print(f"To:      {message.recipients}")
    print(f"From:    {message.sender}")
    print(f"Subject: {message.subject}")
    print(f"Body:\n{message.body}")
    print("="*30 + "\n")

# Connect the function to Flask-Mail
email_dispatched.connect(log_message)
