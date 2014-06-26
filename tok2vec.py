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

def word_feats(words):
    return dict([(word, True) for word in words])

def getWords(File):    # vec : []
    f = open(File,'r')
    words = []
    for line in f:
            if '(' not in line:	     # Empty line
                    continue
            line = line.replace('¡@','\t').strip().split('\t')
            for e in line:
                    r = re.split('(\(\w+\))', e)
                    try:
                        if checkstop(r[0]) == False:
                                words.append(r[0])
                    except:
                        pass
    return words
 
stop = []
pos = []
neg = []
read_list('stopword.list',stop)
read_list('ntusd-positive.txt',pos)

pos_dir = sys.argv[1]
neg_dir = sys.argv[2]

pos_files = os.listdir(pos_dir)
neg_files = os.listdir(neg_dir)
pos_vec = []
neg_vec = []

print os.path.join(pos_dir,pos_files[0])
w = getWords(os.path.join(pos_dir,pos_files[0]))
   


#sr = sorted(vec.items(), key=lambda x:x[1],reverse=True)

