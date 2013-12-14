from debug import *
from zoodb import *
import rpclib

#(progname, sockname) = sys.argv

def modify(username, update, token):
    with rpclib.client_connect('/profileDBsvc/sock') as c:
        kwargs =  {'username':username,'update':update,'token':token}
        return c.call('modify', **kwargs)
    ## Fill in code here.

def get_profile(username):
    with rpclib.client_connect('/profileDBsvc/sock') as c:
        kwargs =  {'username':username}
        return c.call('get_profile', **kwargs)
    ## Fill in code here.




