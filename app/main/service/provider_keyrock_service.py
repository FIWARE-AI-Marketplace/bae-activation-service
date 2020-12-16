from flask import current_app

import requests
import json

class ProviderKeyrockError(Exception):
    def __init__(self, msg):
        self.message = msg

    def get_message(self):
        return self.message

def assign_role(consumer_id, role):
    # Assign role in Provider Keyrock
    if current_app.config['DEBUG']:
        print('Assigning role in provider Keyrock. Role: ' + role)

    # Keyrock config
    KEYROCK_URL = current_app.config['PROVIDER_KEYROCK_SERVER']
    KEYROCK_APPID = current_app.config['PROVIDER_KEYROCK_APPID']
    KEYROCK_USER = current_app.config['PROVIDER_KEYROCK_USERNAME']
    KEYROCK_PW = current_app.config['PROVIDER_KEYROCK_PASSWORD']

    # Function return value
    ret_val = {}

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
        raise ProviderKeyrockError('Could not login to Marketplace Keyrock')
    provider_token = resp.headers['X-Subject-Token']

    # Check if role exists
    # --> If not, create role in AppX
    # --> Get role ID
    url = KEYROCK_URL + '/v1/applications/{}/roles'.format(KEYROCK_APPID)
    headers = {"X-Auth-Token": provider_token}
    resp = requests.get(url, headers=headers)
    if (not resp) or (not resp.status_code==200) or (not resp.json) or (not resp.json()['roles']):
        raise ProviderKeyrockError('Could not obtain application roles in Provider Keyrock, there are no roles')
    app_roles = resp.json()['roles']
    role_id = None
    for r in app_roles:
        # Find role ID
        if r['name'] == role:
            role_id = r['id']
            break
    if not role_id:
        # Create role in AppX
        url = KEYROCK_URL + '/v1/applications/{}/roles'.format(KEYROCK_APPID)
        headers = {'Content-Type': 'application/json', "X-Auth-Token": provider_token}
        json_body = """
          {
            "role": {
              "name": \"""" + role + """\"
            }
          } 
        """
        resp = requests.post(url, data=json_body, headers=headers)
        if (not resp) or (not resp.status_code==201) or (not resp.json) or (not resp.json()['role']) or (not resp.json()['role']['id']):
            raise ProviderKeyrockError('Could not create role ' + role + ' in Provider Keyrock')
        role_id = resp.json()['role']['id']
    ret_val['role_id'] = role_id
    
    # Check if user/org exists
    # --> If not, create user/org
    # --> Get user ID
    url = KEYROCK_URL + '/v1/organizations'
    headers = {"X-Auth-Token": provider_token}
    resp = requests.get(url, headers=headers)
    org_id = None
    if (not resp) or (not resp.status_code==200) or (not resp.json) or (not resp.json()['organizations']):
        # There are no organizations, create one
        org_id = create_org(KEYROCK_URL, consumer_id, provider_token)
    else:
        # Look for org
        orgs = resp.json()['organizations']
        for o in orgs:
            if o['Organization']['name'] == consumer_id:
                org_id = o['Organization']['id']

    if not org_id:
        # Org not found, create it
        org_id = create_org(KEYROCK_URL, consumer_id, provider_token)
    ret_val['org_id'] = org_id
        
    # Assign role to user/org in AppX
    url = KEYROCK_URL + '/v1/applications/{}/organizations/{}/roles/{}/organization_roles/member'.format(KEYROCK_APPID, org_id, role_id)
    headers = {"X-Auth-Token": provider_token, "Content-Type": "application/json"}
    resp = requests.post(url, headers=headers)
    if (not resp) or (not resp.status_code==201) or (not resp.json) or (not resp.json()['role_organization_assignments']):
            raise ProviderKeyrockError('Could not assign role ' + role + ' to organization ' + consumer_id  + ' in Provider Keyrock')

    # Return values
    return ret_val

def create_org(KEYROCK_URL, consumer_id, provider_token):
    url = KEYROCK_URL + '/v1/organizations'
    headers = {'Content-Type': 'application/json', "X-Auth-Token": provider_token}
    json_body = """
      {
        "organization": {
          "name": \"""" + consumer_id + """\",
          "description": \"""" + consumer_id + """\"
      }
    } 
    """
    resp = requests.post(url, data=json_body, headers=headers)
    if (not resp) or (not resp.status_code==201) or (not resp.json) or (not resp.json()['organization']) or (not resp.json()['organization']['id']):
            raise ProviderKeyrockError('Could not create organization ' + consumer_id + ' in Provider Keyrock')
    return resp.json()['organization']['id']
