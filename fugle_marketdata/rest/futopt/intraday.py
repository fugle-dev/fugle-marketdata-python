from ..base_rest import BaseRest

class Intraday(BaseRest):
    def contracts(self, **params):
        return self.request(f"intraday/contracts", **params)
    
    def products(self, **params):
        return self.request(f"intraday/products", **params)
    
    def ticker(self, **params):
        symbol = params.pop('symbol')
        return self.request(f"intraday/ticker/{symbol}", **params)
    
    def quote(self, **params):
        symbol = params.pop('symbol')
        return self.request(f"intraday/quote/{symbol}", **params)
    
    def candles(self, **params):
        symbol = params.pop('symbol')
        return self.request(f"intraday/candles/{symbol}", **params)