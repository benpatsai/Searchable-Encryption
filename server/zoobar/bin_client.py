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
def get_data(username, filename, idx):
    s = xmlrpclib.ServerProxy('http://localhost:8000')
    return s.get_data(username, filename, idx)
    ## Fill in code here.

def get_data_len(username, filename):
    s = xmlrpclib.ServerProxy('http://localhost:8000')
    return s.get_data_len(username, filename)
    ## Fill in code here.

def get_blocks(username, filename, start, end):
    s = xmlrpclib.ServerProxy('http://localhost:8000')
    return s.get_blocks(username, filename, start, end)
    ## Fill in code here.

def bin_load_file(username, filename):
    s = xmlrpclib.ServerProxy('http://localhost:8000')
    return s.bin_load_file(username, filename)
    ## Fill in code here.

