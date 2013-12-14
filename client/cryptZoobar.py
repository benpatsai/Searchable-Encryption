#!/usr/bin/python
import urllib
import requests
import cmd, os, shutil
import time
import json
import base64
from subprocess import call
from sa import *
import search_tools as st
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import MD5
from Crypto.Cipher import AES
from Crypto import Random
#from pbkdf2 import PBKDF2


s = requests.session()
ID = ''
PW = ''
MPW = ''
profile = { 'enc':{} , 'bin':{}}
website = "http://128.30.93.9:8080/zoobar/index.cgi/"
#salt=random_str(10)
#print salt

def search_hash(hashed_query, filename):
    global s, profile, ID

    url = website+"enc_search"
    payload = {"keyword" : hashed_query, "filename": filename}
    r = s.post(url, data = payload)
    #print r.text
    result = json.loads(r.text)
    return result['idx']

def get_encrypted_blocks(filename, start, end):
    global s, profile, ID

    url = website+"get_enc_block"
    payload = {"start" : start, "end":end, "filename": filename}
    r = s.post(url, data = payload)
    #print r.text
    result = json.loads(r.text)
    return result['enc_block']
    #f = open(filename+'block').read()
    #enc_block = json.loads(f)
    #return enc_block[start:end+1]


def search_substring(query,salt,key_index,block_index_iv,key_blocks, filename):
    global s, profile, ID
  
    #First, check if the whole query is in the list of hashes
    enc_index=search_hash(hash_with_salt(query,salt), filename)
    if enc_index == -2:
        return -2
        #TODO: Is this the value it should return if it found multiple matches but doesn't know the index?
    elif enc_index!=-1:
        return decrypt_integer(enc_index,block_index_iv,key_index)

    #Now, do binary search to find the longest subquery in the list of hashes
    upper = len(query)
    lower = 1

    enc_ind = -1
    while upper >= lower:
        mid = (upper + lower) / 2
        enc_ind = search_hash(hash_with_salt(query[0:mid],salt), filename)
        #print "Querying for %s at location %d in range %d,%d"%(query[0:mid],mid,lower,upper)
        #print "Received answer ",enc_ind

        if enc_ind == -1:
            upper = mid - 1
        elif enc_ind == -2:
            lower = mid + 1
        else:
            break
    if enc_ind == -1 or enc_ind == -2:
        return -1

    #We received an index from the hash table. Now see if the index matches.
    index=decrypt_integer(enc_ind,block_index_iv,key_index)
    start_index=index
    end_index=start_index+len(query)
    start_block_index=start_index/st.BLOCK_SIZE
    end_block_index=(end_index-1)/st.BLOCK_SIZE

    encrypted_blocks=get_encrypted_blocks(filename, start_block_index,end_block_index)
    decrypted_string=''

    for (index1,encrypted_block) in enumerate(encrypted_blocks):
        block_id=start_block_index+index1
        decrypted_string+=decrypt_block(encrypted_block,block_id,block_index_iv,key_blocks)
    #print decrypted_string
    check_start_index=start_index-start_block_index*st.BLOCK_SIZE
    check_end_index=check_start_index+len(query)
    to_compare=decrypted_string[check_start_index:check_end_index]
    if (to_compare==query):
        return index
    else:
        return -1

    
    
    '''
    prefix_len=len(query)
    delta=next_greater_power_of_2(prefix_len)/2

    enc_shorter_index=search_hash(hash_with_salt(query[0:prefix_len-1],salt),filename)

    while not((enc_index==-1) and (enc_shorter_index!=-1)):
        if enc_shorter_index == -1:
            prefix_len-=delta
        if enc_index > -1:
            prefix_len+=delta
        delta=delta/2
        enc_index=search_hash(hash_with_salt(query[0:(0 if prefix_len<0 else prefix_len)],salt), filename)
        enc_shorter_index=(0 if (prefix_len - 1 <= 0 ) else (search_hash(hash_with_salt(query[0:(prefix_len-1)],salt), filename)))

    index=decrypt_integer(enc_shorter_index,block_index_iv,key_index)
    start_index=index
    end_index=start_index+len(query)
    start_block_index=start_index/st.BLOCK_SIZE
    end_block_index=(end_index-1)/st.BLOCK_SIZE
    '''

    '''
    encrypted_blocks=get_encrypted_blocks(filename, start_block_index,end_block_index)
    decrypted_string=''
    for (index1,encrypted_block) in enumerate(encrypted_blocks):
        block_id=start_block_index+index1
        decrypted_string+=decrypt_block(encrypted_block,block_id,block_index_iv,key_blocks)
    #print decrypted_string
    check_start_index=start_index-start_block_index*st.BLOCK_SIZE
    check_end_index=check_start_index+len(query)
    to_compare=decrypted_string[check_start_index:check_end_index]
    if (to_compare==query):
        return index
    else:
        return -1
'''

