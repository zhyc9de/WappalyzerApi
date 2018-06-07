#
# Authors:  Xavi Álvarez
#			Pedro Galindo

from app.init_app import app, db
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
def update_row(conn,table,url,data): 
	print('Updating information... ' + url)
	try:
		cur = conn.cursor()
		sql = ''' UPDATE '%s' SET json_last_updated = '%s', json = '%s' WHERE url = '%s' ''' % (table,datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),data,url)
		cur.execute(sql) 
		conn.commit()
	except Error as e:
		print(e)

# method to check if url exists in bbdd
def select_row(conn,table,url):
	cur = conn.cursor()
	cur.execute("SELECT * FROM '%s' WHERE url = '%s'" % (table,url,)) 
	rows = cur.fetchall()
	return rows
			
#method to create a new row if url doesn't exist in bbdd			
def create_row(conn,table,url,data): 
	print('Creating new entry by ...' + url)
	try:
		cur = conn.cursor()
		sql = '''INSERT INTO '%s' VALUES (NULL,'%s','%s','%s') ''' % (table,url,data,datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
		cur.execute(sql) 
		conn.commit()
	except Error as e:
		print(e)
	
#method to receive post requests
@app.route("/", methods=['POST'])
def receive():
	try:
		url = json.loads(request.form['url'])['url']
		url = urlparse(url).netloc
		data = request.form['json']
		conn = connect('app.sqlite')
		if not select_row(conn,'projects',url): #if url doesn't exist
			create_row(conn,'projects',url,data)
		else:	
			update_row(conn,'projects',url,data)
		return 'Saved.'	
	except Exception as e:
		print(e)