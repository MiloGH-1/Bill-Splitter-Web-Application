from routes.extensions import db

class users(db.Model):
    id = db.Column("userID", db.Integer, primary_key = True)
    username = db.Column("username", db.String(12), nullable = False)
    email = db.Column("email", db.String(100), nullable = False)
    password = db.Column("password", db.String(255), nullable = False)

    bills_sent = db.relationship('bills', foreign_keys='bills.user_id', backref='sender', lazy=True)
    bills_received = db.relationship('bills', foreign_keys='bills.recipient_id', backref='recipient', lazy=True)

    def __init__(self, username, email, password):
        self.username=username
        self.email=email
        self.password=password


class bills(db.Model):
    id = db.Column("billID", db.Integer, primary_key = True)
    amount = db.Column("amount", db.Float, nullable=False)
    paid = db.Column("paid", db.Float, nullable=False)
    name = db.Column("name", db.String, nullable=False)

    image = db.Column(db.LargeBinary, nullable=True) 
    type = db.Column(db.String(50), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.userID'), nullable=False) #Secondary key
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.userID'), nullable=False) #Secondary key

    def __init__(self, amount, name, user_id, recipient_id, image=None, type=None):
        self.user_id = user_id
        self.paid = 0
        self.amount = amount
        self.recipient_id = recipient_id
        self.name = name
        self.image = image
        self.type = type




