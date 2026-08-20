from urllib.parse import urlencode
import requests
from ..exceptions import FugleAPIError


class RestProductClient(object):
    """What a caller holds when they take `.stock` or `.futopt` off the factory.

    The Node SDK gets this for free — its product clients extend `RestClient`.
    Here the product clients are facades over the endpoint groups rather than
    `BaseRest` subclasses, so they need a shared ancestor of their own.
    """

    def __init__(self, **config):
        # config: base_url, api_key?, bearer_token?
        self.config = config

    @property
    def base_url(self):
        """The prefix every request from this client is built on, fully
        resolved — host, version segment and product. Endpoints are appended
        to it.

        The version segment is chosen by the SDK rather than written by the
        caller, so this is the only way to see what a client resolved to.
        """
        return self.config['base_url']


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

        # `from` is a reserved keyword in Python; accept `from_` as an alias.
        if 'from_' in params:
            params['from'] = params.pop('from_')

        if len(params) == 0:
            query = ''
        else:
            query = '?' + urlencode(params)

        url = baseUrl + endpoint + query

        try:
            response = requests.get(url, headers=headers)

            # 檢查 HTTP 錯誤狀態
            if response.status_code >= 400:
                error_msg = f"HTTP {response.status_code}"
                try:
                    error_data = response.json()
                    if 'message' in error_data:
                        error_msg = error_data['message']
                except:
                    pass

                raise FugleAPIError(
                    error_msg,
                    url=url,
                    status_code=response.status_code,
                    params=params,
                    response_text=response.text
                )

            return response.json()

        except ValueError as e:
            raise FugleAPIError(
                "Failed to parse JSON response",
                url=url,
                status_code=response.status_code,
                params=params,
                response_text=response.text
            )

        except requests.exceptions.RequestException as e:
            raise FugleAPIError(
                f"{type(e).__name__}: {str(e)}",
                url=url,
                params=params
            )
