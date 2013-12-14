#!python
# This profile will work like a facebook wall.

# If anyone posted a message on your wall with the text area on user.html,
# this profile can retrive them as a facebook wall

# The 'get_my_message' api will use the message RPC server, which has 
# ability to acceess the message data base, for getting messages.

# Also, for readabiliy of the web page, 
# this profile will be shown on the bottom of that page

import time, errno

global api
selfuser = api.call('get_self')
visitor = api.call('get_visitor')
messages = api.call('get_my_message')

print '<center>'
for msg in messages:
  print '<li>'+ msg[0] + " said:" + '</li>'
  print msg[1] + '<br>'
  print "@ " + msg[2] + '<br>'
  print '<br>'

print '</center>'
