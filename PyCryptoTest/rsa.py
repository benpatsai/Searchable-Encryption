#!/usr/bin/python

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import MD5
from Crypto.Cipher import AES
from Crypto import Random

def key_gen():
    key = RSA.generate(2048)
    f = open('Pkey','w')
    f.write(str(key.n)+' '+str(key.e))
    f.close()
    f = open('Skey.pem','w')
    f.write(key.exportKey('PEM'))
    f.close()


message = 'Message'
f = open('Pkey','r').read()
[n, e] = f.split(' ')
Pkey = RSA.construct([long(n),long(e)])
cipher = PKCS1_OAEP.new(Pkey)
ciphertext = cipher.encrypt(message)

f = open('Skey.pem','r')
Skey = RSA.importKey(f.read())
cipher = PKCS1_OAEP.new(Skey) 
print ciphertext
print cipher.decrypt(ciphertext)

h = MD5.new()
h.update(b'masterKPW')
print h.hexdigest()

key = h.hexdigest()
iv = Random.new().read(AES.block_size)
cipher = AES.new(key, AES.MODE_CFB, iv)
ctxt = iv + cipher.encrypt(b'Attack at dawn')

ptxt = cipher.decrypt(ctxt)
iv_size = AES.block_size
print ptxt[iv_size:]
