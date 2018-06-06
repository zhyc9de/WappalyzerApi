#
# Authors: Xavi Álvarez
#          Pedro Galindo

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager

app = Flask(__name__)
db = SQLAlchemy()               # Setup Flask-SQLAlchemy
manager = Manager(app)          # Setup Flask-Script

# Initialize Flask Application
def init_app(app):
	# Read common settings from 'app/settings.py'
	app.config.from_object('app.settings')

	# Read environment-specific settings from 'app/local_settings.py'
	try:
		app.config.from_object('app.local_settings')
	except ImportError:
		print("The configuration file 'app/local_settings.py' does not exist.\n"+
			  "Please copy app/local_settings_example.py to app/local_settings.py\n"+
			  "and customize its settings before you continue.")
		exit()

	# Initialize Flask-SQLAlchemy and Flask-Script _after_ app.config has been read
	db.init_app(app)

	import app.manage_commands
	from app import views