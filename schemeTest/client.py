#!/usr/bin/python

import rpclib
        
#(progname, sockname) = sys.argv
def search(user, keyword):
    with rpclib.client_connect('/tmp/xsock') as c:
        kwargs = {'user':user, 'keyword':keyword} 
        return c.call('search', **kwargs)

def upload(user, path, filename):
    with rpclib.client_connect('/tmp/xsock') as c:
        kwargs = {'user':user, 'path':path, 'filename':filename} 
        return c.call('upload', **kwargs)
  
def request1():
    with rpclib.client_connect('/tmp/xsock') as c:
        kwargs = {} 
        return c.call('request1', **kwargs)
        
def request2():
    with rpclib.client_connect('/tmp/xsock') as c:
        kwargs = {} 
        return c.call('request2', **kwargs)

