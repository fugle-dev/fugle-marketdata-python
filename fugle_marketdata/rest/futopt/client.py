from .intraday import Intraday



class RestFutOptClient:
    def __init__(self, **config):
        # config: base_url, api_key?, bearer_token?
        self.config = config

    @property
    def intraday(self):
        return Intraday(**self.config)
    
