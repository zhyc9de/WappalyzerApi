# coding:utf-8
import time, os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from libs import get_root_path
import sqlite3
from sqlite3 import Error

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
		time.sleep(3)
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

## while...
if __name__ == '__main__':
	try:
		conn = connect('app.sqlite')
		dicc = select_all(conn)
		urls = get_urls(dicc)
		if not not urls:
			for url in urls:
				print("Reading URL ..." + url)
				try:
					probe('http://'+url)
					probe('https://'+url)
				except:
					continue
		else:
			print("Please add URL in BBDD.")			
	except Exception as e:
		print(e)		