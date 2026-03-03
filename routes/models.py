from routes.extensions import db

class users(db.Model):
    id = db.Column("userID", db.Integer, primary_key = True)
    username = db.Column("username", db.String(12), nullable = False)
    email = db.Column("email", db.String(100), nullable = False)
    password = db.Column("password", db.String(255), nullable = False)

    bills_sent = db.relationship('bills', foreign_keys='bills.user_id', backref='sender', lazy=True)
  

    def __init__(self, username, email, password):
        self.username=username
        self.email=email
        self.password=password


class bills(db.Model):
    id = db.Column("billID", db.Integer, primary_key = True)
    amount = db.Column("amount", db.Float, nullable=False)
    name = db.Column("name", db.String, nullable=False)

    image = db.Column(db.LargeBinary, nullable=True) 
    type = db.Column(db.String(50), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.userID'), nullable=False) #Secondary key

    def __init__(self, amount, name, user_id, recipient_id, image=None, type=None):
        self.user_id = user_id
        self.paid = 0
        self.amount = amount
        self.recipient_id = recipient_id
        self.name = name
        self.image = image
        self.type = type


class payments(db.Model):
    id = db.Column("paymentID", db.Integer, primary_key=True)

    bill_id = db.Column(db.Integer, db.ForeignKey('bills.billID'), nullable=False) #Secondary key
    user_id = db.Column(db.Integer, db.ForeignKey('users.userID'), nullable=False) #Secondary key

    amount_owed = db.Column(db.Float, nullable = False)
    paid = db.Column(db.Boolean, nullable = False)

    def __init__(self, bill_id, user_id, amount_owed):
        self.bill_id = bill_id
        self.user_id = user_id
        self.paid = False
        self.amount_owed = amount_owed