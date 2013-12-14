#!/usr/bin/env python

from flask import Flask, g

import login
import index
import users
import transfer
import echo
import zoobarjs
import zoodb
import upload
import enc_upload
import bin_upload
import download
import enc_download
import search
import enc_search
import bin_search
import getlist
import registerPkey
import get_enc_block
#import get_file_list
import share
import bin_init

from debug import catch_err

app = Flask(__name__)

app.add_url_rule("/", "index", index.index, methods=['GET', 'POST'])
app.add_url_rule("/users", "users", users.users)
app.add_url_rule("/transfer", "transfer", transfer.transfer, methods=['GET', 'POST'])
app.add_url_rule("/zoobarjs", "zoobarjs", zoobarjs.zoobarjs, methods=['GET'])
app.add_url_rule("/upload","upload",upload.upload, methods=['GET', 'POST'])
app.add_url_rule("/enc_upload","enc_upload",enc_upload.enc_upload, methods=['GET', 'POST'])
app.add_url_rule("/bin_upload","bin_upload",bin_upload.bin_upload, methods=['GET', 'POST'])
app.add_url_rule("/download","download",download.download, methods=['GET'])
app.add_url_rule("/enc_download","enc_download",enc_download.enc_download, methods=['GET'])
app.add_url_rule("/search","search",search.search, methods=['GET', 'POST'])
app.add_url_rule("/enc_search","enc_search",enc_search.enc_search, methods=['GET', 'POST'])
app.add_url_rule("/bin_search","bin_search",bin_search.bin_search, methods=['GET', 'POST'])
app.add_url_rule("/get_enc_block","get_enc_block",get_enc_block.get_enc_block, methods=['GET', 'POST'])
app.add_url_rule("/getlist","getlist",getlist.getlist, methods=['GET'])
app.add_url_rule("/registerPkey","registerPkey",registerPkey.registerPkey, methods=['GET', 'POST'])
app.add_url_rule("/share","share",share.share, methods=['GET', 'POST'])
app.add_url_rule("/bin_init","bin_init",bin_init.bin_init, methods=['GET', 'POST'])

#app.add_url_rule("/get_file_list","get_file_list",get_file_list.get_file_list, methods=['GET', 'POST'])

app.add_url_rule("/login", "login", login.login, methods=['GET', 'POST'])
app.add_url_rule("/logout", "logout", login.logout)
app.add_url_rule("/echo", "echo", echo.echo)

@app.after_request
@catch_err
def disable_xss_protection(response):
    response.headers.add("X-XSS-Protection", "1")
    return response

if __name__ == "__main__":
    app.run()
