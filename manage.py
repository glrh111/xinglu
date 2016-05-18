#! /usr/bin/env python
import os
from app import create_app, db
from app.models import User, Role
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrageCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
	return dict(app=app, db=db, User=User, Role=Role)

maneger.add_command("shell", Shell(make_context=make_shell_context))
manage.add_command('db', MigrageCommand)

@manager.command
def test():
	'''
	unittests
	'''
	import unittest
	tests = unittest.TestLoader().discover('tests')
	unittests.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
	manager.run()