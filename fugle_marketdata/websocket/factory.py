from ..base_url import with_version
from ..client_factory import ClientFactory
from .futopt import WebSocketFutOptClient
from .stock import WebSocketStockClient
from .version import VERSION_OPTION_HINT, resolve_version
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
        """`base_url` picks the host and path prefix; `version` picks the
        version. Nothing else: a custom endpoint is written the same way as the
        public one, and pointing at a different host never forces the caller to
        track versions by hand.
        """
        version = resolve_version(type, self.options.get('version'))
        base_url = self.options.get('base_url') or FUGLE_MARKETDATA_API_WEBSOCKET_BASE_URL
        return with_version(base_url, version, VERSION_OPTION_HINT)

    def get_client(self, type):
        if type in self.__clients:
            return self.__clients[type]

        base_url = self.__resolve_base_url(type)
        url = f'{base_url}/{type}/streaming'

        client_options = {**self.options, 'base_url': url}

        if type == 'stock':
            client = WebSocketStockClient(**client_options)
        elif type == 'futopt':
            client = WebSocketFutOptClient(**client_options)
        else:
            raise TypeError('invalid client type')

        self.__clients[type] = client
        return client
