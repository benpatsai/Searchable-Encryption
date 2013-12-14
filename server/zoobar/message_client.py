from debug import *
from zoodb import *
import rpclib
import bank
#(progname, sockname) = sys.argv

def new_message(sender, recipient, content):
    with rpclib.client_connect('/msgsvc/sock') as c:
        kwargs =  {'sender':sender,'recipient':recipient,'content':content}
        return c.call('new_message', **kwargs)
    ## Fill in code here.

def get_my_message(username):
    with rpclib.client_connect('/msgsvc/sock') as c:
        kwargs =  {'username':username}
        return c.call('get_my_message', **kwargs)
    ## Fill in code here.

