from zoodb import *
from debug import *

import time
import auth_client
def transfer(sender, recipient, zoobars, token):
    bankdb = bank_setup()
    senderp = bankdb.query(Bank).get(sender)
    recipientp = bankdb.query(Bank).get(recipient)
    sender_balance = senderp.zoobars
    recipient_balance = recipientp.zoobars
    if not auth_client.check_token(sender, token):
        return False
    if sender != recipient :
        sender_balance = senderp.zoobars - zoobars
        recipient_balance = recipientp.zoobars + zoobars

    if sender_balance < 0 or recipient_balance < 0:
        return False

    senderp.zoobars = sender_balance
    recipientp.zoobars = recipient_balance
    bankdb.commit()

    transfer = Transfer()
    transfer.sender = sender
    transfer.recipient = recipient
    transfer.amount = zoobars
    transfer.time = time.asctime()

    transferdb = transfer_setup()
    transferdb.add(transfer)
    transferdb.commit()
    return True

def balance(username):
    db = bank_setup()
    bank = db.query(Bank).get(username)
    zoobars = bank.zoobars
    return zoobars

def get_log(username):
    db = transfer_setup()
    arg = db.query(Transfer).filter(or_(Transfer.sender==username,
                                         Transfer.recipient==username))
    return arg
def new_user(username):
    bank_db = bank_setup()
    newbank = Bank()
    newbank.username = username
    bank_db.add(newbank)
    bank_db.commit()
    return True
    
