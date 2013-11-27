#!/usr/bin/python
##
## Run this server using something like:
##
##   ./rpctest-server.py 0 /tmp/xsock

import rpclib
import sys
import hashlib
from debug import *

class MyServer(rpclib.RpcServer):
    def rpc_search(self, **kwargs):
        return ''
        
    def rpc_echo(self, **kwargs):
        print >>sys.stderr, 'running echo', kwargs
        return kw_sorted(kwargs)
    
(_, dummy_zookld_fd, sockpath) = sys.argv
    
s = MyRpcServer()
setattr(s, 'rpc_hash take\ntwo', MyRpcServer.rpc_hash.__get__(s, MyRpcServer))
s.run_sockpath_fork(sockpath)

