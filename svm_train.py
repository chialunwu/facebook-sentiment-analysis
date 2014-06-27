# -*- coding: utf-8 -*-
# Name: tok2vec.py
# Description: transform the results in tokenized/[happy] to VSM, for SVM
# Author: Leo Wu
# Date: 2014.06.23
# Example : python svm_train.py dataset/pos dataset/neg -m bin -c 0.9 -o classifier -d

import re
import os
import sys
import pickle
import json
from libsvm.python.svmutil import *
import logging

logger = logging.getLogger( __name__  )
logging.basicConfig(filename="log", level=logging.DEBUG)

def checkstop(word):
    if word in stop:
        return True
    else:
        return False

def read_list(path,List):
    with open(path,'r') as f:
        for e in f:
            List.append(e.strip())

dic = {}
def wordindex(word):
    word = word.decode('big5')
    if dic.get(word) == None:
        dic[word] = len(dic)
    return dic[word]

def word_feats(words, method):
    if method == 'bin':  # binary
        return dict([(wordindex(word), 1) for word in words])
    elif method == 'mul': # multiple
        d = {}
        for w in words:
            w = wordindex(w)
            if w in d:
                d[w] += 1
            else:
                d[w] = 1
        return d
    elif method == 'tf-idf':
        pass


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
 
def save_dic(d):
    f = open(os.path.join(d,'SVM.dictionary'),'w')
    f.write(json.dumps(dic))
    f.close()


if __name__ == '__main__':
    stop = []
    pos = []
    neg = []
    read_list('lib/stopword.list',stop)
    #read_list('ntusd-positive.txt',pos)

    pos_dir = sys.argv[1]
    neg_dir = sys.argv[2]
    method = sys.argv[sys.argv.index('-m')+1]
    cutoff = float(sys.argv[sys.argv.index('-c')+1])
    out_dir = sys.argv[sys.argv.index('-o')+1]

    logger.info('SVM- method:{0} cutoff:{1}'.format(method,cutoff))

    pos_files = os.listdir(pos_dir)
    neg_files = os.listdir(neg_dir)

    pos_feats = [word_feats(getWords(os.path.join(pos_dir,f)), method) for f in pos_files]
    neg_feats = [word_feats(getWords(os.path.join(neg_dir,f)), method) for f in neg_files]

    negcutoff = int(len(neg_feats)*cutoff)
    poscutoff = int(len(pos_feats)*cutoff)
     
    train_feats = neg_feats[:negcutoff] + pos_feats[:poscutoff]
    test_feats = neg_feats[negcutoff:] + pos_feats[poscutoff:]

    s = 'Train on %d instances, test on %d instances' % (len(train_feats), len(test_feats))
    print s    
    logger.info(s)

    train_signs = [-1 for i in range(negcutoff)] + [1 for i in range(poscutoff)]
    test_signs = [-1 for i in range(len(neg_feats) - negcutoff)] + [1 for i in range(len(pos_feats) - poscutoff)]

    prob = svm_problem(train_signs, train_feats)
    param = svm_parameter('-t 0 -c 4 -b 1')
    model = svm_train(prob, param)

    p_label, p_acc, p_val = svm_predict(test_signs, test_feats, model, '-b 1')
    
    s = 'Accuracy: '+ str(p_acc)
    print s
    logger.info(s)

    if '-d' in sys.argv:
        pass
    else:
        svm_save_model(os.path.join(out_dir,'SVM.classifier'), model)
        print 'Save classifier in \'{0}/SVM.classifier\''.format(out_dir)
        save_dic(out_dir)
        f = open(os.path.join(out_dir,'SVM.method'),'w')
        f.write(method)
        f.close()
