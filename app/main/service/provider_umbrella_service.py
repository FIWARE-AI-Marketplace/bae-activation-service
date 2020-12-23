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
    current_app.logger.debug('Adding IDP of consumer ' + consumer_id + ' (OrgID: '+org_id+') with JWT secret in provider API Umbrella.')

    # API Umbrella config
    UMBRELLA_URL = current_app.config['PROVIDER_UMBRELLA_SERVER']
    UMBRELLA_TOKEN = current_app.config['PROVIDER_UMBRELLA_ADMIN_TOKEN']
    UMBRELLA_API_KEY = current_app.config['PROVIDER_UMBRELLA_API_KEY']

    if not UMBRELLA_URL or len(UMBRELLA_URL) < 1:
        err_msg = 'Provider API Umbrella URL not set'
        raise ProviderUmbrellaError(err_msg)

    # Check if IDP with this endpoint already exists
    url = UMBRELLA_URL + '/api-umbrella/v1/idps'
    headers = {
        'X-Api-Key': UMBRELLA_API_KEY,
        'X-Admin-Auth-Token': UMBRELLA_TOKEN
    }
    resp = requests.get(url, headers=headers)
    if (not resp) or (not resp.status_code==200):
        raise ProviderUmbrellaError('Could not get list of IDPs from API Umbrella')
    idp_id = None
    if resp.json()['data'] and len(resp.json()['data']) > 0:
        for idp in resp.json()['data']:
            if idp['endpoint'] == endpoint:
                idp_id = idp['id']
                break
    
    # Add/Update IDP
    url = UMBRELLA_URL + '/api-umbrella/v1/idps'
    body = {
        "organization_id": org_id,
        "type": "keyrock",
        "endpoint": endpoint,
        "secret": secret
    }
    if idp_id:
        # Update IDP
        url += '/' + idp_id
        resp = requests.put(url, json=body, headers=headers)
        if (not resp) or (not resp.status_code==204):
            raise ProviderUmbrellaError('Could not update IDP ' + endpoint + ' for ' + consumer_id + ' in API Umbrella')
    else:
        # Create IDP
        resp = requests.post(url, json=body, headers=headers)
        if (not resp) or (not resp.status_code==201):
            raise ProviderUmbrellaError('Could not add IDP ' + endpoint + ' for ' + consumer_id + ' to API Umbrella')


