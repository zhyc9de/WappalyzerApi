# coding:utf-8

#
# Authors:  Xavi Álvarez
#			Pedro Galindo

import os
import tldextract
from sys import platform as _platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from libs import get_root_path
import sys, getopt
import requests
import re
import time

#main method to specify arguments
def main(argv):
	url = ''
	file = ''
	try:
		opts, args = getopt.getopt(argv,"hu:f:c:",["url=","file=","certfile="])
	except getopt.GetoptError:
		print('analyze.py -u <url>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('analyze.py -u <url>')
			sys.exit()
		elif opt in ("-u", "--url"):
			print('[!] Reading URL: '+arg)
			url = arg
			dynamic_analyze(url)
		elif opt in ("-f", "--file"):
			print('[!] Reading URLs from file: '+arg)
			file = open(arg,'r').readlines()
			static_analyze(file)
		elif opt in ("-c", "--certfile"):
			print('[!] Reading URLs from file: '+arg)
			file = open(arg,'r').readlines()
			dynamic_analyze(file)

# Check Operating System
def checkOS():
	operating_system = _platform
	if operating_system == "linux" or operating_system == "linux2":
		# Linux
		print('[!] Launching ChromeDriver for Linux')
		return 'linux'	
	elif operating_system == "darwin":
		# Mac
		print('[!] Launching ChromeDriver for Mac OS X')
		return 'mac'
	elif operating_system == "win32" or operating_system == "win64":
		# Windows
		print('[!] Launching ChromeDriver for Windows')
		return 'win'

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
					   extensions=None,operating_system=None):
	options = Options()

	options.add_argument("window-size=1,1")

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

	if operating_system:
		if operating_system == "linux":
			# Linux
			return webdriver.Chrome(os.getcwd()+'/chromedriver_linux', chrome_options=options) #loading selenium chromedriver for Linux
		elif operating_system == "mac":
			# Mac
			return webdriver.Chrome(os.getcwd()+'/chromedriver_mac', chrome_options=options) #loading selenium chromedriver for Linux
		elif operating_system == "win":
			# Windows
			return webdriver.Chrome(os.getcwd()+'/chromedriver.exe', chrome_options=options) #loading selenium chromedriver for Linux
	return webdriver.Chrome(chrome_options=options)

## driver open browser
def probe(driver,page_url):
	try:
		driver.get(page_url)
		time.sleep(2)
	except Exception as e:
		print('[!] '+page_url+' TIMEOUT')

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
	driver = chrome_new_session(extensions=['wappalyzer'],operating_system=checkOS())
	driver.set_page_load_timeout(30)
	try:
		for url in urls:
			url = url.strip('\r\n')
			try:
				print('[*] Scanning http://'+url)
				probe(driver,'http://'+url)
				print('[*] Scanning https://'+url)
				probe(driver,'https://'+url)
			except:
				continue	
		driver.quit()
	except Exception as e:
		print(e)

#method to extract url from comodo page
def get_comodo_urls(url):
	url = tldextract.extract(url)
	url = url.domain + '.' + url.suffix
	print('[*] Launching CRT.sh Discovery for URL: ' + url)
	result = []
	url_comodo = 'https://crt.sh/?q=%.'
	analyze_url = url_comodo+url
	html = requests.get(analyze_url).text
	regex = re.compile(r'<TD>\S+</TD>') #define regex
	urls = regex.findall(html)
	for url in urls:
		url = url.strip('<TD>')
		url = url.strip('</TD>')
		result.append(url)
	return set(result)

#method to analyze multiple urls to comodo CA crt.sh
def dynamic_analyze(urls):
	driver = chrome_new_session(extensions=['wappalyzer'],operating_system=checkOS())
	driver.set_page_load_timeout(30)
	if isinstance(urls,list) == True or isinstance(urls,set) == True:
		for u in urls:
			u = u.strip("\r\n")
			try:
				cert_urls = get_comodo_urls(u)
				for url in cert_urls:
					print('[!] Found URL: '+url)
					print('[*] Scanning http://'+url)
					probe(driver,'http://'+url)
					print('[*] Scanning https://'+url)
					probe(driver,'https://'+url)
			except Exception as e:
				print(e)
		driver.quit()
	if isinstance(urls, str) == True:
		try:
			cert_urls = get_comodo_urls(urls)
			if cert_urls:
				for url in cert_urls:
					print('[!] Found URL: '+url)
					probe(driver,'http://'+url)
					print('[*] Checking HTTP')
					probe(driver,'https://'+url)
					print('[*] Checking HTTPS')
		except Exception as e:
			print(e)

## while...
if __name__ == '__main__':
	main(sys.argv[1:])
		