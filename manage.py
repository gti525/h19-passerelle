import os

from flask_migrate import MigrateCommand, Migrate
from flask_script import Manager

from app import create_app, db

config = os.getenv('APP_SETTINGS')  # config_name = config.DevelopmentConfig

app = create_app(config)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
