from flask import Blueprint, render_template, redirect, url_for, session
from routes.models import users, bills, payments
import os
from routes.extensions import mail

def send_bill_email(recipient_email, bill_name, amount):
    sender = f"{os.getlogin()}@dcs.warwick.ac.uk"
    
    mail.send_message(
        sender=("Bill Splitter App", sender),
        subject=f"New Bill: {bill_name}",
        body=f"You have been added to a new bill '{bill_name}'. You owe £{amount:.2f}.",
        recipients=[recipient_email]
    )

def paid_bill_email(recipient_email, bill_name, payer_username, amount):
    sender = f"{os.getlogin()}@dcs.warwick.ac.uk"
    
    mail.send_message(
        sender=("Bill Splitter App", sender),
        subject=f"Payment Received: {bill_name}",
        body=f"IMPORTANT: {payer_username} has paid their share of £{amount:.2f} for the bill '{bill_name}'.\n\nLog in to view proof of payment.",
        recipients=[recipient_email]
    )