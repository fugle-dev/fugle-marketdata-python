from .intraday import Intraday
from .historical import Historical
from ..base_rest import RestProductClient


class RestFutOptClient(RestProductClient):
    @property
    def intraday(self):
        return Intraday(**self.config)
    
    @property
    def historical(self):
        return Historical(**self.config)