from urllib.parse import quote as urlquote

from ..base_rest import BaseRest

class Intraday(BaseRest):
    def products(self, **params):
        return self.request(f"intraday/products", **params)

    def tickers(self, **params):
        return self.request(f"intraday/tickers", **params)

    def ticker(self, **params):
        symbol = urlquote(params.pop('symbol'), safe='')
        return self.request(f"intraday/ticker/{symbol}", **params)

    def quote(self, **params):
        symbol = urlquote(params.pop('symbol'), safe='')
        return self.request(f"intraday/quote/{symbol}", **params)

    def candles(self, **params):
        symbol = urlquote(params.pop('symbol'), safe='')
        return self.request(f"intraday/candles/{symbol}", **params)

    def trades(self, **params):
        symbol = urlquote(params.pop('symbol'), safe='')
        return self.request(f"intraday/trades/{symbol}", **params)

    def volumes(self, **params):
        symbol = urlquote(params.pop('symbol'), safe='')
        return self.request(f"intraday/volumes/{symbol}", **params)
