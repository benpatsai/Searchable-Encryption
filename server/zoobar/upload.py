from flask import g, render_template, request, Flask, url_for, make_response
from login import requirelogin
from debug import *
from zoodb import *
from werkzeug import secure_filename
import cgi, os, time, json
import cgitb; cgitb.enable()

@catch_err
@requirelogin

def upload():
    userdir = 'uploads/' + g.user.person.username + '/'
    if not os.path.exists(userdir):
        os.mkdir(userdir,0777)
    message = ''
    filelists = os.listdir('uploads/'+g.user.person.username)
    filestats = []

    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(userdir, filename))
            message = 'Successfully Uploaded'

    for i in filelists:
        a = os.stat(os.path.join(userdir,i))
        filestats.append([i,time.ctime(a.st_ctime)]) #[file,created]
    args = {}
    args['filestats'] = filestats       
    args['message'] = message
    return render_template('upload.html', **args)