def RSA_key_gen():
    key = RSA.generate(2048)
    return [key.n,key.e,key.d,key.p,key.q,key.u]

def upload_profile(username):
    global s, profile, ID, MPW, PW
    Mkey=MD5.new()
    Mkey.update(MPW+'iv')
    #Mkey = PBKDF2(MPW+'iv',"aaaaaaaa").read(32)
    iv = Mkey.hexdigest()[:AES.block_size]
    #iv = Mkey[:AES.block_size]

    Mkey=MD5.new()
    Mkey.update(PW)
    #Mkey = PBKDF2(MPW,"aaaaaaaa").read(32)

    cipher = AES.new(Mkey.hexdigest(), AES.MODE_CFB, iv)
    #cipher = AES.new(Mkey, AES.MODE_CFB, iv)


    #print profile
    enc_profile = iv + cipher.encrypt(json.dumps(profile))
    iv_size = AES.block_size
    dec_profile = cipher.decrypt(enc_profile)[iv_size:]
    #print dec_profile
    f = open(username+'profile','w')
    f.write(enc_profile)
    f.close()
    url = website+"upload"
    files = {'file': (username+'profile', open(username+'profile','rb'))}
    s.post(url, files=files)

    f = open('msg','w')
    f.write("")
    url = website+"upload"
    files = {'file': ('msg', open('msg','rb'))}
    s.post(url, files=files)


def download_profile(username):
    global s, profile, ID, MPW, PW
    Mkey=MD5.new()
    Mkey.update(MPW+'iv')
    #Mkey = PBKDF2(MPW+'iv',"aaaaaaaa").read(32)
    iv = Mkey.hexdigest()[:AES.block_size]
    #iv = Mkey[:AES.block_size]

    Mkey=MD5.new()
    Mkey.update(PW)
    #Mkey = PBKDF2(MPW,"aaaaaaaa").read(32)

    cipher = AES.new(Mkey.hexdigest(), AES.MODE_CFB, iv)
    #cipher = AES.new(Mkey, AES.MODE_CFB, iv)
    url = website+"download"
    payload = {"filename" : username+'profile'}
    r = s.get(url, params=payload)
    f = open(username+'profile', 'wb')
    for chunk in r.iter_content(chunk_size=512 * 1024):
        if chunk: # filter out keep-alive new chunks
            f.write(chunk)
    f.close()

    f = open(username+'profile','r').read()
    iv_size = AES.block_size
    ptxt = cipher.decrypt(f)[iv_size:]
    dec = cipher.decrypt(f)[iv_size:]
    #print dec
    profile = json.loads(dec)

    url = website+"download"
    payload = {"filename" : 'msg'}
    r = s.get(url, params=payload)
    f = open('msg', 'wb')
    for chunk in r.iter_content(chunk_size=512 * 1024):
        if chunk: # filter out keep-alive new chunks
            f.write(chunk)
    f.close()

    [n, e, d, p, q, u] = [profile['n'],profile['e'],profile['d'],profile['p'],profile['q'],profile['u'],]
    key = RSA.construct([long(n),long(e),long(d),long(p),long(q),long(u)])
    cipher = PKCS1_OAEP.new(key)


    f = open('msg')
    lines = f.readlines()
    f.close()
    i = 0
    while i+1 < len(lines):
        c1 = ''.join(chr(e) for e in (json.loads(lines[i+1])))
        c2 = ''.join(chr(e) for e in (json.loads(lines[i+2])))
        msg1 = cipher.decrypt(c1)
        msg2 = cipher.decrypt(c2)
        file_profile = json.loads(msg1+msg2)
        filename = file_profile['filename']
        overwrite = "y"
        Q = "Someone want to overwrite your file: "+filename+", is that OK? (y/n)"
        if filename in profile['enc'].keys():
            overwrite = raw_input(Q)
        if overwrite is not "n":
            profile['enc'][filename] = file_profile
        i = i+3



