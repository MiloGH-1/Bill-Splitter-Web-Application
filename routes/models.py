from routes.extensions import db

class users(db.Model):
    id = db.Column("userID", db.Integer, primary_key = True)
    username = db.Column("username", db.String(12), nullable = False)
    email = db.Column("email", db.String(100), nullable = False)
    password = db.Column("password", db.String(255), nullable = False)

    def __init__(self, username, email, password):
        self.username=username
        self.email=email
        self.password=password