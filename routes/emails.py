from flask import Blueprint, render_template, redirect, url_for, session
from routes.models import users, bills, payments
import os
from routes.extensions import mail

#Method to send an email to alert a user that a new bill has been created that they need to pay
def send_bill_email(recipient_email, bill_name, amount):
    #Gets the email of the current logged in user in the OS
    sender = f"{os.getlogin()}@dcs.warwick.ac.uk"
    
    #Method from the 'mail' library to send a message
    mail.send_message(
        sender=("Bill Splitter App", sender),
        subject=f"New Bill: {bill_name}",
        body=f"You have been added to a new bill '{bill_name}'. You owe £{amount:.2f}.",
        recipients=[recipient_email]
    )


#Method to send an email to alert a user that someone has paid their share of a bill
def paid_bill_email(recipient_email, bill_name, payer_username, amount):
    #Gets the email of the current logged in user in the OS
    sender = f"{os.getlogin()}@dcs.warwick.ac.uk"
    
    #Method from the 'mail' library to send a message
    mail.send_message(
        sender=("Bill Splitter App", sender),
        subject=f"Payment Received: {bill_name}",
        body=f"IMPORTANT: {payer_username} has paid their share of £{amount:.2f} for the bill '{bill_name}'.\n\nLog in to view proof of payment.",
        recipients=[recipient_email]
    )