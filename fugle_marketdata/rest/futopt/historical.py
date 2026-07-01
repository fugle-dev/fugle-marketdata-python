from urllib.parse import quote as urlquote

from ..base_rest import BaseRest

class Historical(BaseRest):
    def daily(self, **params):
        symbol = urlquote(params.pop('symbol'), safe='')
        return self.request(f"historical/daily/{symbol}", **params)

    def candles(self, **params):
        symbol = urlquote(params.pop('symbol'), safe='')
        return self.request(f"historical/candles/{symbol}", **params)
