class ClientFactory:
    def __init__(self, **options):
        self.options = options
        api_key = options.get('api_key')
        bearer_token = options.get('bearer_token')
        sdk_token = options.get('sdk_token')
        token_count = sum(bool(token) for token in [api_key, bearer_token, sdk_token])

        if token_count == 0:
            raise TypeError('One of the "apiKey", "bearerToken", or "sdkToken" options must be specified')

        if token_count > 1:
            raise TypeError('Only one of the "apiKey", "bearerToken", or "sdkToken" options must be specified')
