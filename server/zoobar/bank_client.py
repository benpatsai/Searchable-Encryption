from debug import *
from zoodb import *
import rpclib
import bank
#(progname, sockname) = sys.argv

def transfer(sender, recipient, zoobars, token):
    with rpclib.client_connect('/banksvc/sock') as c:
        kwargs =  {'sender':sender,'recipient':recipient,'zoobars':zoobars,'token':token}
        return c.call('transfer', **kwargs)
    ## Fill in code here.

def balance(username):
    with rpclib.client_connect('/banksvc/sock') as c:
        kwargs =  {'username':username}
        return c.call('balance', **kwargs)
    ## Fill in code here.

def get_log(username):
        return bank.get_log(username)
    ## Fill in code here.

def new_user(username):
    with rpclib.client_connect('/banksvc/sock') as c:
        kwargs =  {'username':username}
        return c.call('new_user', **kwargs)
    ## Fill in code here.

