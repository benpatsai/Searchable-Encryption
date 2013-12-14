from flask import g, render_template, request, Flask, url_for, make_response, send_file
from login import requirelogin
from debug import *
from zoodb import *
from search_in_file import *
from werkzeug import secure_filename
import cgi, os, time
import cgitb; cgitb.enable()

@catch_err
@requirelogin

def download():
    userdir = '/uploads/' + g.user.person.username + '/'
    if not os.path.exists(userdir):
        os.mkdir(userdir,0777)
    filename = request.values['filename']
    filepath = userdir+filename
    filesize = str(os.path.getsize(filepath))
    response = make_response( send_file(filepath, as_attachment= True, attachment_filename = filename))
    response.headers['Content-Length'] = filesize
    return response
