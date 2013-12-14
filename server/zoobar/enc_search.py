from flask import g, render_template, request, Flask, url_for, make_response
from login import requirelogin
from debug import *
from zoodb import *
from search_in_file import *
from werkzeug import secure_filename
import cgi, os, time, json
import cgitb; cgitb.enable()
import hash_client

@catch_err
@requirelogin


def enc_search():
    userdir = 'uploads/' + g.user.person.username + '/enc/'
    if not os.path.exists(userdir):
        os.mkdir(userdir,0777)
    searchResults = {}

    if request.method == 'POST':
        keyword = request.values['keyword']
        filename = request.values['filename']
        result = {'idx':-1}

        if keyword:
            #h = open(userdir+filename+'hash','r').read()
            #hashes = json.loads(h)
            #idx = -1
            #for (hashed_substr,enc_index) in hashes:
            '''log(hashed_substr)'''
            #if keyword in hashes.keys():
            #    idx = hashes[keyword]
            
            result['idx'] = hash_client.search_hash(g.user.person.username, filename, keyword)
    return make_response(json.dumps(result))
