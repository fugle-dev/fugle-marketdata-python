from .intraday import Intraday
from .historical import Historical
from .snapshot import Snapshot
from .technical import Technical
from .corporate_actions import CorporateActions
from .ownership import Ownership
from ..base_rest import RestProductClient


class RestStockClient(RestProductClient):
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

    @property
    def ownership(self):
        return Ownership(**self.config)
