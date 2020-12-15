from flask import current_app

import requests
import json

class MarketplaceKeyrockError(Exception):
    def __init__(self, msg):
        self.message = msg

    def get_message(self):
        return self.message

def check_role(token, role):
    # Check in Marketplace Keyrock for acquired role
    if current_app.config['DEBUG']:
        print('Checking Marketplace role. Token: ' + token + ', Role: ' + role)

    # Keyrock config
    KEYROCK_URL = current_app.config['BAE_KEYROCK_SERVER']
    KEYROCK_APPID = current_app.config['BAE_KEYROCK_APPID']
    KEYROCK_USER = current_app.config['BAE_KEYROCK_USERNAME']
    KEYROCK_PW = current_app.config['BAE_KEYROCK_PASSWORD']

    # Obtain user info, extract user ID
    url = KEYROCK_URL + '/user?access_token={}'.format(token)
    resp = requests.get(url)
    if (not resp) or (not resp.status_code==200) or (not resp.json) or (not resp.json()['id']):
        raise MarketplaceKeyrockError('Could not obtain user info in Marketplace Keyrock.')
    user_id = resp.json()['id']
    
    # Login via Provider credentials
    url = KEYROCK_URL + '/v1/auth/tokens'
    json_body = """
      {
        "name": \""""+KEYROCK_USER+"""\",
        "password": \""""+KEYROCK_PW+"""\"
      }
    """
    headers = {"Content-Type": "application/json"}
    resp = requests.post(url, data=json_body, headers=headers)
    if (not resp) or (not resp.status_code==201) or (not resp.headers) or (not resp.headers['X-Subject-Token']):
        raise MarketplaceKeyrockError('Could not login to Marketplace Keyrock')
    provider_token = resp.headers['X-Subject-Token']

    # Obtain available roles of application, extract ID of claimed role
    url = KEYROCK_URL + '/v1/applications/{}/roles'.format(KEYROCK_APPID)
    headers = {"X-Auth-Token": provider_token}
    resp = requests.get(url, headers=headers)
    if (not resp) or (not resp.status_code==200) or (not resp.json) or (not resp.json()['roles']):
        raise MarketplaceKeyrockError('Could not obtain application roles in Marketplace Keyrock, there are no roles')
    app_roles = resp.json()['roles']
    role_id = None
    for r in app_roles:
        if r['name'] == role:
            role_id = r['id']
            break
    if not role_id:
        raise MarketplaceKeyrockError('Claimed role ' + role + ' could not be found for application')

    # Obtain assigned user roles, check for specific ID
    url = KEYROCK_URL + '/v1/applications/{}/users/{}/roles'.format(KEYROCK_APPID, user_id)
    headers = {"X-Auth-Token": provider_token}
    resp = requests.get(url, headers=headers)
    if (not resp) or (not resp.status_code==200) or (not resp.json) or (not resp.json()['role_user_assignments']):
        raise MarketplaceKeyrockError('Could not obtain user roles, there are no roles assigned')
    user_roles = resp.json()['role_user_assignments']
    for r in user_roles:
        if r['role_id'] == role_id:
            return True

    raise MarketplaceKeyrockError('User has not claimed role ' + role)
