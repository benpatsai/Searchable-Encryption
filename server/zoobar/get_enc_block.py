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


def get_enc_block():
    userdir = 'uploads/' + g.user.person.username + '/enc/'
    if not os.path.exists(userdir):
        os.mkdir(userdir,0777)
    result = {}
 
    if request.method == 'POST':
        start = int(request.values['start'])
        end = int(request.values['end'])
        filename = request.values['filename']
        f = open(userdir+filename+'block','r').read()
        enc_block = json.loads(f)
        result['enc_block'] = enc_block[start:end+1]
    return make_response(json.dumps(result))