def login(username, password, MkeyPW):
    global s, profile, ID, MPW

    payload = { "submit_login" : "1" ,
            "login_username": username ,
            "login_password": password }

    r = s.post(website+"login", data=payload)

    if (username in r.text):
        ID = username
        MPW = MkeyPW
        PW = password
        download_profile(username)
        return True
    else:
        return False

def register(username, password, MkeyPW):
    [n, e, d, p, q, u] = RSA_key_gen()
    global s, profile, ID
    payload = { "submit_registration" : "1" ,
            "login_username": username ,
            "login_password": password }
    
    r = s.post(website+"login", data=payload)

    if 'Registration failed' in r.text:
        return False

    if username in r.text:
        ID = username
        MPW = MkeyPW
        PW = password
        pkey = {"n": n, "e": e}
        profile = {"enc":{}, "bin":{}, "n": str(n), "e": str(e), "d": str(d), "p": str(p), "q": str(q), "u":str(u)}
        upload_profile(username)
        s.post(website+"registerPkey", data=pkey)
        return True
    else:
        return False

def upload(filename, path):
    global s, profile, ID

    url = website+"upload"
    files = {'file': (filename, open(path,'rb'))}
    s.post(url, files=files)

def enc_upload(filename, path):
    global s, profile, ID

    f = open(path,'r').read()
    #salt = Random.new().read(AES.block_size)
    salt = [ord(x) for x in Random.new().read(AES.block_size)]
    #key_index = Random.new().read(AES.block_size)
    key_index = [ord(x) for x in Random.new().read(AES.block_size)]
    key_blocks = [ord(x) for x in Random.new().read(AES.block_size)]

    block_index_iv=random_str(15)
    encrypted_filename = encrypt_blocks(filename,key_blocks,block_index_iv,st.BLOCK_SIZE)
    enc_filename  = ''.join(str(e) for e in encrypted_filename[0])

    #key_blocks = Random.new().read(AES.block_size)
    profile['enc'][filename] = {'salt':salt, 'key_index':key_index, 'key_blocks':key_blocks, 'block_index_iv':block_index_iv, 'enc_filename':enc_filename, 'filename':filename}

    hashed = hash_substrings(f, salt,block_index_iv, key_index, path)
    #h = open(filename+'hash', 'w')
    #h = open(enc_filename+'hash', 'w')
    #h.write(json.dumps(hashed))
    #h.write(hashed)
    #h.close()
    h = open(enc_filename+'hash', 'wb')
    h.write(json.dumps(hashed))
    h.close()
    call(['gzip',enc_filename+'hash'])
    h = open(enc_filename+'hash.gz','r')
    zippedstring = h.read()
    h.close()
    os.unlink(enc_filename+'hash.gz')
    h = open(enc_filename+'hash', 'wb')
    h.write(base64.b64encode(zippedstring))
    h.close()
    zippedstring = ""


    url = website+"enc_upload"
    #files = {'file': (filename+'hash', open(filename+'hash','rb'))}
    files = {'file': (enc_filename+'hash', open(enc_filename+'hash','rb'))}

    s.post(url, files=files)
    print "done:hash upload"
    encrypted_blocks = encrypt_blocks(f,key_blocks,block_index_iv,st.BLOCK_SIZE)
    print "done:enc block"
    #b = open(enc_filename+'block','w')
    #b.write(json.dumps(encrypted_blocks))
    #b.close()
    b = open(enc_filename+'block','w')
    b.write(json.dumps(encrypted_blocks))
    b.close()
    call(['gzip',enc_filename+'block'])
    b = open(enc_filename+'block.gz','r')
    zippedblocks = b.read()
    b.close()
    os.unlink(enc_filename+'block.gz')
    b = open(enc_filename+'block','w')
    b.write(base64.b64encode(zippedblocks))
    b.close()
    zippedblocks = ""
    
    
    url = website+"enc_upload"
    files = {'file': (enc_filename+'block', open(enc_filename+'block','rb'))}
    s.post(url, files=files)
    print "done:enc_block upload"
    upload_profile(ID)

