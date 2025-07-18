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
        if self.config.get('sdk_token'):
            headers['X-SDK-TOKEN'] = self.config['sdk_token']


        endpoint = path if (path.startswith('/')) else '/' + path

        if len(params) == 0:
            query = ''
        else:
            query = '?' + urlencode(params)

        response = requests.get(baseUrl + endpoint + query, headers=headers)

        try:
            return response.json()
        except ValueError as e:
            raise Exception("An unexpected data error occurred.\nPlease try again later. If the issue persists, please contact support at  (tech.support@fugle.tw)")
