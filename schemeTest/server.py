#!/usr/bin/python
##
## Run this server using something like:
##
##   ./rpctest-server.py 0 /tmp/xsock

import rpclib
import sys
import shutil
import os

class SchemeTestServer(rpclib.RpcServer):

    def rpc_search(self, user, keyword):
        resultlist = []
        filelists = os.listdir(user + '/')
        for f in filelists:
            linestring = open(user+'/'+f, 'r').read()
            linestring += ' '
            linestring = linestring.replace('\n',' ')
            words = linestring.split(' ')
            if keyword in words:
                resultlist.append(f)

        return resultlist

    def rpc_upload(self, user, path, filename):
        userdir = user + '/' 
        if not os.path.exists(userdir):
            os.mkdir(userdir,0777)
        shutil.copy2(path, userdir + filename)
        return 'success'

    def rpc_request1(self, **kwargs):
        return 'response1'
        
    def rpc_request2(self, **kwargs):
        return 'response2'
    
(_, dummy_zookld_fd, sockpath) = sys.argv
    
s = SchemeTestServer()
s.run_sockpath_fork(sockpath)

