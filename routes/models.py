from routes.extensions import db

#Class for the users table
class users(db.Model):
    id = db.Column("userID", db.Integer, primary_key = True)
    username = db.Column("username", db.String(12), nullable = False)
    email = db.Column("email", db.String(100), nullable = False)
    password = db.Column("password", db.String(255), nullable = False)

    created_at = db.Column("created_at", db.DateTime(timezone=True), server_default=db.func.now()) #Gets the current time and date 

    admin = db.Column("admin", db.Boolean, default=False) #Checks if account should have admin permissions

    #Insantiates new entry for the table
    def __init__(self, username, email, password, admin = False):
        self.username=username
        self.email=email
        self.password=password
        self.admin = admin


#Class for the bills table
class bills(db.Model):
    id = db.Column("billID", db.Integer, primary_key = True)
    amount = db.Column("amount", db.Float, nullable=False)
    name = db.Column("name", db.String, nullable=False)

    image = db.Column(db.LargeBinary, nullable=True)  #Holds the BLOB image
    type = db.Column(db.String(50), nullable=True) #Holds the type of the image, E.G: JPEG

    user_id = db.Column(db.Integer, db.ForeignKey('users.userID'), nullable=False) #Secondary key

    created_at = db.Column("created_at", db.DateTime(timezone=True), server_default=db.func.now())

    hidden_by_creator = db.Column(db.Boolean, default=False) #Attribute to check if hidden, if it is hidden then it has been 'soft deleted'

    #Insantiates new entry for the table
    def __init__(self, amount, name, user_id, image=None, type=None):
        self.user_id = user_id
        self.paid = 0
        self.name = name
        self.image = image
        self.type = type
        self.amount = amount

#Class for the payments table
class payments(db.Model):
    id = db.Column("paymentID", db.Integer, primary_key=True)

    bill_id = db.Column(db.Integer, db.ForeignKey('bills.billID'), nullable=False) #Secondary key
    user_id = db.Column(db.Integer, db.ForeignKey('users.userID'), nullable=False) #Secondary key
    name = db.Column(db.String, db.ForeignKey('bills.name'), nullable=False) #Secondary key

    amount_owed = db.Column(db.Float, nullable = False)
    paid = db.Column(db.Boolean, nullable = False)
    
    proof_of_payment = db.Column(db.LargeBinary, nullable=True)  #Image to show proof of payment
    type = db.Column(db.String(50), nullable=True) #Image type

    hidden_by_payer = db.Column(db.Boolean, default=False) #Attribute to check if hidden, if it is hidden then it has been 'soft deleted'

    #Insantiates new entry for the table
    def __init__(self, bill_id, user_id, amount_owed, name):
        self.bill_id = bill_id
        self.user_id = user_id
        self.name = name
        self.paid = False
        self.amount_owed = amount_owed

#Class for the login attempts table
class login_attempts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_attempted = db.Column(db.String(100), nullable=False)
    successful = db.Column(db.Boolean, nullable=False, default=False)
    timestamp = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    #Insantiates new entry for the table
    def __init__(self, email_attempted, successful):
        self.email_attempted = email_attempted
        self.successful = successful 