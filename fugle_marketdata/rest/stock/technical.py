from ..base_rest import BaseRest

class Technical(BaseRest):
    def sma(self, **params):
        symbol = params.pop('symbol')
        return self.request(f"technical/sma/{symbol}", **params)

    def rsi(self, **params):
        symbol = params.pop('symbol')
        return self.request(f"technical/rsi/{symbol}", **params)

    def kdj(self, **params):
        symbol = params.pop('symbol')
        return self.request(f"technical/kdj/{symbol}", **params)

    def macd(self, **params):
        symbol = params.pop('symbol')
        return self.request(f"technical/macd/{symbol}", **params)

    def bb(self, **params):
        symbol = params.pop('symbol')
        return self.request(f"technical/bb/{symbol}", **params)
