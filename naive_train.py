# -*- coding: utf-8 -*-
# Name: naive_train.py
# Description: transform the results in tokenized/[happy] to VSM, for SVM
# Author: Leo Wu
# Date: 2014.06.23
# Update: 2014.06.27
# Example : python naive_train.py tokenized/pos tokenized/neg -m bin -c 0.9 -o classifier -d

import re
import os
import sys
import pickle
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
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

def save_classifier(classifier, path):
   f = open(path, 'wb')
   pickle.dump(classifier, f)
   f.close()

def word_feats(words, method):
    if method == 'bin':  # binary
        return dict([(word, 1) for word in words])
    elif method == 'mul': # multiple
        dic = {}
        for w in words:
            if w in dic:
                dic[w] += 1
            else:
                dic[w] = 1
        return dic
 
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


if __name__ == '__main__': 
    stop = []
    pos = []
    neg = []
    read_list('lib/stopword.list',stop)
    #read_list('ntusd-positive.txt',pos)
    #read_list('ntusd-negative.txt',neg)

    pos_dir = sys.argv[1]
    neg_dir = sys.argv[2]
    method = sys.argv[sys.argv.index('-m')+1]
    cutoff = float(sys.argv[sys.argv.index('-c')+1])
    out_dir = sys.argv[sys.argv.index('-o')+1]

    logger.info('Naive bayes- method:{0} cutoff:{1}'.format(method,cutoff))

    pos_files = os.listdir(pos_dir)
    neg_files = os.listdir(neg_dir)

    pos_feats = [(word_feats(getWords(os.path.join(pos_dir,f)), method), 'pos') for f in pos_files]
    neg_feats = [(word_feats(getWords(os.path.join(neg_dir,f)), method), 'neg') for f in neg_files]

    negcutoff = int(len(neg_feats)*cutoff)
    poscutoff = int(len(pos_feats)*cutoff)
     
    train_feats = neg_feats[:negcutoff] + pos_feats[:poscutoff]
    testfeats = neg_feats[negcutoff:] + pos_feats[poscutoff:]

    s = 'Train on %d instances, test on %d instances' % (len(train_feats), len(testfeats))
    print s
    logger.info(s)

    classifier = NaiveBayesClassifier.train(train_feats)

    s = 'Accuracy: '+ str(nltk.classify.util.accuracy(classifier, testfeats))
    print s
    logger.info(s)

    if '-d' in sys.argv:
        pass
    else:
        save_classifier(classifier,os.path.join(out_dir,'Naive.classifier'))
        print 'Save classifier in \'{0}/Naive.classifier\''.format(out_dir)
        f = open(os.path.join(out_dir,'Naive.method'),'w')
        f.write(method)
        f.close()
