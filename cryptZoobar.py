#!/usr/bin/python
import requests
import cmd, os

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

def search(s, keyword):
    url = "http://128.30.93.9:8080/zoobar/index.cgi/search"
    payload = {"keyword" : keyword}
    r = s.post(url, data = payload)
    html = r.text
    result = html[html.rfind("<table")+35:]
    result = result.replace("<tr>",'')
    result = result.replace("</tr>\n",'\n')
    result = result.replace("<th>",'')
    result = result.replace("</th>\n",'')
    result = result.replace("</th>",'')
    result = result.replace('<td align="center">','')
    result = result.replace("</td>\n",'')
    result = result.replace("</td>",'')
    result = result.replace("<b>",'')
    result = result.replace("</b>",'')
    result = result.replace("</table>",'')
    result = result.replace("</center>",'')
    result = result.replace("</body>",'')
    result = result.replace("</html>",'')
    result = result[:len(result)-15]

    print result
   


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
        args = line.split(' ')
        upload(s, args[0], args[1])

    def do_search(self, line):
        "search $keyword"
        "Get files that contain $keyword"
        args = line.split(' ')
        search(s, args[0])

    def do_EOF(self, line):
        print ""
        return True 

if __name__ == '__main__':
    s = requests.session()
    loggedIn = False
    cmdlineInterface().cmdloop()
