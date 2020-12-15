from flask import Flask
from healthcheck import HealthCheck

from .config import config_by_name


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Add health endpoint
    health = HealthCheck()
    app.add_url_rule("/health", "healthcheck", view_func=lambda: health.run())

    return app
