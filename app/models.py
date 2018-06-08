#
# Authors:  Xavi Álvarez
#			Pedro Galindo

from app.init_app import app, db

# Define the Role data model
class Projects(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer(), primary_key=True)
    url = db.Column(db.String(50), nullable=False, unique=True)
    json_http = db.Column(db.Text, nullable=True)
    json_https = db.Column(db.Text, nullable=True)
    json_last_updated = db.Column(db.DateTime())
    def __init__(self,url,json_http,json_https,json_last_updated):
        self.url = url
        self.json_http = json_http
        self.json_https = json_https
        self.json_last_updated = json_last_updated

