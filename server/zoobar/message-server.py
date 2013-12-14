#!/usr/bin/python
#
# Insert bank server code here.
#
import rpclib
import sys
import bank
import time
from debug import *
from zoodb import *

class MessageRpcServer(rpclib.RpcServer):
    def rpc_new_message(self, sender, recipient, content):
        messagedb = message_setup()
        message = Message()
        message.sender = sender
        message.recipient = recipient
        message.content = content
        message.time = time.asctime()

        messagedb.add(message)
        messagedb.commit()
        

    def rpc_get_my_message(self, username):
        messagedb = message_setup()
        messages = messagedb.query(Message).filter(Message.recipient==username)
        ret_msg = []
        for msg in messages:
            ret_msg.append([msg.sender, msg.content, msg.time])
        return ret_msg
    pass

(_, dummy_zookld_fd, sockpath) = sys.argv

s = MessageRpcServer()
s.run_sockpath_fork(sockpath)
