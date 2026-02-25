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


class bills(db.Model):
    id = db.Column("billID", db.Integer, primary_key = True)
    amount = db.Column("amount", db.Float, nullable=False)
    paid = db.Column("paid", db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.userID'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.groupID'), nullable=False)


    def __init__(self, amount, user_id, group_id):
        self.user_id = user_id
        self.paid = 0
        self.amount = amount




