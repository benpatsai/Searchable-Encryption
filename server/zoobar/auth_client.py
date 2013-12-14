from debug import *
from zoodb import *
import rpclib

#(progname, sockname) = sys.argv

def login(username, password):
    with rpclib.client_connect('/authsvc/sock') as c:
        kwargs =  {'username':username,'password':password}
        return c.call('login', **kwargs)
    ## Fill in code here.

def register(username, password):
    with rpclib.client_connect('/authsvc/sock') as c:
        kwargs =  {'username':username,'password':password}
        return c.call('register', **kwargs)
    ## Fill in code here.

def check_token(username, token):
    with rpclib.client_connect('/authsvc/sock') as c:
        kwargs =  {'username':username,'token':token}
        return c.call('check_token', **kwargs)
    ## Fill in code here.


