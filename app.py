from flask import Flask, render_template, session
from flask_sqlalchemy import SQLAlchemy
from routes.user import user_bp
from routes.auth import auth_bp
from routes.extensions import db, mail
from routes.models import users
from routes.bills import bills_bp
from werkzeug.security import generate_password_hash

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
    admin_user = users.query.filter_by(username="admin").first()
    if not admin_user:
        hashed_pwd = generate_password_hash("adminpassword")
        new_admin = users(username="admin", email="admin@account.com", password=hashed_pwd, admin=True)
        db.session.add(new_admin)
        db.session.commit()

