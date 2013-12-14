from flask import g, render_template, request, Flask, url_for, make_response
from login import requirelogin
from debug import *
from zoodb import *
from search_in_file import *
from werkzeug import secure_filename
import cgi, os, time, json
import cgitb; cgitb.enable()
import hash_client
import shutil

@catch_err
@requirelogin


def share():
    userdir = 'uploads/' + g.user.person.username + '/enc/'
    friend = request.values['friend']
    filename = request.values['filename']
    msg1 = request.values['msg1']
    msg2 = request.values['msg2']

    if not os.path.exists(userdir):
        os.mkdir(userdir,0777)

    frienddir = 'uploads/' + friend
    if not os.path.exists(frienddir):
        os.mkdir(frienddir,0777)

    frienddir = 'uploads/' + friend + '/enc/'
    if not os.path.exists(frienddir):
        os.mkdir(frienddir,0777)

    shutil.copy2(userdir+filename+"hash", frienddir+filename+"hash")
    shutil.copy2(userdir+filename+"block", frienddir+filename+"block")

    frienddir = 'uploads/' + friend+'/'
   
    f = open(frienddir+'msg','a')
    f.write(filename+'\n')
    f.write(msg1+'\n')
    f.write(msg2+'\n')

    return make_response("success")

