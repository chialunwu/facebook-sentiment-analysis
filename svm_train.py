# -*- coding: utf-8 -*-
# Name: tok2vec.py
# Description: transform the results in tokenized/[happy] to VSM, for SVM
# Author: Leo Wu
# Date: 2014.06.23

import re
import os
import sys
import pickle
import json
#import nltk.classify.util
from libsvm.python.svmutil import *

def checkstop(word):
    if word in stop:
        return True
    else:
        return False

def read_list(path,List):
    with open(path,'r') as f:
        for e in f:
            List.append(e.strip())

def save_classifier(classifier, path):
   f = open(path, 'wb')
   pickle.dump(classifier, f)
   f.close()

dic = {}
def wordindex(word):
    word = word.decode('big5')
    if dic.get(word) == None:
        dic[word] = len(dic)
    return dic[word]

def word_feats(words):
    return dict([(wordindex(word), 1) for word in words])

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
 
def save_dic():
    f = open('SVM.dictionary','w')
    f.write(json.dumps(dic))
    f.close()

stop = []
pos = []
neg = []
read_list('lib/stopword.list',stop)
#read_list('ntusd-positive.txt',pos)

pos_dir = sys.argv[1]
neg_dir = sys.argv[2]

pos_files = os.listdir(pos_dir)
neg_files = os.listdir(neg_dir)

pos_vec = []
neg_vec = []

pos_feats = [word_feats(getWords(os.path.join(pos_dir,f))) for f in pos_files]
print pos_feats[2]
neg_feats = [word_feats(getWords(os.path.join(neg_dir,f))) for f in neg_files]

save_dic()

negcutoff = len(neg_feats)*3/4
poscutoff = len(pos_feats)*3/4
 
train_feats = neg_feats[:negcutoff] + pos_feats[:poscutoff]
test_feats = neg_feats[negcutoff:] + pos_feats[poscutoff:]

print 'Train on %d instances, test on %d instances' % (len(train_feats), len(test_feats))

train_signs = [-1 for i in range(negcutoff)] + [1 for i in range(poscutoff)]
test_signs = [-1 for i in range(len(neg_feats) - negcutoff)] + [1 for i in range(len(pos_feats) - poscutoff)]

prob = svm_problem(train_signs, train_feats)
param = svm_parameter('-t 0 -c 4 -b 1')
model = svm_train(prob, param)

p_label, p_acc, p_val = svm_predict(test_signs, test_feats, model, '-b 1')
print 'Label:', p_label
print 'Accuracy:', p_acc
print 'Value:', p_val

svm_save_model('SVM.classifier', model)
print 'Save classifier in \'SVM.classifier\''
#sr = sorted(vec.items(), key=lambda x:x[1],reverse=True)

