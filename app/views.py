from app.init_app import app, db
from flask import request
import os
import random
import string
import time
import json
import datetime

def connect(db_file='app.sqlite'):
	try:
		conn = sqlite3.connect(db_file)
		return conn
	except Error as e:
		print(e)
 
	return None

def update_row(conn,table,url,row_dicc): #select all funtion, return a dictionar key=column name, value=content column
	print('Updating information...' + url)
	cur = conn.cursor()
	cur.execute(''' UPDATE '%s' SET updated_date = '%s',json = '%s' WHERE 'url' = '%s' ''' % (table,datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),row_dicc['json'],url)) 
	conn.commit()

def select_row(conn,table,url): #select all funtion, return a dictionar key=column name, value=content column
	cur = conn.cursor()
	cur.execute("SELECT * FROM '%s' WHERE url = '%s'" % (table,url,)) 
	columns = [column[0] for column in cur.description]
	result_dicc = [] # array
	for row in cur.fetchall():
		result_dicc.append(dict(zip(columns, row)))
	return result_dicc[0] #return dicc
	
@app.route("/", methods=['POST'])
def receive():
	print("hola")
	try:
		url = json.loads(request.form['url'])['url']
		url = urlparse(url).netloc
		data = json.loads(request.form['json'])
		print(data)
		conn = connect('app.sqlite')
		dicc = select_row(conn,'projects',url)
		update_row(conn,'projects',url,dicc)
		return 'Saved.'
	except Exception as e:
		print(e)