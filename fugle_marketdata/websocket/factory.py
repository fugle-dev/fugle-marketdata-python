from ..client_factory import ClientFactory
from .futopt import WebSocketFutOptClient
from .stock import WebSocketStockClient
from ..constants import FUGLE_MARKETDATA_API_WEBSOCKET_BASE_URL, FUGLE_MARKETDATA_API_VERSION

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

    def get_client(self, type):
        base_url = self.options.get('base_url')
        if not base_url:
            base_url = f"{FUGLE_MARKETDATA_API_WEBSOCKET_BASE_URL}/{FUGLE_MARKETDATA_API_VERSION}"
        
        url = f'{base_url.rstrip("/")}/{type}/streaming'

        if type in self.__clients:
            return self.__clients[type]
        
        client_options = {**self.options, 'base_url': url}

        if type == 'stock': 
            client = WebSocketStockClient(**client_options)
        elif type == 'futopt' :
            client = WebSocketFutOptClient(**client_options)
        else: 
            None

        self.__clients[type] = client
        return client