def bin_upload(filename, path):
    global s, profile, ID

    f = open(path,'r').read()
    key = [ord(x) for x in Random.new().read(AES.block_size)]
    iv = random_str(0)

    encrypted_filename = encrypt_blocks(filename, key, iv, st.BLOCK_SIZE)
    enc_filename  = ''.join(str(e) for e in encrypted_filename[0])

    profile['enc'][filename] = {'key':key, 'iv':iv, 'enc_filename':enc_filename, 'filename':filename}

    ### encrypt file ###
    encrypted_blocks = encrypt_blocks(f, key, iv, st.BLOCK_SIZE)

    tree = st.construct_suffix_tree(path)
    arr = st.tree_to_array(tree)

    aux_data = json.dumps({"bin_search_tree":arr});

    with open(enc_filename,'w') as b:
        b.write(json.dumps(encrypted_blocks))

    with open(enc_filename+'_bin','w') as b:
        b.write(aux_data)

    url = website+"bin_upload"
    files = {'file': (enc_filename+'_bin', open(enc_filename+'_bin','rb'))}
    s.post(url, files=files)

    files = {'file': (enc_filename, open(enc_filename,'rb'))}
    s.post(url, files=files)

    upload_profile(ID)


def download(filename, local_path):
    global s, profile, ID

    url = website+"download"
    payload = {"filename" : filename}
    r = s.get(url, params=payload)
    f = open(local_path, 'wb')
    for chunk in r.iter_content(chunk_size=512 * 1024):
        if chunk: # filter out keep-alive new chunks
            f.write(chunk)
    f.close()

def enc_download(filename, local_path):
    global s, profile, ID
    if filename not in profile['enc'].keys():
        print "Cannot find file!"
        return
    file_profile = profile['enc'][filename]
    salt = file_profile['salt']
    key_index = file_profile['key_index']
    key_blocks= file_profile['key_blocks']
    block_index_iv=file_profile['block_index_iv']
    enc_filename = file_profile['enc_filename']

    url = website+"enc_download"
    payload = {"filename" : enc_filename}
    r = s.get(url, params=payload)
    f = open(filename+'tmp', 'wb')
    for chunk in r.iter_content(chunk_size=512 * 1024):
        if chunk: # filter out keep-alive new chunks
            f.write(chunk)
    f.close()
 
    f = open(filename+'tmp','r').read()
    encrypted_blocks = json.loads(f)
    decrypted_string = '' 
    for (index1,encrypted_block) in enumerate(encrypted_blocks):
        block_id=index1
        decrypted_string+=decrypt_block(encrypted_block,block_id,block_index_iv,key_blocks)

    f = open(filename+'tmp','w')
    f.write(decrypted_string)
    f.close()

def search(keyword, filename):
    global s, profile, ID

    url = website+"search"
    payload = {"keyword" : keyword, "filename": filename}
    r = s.post(url, data = payload)
    result = json.loads(r.text)
    print result

def enc_search(keyword, filename):
    global s, profile, ID
    if filename not in profile['enc'].keys():
        print "Cannot find file!"
        return

    file_profile = profile['enc'][filename]
    salt = file_profile['salt']
    key_index = file_profile['key_index']
    key_blocks= file_profile['key_blocks']
    block_index_iv=file_profile['block_index_iv']
    enc_filename = file_profile['enc_filename']

    result = search_substring(keyword, salt, key_index, block_index_iv,key_blocks, enc_filename)
    if (result == -1):
        print "Not Found"
    else:
        print "Found"  

