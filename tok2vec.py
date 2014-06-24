# -*- coding: utf-8 -*-
# Name: tok2vec.py
# Description: transform the results in tokenized/[happy] to VSM, for SVM
# Author: Leo Wu
# Date: 2014.06.23

import re
import os
import sys

def checkstop(word):
    if word in stop:
        return True
    else:
        return False

def read_list(path,List):
    with open(path,'r') as f:
        for e in f:
            List.append(e.strip())




stop = []
pos = []
neg = []
read_list('stopword.list',stop)
read_list('ntusd-positive.txt',pos)

dir = sys.argv[1]
files = os.listdir(dir)
vec = {}

for file in files:
	file = os.path.join(dir,file)
	f = open(file,'r')
	for line in f:
		if '(' not in line:	     # Empty line
			continue
		line = line.replace('¡@','\t').strip().split('\t')
		for e in line:
			r = re.split('(\(\w+\))', e)
                        try:
			    if checkstop(r[0]) == False:
                                if r[0] not in vec:
                                    vec[r[0]] = 1
                                else:
                                    vec[r[0]] +=1
                        except:
                            pass

sr = sorted(vec.items(), key=lambda x:x[1],reverse=True)
c = 0
for e in vec:
    if e


print len(vec)

