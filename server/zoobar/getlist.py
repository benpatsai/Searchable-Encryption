from flask import g, render_template, request, Flask, url_for, make_response
from login import requirelogin
from debug import *
from zoodb import *
from werkzeug import secure_filename
import cgi, os, time, json
import cgitb; cgitb.enable()

@catch_err
@requirelogin

def getlist():
    userdir = 'uploads/' + g.user.person.username + '/'
    if not os.path.exists(userdir):
        os.mkdir(userdir,0777)
    filelists = os.listdir('uploads/'+g.user.person.username)
    return make_response(json.dumps(filelists))
