#!/usr/bin/ python
import tools_karkkainen_sanders as tks

#x is a string which is converted into suffix array
def construct_suffix_array(x):
    x = unicode(x,'utf-8','replace')
    n = len(x)
    return tks.simple_kark_sort(x)[0:n]

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
    
    return root;


class BST_Node:
    def __init__(self, index):
        self.index = index;
