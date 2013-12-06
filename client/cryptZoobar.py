#!/usr/bin/python
import requests
import cmd, os, shutil
import time
import json
from s import*
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import MD5
from Crypto.Cipher import AES
from Crypto import Random

block_length = 3

def search_hash(s, hashed_query, filename):
    url = "http://128.30.93.9:8080/zoobar/index.cgi/enc_search"
    payload = {"keyword" : hashed_query, "filename": filename}
    r = s.post(url, data = payload)
    print r.text
    result = json.loads(r.text)
    return result['idx']


def search_substring(s, query,salt,key_index,block_length, filename):
    
    enc_index=search_hash(s, hash_with_salt(query,salt), filename)

    if enc_index!=-1:
        return decrypt_integer(enc_index,key_index)

    prefix_len=len(query)
    delta=next_greater_power_of_2(prefix_len)/2

    enc_shorter_index=search_hash(s,hash_with_salt(query[0:prefix_len-1],salt),filename)

    while not((enc_index==-1) and (enc_shorter_index!=-1)):
        if enc_shorter_index == -1:
            prefix_len-=delta
        if enc_index > -1:
            prefix_len+=delta
        #print prefix_len
        delta=delta/2
        enc_index=search_hash(s,hash_with_salt(query[0:(0 if prefix_len<0 else prefix_len)],salt), filename)
        enc_shorter_index=search_hash(s,hash_with_salt(query[0:(0 if (prefix_len-1<0) else (prefix_len-1))],salt), filename)
        #print enc_index, enc_shorter_index
        #print prefix_len-1
        #print query[0:(0 if prefix_len<0 else prefix_len)],'!',query[0:(0 if (prefix_len-1<0) else (prefix_len-1))]
        #input("!")
    #print enc_shorter_index

    index=decrypt_integer(enc_shorter_index,key_index)
    #print index
    start_index=index
    end_index=start_index+len(query)
    #print end_index
    start_block_index=start_index/block_length
    end_block_index=(end_index-1)/block_length
    #print start_block_index,end_block_index

    encrypted_blocks=get_encrypted_blocks(start_block_index,end_block_index)
    decrypted_string=''
    for encrypted_block in encrypted_blocks:
        decrypted_string+=decrypt_block(encrypted_block,key_blocks)
    #print decrypted_string
    check_start_index=start_index-start_block_index*block_length
    check_end_index=check_start_index+len(query)
    to_compare=decrypted_string[check_start_index:check_end_index]
    if (to_compare==query):
        return index
    else:
        return -1


def RSA_key_gen():
    key = RSA.generate(2048)
    return [key.n,key.e,key.d,key.p,key.q,key.u]

def upload_profile(username, profile):
    iv = profile['iv']
    cipher = AES.new(Mkey.hexdigest(), AES.MODE_CFB, iv)
    enc_profile = iv + cipher.encrypt(json.dumps(unicode(profile)))

    f = open(username+'profile','w')
    f.write(enc_profile)
    f.close()
    url = "http://128.30.93.9:8080/zoobar/index.cgi/upload"
    files = {'file': (username+'profile', open(username+'profile','rb'))}
    s.post(url, files=files)

def download_profile(username, profile):
    iv = profile['iv']
    cipher = AES.new(Mkey.hexdigest(), AES.MODE_CFB, iv)
    url = "http://128.30.93.9:8080/zoobar/index.cgi/download"
    payload = {"filename" : username+'profile'}
    r = s.get(url, params=payload)
    f = open(username+'profile', 'wb')
    for chunk in r.iter_content(chunk_size=512 * 1024): 
        if chunk: # filter out keep-alive new chunks
            f.write(chunk)
    f.close()

    f = open(username+'profile','r').read()
    iv_size = AES.block_size
    profile = json.loads(cipher.decrypt(f)[iv_size:])


def login(s, profile, username, password, MkeyPW):

    payload = { "submit_login" : "1" ,
            "login_username": username ,
            "login_password": password }

    r = s.post("http://128.30.93.9:8080/zoobar/index.cgi/login", data=payload)

    if (username in r.text):
        ID = username

        Mkey.update(MkeyPW+'iv')
        iv = Mkey.hexdigest()[:AES.block_size]
        Mkey.update(MkeyPW)
        profile['iv'] = iv
        download_profile(username, profile)
        return True
    else:
        return False

def register(s, profile, username, password, MkeyPW):
    [n, e, d, p, q, u] = RSA_key_gen()
    payload = { "submit_registration" : "1" ,
            "login_username": username ,
            "login_password": password }

    r = s.post("http://128.30.93.9:8080/zoobar/index.cgi/login", data=payload)

    if (username in r.text):
        ID = username

        pkey = {"n": n, "e": e}
        profile = {"d": d, "p": p, "q": q, "u":u}
        Mkey.update(MkeyPW+'iv')
        iv = Mkey.hexdigest()[:AES.block_size]
        profile['iv'] = iv
        Mkey.update(MkeyPW)
        upload_profile(username, profile)

        s.get("http://128.30.93.9:8080/zoobar/index.cgi/registerPkey", params=pkey)
        return True
    else:
        return False

