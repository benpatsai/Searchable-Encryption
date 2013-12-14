#!/usr/bin/python
#
#
import rpclib
import sys
import auth_client
from zoodb import *
from debug import *

class ProfileDatabaseRpcServer(rpclib.RpcServer):
    def rpc_new_profile(self, username):
        profile_db = profile_setup()
        newprofile = Profile()
        newprofile.username = username
        profile_db.add(newprofile)
        profile_db.commit()
        return True

    def rpc_modify(self, username, update, token):
        if auth_client.check_token(username, token):
            profiledb = profile_setup()
            person = profiledb.query(Profile).get(username)
            person.profile = update
            profiledb.commit()
        else:
            profiledb = profile_setup()
            person = profiledb.query(Profile).get(username)
        return person.profile

    def rpc_get_profile(self, username):
        profiledb = profile_setup()
        person = profiledb.query(Profile).get(username)
        return person.profile 


    pass

(_, dummy_zookld_fd, sockpath) = sys.argv

s = ProfileDatabaseRpcServer()
s.run_sockpath_fork(sockpath)
