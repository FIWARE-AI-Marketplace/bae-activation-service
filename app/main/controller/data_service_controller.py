from flask import request
from flask_restplus import Resource

from ..util.dto import DataServiceDto

from ..service.marketplace_keyrock_service import check_role, MarketplaceKeyrockError
from ..service.provider_keyrock_service import assign_role, ProviderKeyrockError
from ..service.provider_umbrella_service import add_idp, ProviderUmbrellaError

api = DataServiceDto.api
_data_service = DataServiceDto.data_service

ROLE_POSTFIX = ".admin"

@api.route('/')
class ActivateDataService(Resource):

    @api.response(200, 'Data Service access successfully activated.')
    @api.doc('Activate data service')
    @api.expect(_data_service, validate=True)
    def post(self):
        """Activates data service """
        data = request.json
        token = None

        # Check role in Marketplace Keyrock
        try:
            # Check for authorization header with bearer token
            auth_header = request.headers.get('Authorization')
            token = get_token(auth_header)
            if not token:
                raise MarketplaceKeyrockError('Missing authorization header')

            # Check role
            check_role(token=token, role=data.get('role'))
        except MarketplaceKeyrockError as error:
            print('Role ' + data.get('role') + ' was not acquired. ' + error.get_message())
            response_object = {
                'status': 'fail',
                'message': 'Role ' + data.get('role') + ' was not acquired. ' + error.get_message()
            }
            return response_object, 403
        except Exception as err:
            print('General error when checking user role. ' + str(err))
            response_object = {
                'status': 'fail',
                'message': 'General error when checking user role. ' + str(err)
            }
            return response_object, 500
            
        # Assign role in data service Keyrock
        ret_assign = None
        try:
            consumer_id = data.get('name')
            role = data.get('role')
            role = role.replace(ROLE_POSTFIX, '') # Remove .admin
            ret_assign = assign_role(consumer_id, role)
        except ProviderKeyrockError as err:
            print('Role ' + role + ' could not be assigned to ' + consumer_id + ' in Data Service Keyrock. ' + err.get_message())
            response_object = {
                'status': 'fail',
                'message': 'Role ' + role + ' could not be assigned to ' + consumer_id + ' in Data Service Keyrock. ' + err.get_message()
            }
            return response_object, 500
        except Exception as err:
            print('General error when assigning role in data service Keyrock. ' + str(err))
            response_object = {
                'status': 'fail',
                'message': 'General error when assigning role in data service Keyrock. ' + str(err)
            }
            return response_object, 500

        # Store consumer Keyrock information in API Umbrella
        try:
            secret = data.get('secret')
            endpoint = data.get('endpoint')
            org_id = ret_assign['org_id']
            add_idp(consumer_id, org_id, secret, endpoint)
        except ProviderUmbrellaError as err:
            print('IDP could not be added to data service API Umbrella for ' + consumer_id + '. ' + err.get_message())
            response_object = {
                'status': 'fail',
                'message': 'IDP could not be added to data service API Umbrella for ' + consumer_id + '. ' + err.get_message()
            }
            return response_object, 500
        except Exception as err:
            print('General error when adding IDP to data service API Umbrella. ' + str(err))
            response_object = {
                'status': 'fail',
                'message': 'General error when adding IDP to data service API Umbrella. ' + str(err)
            }
            return response_object, 500

        response_object = {
            'status': 'success',
            'message': 'Data service access successfully activated.'
        }
        return response_object, 200

def get_token(header):
    PREFIX = "Bearer"
    if not header or (not header.startswith(PREFIX)):
        return None

    return header[len(PREFIX)+1:]
