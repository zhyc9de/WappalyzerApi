#
# Authors: Xavi Álvarez
#          Pedro Galindo

from app.init_app import app, db, manager
from app.models import Projects

@manager.command
def init_db():
    """ Initialize the database."""
    # Create all tables
    db.create_all()
    # Save to DB
    db.session.commit()
