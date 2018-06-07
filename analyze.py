# coding:utf-8

#
# Authors:  Xavi Álvarez
#			Pedro Galindo

import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from libs import get_root_path
import sqlite3
from sqlite3 import Error
import sys, getopt
import requests
import re

#main method to specify arguments
def main(argv):
	url = ''
	file = ''
	try:
		opts, args = getopt.getopt(argv,"hu:f:",["url=","file="])
	except getopt.GetoptError:
		print('analyze.py -u <url>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('analyze.py -u <url>')
			sys.exit()
		elif opt in ("-u", "--url"):
			url = arg
			print('URL to crawl and analys is: ' + url), url
			dynamic_analyze(url)
		elif opt in ("-f", "--file"):
			print('Normal functionality')
			file = open(arg,'r').readlines()
			static_analyze(file)

################ BD GENERIC METHODS #################

def connect(db_file='app.sqlite'):
	try:
		conn = sqlite3.connect(db_file)
		return conn
	except Error as e:
		print(e)
 
	return None

def select_all(conn):
	cur = conn.cursor()
	cur.execute("SELECT * FROM projects")
	columns = [column[0] for column in cur.description]
	principal_dicc = [] # array
	content_dicc =  []
	num = 1
	for row in cur.fetchall():
		content_dicc.append(dict(zip(columns,row)))
		principal_dicc.append(dict(zip(str(num), content_dicc)))
		content_dicc = []
		num = num + 1

	return principal_dicc #return dicc

##### Functional methods

ext_dir_path = get_root_path('libs/crawler/chrome_ext') #chrome extensions

##method to add extension
def add_ext(options, crx_name):
	crx_path = ext_dir_path + crx_name + '.crx'
	if not os.path.isfile(crx_path):
		raise FileNotFoundError('File not found.')
	options.add_extension(crx_path)

## defining new chrome session
def chrome_new_session(show_image=True, incognito=False, proxy_server=None, ua=None, mobile=False,
					   extensions=None):
	options = Options()

	if not show_image:
		options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})

	if incognito:
		options.add_argument("--incognito")

	if ua:
		options.add_argument("user-agent=" + ua)

	if proxy_server:
		options.add_argument('--proxy-server=' + proxy_server)

	if mobile:  # todo 自由设定device name
		mobile_emulation = {"deviceName": "Google Nexus 5"}
		options.add_experimental_option("mobileEmulation", mobile_emulation)

	if extensions:
		[add_ext(options, crx) for crx in extensions]

	return webdriver.Chrome(chrome_options=options) #loading selenium chromwdriver with specific options

## driver open browser
def probe(page_url):
	print("Analyzing: " + page_url)
	try:
		driver = chrome_new_session(extensions=['wappalyzer'])
		driver.get(page_url)
		driver.quit()
	except Exception as e:
		print(e)

#method to extract urls from list of dict
def get_urls(dicc):
	urls = []
	for item in dicc: #list
		for key,v in item.items(): #first dicc
			for key2,v2 in v.items():
				if key2 == 'url':
					urls.append(v2)
	return urls

#method to analyze a specific url
def static_analyze(urls):
	try:
		for url in urls:
			print("Reading URL ..." + url)
			try:
				probe('http://'+url)
				probe('https://'+url)
			except:
				continue	
	except Exception as e:
		print(e)

#method to extract url from comodo page
def get_comodo_urls(url):
	url_comodo = 'https://crt.sh/?q=%.'
	analyze_url = url_comodo+url
	html = requests.get(analyze_url).text
	regex = re.compile(r'<TD>\S+</TD>') #define regex
	urls = regex.findall(html)
	return set(urls)

#method to analyze multiple urls to comodo CA crt.sh
def dynamic_analyze(url):
	try:
		conn = connect('app.sqlite')
		urls = get_comodo_urls(url)
		if urls:
			for url in urls:
				url = url.replace('<TD>','')
				url = url.replace('</TD>','')
				print("Reading URL: " + url)
				try:
					probe('http://'+url)
					probe('https://'+url)
				except:
					continue
		else:
			print("Please add URL in BBDD.")			
	except Exception as e:
		print(e)

## while...
if __name__ == '__main__':
	main(sys.argv[1:])
		