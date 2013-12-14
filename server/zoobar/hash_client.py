from debug import *
from zoodb import *
import rpclib
import xmlrpclib

#(progname, sockname) = sys.argv
'''
def search_hash(username, filename, keyword):
    with rpclib.client_connect('/hashsvc/sock') as c:
        kwargs =  {'username':username,'filename':filename, 'keyword':keyword}
        return c.call('search_hash', **kwargs)
    ## Fill in code here.

def load_user(username):
    with rpclib.client_connect('/hashsvc/sock') as c:
        kwargs =  {'username':username}
        return c.call('load_user', **kwargs)
    ## Fill in code here.

def load_file(username, filename):
    with rpclib.client_connect('/hashsvc/sock') as c:
        kwargs =  {'username':username,'filename':filename}
        return c.call('load_file', **kwargs)
    ## Fill in code here.
'''
def search_hash(username, filename, keyword):
    s = xmlrpclib.ServerProxy('http://localhost:8000')
    return s.search_hash(username, filename, keyword)
    ## Fill in code here.

def load_user(username):
    s = xmlrpclib.ServerProxy('http://localhost:8000')
    return s.load_user(username)
    ## Fill in code here.

def load_file(username, filename):
    s = xmlrpclib.ServerProxy('http://localhost:8000')
    return s.load_file(username, filename)
    ## Fill in code here.

