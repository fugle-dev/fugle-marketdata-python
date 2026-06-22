from ..base_rest import BaseRest


class Ownership(BaseRest):
    def etf_holdings(self, **params):
        symbol = params.pop('symbol')
        # `from` is a reserved keyword in Python, so callers pass `from_`.
        # Rebuild the dict to keep the original argument order in the query string.
        query = {('from' if key == 'from_' else key): value for key, value in params.items()}
        return self.request(f"ownership/etf-holdings/{symbol}", **query)
