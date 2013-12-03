#!/usr/bin/python

import client 

user = 'user1'
# client.upload(user, path, filename)
client.upload(user, '12345', 'test_12345')
client.upload(user, '2468', 'test_2468')
client.upload(user, '13579', 'test_13579')

# client.search(user, keyword)
print client.search(user, '5')

