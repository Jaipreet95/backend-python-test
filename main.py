"""AlayaNotes

Usage:
  main.py [run]
  main.py initdb
"""
from docopt import docopt
import subprocess
import os

from alayatodo import app, db
from alayatodo.models import Todo,Users


def _create_default_user():
    user = Users(username='admin1', password='admin1')
    db.session.add(user)
    db.session.commit()

def _create_dummy_todos():
    user = Users.query.get(1)
    for i in range(15):
        t = Todo(description='randomDescription'+str(i), users=user)
        db.session.add(t)
    db.session.commit()

if __name__ == '__main__':
    args = docopt(__doc__)
    if args['initdb']:
        os.system('flask db init')
        os.system('flask db migrate -m "Initial Migrations"')
        os.system('flask db upgrade')
        _create_default_user()
        _create_dummy_todos()
        print "AlayaTodo: Database initialized."
    else:
        app.run(use_reloader=True)
