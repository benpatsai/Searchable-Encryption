#!/usr/bin/python

import client 

user = 'user1'
f = open('12345', 'w')
f.write('1 2 3 4 5 \n')
f = open('2468', 'w')
f.write('2 4 6 8 \n')
f = open('13579', 'w')
f.write('1 3 5 7 9\n')
f.close()

#client.upload(user, path, filename)
client.upload(user, '12345', 'test_12345')
client.upload(user, '2468', 'test_2468')
client.upload(user, '13579', 'test_13579')

# client.search(user, keyword)
print client.search(user, '5')

