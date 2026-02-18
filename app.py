from flask import Flask, render_template, session
from flask_sqlalchemy import SQLAlchemy
from routes.user import user_bp
from routes.auth import auth_bp
from routes import models
 

app = Flask(__name__)
app.secret_key = "secretkey"

app.register_blueprint(user_bp)
app.register_blueprint(auth_bp)