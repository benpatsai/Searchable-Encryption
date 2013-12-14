#!/usr/bin/python
#usage: ./test_num_hashes.py file.txt

import sys
import sa
import search_tools

def count_substrings(path):
    (sufar,lcp) = search_tools.construct_suf_lcp(path)
    n = len(sufar) - 1 #Subtract one due to weird suffix array implementation
    k = 100
    ha0repcount=0
    ha1uniqcount=0
    for i in range(1,n):
        if lcp[i] > lcp[i-1]:
            for j in range(lcp[i-1]+1,lcp[i]+1):
                if j < k:
                    ha0repcount += 1
        if i < n-1 and  sufar[i] + lcp[i] + 1 <= n and sufar[i]+lcp[i+1]+1 <= n:
            if max(lcp[i],lcp[i+1])+1 < k:
                    ha1uniqcount += 1
    if sufar[0]+lcp[1] + 1 <= n:
        if lcp[1] + 1 < k:
            ha1uniqcount += 1
    if sufar[n-1]+lcp[n-1]+1<=n:
        if lcp[n-1]+1 < k:
            ha1uniqcount += 1

    print "using cap of %d"%k
    print "%d nonunique strings, %d unique ones hashed, %d total hashes" % (ha0repcount,ha1uniqcount,ha0repcount+ha1uniqcount)
    filelength = len(open(sys.argv[1],'r').read())
    print "File size %d. Ratio %.4f"%(filelength, (ha0repcount+ha1uniqcount)/(1.0*filelength))
    print "& %.1f MB & %d & %d & %.3f\\\\" % ((1.0*filelength)/1048576, filelength, ha0repcount+ha1uniqcount, (ha0repcount+ha1uniqcount)/(1.0*filelength))
    print "& %d kB & %d & %d & %.3f\\\\" % ((1.0*filelength)/1024, filelength, ha0repcount+ha1uniqcount, (ha0repcount+ha1uniqcount)/(1.0*filelength))

    return

count_substrings(sys.argv[1])

