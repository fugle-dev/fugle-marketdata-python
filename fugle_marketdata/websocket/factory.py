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

        base_url = f"{FUGLE_MARKETDATA_API_WEBSOCKET_BASE_URL}/{FUGLE_MARKETDATA_API_VERSION}/{type}/streaming"
                    
        if type in self.__clients:
            return self.__clients[type]
        
        if type == 'stock': 
            client = WebSocketStockClient(base_url=base_url, **self.options)
        elif type == 'futopt' :
            client = WebSocketFutOptClient(base_url=base_url, **self.options)
        else: 
            None

        self.__clients[type] = client
        return client





