from app import db

class users(db.Model):
    id = db.Column("userID", db.Integer, primary_key = True)
    username = db.Column("username", db.String(12), nullable = False)
    email = db.Column("email", db.String(100), nullable = False)
    password = db.Column("password", db.String(20), nullable = False)