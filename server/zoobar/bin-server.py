#!/usr/bin/python

import rpclib
import sys
import auth
import json, os
import socket
import stat
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
import search_tools as st
# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)
'''
class HashRpcServer:
    def __init__(self):
        self.hash_dic = {}

    def search_hash(self, username, filename, keyword):
        print self.hash_dic
        user_hash = self.hash_dic[username]
        hashes = user_hash[filename]
        idx = -1
        if keyword in hashes.keys():
            idx = hashes[keyword]
        return idx

    def load_user(self, username):
        userdir = 'uploads/' + username + '/enc/'
        filelists = os.listdir(userdir)
        user_hash = {}
        for f in filelists:
            if f[-4:] == 'hash':
                h = open(f,'r').read()
                hashes = json.loads(h)
                user_hash[f[:-4]] = hashes
        self.hash_dic[username] = user_hash
        print self.hash_dic
        return "success"

    def load_file(self, username, filename):
        userdir = 'uploads/' + username + '/enc/'
        h = open(userdir+filename+'hash','r').read()
        hashes = json.loads(h)
        if not username in self.hash_dic.keys():
            self.hash_dic[username] = {}
        user_hash = self.hash_dic[username]
        user_hash[filename] = hashes
        self.hash_dic[username] = user_hash
        print self.hash_dic
        return "Success"
    ## Fill in RPC methods here.
    pass
'''
bin_dic = {}
file_dic = {}

server = SimpleXMLRPCServer(("localhost", 8000),
                            requestHandler=RequestHandler)
server.register_introspection_functions()

#-1 represents not in list of hashes
#-2 represents in list 1 (occurs multiple times in input)
#else is nonnegative index from list 0 (occurs once in input)
def get_data(username, filename,idx):
    global bin_dic
    return bin_dic[username][filname][idx]
server.register_function(get_data,'get_data')

def get_data_len(username, filename):
    global bin_dic
    return len(bin_dic[username][filname])
server.register_function(get_data_len,'get_data_len')

def load_file(username, filename):
    global bin_dic

    userdir = 'uploads/' + username + '/bin/'
    h = open(userdir+filename+'bin','r').read()
    bines = json.loads(h)["bin_search_tree"]
    if not username in bin_dic.keys():
        bin_dic[username] = {}
    user_bin = bin_dic[username]
    user_bin[filename] = bines
    bin_dic[username] = user_bin

    content = open(userdir+filename,'r').read()
    if not username in file_dic.keys():
        file_dic[username] = {}
    user_file = file_dic[username]
    user_file[filename] = content
    file_dic[username] = user_file


    return "Success"
server.register_function(load_file,'load_file')

def get_blocks(username, filename, start, end):   
    start = start / st.BLOCK_SIZE # find right block
    start = start * st.BLOCK_SIZE # scale by BLOCK_SIZE
    if end % st.BLOCK_SIZE != 0:
        end = end / st.BLOCK_SIZE
        end = (end + 1) * st.BLOCK_SIZE
    return file_dic[username][filename][start:end] 
server.register_function(get_blocks,'get_blocks')


server.serve_forever()