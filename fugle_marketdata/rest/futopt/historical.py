from ..base_rest import BaseRest

class Historical(BaseRest):
    def daily(self, **params):
        symbol = params.pop('symbol')
        return self.request(f"historical/daily/{symbol}", **params)
    def candles(self, **params):
        symbol = params.pop('symbol')
        return self.request(f"historical/candles/{symbol}", **params)
    

    