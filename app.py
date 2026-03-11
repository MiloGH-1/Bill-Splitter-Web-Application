from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from routes.user import user_bp
from routes.auth import auth_bp
from routes.extensions import db, mail
from routes.models import users
from routes.bills import bills_bp
from werkzeug.security import generate_password_hash

#Configs for the database and also the mail systems
app = Flask(__name__)
app.secret_key = "secretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db" #Creates the DB with this name
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 
app.config['MAIL_SUPPRESS_SEND'] = True #Stops mail before being sent

#Initalises both the database and the mail systems
db.init_app(app)
mail.init_app(app)

#Registers the blueprints from the files in the routes folder
app.register_blueprint(user_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(bills_bp)

with app.app_context():
    #Creates the database
    db.create_all()
    
    admin_user = users.query.filter_by(username="admin").first()
    if not admin_user:
        #Creates an admin user in the DB, this would not be here in a real DB as it shows the password in plaintext but is only here to allow markers to find admin credentials
        hashed_pwd = generate_password_hash("adminpassword")
        new_admin = users(username="admin", email="admin@account.com", password=hashed_pwd, admin=True)
        db.session.add(new_admin)
        db.session.commit()

