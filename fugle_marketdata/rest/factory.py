from ..client_factory import ClientFactory
from ..constants import FUGLE_MARKETDATA_API_REST_BASE_URL, FUGLE_MARKETDATA_API_VERSION
from .stock import RestStockClient
from .futopt import RestFutOptClient


class RestClientFactory(ClientFactory):
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
            base_url = f"{FUGLE_MARKETDATA_API_REST_BASE_URL}/{FUGLE_MARKETDATA_API_VERSION}"

        url = f'{base_url.rstrip("/")}/{type}'

        if type in self.__clients:
            return self.__clients[type]

        # Create a copy of options and override base_url
        client_options = {**self.options}
        client_options['base_url'] = url

        if type == 'stock':
            client = RestStockClient(**client_options)

        elif type == 'futopt':
            client = RestFutOptClient(**client_options)

        else:
            None

        self.__clients[type] = client
        return client
