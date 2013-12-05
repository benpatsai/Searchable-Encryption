#!/usr/bin/python
import requests
import cmd, os, shutil
import time
import json

def login(s, username, password):

    payload = { "submit_login" : "1" ,
            "login_username": username ,
            "login_password": password }

    r = s.post("http://128.30.93.9:8080/zoobar/index.cgi/login", data=payload)
    if (username in r.text):
        return True
    else:
        return False

def register(s, username, password):

    payload = { "submit_registration" : "1" ,
            "login_username": username ,
            "login_password": password }

    r = s.post("http://128.30.93.9:8080/zoobar/index.cgi/login", data=payload)
    if (username in r.text):
        return True
    else:
        return False

def upload(s, filename, path):
    url = "http://128.30.93.9:8080/zoobar/index.cgi/upload"
    files = {'file': (filename, open(path,'rb'))}
    s.post(url, files=files)

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
        "login $username $password"
        "Log into Zoobar as $username"
        args = line.split(' ')
        login(s, args[0], args[1])

    def do_register(self, line):
        "register $username $password"
        "Register in Zoobar as $username"
        args = line.split(' ')
        register(s, args[0], args[1])

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


    def do_EOF(self, line):
        print ""
        return True 

if __name__ == '__main__':
    s = requests.session()
    loggedIn = False
    cmdlineInterface().cmdloop()
