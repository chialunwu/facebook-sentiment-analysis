# -*- coding: utf-8 -*-
# Example: python naive_classify 12345 classifier/
import os
import sys
import socket
import json
import pickle
import nltk

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

def load_classifier(path):
   f = open(path, 'rb')
   classifier = pickle.load(f)
   f.close()
   return classifier

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = int(sys.argv[1])                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port
s.listen(5)                 # Now wait for client connection.

print 'Loading classifier...'
c_dir = sys.argv[2]
f = open(os.path.join(c_dir,'Naive.method'),'r')
method = f.readline().strip()
f.close()
classifier = load_classifier(os.path.join(c_dir,'Naive.classifier'))

print 'Start classifier service...'
while True:
    c, addr = s.accept()     # Establish connection with client.
    print 'Got connection from', addr
    try:
        data = json.loads(c.recv(4096))
        data = [e.encode('big5') for e in data]
        print '    got {0} tokens'.format(len(data))
    except:
        c.send(json.dumps({'pos':-1,'neg':-1}))
        c.close()
        continue
    result = classifier.prob_classify(word_feats(data, method))
    pos = result.prob('pos')
    neg = result.prob('neg')
    print '    pos:{0} neg:{1}'.format(pos,neg)

    c.send(json.dumps({'pos':pos,'neg':neg}))
    c.close()

s.close()
print method 
