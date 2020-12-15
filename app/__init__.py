from flask_restplus import Api
from flask import Blueprint

from .main.controller.data_service_controller import api as data_service_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='Marketplace Activation Service API',
          version='1.0',
          description='Activation Service for services offered on Marketplace',
          doc='/swagger/'
          )

api.add_namespace(data_service_ns, path='/data_service')
