from ..base_rest import BaseRest


class CorporateActions(BaseRest):
    def capital_changes(self, **params):
        return self.request("corporate-actions/capital-changes", **params)

    def dividends(self, **params):
        return self.request("corporate-actions/dividends", **params)

    def listing_applicants(self, **params):
        return self.request("corporate-actions/listing-applicants", **params)
