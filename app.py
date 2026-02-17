from flask import Flask, render_template
from routes.user import user_bp
from routes.auth import auth_bp
from routes.models import data, User
from flask_login import LoginManager

app = Flask(__name__)


app.register_blueprint(user_bp)
app.register_blueprint(auth_bp)