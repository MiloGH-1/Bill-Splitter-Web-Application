from routes.extensions import db

class users(db.Model):
    id = db.Column("userID", db.Integer, primary_key = True)
    username = db.Column("username", db.String(12), nullable = False)
    email = db.Column("email", db.String(100), nullable = False)
    password = db.Column("password", db.String(255), nullable = False)

    created_at = db.Column("created_at", db.DateTime(timezone=True), server_default=db.func.now())


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

    created_at = db.Column("created_at", db.DateTime(timezone=True), server_default=db.func.now())

    hidden_by_creator = db.Column(db.Boolean, default=False)


    def __init__(self, amount, name, user_id, image=None, type=None):
        self.user_id = user_id
        self.paid = 0
        self.name = name
        self.image = image
        self.type = type
        self.amount = amount

class payments(db.Model):
    id = db.Column("paymentID", db.Integer, primary_key=True)

    bill_id = db.Column(db.Integer, db.ForeignKey('bills.billID'), nullable=False) #Secondary key
    user_id = db.Column(db.Integer, db.ForeignKey('users.userID'), nullable=False) #Secondary key
    name = db.Column(db.String, db.ForeignKey('bills.name'), nullable=False) #Secondary key

    amount_owed = db.Column(db.Float, nullable = False)
    paid = db.Column(db.Boolean, nullable = False)
    
    proof_of_payment = db.Column(db.LargeBinary, nullable=True) 
    type = db.Column(db.String(50), nullable=True)

    hidden_by_payer = db.Column(db.Boolean, default=False)

    def __init__(self, bill_id, user_id, amount_owed, name):
        self.bill_id = bill_id
        self.user_id = user_id
        self.name = name
        self.paid = False
        self.amount_owed = amount_owed

    