def bin_search(keyword, filename):
    global s, profile, ID
    if filename not in profile['enc'].keys():
        print "The file requested could not be found!"
        return

    file_profile = profile['enc'][filename]
    key = file_profile['key']
    iv = file_profile['iv']
    enc_filename = file_profile['enc_filename']

    results = []
    kw_len = len(keyword)
    url = website+"bin_init"
    payload = {"filename" : enc_filename, "kw_len":kw_len}
    r = s.post(url, data=payload)
    resp = json.loads(r.text)
    if resp is None:
        print "The file requested could not be found!"
        return

    found = 0

    if resp is not None:
        (cur_dat, c_idx, left_dat, l_idx, right_dat, r_idx) = resp
        last_iter = False
        decrypted_cur = decrypt_blocks(cur_dat, c_idx, iv, key)
        decrypted_left = decrypt_blocks(left_dat, l_idx, iv, key)
        decrypted_right = decrypt_blocks(right_dat, r_idx, iv, key)

        decrypted_cur = st.align_text(decrypted_cur, c_idx, kw_len)
        decrypted_left = st.align_text(decrypted_left, l_idx, kw_len)
        decrypted_right = st.align_text(decrypted_right, r_idx, kw_len)

        if decrypted_cur is None or \
            decrypted_left is None or \
            decrypted_right is None:
            last_iter = True

        if decrypted_cur == keyword or \
            decrypted_left == keyword or \
            decrypted_right == keyword:
            found = 1
        else:
            if decrypted_cur < keyword:
                if decrypted_left > decrypted_cur:
                    choice = st.LEFT
                    prev_block = decrypted_left
                else:
                    choice = st.RIGHT
                    prev_block = decrypted_right
            else: # decrypted_cur > keyword
                if decrypted_left < decrypted_cur:
                    choice = st.LEFT
                    prev_block = decrypted_left
                else:
                    choice = st.RIGHT
                    prev_block = decrypted_right
            url = website+"bin_search"
            payload = {"filename" : enc_filename, "kw_len":kw_len, "choice":str(choice)}
            r = s.post(url, data=payload)
            content = r.content.split("\n")
            resp = json.loads(content[-1])["result"]

            while resp is not None:
                (left_dat, l_idx, right_dat, r_idx) = resp

                last_iter = False
                decrypted_left = decrypt_blocks(left_dat, l_idx, iv, key)
                decrypted_right = decrypt_blocks(right_dat,r_idx,iv, key)

                decrypted_left = st.align_text(decrypted_left,l_idx,kw_len)
                decrypted_right=st.align_text(decrypted_right,r_idx,kw_len)

                if decrypted_left is None or decrypted_right is None:
                    last_iter = True

                if decrypted_left == keyword or \
                    decrypted_right == keyword:
                    found = 1
                    break
                elif last_iter:
                    break
                else:
                    if prev_block < keyword:
                        if decrypted_left > prev_block:
                            choice = st.LEFT
                            prev_block = decrypted_left
                        else:
                            choice = st.RIGHT
                            prev_block = decrypted_right
                    else: # prev_block > keyword
                        if decrypted_left < prev_block:
                            choice = st.LEFT
                            prev_block = decrypted_left
                        else:
                            choice = st.RIGHT
                            prev_block = decrypted_right
                url = website+"bin_search"
                payload = {"filename" : enc_filename, "kw_len":kw_len, 'choice':choice}
                r = s.post(url, data=payload)
                content = r.content.split("\n")
                resp = json.loads(content[-1])["result"]

    if(found == 1):
        print "Found"
    else:
        print "Not Found"


def search_in_file(path, keyword):
    global s, profile, ID

    linestring = open(path, 'r').read()
    linestring = linestring.replace('\n',' ')
    words = linestring.split(' ')
    if keyword in words:
        return True
    else:
        return False

def local_search( keyword, filename):
    global s, profile, ID

    if not os.path.exists('tmp'):
        os.mkdir('tmp',0777)
    if filename != "ALL":
        download(s, filename, 'tmp/'+filename )
        local_list = [filename]
    else:
        url = website+"getlist"
        r = s.get(url)
        file_list = json.loads(r.text)
        for f in file_list:
            download(s, f, 'tmp/'+f )
        local_list = os.listdir('tmp/')
 
    search_results = []
    for f in local_list:
        if search_in_file('tmp/'+f, keyword):
            search_results.append(f)
    print search_results

def get_file_list():
    global s, profile, ID
    print "enc:"
    for key in profile['enc'].keys():
        print "    " + key
    #print "bin:"
    #for key in profile['bin'].keys():
    #    print "    " + key

   
