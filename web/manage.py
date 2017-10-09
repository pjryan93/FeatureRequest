import os
from flask_script import Manager # class for handling a set of commands
from flask_migrate import Migrate, MigrateCommand
from app import db, create_app
from app import models

app_settings = os.getenv('APP_SETTINGS')
if app_settings is None:
	app = create_app('development')
else:
	app = create_app(config_name=app_settings)
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()