def upload(s, filename, path):
    url = "http://128.30.93.9:8080/zoobar/index.cgi/upload"
    files = {'file': (filename, open(path,'rb'))}
    s.post(url, files=files)

def enc_upload(s, profile, filename, path):
    f = open(path,'r').read()
    salt = Random.new().read(AES.block_size) 
    key_index = Random.new().read(AES.block_size) 
    key_blocks = Random.new().read(AES.block_size) 

    profile[filename] = {'salt':salt, 'key_index':key_index, 'key_blocks':key_blocks} 
    hashed = hash_substrings(f, salt, key_index)
    h = open(filename+'hash', 'w')
    h.write(json.dumps(hashed))
    h.close()
    url = "http://128.30.93.9:8080/zoobar/index.cgi/enc_upload"
    files = {'file': (filename+'hash', open(filename+'hash','rb'))}
    s.post(url, files=files)

    encrypted_blocks = encrypt_blocks(f,key_blocks,block_length)
    url = "http://128.30.93.9:8080/zoobar/index.cgi/enc_upload"
    files = {'file': (filename, open(filename,'rb'))}
    s.post(url, files=files)

    print profile
    upload_profile(ID, profile)


def download(s, filename, local_path):
    url = "http://128.30.93.9:8080/zoobar/index.cgi/download"
    payload = {"filename" : filename}
    r = s.get(url, params=payload)
    f = open(local_path, 'wb')
    for chunk in r.iter_content(chunk_size=512 * 1024): 
        if chunk: # filter out keep-alive new chunks
            f.write(chunk)
    f.close()

def search(s, keyword, filename):
    url = "http://128.30.93.9:8080/zoobar/index.cgi/search"
    payload = {"keyword" : keyword, "filename": filename}
    r = s.post(url, data = payload)
    result = json.loads(r.text)
    print result

def enc_search(s,profile, keyword, filename):
    salt = profile[filename]['salt']
    key_index = profile[filename]['key_index']
    print search_substring(s, keyword, salt, key_index, block_length, filename)


def search_in_file(path, keyword):
    linestring = open(path, 'r').read()
    linestring = linestring.replace('\n',' ')
    words = linestring.split(' ')
    if keyword in words:
        return True
    else: 
        return False

def local_search(s, keyword, filename):
    if not os.path.exists('tmp'):
        os.mkdir('tmp',0777)
    if filename != "ALL":
        download(s, filename, 'tmp/'+filename )
        local_list = [filename]
    else:
        url = "http://128.30.93.9:8080/zoobar/index.cgi/getlist"
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
    

class cmdlineInterface(cmd.Cmd):
    prompt = 'cryptZooBar>> '

    def do_login(self, line):
        "login $username $password $Mkeypassword"
        "Log into Zoobar as $username"
        args = line.split(' ')
        login(s, profile, args[0], args[1], args[2])

    def do_register(self, line):
        "register $username $password $Mkeypassword"
        "Register in Zoobar as $username"
        args = line.split(' ')
        register(s, profile, args[0], args[1], args[2])

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
        args = line.split(' ')
        upload(s, args[0], args[1])
        end = time.time()
        timespend = end - start
        print "spent:" + str(timespend)

    def do_enc_upload(self, line):
        "enc_upload $new_name $path"
        "Upload encrypted $path as $new_name to Zoobar, need log in first"
        start = time.time()
        args = line.split(' ')
        enc_upload(s, profile, args[0], args[1])
        end = time.time()
        timespend = end - start
        print "spent:" + str(timespend)

    def do_download(self, line):
        "download $remote_name $local_path"
        "Download $remote_name in server and save as $local_path, need log in first"
        start = time.time()
        args = line.split(' ')
        download(s, args[0], args[1])
        end = time.time()
        timespend = end - start
        print "spent:" + str(timespend)

    def do_search(self, line):
        "search $keyword"
        "Get files that contain $keyword"
        start = time.time()
        args = line.split(' ')
        if len(args) > 1:
            search(s, args[0], args[1])
        else:
            search(s, args[0], 'ALL')

        end = time.time()
        timespend = end - start
        print "spent:" + str(timespend)

    def do_enc_search(self, line):
        "search $keyword ($file)"
        "Get files that contain $keyword"
        start = time.time()
        args = line.split(' ')
        if len(args) > 1:
            enc_search(s, profile, args[0], args[1])
        else:
            enc_search(s, profile, args[0], 'ALL')

        end = time.time()
        timespend = end - start
        print "spent:" + str(timespend)


    def do_local_search(self, line):
        "search $keyword"
        "Get files that contain $keyword"
        start = time.time()
        args = line.split(' ')
        if len(args) > 1:
            local_search(s, args[0], args[1])
        else:
            local_search(s, args[0], 'ALL')
        end = time.time()
        timespend = end - start
        print "spent:" + str(timespend)

    def do_logout(self, line):
        s = requests.session()
        Mkey = MD5.new()
        profile = {}

    def do_EOF(self, line):
        print ""
        return True 

if __name__ == '__main__':
    s = requests.session()
    ID = ''
    Mkey = MD5.new()
    profile = {}
    loggedIn = False
    cmdlineInterface().cmdloop()
