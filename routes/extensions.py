from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

#Instantiates the database and the mail libraries
db = SQLAlchemy()
mail = Mail()