from zoodb import *
from debug import *

import hashlib
import random
import string
import pbkdf2
import os
import bank_client
import profileDB_client

def gen_random_string(alphabet, length=10):
    r = random.SystemRandom()
    return u''.join(r.choice(alphabet) for _ in range(length))

def newtoken(db, cred):
    hashinput = "%s%.10f" % (cred.password, random.random())
    cred.token = hashlib.md5(hashinput).hexdigest()
    db.commit()
    return cred.token

def login(username, password):
    db = cred_setup()
    cred = db.query(Cred).get(username)
    if not cred:
        return None
    if cred.password == pbkdf2.PBKDF2(password,cred.salt).hexread(32):
        return newtoken(db, cred)
    else:
        return None

def register(username, password):
    person_db = person_setup()
    cred_db = cred_setup()
    person = person_db.query(Person).get(username)
    cred = cred_db.query(Cred).get(username)
    if person:
        return None
    newperson = Person()
    newcred = Cred()
    newperson.username = username
    newcred.username = username
    newcred.salt = gen_random_string(string.ascii_letters)
    newcred.password = pbkdf2.PBKDF2(password,newcred.salt).hexread(32)
    person_db.add(newperson)
    person_db.commit()
    cred_db.add(newcred)
    cred_db.commit()
    profileDB_client.new_profile(username)
    return newtoken(cred_db, newcred)

def check_token(username, token):
    db = cred_setup()
    cred = db.query(Cred).get(username)
    if cred and cred.token == token:
        return True
    else:
        return False

