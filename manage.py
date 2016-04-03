import os
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from appflask import appf, db

migrate = Migrate(appf, db)
manager = Manager(appf)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
	manager.run()