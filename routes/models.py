from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

data = SQLAlchemy()

class User(UserMixin, data.Model):
    id = data.Column(data.Integer, primary_key = True, nullable=False)
    username = data.Column(data.String(12), unique=True, nullable=False)
    password = data.Column(data.String(20), nullable=False)