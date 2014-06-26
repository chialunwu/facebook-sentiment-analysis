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
    if dic.get(word) == None:
        print 'Word not found!!!'
    return dic[word]

def word_feats(words):
    return dict([(wordindex(word), 1) for word in words])

def load_classifier(path):
   f = open(path, 'rb')
   classifier = pickle.load(f)
   f.close()
   return classifier

print 'Loading classifier...'
model = svm_load_model('SVM.classifier')
f = open('SVM.dictionary','r')
dic = f.read()
dic = json.loads(dic)

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

    feats = [word_feats(data)]
    signs = [1 for i in range(len(feats))]
    label, acc, value = svm_predict(signs, feats, model, '-b 1') 
    print value

    pos = value[0][0]
    neg = value[0][1]
    c.send(json.dumps({'pos':pos,'neg':neg}))
    c.close()

s.close()
