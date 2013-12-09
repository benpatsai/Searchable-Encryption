#!/usr/bin/env python
import random, string
import os
import hashlib
import pickle
import copy
import search_tools
import json
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import MD5
from Crypto.Cipher import AES
from Crypto import Random



#server
'''
block_length=3

hashes_server=[]

def send_hashes(hashes):
    global hashes_server
    hashes_server=hashes
    return 
'''
'''
def search_hash(hashed_query):
    for (hashed_substr,enc_index) in hashes_server:
        if (hashed_query==hashed_substr):
            return enc_index
    return -1
'''
#server_encrypted_blocks=[]
'''
def send_encrypted_blocks(encrypted_blocks):
    global server_encrypted_blocks
    server_encrypted_blocks=encrypted_blocks
    return
'''
'''
def get_encrypted_blocks(start_block_index,end_block_index):
    return server_encrypted_blocks[start_block_index:end_block_index+1]
'''
##################################Client

#block_length=3

def random_str(length):
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    id = ''
    for i in range(0,length):
        id += random.choice(alpha)
    return id

#salt=random_str(5)

#text='It will be seen that this mere painstaking burrower and grub-worm of a poor devil of a Sub-Sub appea'
#text='banana'
#text='01234567890'

#key_index='????'

def next_greater_power_of_2(x):  
    return 2**(x).bit_length()

def encrypt_integer(integer,block_index_iv,key_index):
    s=str(integer)
    enc_integer=encrypt_block(s,0,block_index_iv,key_index)
    return enc_integer

def decrypt_integer(enc_integer,block_index_iv,key_index):
    s=decrypt_block(enc_integer,0,block_index_iv,key_index)
    integer=int(s)
    return integer

def list_to_str(l):
    return ''.join(str(e) for e in l)

def hash_with_salt(string,salt):
    #return hashlib.md5(salt+str)
    #return string
    #print str(salt)
    ssalt=list_to_str(salt)
    #print ssalt
    hash_object=hashlib.sha1(ssalt+string)
    s=hash_object.hexdigest()
    return s[:5]
    #return string

def hash_substrings_o2(text,salt,block_index_iv,key_index):
    sufar = search_tools.construct_suffix_array(text)
    n = len(sufar)
    hashes=[]
    shared=[0]*n
    for i in range(1,n):
        #Determine the number of characters shared between text[i:n] and text[i-1:n]
        shared[i] = 0
        while sufar[i] + shared[i] < n and sufar[i-1] + shared[i] < n and text[sufar[i]+shared[i]]==text[sufar[i-1]+shared[i]]:
            shared[i]+=1
    #print sufar
    #print shared
    for i in range(1,n):
        if shared[i] > shared[i-1]:
            for j in range(shared[i-1]+1,shared[i]+1):
                substr = text[sufar[i]:sufar[i]+j]
                #print "type 1 substr %s"%substr
                hashes.append((hash_with_salt(substr,salt),encrypt_integer(sufar[i-1],block_index_iv,key_index)))
        if i < n-1 and  sufar[i] + shared[i] + 1 <= n and sufar[i]+shared[i+1]+1 <= n:
            substr = text[sufar[i]:sufar[i]+max(shared[i],shared[i+1])+1]
            #print "type 2 substr %s"%substr
            hashes.append((hash_with_salt(substr,salt),encrypt_integer(sufar[i],block_index_iv,key_index)))

    #Don't forget to include the shortest unique substring starting at text[suff_arr[0]]
    #and also starting at text[sufar[n-1]
    if sufar[0]+shared[1] + 1 <= n:
        hashes.append((hash_with_salt(text[sufar[0]:sufar[0]+shared[1]+1],salt),encrypt_integer(sufar[0],block_index_iv,key_index)))
    if sufar[n-1]+shared[n-1]+1<=n:
        hashes.append((hash_with_salt(text[sufar[n-1]:sufar[n-1]+shared[n-1]+1],salt),encrypt_integer(sufar[n-1],block_index_iv,key_index)))

    hashes.append((hash_with_salt("",salt),encrypt_integer(0,block_index_iv,key_index)))
    #Also sort the array to avoid leaking information about the order
    hashes.sort()
    
    return hashes

#x = hash_substrings_o2( "The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.",0,0)
#print x
#print len(x)


def hash_substrings_optimized(text,salt,key_index):
    textLength=len(text)
    hashed_prefixes={}

    prime=271
    modulo=100000000000

    prime_pow={}
    prime_pow[0]=1
    for index in range(1,textLength):
        prime_pow[index]=(prime_pow[index-1]*prime)%modulo

    for index in range(0,textLength):
        hashed_prefixes[index]=(ord(text[index])+1)*prime_pow[index]
        if (index>0):
            hashed_prefixes[index]+=hashed_prefixes[index-1]
        hashed_prefixes[index]%=modulo
    #print hashed_prefixes

