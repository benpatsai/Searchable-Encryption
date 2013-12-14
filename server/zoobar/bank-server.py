#!/usr/bin/python
#
# Insert bank server code here.
#
import rpclib
import sys
import bank
from debug import *

class BankRpcServer(rpclib.RpcServer):
    def rpc_transfer(self, sender, recipient, zoobars, token):
        return bank.transfer(sender, recipient, zoobars, token)

    def rpc_balance(self, username):
        return bank.balance(username)

    def rpc_get_log(self, username):
        return bank.get_log(username)
    ## Fill in RPC methods here.
    def rpc_new_user(self, username):
        return bank.new_user(username)

    pass

(_, dummy_zookld_fd, sockpath) = sys.argv

s = BankRpcServer()
s.run_sockpath_fork(sockpath)
