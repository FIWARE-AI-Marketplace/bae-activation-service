import os
from flask_restplus import Api
from flask import Blueprint, url_for

from .main.controller.data_service_controller import api as data_service_ns

blueprint = Blueprint('api', __name__)

if os.getenv('HTTPS_SCHEME', True):
    @property
    def specs_url(self):
        return url_for(self.endpoint('specs'), _external=True, _scheme='https')
 
    Api.specs_url = specs_url
    

api = Api(blueprint,
          title='Marketplace Activation Service API',
          version='1.0',
          description='Activation Service for services offered on Marketplace',
          doc='/swagger/'
          )

api.add_namespace(data_service_ns, path='/data_service')
