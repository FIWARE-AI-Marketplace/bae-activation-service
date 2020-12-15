import os
import unittest

from flask_script import Manager

from app.main import create_app
from app import blueprint

app = create_app(os.getenv('CONFIG_ENV') or 'dev')
app.register_blueprint(blueprint)

app.app_context().push()

manager = Manager(app)

@manager.command
def run():
    print("--- Starting BAE Activation Service ---")
    app.run()

if __name__ == '__main__':
    manager.run()
