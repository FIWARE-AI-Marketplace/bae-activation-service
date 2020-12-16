from flask_restplus import Namespace, fields


class DataServiceDto:
    api = Namespace('data_service', description='activation of data service')
    data_service = api.model('data_service', {
        'name': fields.String(required=True, description='Name of organization to activate service for (should be unique)'),
        'role': fields.String(required=True, description='Acquired role in Marketplace'),
        'secret': fields.String(required=True, description='JWT secret of signing IDP'),
        'endpoint': fields.String(required=True, description='Endpoint of signing IDP')
    })

