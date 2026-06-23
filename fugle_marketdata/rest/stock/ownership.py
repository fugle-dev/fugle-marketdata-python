from ..base_rest import BaseRest


class Ownership(BaseRest):
    def etf_holdings(self, **params):
        symbol = params.pop('symbol')
        return self.request(f"ownership/etf-holdings/{symbol}", **params)
