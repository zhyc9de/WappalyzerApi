#
# Authors: Xavi Álvarez
#          Pedro Galindo

from app.init_app import app, init_app, manager

# Start a development web server, processing extra command line parameters. E.g.:
# - python manage.py init_db
# - python manage.py runserver
if __name__ == "__main__":
    init_app(app)
    manager.run()