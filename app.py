from flask import Flask, render_template, session
from flask_sqlalchemy import SQLAlchemy
from routes.user import user_bp
from routes.auth import auth_bp

app = Flask(__name__)
app.secret_key = "secretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATONS"] = False

db = SQLAlchemy(app)

app.register_blueprint(user_bp)
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)