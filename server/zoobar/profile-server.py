#!/usr/bin/python
import re
import rpclib
import sys
import os
import sandboxlib
import urllib
import socket
import bank_client as bank
import zoodb
import urllib
from debug import *
from zoodb import *
## Cache packages that the sandboxed code might want to import
import time
import errno
import profileDB_client
import message_client

class ProfileAPIServer(rpclib.RpcServer):
    def __init__(self, user, visitor, token):
        self.user = user
        self.visitor = visitor
        self.token = token
        os.setuid(61017)
    def rpc_get_self(self):
        return self.user

    def rpc_get_visitor(self):
        return self.visitor

    def rpc_get_xfers(self, username):
        xfers = []
        for xfer in bank.get_log(username):
            xfers.append({ 'sender': xfer.sender,
                           'recipient': xfer.recipient,
                           'amount': xfer.amount,
                           'time': xfer.time,
                         })
        return xfers

    def rpc_get_user_info(self, username):
        person_db = zoodb.person_setup()
        p = person_db.query(zoodb.Person).get(username)
        if not p:
            return None
        return { 'username': p.username,
                 'profile': profileDB_client.get_profile(username),
                 'zoobars': bank.balance(username),
               }

    def rpc_xfer(self, target, zoobars):
        bank.transfer(self.user, target, zoobars, self.token)

    def rpc_get_my_message(self):
        return message_client.get_my_message(self.user)

def run_profile(pcode, user, profile_api_client):
    globals = {'api': profile_api_client}
    exec pcode in globals

class ProfileServer(rpclib.RpcServer):
    def rpc_run(self, user, visitor):
        db = cred_setup()
        cred = db.query(Cred).get(user)
        token = cred.token
        pcode = profileDB_client.get_profile(user)

        uid = 61016
        user_re = user.replace("=","=e")
        user_re = user_re.replace("/","=s")
        user_re = user_re.replace("\n","=endl")
        user_re = user_re.replace("\0","=nul")
        visitor_re =  visitor.replace("=","=e")
        visitor_re = visitor_re.replace("/","=s")
        visitor_re = visitor_re.replace("\n","=endl")
        visitor_re = visitor_re.replace("\0","=nul")
        userdir = '/tmp/'+ user_re
        if not os.path.exists(userdir):
            os.mkdir(userdir,1770)
            os.chown(userdir,61016,61016)
        (sa, sb) = socket.socketpair(socket.AF_UNIX, socket.SOCK_STREAM, 0)
        pid = os.fork()
        if pid == 0:
            if os.fork() <= 0:
                sa.close()
                ProfileAPIServer(user_re, visitor_re, token).run_sock(sb)
                sys.exit(0)
            else:
                sys.exit(0)
        sb.close()
        os.waitpid(pid, 0)

        sandbox = sandboxlib.Sandbox(userdir, uid, '/profilesvc/lockfile')
        with rpclib.RpcClient(sa) as profile_api_client:
            return sandbox.run(lambda: run_profile(pcode, user, profile_api_client))

(_, dummy_zookld_fd, sockpath) = sys.argv

s = ProfileServer()
s.run_sockpath_fork(sockpath)
