from flask import g, render_template, request, Flask, url_for, make_response
from login import requirelogin
from debug import *
from zoodb import *
from search_in_file import *
from werkzeug import secure_filename
import cgi, os, time, json
import cgitb; cgitb.enable()

@catch_err
@requirelogin

def search():
    userdir = 'uploads/' + g.user.person.username + '/'
    if not os.path.exists(userdir):
        os.mkdir(userdir,0777)
    searchResults = []

    if request.method == 'POST':
        keyword = request.values['keyword']
        filename = request.values['filename']
        if keyword:
            if filename == 'ALL':
                filelists = os.listdir('uploads/'+g.user.person.username)
                for f in filelists:
                    if search_in_file(userdir+f, keyword):
                        searchResults.append(f)
            else:
                if search_in_file(userdir+filename, keyword):
                    searchResults.append(filename)
    return make_response(json.dumps(searchResults))