def enc_share(filename, user):
    global s, profile, ID
    if filename not in profile['enc'].keys():
        print "Cannot find file!"
        return

    file_profile = profile['enc'][filename]
    enc_filename = file_profile['enc_filename']

    url = website+"share"
    msg = json.dumps(file_profile)
    payload = {"user":user}
    r = s.get(website+"registerPkey", params=payload)
    if (r.text == "not found"):
        print "Cannot find this user:" , user
        return
    pkey = json.loads(r.text)
    n = pkey['n']
    e = pkey['e']
    Pkey = RSA.construct([long(n),long(e)])
    cipher = PKCS1_OAEP.new(Pkey)
    text1 = [ord(x) for x in cipher.encrypt(msg[:150])]
    text2 = [ord(x) for x in cipher.encrypt(msg[150:])]
    ciphertext1 = json.dumps(text1)
    ciphertext2 = json.dumps(text2)
    
    payload = {"filename" : enc_filename, "friend": user, "msg1":ciphertext1, "msg2":ciphertext2}
    r = s.post(url, data = payload)
    result = r.text
    print result
   


class cmdlineInterface(cmd.Cmd):
    prompt = 'cryptZoobar>> '

    def do_login(self, line):
        "login $username $password $Mkeypassword"
        "Log into Zoobar as $username"
        args = [a for a in line.split(' ') if len(a) > 0]
        if len(args) != 3:
            print "usage: login $username $password $Mkeypassword"
            return
        usrname = args[0]
        cmdlineInterface.prompt = urllib.quote(usrname) + '@cryptZoobar>>'

        login(usrname, args[1], args[2])

    def do_register(self, line):
        "register $username $password $Mkeypassword"
        "Register in Zoobar as $username"
        args = [a for a in line.split(' ') if len(a) > 0]
        if len(args) != 3:
            print "usage: register $username $password $Mkeypassword"
            return
        #print "args %s %s %s" % (args[0],args[1],args[2])
        usrname = args[0]
        if not register(args[0], args[1], args[2]):
            print "Shoot! Somebody already has your username."

    def do_shell(self, line):
        "Run a shell command"
        print "running shell command:", line
        output = os.popen(line).read()
        print output
        self.last_output = output

    def do_upload(self, line):
        "upload $new_name $path"
        "Upload $path as $new_name to Zoobar, need log in first"
        start = time.time()
        args = [a for a in line.split(' ') if len(a) > 0]
        if len(args) != 2:
            print "usage: upload $new_name $path"
            return
        upload(args[0], args[1])
        end = time.time()
        timespend = end - start
        print "spent:" + str(timespend)

    def do_enc_upload(self, line):
        "enc_upload $new_name $path"
        "Upload encrypted $path as $new_name to Zoobar, need log in first"
        start = time.time()
        args = [a for a in line.split(' ') if len(a) > 0]
        if len(args) != 2:
            print "usage: enc_upload $new_name $path"
            return

        enc_upload(args[0], args[1])
        end = time.time()
        timespend = end - start
        print "spent:" + str(timespend)

    def do_bin_upload(self, line):
        "bin_upload $new_name $path"
        "Upload encrypted $path as $new_name to Zoobar for scheme2, need log in first"
        start = time.time()
        args = [a for a in line.split(' ') if len(a) > 0]
        if len(args) != 2:
            print "usage: enc_upload $new_name $path"
            return

        bin_upload(args[0], args[1])
        end = time.time()
        timespend = end - start
        print "spent:" + str(timespend)

    def do_download(self, line):
        "download $remote_name $local_path"
        "Download $remote_name in server and save as $local_path, need log in first"
        start = time.time()
        args = [a for a in line.split(' ') if len(a) > 0]
        if len(args) != 2:
            print "usage: download $remote_name $local_path"
            return

        download(args[0], args[1])
        end = time.time()
        timespend = end - start
        print "spent:" + str(timespend)

    def do_enc_download(self, line):
        "enc_download $remote_name $local_path"
        "Download encrypted $remote_name in server and save as $local_path, need log in first"
        start = time.time()
        args = [a for a in line.split(' ') if len(a) > 0]
        if len(args) != 2:
            print "usage: enc_download $remote_name $local_path"
            return

        enc_download(args[0], args[1])
        end = time.time()
        timespend = end - start
        print "spent:" + str(timespend)

    def do_search(self, line):
        "search \"keyword\" (file)"
        "Get files that contain keyword (linear plaintext search)"
         ### CHECK ARGS ####
        if " " not in line:
            print "usage: search \"keyword\" (file)"
            return
        line = line.strip()
        if line[0] != "\"":
            print "usage: search \"keyword\" (file)"
            return
        line = line[1:]
        if "\"" not in line:
            print "usage: search \"keyword\" (file)"
            return
        args = line.split('\"')
        if len(args) > 2:
            print "usage: search \"keyword\" (file)"
            return

        filename = args[1].strip() 
        start = time.time()

        if len(args) > 1:
            search(args[0], args[1].strip())
        else:
            search(args[0], 'ALL')

        end = time.time()
        timespend = end - start
        print "spent:" + str(timespend)

    def do_enc_search(self, line):
        "enc_search \"keyword\" (file)"
        "Get files that contain $keyword"
          ### CHECK ARGS ####
        if " " not in line:
            print "usage: enc_search \"keyword\" (file)"
            return
        line = line.strip()
        if line[0] != "\"":
            print "usage: enc_search \"keyword\" (file)"
            return
        line = line[1:]
        if "\"" not in line:
            print "usage: enc_search \"keyword\" (file)"
            return
        args = line.split('\"')
        if len(args) > 2:
            print "usage: enc_search \"keyword\" (file)"
            return

        start = time.time()

        if len(args) > 1:
            enc_search(args[0], args[1].strip())
        else:
            enc_search(args[0], 'ALL')

        end = time.time()
        timespend = end - start
        print "spent:" + str(timespend)

    def do_bin_search(self, line):
        "bin_search \"keyword\" (file)"
        "Get files that contain keyword"

        ### CHECK ARGS ####
        if " " not in line:
            print "syntax: \"keyword\" (file)"
            return
        line = line.strip()
        if line[0] != "\"":
            print "syntax: \"keyword\" (file)"
            return
        line = line[1:]
        if "\"" not in line:
            print "syntax: \"keyword\" (file)"
            return
        args = line.split('\"')
        if len(args) > 2:
            print "syntax: \"keyword\" (file)"
            return

        keyword = args[0]

        start = time.time()
        if len(args) > 1:
            bin_search(keyword, args[1].strip())
        else:
            bin_search(keyword, 'ALL')

        end = time.time()
        timespend = end - start
        print "spent:" + str(timespend)

    def do_local_search(self, line):
        "local_search \"keyword\" (file)"
        "Get files that contain keyword"
         ### CHECK ARGS ####
        if " " not in line:
            print "syntax: \"keyword\" (file)"
            return
        line = line.strip()
        if line[0] != "\"":
            print "syntax: \"keyword\" (file)"
            return
        line = line[1:]
        if "\"" not in line:
            print "syntax: \"keyword\" (file)"
            return
        args = line.split('\"')
        if len(args) > 2:
            print "syntax: \"keyword\" (file)"
            return

        keyword = args[0]

        start = time.time()
        if len(args) > 1:
            local_search(keyword, args[1].strip())
        else:
            local_search(keyword, 'ALL')

        end = time.time()
        timespend = end - start
        print "spent:" + str(timespend)

    def do_enc_share(self, line):
        "enc_share $file $user"
        "Share $file with $user"

        args = [a for a in line.split(' ') if len(a) > 0]
        if len(args) != 2:
            print "usage: enc_share $file $user"
            return

        enc_share(args[0], args[1])

    def do_logout(self, line):
        self.s = requests.session()
        Mkey = MD5.new()
        self.profile = {}
        cmdlineInterface.prompt = 'cryptZoobar>>'
        

    def do_ls(self, line):
        get_file_list()

    def do_EOF(self, line):
        print ""
        return True


if __name__ == '__main__':
    Mkey = MD5.new()
    loggedIn = False
    c = cmdlineInterface()
#    salt=random_str(10)
    #print salt
    c.cmdloop()
