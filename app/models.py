#
# Authors:  Xavi Álvarez
#			Pedro Galindo

from app.init_app import app, db

# Define the Role data model
class Projects(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer(), primary_key=True)
    url = db.Column(db.String(50), nullable=False, server_default='')
    json = db.Column(db.Text, nullable=False, server_default='')
    json_last_updated = db.Column(db.DateTime())
    def __init__(self,url,json,json_last_updated):
        self.url = url
        self.json = json
        self.json_last_updated = json_last_updated

