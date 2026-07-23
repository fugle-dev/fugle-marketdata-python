from ..client_factory import ClientFactory
from .futopt import WebSocketFutOptClient
from .stock import WebSocketStockClient
from .version import apply_version_to_base_url, resolve_version
from ..constants import FUGLE_MARKETDATA_API_WEBSOCKET_BASE_URL

class WebSocketClientFactory(ClientFactory):
    def __init__(self, **options):
        super().__init__(**options)
        self.__clients = {}
        self.options = options

    @property
    def stock(self):
        return self.get_client('stock')

    @property
    def futopt(self):
        return self.get_client('futopt')

    def __resolve_base_url(self, type):
        """A base_url is only re-versioned when `version` was explicitly
        supplied. Left alone otherwise, the version the caller wrote into their
        URL wins — which keeps custom and internal deployments (whose paths need
        not follow the public versioning at all) working exactly as before.
        """
        version = resolve_version(type, self.options.get('version'))
        base_url = self.options.get('base_url')

        if not base_url:
            return f"{FUGLE_MARKETDATA_API_WEBSOCKET_BASE_URL}/{version}"

        if self.options.get('version') is None:
            return base_url

        return apply_version_to_base_url(base_url, version)

    def get_client(self, type):
        if type in self.__clients:
            return self.__clients[type]

        base_url = self.__resolve_base_url(type)
        url = f'{base_url.rstrip("/")}/{type}/streaming'

        client_options = {**self.options, 'base_url': url}

        if type == 'stock':
            client = WebSocketStockClient(**client_options)
        elif type == 'futopt':
            client = WebSocketFutOptClient(**client_options)
        else:
            raise TypeError('invalid client type')

        self.__clients[type] = client
        return client