def hash_substrings(text,salt,block_index_iv,key_index):
    return hash_substrings_o2(text,salt,block_index_iv,key_index)
    '''all_substr=[]
    textLength=len(text)
    for i in range(0,textLength+1):
        for j in range(i,textLength+1):
            all_substr.append(text[i:j])
    #print all_hashes

    hashes=[]
    for i in range(0,textLength+1):
        for j in range(i+1,textLength+1):
            substr=text[i:j]
            count1=0
            substr_shorter=text[i:j-1]
            count2=0
            for string in all_substr:
                if (string==substr):
                    count1+=1
                if (string==substr_shorter):
                    count2+=1
            #print hashed_substr, count1, hashed_substr_shorter, count2
            if count1>1 or (count1==1 and count2>1):
                hashes.append((hash_with_salt(substr,salt),encrypt_integer(i,key_index)))
    hashes.append((hash_with_salt('',salt),encrypt_integer(0,key_index)))
    return hashes
'''

#hashes_client=hash_substrings(text,salt,key_index)

#send_hashes(hashes_client)

#key_blocks='????'

def splitString(string, block_length):
    blocks=[]
    while len(string)!=0:
        blocks.append(string[:block_length])
        string=string[block_length:]
    return blocks

def encrypt_block(block,block_id,block_index_iv,key_blocks):
    Mkey=MD5.new()
    Mkey.update(block_index_iv+str(block_id))
    iv = Mkey.hexdigest()[:AES.block_size]
    Mkey=MD5.new()
    Mkey.update(list_to_str(key_blocks))
    cipher = AES.new(Mkey.hexdigest(), AES.MODE_CFB, iv)
    #print profile
    encrypted_block = cipher.encrypt(block)
    encrypted_block_ints=[ord(x) for x in encrypted_block]
    #print 'encrypt: ',block,'->',encrypted_block_ints
    #iv_size = AES.block_size
    #dec_profile = cipher.decrypt(enc_profile)[iv_size:]
    #print dec_profile

    #encrypted_block=block
    #return encrypted_block_ints
    return encrypted_block_ints

def decrypt_block(encrypted_block,block_id,block_index_iv,key_blocks):
    encrypted_block_str=''.join([chr(x) for x in encrypted_block])
    Mkey=MD5.new()
    Mkey.update(block_index_iv+str(block_id))
    iv = Mkey.hexdigest()[:AES.block_size]
    Mkey=MD5.new()
    Mkey.update(list_to_str(key_blocks))
    #print profile
    #encrypted_block = iv + cipher.encrypt(block)
    #print block,'->',encrypted_block
    #iv_size = AES.block_size
    cipher = AES.new(Mkey.hexdigest(), AES.MODE_CFB, iv)
    block = cipher.decrypt(encrypted_block_str)
    #print 'decrypt: ',encrypted_block,'->',block
    #print dec_profile
    #block=encrypted_block
    return block

def encrypt_blocks(text,key_blocks,block_index_iv,block_length):
    blocks=splitString(text,block_length)
    encrypted_blocks=[]
    for (block_id,block) in enumerate(blocks):
        encrypted_blocks.append(encrypt_block(block,block_id,block_index_iv,key_blocks))
    #encrypt_block('asdlfkjsadsdfksdfjsdfsdflkj',0,'asdf',[12,2,3])
    return encrypted_blocks

#encrypted_blocks=encrypt_blocks(text,key_blocks,block_length)

#send_encrypted_blocks(encrypted_blocks)
'''
def search_substring(query,salt,key_index,block_length):

    enc_index=search_hash(hash_with_salt(query,salt))

    if enc_index!=-1:
        return decrypt_integer(enc_index,key_index)

    prefix_len=len(query)
    delta=next_greater_power_of_2(prefix_len)/2

    enc_shorter_index=search_hash(hash_with_salt(query[0:prefix_len-1],salt))

    while not((enc_index==-1) and (enc_shorter_index!=-1)):
        if enc_shorter_index == -1:
            prefix_len-=delta
        if enc_index > -1:
            prefix_len+=delta
        #print prefix_len
        delta=delta/2
        enc_index=search_hash(hash_with_salt(query[0:(0 if prefix_len<0 else prefix_len)],salt))
        enc_shorter_index=search_hash(hash_with_salt(query[0:(0 if (prefix_len-1<0) else (prefix_len-1))]
,salt))
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

#query='4567'
query='890'

print 'text : ',text
print 'query : ',query

print search_substring(query,salt,key_index,block_length)
#print hashes_client
#print hashes_server
#print splitString('aabbccdde',2)
'''
