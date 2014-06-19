#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Leo Wu
# Date: 2014.6.19
#
# Name: getPTTBoard.py
# Description: get the contents(only) of a PTT board
# Arguments: ./getPTTBoard.py board_name index_page_num1 [index_page_num2] dir_name
#	     it will get pages from index index_page_num1 to index_page_num2#

import pycurl
import sys
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger( __name__  )
logging.basicConfig(filename="log", level=logging.DEBUG)

class GetPage:
    def __init__ (self, url):
        self.contents = ''
        self.url = url

    def read_page (self, buf):
        self.contents = self.contents + buf

    def get_page (self):
        return self.contents

def Download(href):
	page = GetPage(href)
	testcurl = pycurl.Curl()
	testcurl.setopt(testcurl.URL, page.url)
	testcurl.setopt(testcurl.WRITEFUNCTION, page.read_page)
	testcurl.perform()
	testcurl.close()
	return page

def main():
	board_name = sys.argv[1]
	board = "https://www.ptt.cc/bbs/{0}/".format(sys.argv[1])
	start = int(sys.argv[2])
	end = int(sys.argv[3])
	out_dir = sys.argv[4]

	for num in range(start,end+1):
		print "{0}: Get page {1}...".format(board_name,num)
		# get links page
		href = board+"index{0}.html".format(num)
		page = Download(href)
		links = []
		soup = BeautifulSoup(page.get_page())
		# extract links
		s = soup.find_all(class_="r-ent")
		for e in s:
			a = e.find(class_="title").a
			if a != None:
				links.append(a.get('href'))
		# get page of each link
		for index, link in enumerate(links):
			href = str("https://www.ptt.cc"+link)
			try:
				page = Download(href)
				soup = BeautifulSoup(page.get_page())
				soup = soup.find(id="main-content")
				content = soup.div.next_sibling.next_sibling.next_sibling.next_sibling
			except:
				logger.error(href)
				continue
			if content != None:
				f = open(out_dir+'/'+str(num)+'-'+str(index)+'.txt','w')
				f.write(content.encode('utf-8'))

if __name__ == '__main__':
    main()

