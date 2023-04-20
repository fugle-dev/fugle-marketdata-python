from .intraday import Intraday
from .historical import Historical
from .snapshot import Snapshot


class RestStockClient:
    def __init__(self, **config):
        # config: base_url, api_key?, bearer_token?
        self.config = config

    @property
    def intraday(self):
        return Intraday(**self.config)
    
    @property
    def historical(self):
        return Historical(**self.config)
    
    @property
    def snapshot(self):
        return Snapshot(**self.config)
