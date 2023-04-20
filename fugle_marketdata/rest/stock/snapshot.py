from ..base_rest import BaseRest

class Snapshot(BaseRest):
    def quotes(self, **params):
        market = params.pop('market')
        return self.request(f"snapshot/quotes/{market}", **params)
    
    def movers(self, **params):
        market = params.pop('market')
        return self.request(f"snapshot/movers/{market}", **params)
    
    def actives(self, **params):
        market = params.pop('market')
        return self.request(f"snapshot/actives/{market}", **params)
    