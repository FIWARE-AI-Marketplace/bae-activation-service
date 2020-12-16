from flask import current_app

import requests
import json

class ProviderUmbrellaError(Exception):
    def __init__(self, msg):
        self.message = msg

    def get_message(self):
        return self.message

def add_idp(consumer_id, org_id, secret, endpoint):
    # Add consumer IDP in Provider API Umbrella
    if current_app.config['DEBUG']:
        print('Adding IDP of consumer ' + consumer_id + ' (OrgID: '+org_id+') with JWT secret in provider API Umbrella.')

    # API Umbrella config
    UMBRELLA_URL = current_app.config['PROVIDER_UMBRELLA_SERVER']
    UMBRELLA_TOKEN = current_app.config['PROVIDER_UMBRELLA_ADMIN_TOKEN']
    UMBRELLA_API_KEY = current_app.config['PROVIDER_UMBRELLA_API_KEY']

    # Add IDP
    url = UMBRELLA_URL + '/api-umbrella/v1/idps'
    headers = {
        'X-Api-Key': UMBRELLA_API_KEY,
        'X-Admin-Auth-Token': UMBRELLA_TOKEN
    }
    body = {
        "organization_id": org_id,
        "type": "keyrock",
        "endpoint": endpoint,
        "secret": secret
    } #TODO: Uncomment!!!
    #resp = requests.post(url, json=body, headers=headers)
    #if (not resp) or (not resp.status_code==201):
    #    raise ProviderUmbrellaError('Could not add IDP to API Umbrella')


