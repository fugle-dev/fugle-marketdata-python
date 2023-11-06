class ClientFactory:
    def __init__(self, **options):
        self.options = options
        if not self.options.get('api_key') and not self.options.get('bearer_token'):
            raise TypeError('One of the "api_key" or "bearer_token" options must be specified')
        if self.options.get('api_key') and self.options.get('bearer_token'):
            raise TypeError('One and only one of the "api_key" or "bearer_token" options must be specified')