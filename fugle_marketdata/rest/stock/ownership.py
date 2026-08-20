from ..base_rest import BaseRest


class Ownership(BaseRest):
    def etf_holdings(self, **params):
        symbol = params.pop('symbol')
        return self.request(f"ownership/etf-holdings/{symbol}", **params)

    def institutional_trades(self, **params):
        symbol = params.pop('symbol')
        return self.request(f"ownership/institutional-trades/{symbol}", **params)

    def director_holdings(self, **params):
        symbol = params.pop('symbol')
        return self.request(f"ownership/director-holdings/{symbol}", **params)

    def tdcc_distribution(self, **params):
        symbol = params.pop('symbol')
        return self.request(f"ownership/tdcc-distribution/{symbol}", **params)
