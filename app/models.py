#
# Authors: Xavi Álvarez
#          Pedro Galindo

from app.init_app import app, db

# Define the Role data model
class Projects(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, server_default='') #1
    created_date = db.Column(db.DateTime())
    url = db.Column(db.String(50), nullable=False, server_default='')
    updated_date = db.Column(db.DateTime())
    json = db.Column(db.String(255), nullable=False, server_default='') #5
