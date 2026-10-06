from urllib.parse import quote as urlquote

from ..base_rest import BaseRest

class Historical(BaseRest):
    def daily(self, **params):
        # `symbol` is the deprecated name; pop both so neither leaks into the query
        symbol = params.pop('symbol', None)
        product = urlquote(params.pop('product', symbol), safe='')
        return self.request(f"historical/daily/{product}", **params)

    def candles(self, **params):
        product = urlquote(params.pop('product'), safe='')
        return self.request(f"historical/candles/{product}", **params)
