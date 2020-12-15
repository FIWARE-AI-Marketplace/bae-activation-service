from flask_restplus import Namespace, fields


class DataServiceDto:
    api = Namespace('data_service', description='activation of data service')
    data_service = api.model('data_service', {
        'id': fields.String(required=True, description='Consumer ID'),
        'role': fields.String(required=True, description='Acquired role in Marketplace'),
        'secret': fields.String(required=True, description='JWT secret of future requests')
    })

