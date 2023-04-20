from ..base_rest import BaseRest

class Historical(BaseRest):
    def candles(self, **params):
        symbol = params.pop('symbol')
        return self.request(f"historical/candles/{symbol}", **params)
    
    def stats(self, **params):
        symbol = params.pop('symbol')
        return self.request(f"historical/stats/{symbol}", **params)
    