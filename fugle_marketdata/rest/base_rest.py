from urllib.parse import urlencode
import requests

class BaseRest(object):
    def __init__(self, **config):
        self.config = config

    def request(self, path, **params):
        baseUrl = self.config['base_url']
        headers = {}
        if self.config.get('api_key'):
            headers['X-API-KEY'] = self.config['api_key']
        if self.config.get('bearer_token'):
            headers['Authorization'] = f"Bearer {self.config['bearer_token']}"

        endpoint = path if (path.startswith('/')) else '/' + path

        if len(params) == 0:
            query = ''
        else:
            query = '?' + urlencode(params)
        return requests.get(baseUrl + endpoint + query, headers=headers).json()
