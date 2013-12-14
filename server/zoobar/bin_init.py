from flask import g, render_template, request, Flask, url_for, make_response
from login import requirelogin
from debug import *
from zoodb import *
from search_in_file import *
from werkzeug import secure_filename
import cgi, os, time, json
import cgitb; cgitb.enable()
import bin_client
import search_tools as st

@catch_err
@requirelogin


def bin_init():
    userdir = 'uploads/' + g.user.person.username + '/bin/'
    username = g.user.person.username
    if not os.path.exists(userdir):
        os.mkdir(userdir,0777)

    if request.method == 'POST':
        kw_len = (int)(request.values['kw_len'])
        filename = request.values['filename']
        try:    
            with open(userdir+filename+'_bin','r') as f:
                data = f.read()
        except IOError:
            return make_response(json.dumps(None))
        #bin_client.bin_load_file(username, filename)
        data = json.loads(data)
        cur = 0
        left = 1  # These are the positions in the array of the left
        right = 2 # and right blocks

        state = [cur, left, right]
        f = open('uploads/'+g.user.person.username+'/state','w+')
        f.write(json.dumps(state))
        f.close()

        data = data["bin_search_tree"]
    
        with open(userdir + filename, 'r') as f:
            filecontents = json.loads(f.read())

        cur_idx = data[cur]
        left_idx = data[left]
        right_idx = data[right]

        def get_blocks(start, end):   
            start = start / st.BLOCK_SIZE # find right block
            end = (end -1) / st.BLOCK_SIZE
            return filecontents[start:end+1] 

        result = (get_blocks(cur_idx, cur_idx + kw_len), 
                cur_idx,
                get_blocks(left_idx, left_idx + kw_len),
                left_idx,
                get_blocks(right_idx, right_idx + kw_len), 
                right_idx);

    return make_response(json.dumps(result))
