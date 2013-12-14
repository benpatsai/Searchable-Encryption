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

def registerPkey():
    f = open('Pkey_list','r').read();
    if request.method == 'POST':
        n = request.values['n']
        e = request.values['e']
        if f =='':
            Pkey_list = {g.user.person.username:''}
        else:
            Pkey_list = json.loads(f) 
        Pkey_list[g.user.person.username] = {'n':n , 'e':e}
        print Pkey_list
        h = open('Pkey_list','w')
        h.write(json.dumps(Pkey_list))
        h.close()
        result = "success"
    if request.method == 'GET':
        user = request.values['user']
        Pkey_list = json.loads(f)
        if user not in Pkey_list.keys():
            return make_response("not found")
        Pkey = Pkey_list[user]
        result = json.dumps(Pkey)

    response = make_response(result)
    return response
