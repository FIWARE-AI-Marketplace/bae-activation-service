import os
import unittest
import logging

from flask_script import Manager

from app.main import create_app
from app import blueprint

app = create_app(os.getenv('CONFIG_ENV') or 'dev')
app.register_blueprint(blueprint)

app.app_context().push()

manager = Manager(app)

@manager.command
def run():
    app.run()

#if __name__ == '__main__':
#    print('Main')
#    gunicorn_logger = logging.getLogger('gunicorn.error')
#    app.logger.handlers = gunicorn_logger.handlers
#    app.logger.setLevel(gunicorn_logger.level)
#    app.logger.error("--- Starting BAE Activation Service ---")
#    manager.run()

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.logger.info("--- Starting BAE Activation Service on worker node ---")
    
