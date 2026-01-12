from .intraday import Intraday
from .historical import Historical
from .snapshot import Snapshot
from .technical import Technical
from .corporate_actions import CorporateActions


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
    
    @property
    def technical(self):
        return Technical(**self.config)

    @property
    def corporate_actions(self):
        return CorporateActions(**self.config)
