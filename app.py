from flask import Flask, render_template, session
from flask_sqlalchemy import SQLAlchemy
from routes.user import user_bp
from routes.auth import auth_bp
from routes.extensions import db
from routes.models import users

app = Flask(__name__)
app.secret_key = "secretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


app.register_blueprint(user_bp)
app.register_blueprint(auth_bp)

with app.app_context():
    db.create_all()
