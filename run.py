import os

from app import create_app

config = os.getenv('APP_SETTINGS') # config_name = config.DevelopmentConfig
app = create_app(config)
app.app_context().push()

if __name__ == '__main__':
    app.run()
