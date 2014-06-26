# -*- coding: utf-8 -*-
# Name: tok2vec.py
# Description: transform the results in tokenized/[happy] to VSM, for SVM
# Author: Leo Wu
# Date: 2014.06.23

import re
import os
import sys
import numpy
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier


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
            if '(' not in line or "¡¯" in line or "ª©³W" in line or "---" in line or "§R°£" in line or "JPTT" in line:
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

pos_feats = [(word_feats(getWords(os.path.join(pos_dir,f))), 'pos') for f in pos_files]
neg_feats = [(word_feats(getWords(os.path.join(neg_dir,f))), 'neg') for f in neg_files]

negcutoff = len(neg_feats)*3/4
poscutoff = len(pos_feats)*3/4
 
train_feats = neg_feats[:negcutoff] + pos_feats[:poscutoff]
testfeats = neg_feats[negcutoff:] + pos_feats[poscutoff:]

print 'train on %d instances, test on %d instances' % (len(train_feats), len(testfeats))

classifier = NaiveBayesClassifier.train(train_feats)

print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)
classifier.show_most_informative_features(40)


print "Done."


#sr = sorted(vec.items(), key=lambda x:x[1],reverse=True)

