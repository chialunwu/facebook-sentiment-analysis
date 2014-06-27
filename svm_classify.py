# -*- coding: utf-8 -*-
import os
import sys
import socket
import json
import pickle
#import nltk
from libsvm.python.svmutil import *

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = int(sys.argv[1])                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port
s.listen(5)                 # Now wait for client connection.

def wordindex(word):
    global dic
    return dic.get(word)

def word_feats(words, method):
    d = {}
    if method == 'bin':  # binary
        for w in words:
            w = wordindex(w)
            if(w != None):
                d[w] = 1
    elif method == 'mul': # multiple
        for w in words:
            w = wordindex(w)
            if w in d:
                d[w] += 1
            else:
                d[w] = 1
    elif method == 'tf-idf':
        pass
    return d

def load_classifier(path):
   f = open(path, 'rb')
   classifier = pickle.load(f)
   f.close()
   return classifier

print 'Loading classifier...'
c_dir = sys.argv[2]
model = svm_load_model(os.path.join(c_dir,'SVM.classifier'))
f = open(os.path.join(c_dir,'SVM.dictionary'),'r')
dic = json.loads(f.read())
f.close()
f = open(os.path.join(c_dir,'SVM.method'),'r')
method = f.readline().strip()
f.close()

print 'Start classifier service...'
while True:
    c, addr = s.accept()     # Establish connection with client.
    print 'Got connection from', addr
    try:
        data = json.loads(c.recv(4096))
        print '    got {0} tokens'.format(len(data))
    except:
        c.send(json.dumps({'pos':-1,'neg':-1}))
        c.close()
        continue
    feats = [word_feats(data, method)]
    signs = [1 for i in range(len(feats))]
    label, acc, value = svm_predict(signs, feats, model, '-b 1') 

    pos = value[0][0]
    neg = value[0][1]
    print '    pos:{0} neg:{1}'.format(pos,neg)

    c.send(json.dumps({'pos':pos,'neg':neg}))
    c.close()

s.close()
