from ..base_url import with_version
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
        # Same rule as streaming: base_url is host and path prefix, the SDK owns
        # the version segment. REST serves one version, so there's no option to
        # choose it with — but a version written into base_url is still rejected
        # rather than silently doubled.
        base_url = with_version(
            self.options.get('base_url') or FUGLE_MARKETDATA_API_REST_BASE_URL,
            FUGLE_MARKETDATA_API_VERSION,
        )

        url = f'{base_url}/{type}'

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
