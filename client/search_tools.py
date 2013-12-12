#!/usr/bin/ python
#import tools_karkkainen_sanders as tks
from subprocess import call
from random import randint
from ctypes import *

LEFT = -1
RIGHT = 1
PREFIX = "/home/poantsai/6.858/projects/client/"
BLOCK_SIZE = 4

def construct_suf_lcp(path):
    suflib = CDLL(PREFIX + 'lcp_sais/lcp_for_py.so')
    n = len(path);
    filen = (c_char * (n+1))()
    for i in range(0,n):
        filen[i] = path[i]
    filen[n] = '\0'
    n = suflib.getSuffixLength(filen)
    suf = (c_int * (n+1))() #extra bit is inherent to algorithm
    lcp = (c_int * n)()
    suflib.getSuffixLCPArray(filen, suf, lcp, c_int(n))
    return (suf, lcp)

def debug_construct_suffix_array(x):
    n = len(x)
    return [i for i in range(0,n)]
        
#x is a string which is converted into suffix array
def construct_suffix_array(path):
    suflib = CDLL(PREFIX + 'sais/suffix_for_py.so')
    n = len(path);
    filen = (c_char * (n+1))()
    for i in range(0,n):
        filen[i] = path[i]
    filen[n] = '\0'
    n = suflib.getSuffixLength(filen)
    sufarr = (c_int * n)()
    suflib.getSuffixArray(filen, sufarr, n)
    #call(["sais/suftest", path])
    #with open("output.txt", 'r') as f:
    #    sufarr = (f.read()).split()
    return sufarr

def construct_suffix_tree(x):
    x = construct_suffix_array(x)
    return suffix_tree_helper(x, 0, len(x)-1)

def suffix_tree_helper(x, start, end):
    if (start > end):
        return None
    mid = start + (end - start)/2
    root = BST_Node(x[mid])
    root.left = suffix_tree_helper(x, start, mid - 1)
    root.right= suffix_tree_helper(x, mid+1, end)
    
    #scramble tree in helper for efficiency
    if randint(0,1):
        temp = root.left
        root.left = root.right
        root.right = temp
    return root;

def scramble_tree(root):
    if root is None:
        return
    if randint(0,1):
        temp = root.left
        root.left = root.right
        root.right = temp

    scramble_tree(root.left)
    scramble_tree(root.right)

def encrypt(payload, key, arg):
    return payload

def align_text(text, offset, kw_len):
    if text is None or offset is None:
        return None
    return text[offset:offset + kw_len]

def kw_eq(text, keyword, offset, kw_len):
#    print kw_len
#    print offset
#    print text
#    print "------"
    if text is None or offset is None or kw_len > (offset + len(text) - 1):
        return False
    for i in range(0, kw_len):
        if text[+ i] != keyword[i]:
            return False
    return True

def decrypt(payload, key, arg):
    return payload

def decrypt_blocks(payload, key, arg):
    if payload is None:
        return None
    pt = ''
    for i in range(0, len(payload)/BLOCK_SIZE):
        pt += decrypt(payload[i*BLOCK_SIZE:(i+1)*BLOCK_SIZE], key, 1)
    return pt

def tree_to_array(root):
    if root is None:
        return []
    ticker = 0
    i = 0
    a = [root]
    b = []
    
    while i < len(a):
        if a[i] is not None:
            if ticker > 0:
                for _ in range(0, ticker):
                    b.append(None)
                ticker = 0
            b.append(a[i].index)
            a.append(a[i].left)
            a.append(a[i].right)
        else:
            ticker += 1
        i += 1
    return b

class BST_Node:
    def __init__(self, index):
        self.index = index;







 
