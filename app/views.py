#
# Authors:  Xavi Álvarez
#			Pedro Galindo

from app.init_app import app, db
from app.models import Projects
from flask import request
import json
import datetime
from urllib.parse import urlparse
import sqlite3
from sqlite3 import Error

#method to connect bbdd
def connect(db_file='app.sqlite'):
	try:
		conn = sqlite3.connect(db_file)
		return conn
	except Error as e:
		print(e)
 
	return None

#method to update a specific url
def UpdateProject(url,data_http=None,data_https=None):
	search_project = Projects.query.filter_by(url=url).first()
	if not search_project:
		project = Projects(url=url,json_http=data_http,json_https=data_https,json_last_updated=datetime.datetime.now())
		db.session.add(project)
		db.session.commit()
		return print('Added '+url+' to DB.')
	search_project.json_https = data_https
	db.session.add(search_project)
	db.session.commit()

	
#method to receive post requests
@app.route("/", methods=['POST'])
def receive():
	try:
		url = json.loads(request.form['url'])['url']
		data = request.form['json']
		if 'http://' in url:
			UpdateProject(urlparse(url).netloc,data_http=data)
		if 'https://' in url:
			UpdateProject(urlparse(url).netloc,data_https=data)
		return 'Saved '+ url + ' on DB.'	
	except Exception as e:
		print(e)