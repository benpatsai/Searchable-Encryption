from flask import g, render_template, request, Flask, url_for, make_response
from login import requirelogin
from debug import *
from zoodb import *
from search_in_file import *
from werkzeug import secure_filename
import cgi, os, time, json
import cgitb; cgitb.enable()
import hash_client
import search_tools as st

@catch_err
@requirelogin


def bin_search():
    userdir = 'uploads/' + g.user.person.username + '/bin/'
    if not os.path.exists(userdir):
        os.mkdir(userdir,0777)

    if request.method == 'POST':
        kw_len = (int)(request.values['kw_len'])
        filename = request.values['filename']
        choice = (int)(request.values['choice'])
    
        with open(userdir+filename+'_bin','r') as f:
            data = (json.loads(f.read()))["bin_search_tree"]
        data_len = len(data)

        with open('uploads/'+g.user.person.username+'/state','r') as f:
            state = json.loads(f.read())
        [cur, left, right] = state           

        with open(userdir + filename, 'r') as f:        
            filecontents = json.loads(f.read())

        if choice == st.LEFT:
            cur = left
        elif choice == st.RIGHT:
            cur = right
        else:
            result = (None, None, None, None)
            return make_response(json.dumps(result))
        left = cur*2 + 1
        right = cur*2 + 2
        if left == data_len-1:
            left_idx = data[left]
            right_idx = None
        elif left >= data_len:
            left_idx = None
            right_idx = None 
        else:
            left_idx = data[left]
            right_idx = data[right]

        def get_blocks(start, end):
            start = start / st.BLOCK_SIZE # find right block
            end = (end -1) / st.BLOCK_SIZE
            return filecontents[start:end+1]

        left_content = None
        right_content = None
        if left_idx is not None:
            left_content = get_blocks(left_idx, left_idx + kw_len)
        if right_idx is not None:
            right_content = get_blocks(right_idx, right_idx + kw_len)
        result = {"result":(left_content, left_idx, right_content, right_idx)}
        state = [cur, left, right]

        f = open('uploads/'+g.user.person.username+'/state','w')
        f.write(json.dumps(state))
        f.close()
        return make_response(json.dumps(result))
