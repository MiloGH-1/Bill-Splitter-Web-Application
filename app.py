from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from routes.user import user_bp
from routes.auth import auth_bp
from routes.models import   User
 

app = Flask(__name__)

app.config["SECRET_KEY"]="mh4235140706"
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///User.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"]=False
db = SQLAlchemy(app)

app.register_blueprint(user_bp)
app.register_blueprint(auth_bp)