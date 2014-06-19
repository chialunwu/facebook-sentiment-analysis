#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Name: utf82big5.py
# Description: convert all utf-8 files in specified dir to Big5
# Arguments: ./utf82big5.py dir_name out_dir
# Author: Leo Wu
# Date: 2014.6.19
#

import os
from os.path import isfile, join
import sys
import codecs

in_dir = sys.argv[1]
out_dir = sys.argv[2]

files = os.listdir(in_dir)

for f in files:
    fi = codecs.open(join(in_dir,f),'r',encoding='utf8')
    try:
        result = fi.read().encode('big5')
    except:
        fi.close()
        continue
    fo = open(join(out_dir,f),'w')
    fo.write(result)
    fi.close()
    fo.close()
    print "convert done: "+f
